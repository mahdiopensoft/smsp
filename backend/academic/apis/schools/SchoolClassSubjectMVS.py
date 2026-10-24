from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from academic.models.schools.SchoolClassSubject import SchoolClassSubject
from academic.serializers.schools.SchoolClassSubject import SchoolClassSubjectSerializer
from django.db.models import Q
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from academic.models.schools.SchoolSubject import SchoolSubject
from academic.models.common.Subject import Subject
from academic.models.schools.SchoolClassTrack import SchoolClassTrack
from academic.models.universities.UniversityGradingSystem import UniversityGradingSystem

class SchoolClassSubjectMVS(AllMVS):
    queryset = SchoolClassSubject.objects.select_related(
        'class_track__level', 
        'class_track__track', 
        'class_track__level__stage', 
        'school_subject',
        'subject'
    ).all()
    serializer_class = SchoolClassSubjectSerializer
    select_serializer_fields = ['id', 'subject_name', 'name_ar']
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
    filterset_fields = {
        'is_active': ['exact'],
        'added_to_total': ['exact'],
        'optional': ['exact'],
        'subject': ['exact'],
        'school_subject': ['exact'],
        'class_track': ['exact'],
        'class_track__level': ['exact'],
        'class_track__track': ['exact'],
        'class_track__level__stage': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        # Hierarchy filters
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(class_track__level__stage_id=stage_id)

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(class_track__level_id=level_id)

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id')
        if track_id:
            qs = qs.filter(class_track__track_id=track_id)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(Q(subject_id=subject_id) | Q(school_subject_id=subject_id))

        # Added to total filter
        added_to_total = self.request.query_params.get('added_to_total')
        if added_to_total is not None and added_to_total != '':
            if added_to_total in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(added_to_total=True)
            elif added_to_total in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(added_to_total=False)

        # Optional filter
        optional = self.request.query_params.get('optional')
        if optional is not None and optional != '':
            if optional in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(optional=True)
            elif optional in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(optional=False)

        # Active filter
        is_active = self.request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            if is_active in [True, 'true', 'True', 1, '1']:
                qs = qs.filter(is_active=True)
            elif is_active in [False, 'false', 'False', 0, '0']:
                qs = qs.filter(is_active=False)

        # Search Query
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(school_subject__name_ar__icontains=search) |
                Q(school_subject__name_en__icontains=search) |
                Q(subject__name_ar__icontains=search) |
                Q(subject__name_en__icontains=search) |
                Q(class_track__level__name_ar__icontains=search) |
                Q(class_track__track__name_ar__icontains=search)
            )

        return qs.order_by('class_track__level__order', 'id')

    @action(detail=False, methods=['get'], url_path='matrix')
    def matrix(self, request):
        class_track_id = request.query_params.get('class_track') or request.query_params.get('class_track_id')
        if not class_track_id:
            return Response({'success': False, 'message': 'مسار الصف مطلوب'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. جلب كافة المواد الدراسية النشطة
        school_subjects = list(SchoolSubject.objects.filter(is_deleted=False, is_active=True).order_by('subject_order', 'id'))
        if not school_subjects:
            school_subjects = list(Subject.objects.filter(is_deleted=False, is_active=True).order_by('subject_order', 'id'))

        # 2. جلب المواد المسندة لمسار الصف المحدد
        assigned_qs = SchoolClassSubject.objects.filter(class_track_id=class_track_id, is_deleted=False)
        assigned_map_school = {cs.school_subject_id: cs for cs in assigned_qs if cs.school_subject_id}
        assigned_map_common = {cs.subject_id: cs for cs in assigned_qs if cs.subject_id}

        # 3. جلب أنظمة الدرجات لربط النظام المناسب تلقائياً إن وجد
        grading_systems = list(UniversityGradingSystem.objects.filter(is_deleted=False, is_active=True))

        matrix_rows = []
        for s in school_subjects:
            cs = assigned_map_school.get(s.id) or assigned_map_common.get(s.id)
            is_assigned = bool(cs)
            min_score = cs.min_score if cs else 50
            max_score = cs.max_score if cs else 100

            # محاولة مطابقة نظام الدرجات التلقائي
            matched_sys_id = None
            for gs in grading_systems:
                if gs.success_grade == min_score and gs.grade_total == max_score:
                    matched_sys_id = gs.id
                    break

            matrix_rows.append({
                'id': cs.id if cs else None,
                'school_subject_id': s.id,
                'subject_id': getattr(cs, 'subject_id', None) or s.id,
                'subject_name': s.name_ar,
                'is_assigned': is_assigned,
                'grading_system_id': matched_sys_id,
                'min_score': min_score,
                'max_score': max_score,
                'added_to_total': cs.added_to_total if cs else True,
                'optional': cs.optional if cs else False,
                'is_active': cs.is_active if cs else True,
                'note': cs.note or '' if cs else ''
            })

        return Response({
            'success': True,
            'data': matrix_rows
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='bulk-save')
    def bulk_save(self, request):
        class_track_id = request.data.get('class_track_id')
        items = request.data.get('items', [])

        if not class_track_id:
            return Response(
                {'success': False, 'message': 'مسار الصف مطلوب'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            class_track = SchoolClassTrack.objects.get(id=class_track_id)
        except SchoolClassTrack.DoesNotExist:
            return Response(
                {'success': False, 'message': 'مسار الصف المحدد غير موجود'},
                status=status.HTTP_404_NOT_FOUND
            )

        with transaction.atomic():
            for item in items:
                rec_id = item.get('id')
                is_assigned = item.get('is_assigned', False)
                school_sub_id = item.get('school_subject_id') or item.get('school_subject')
                sub_id = item.get('subject_id') or item.get('subject')

                if is_assigned:
                    min_score = item.get('min_score')
                    if min_score is None or min_score == '':
                        min_score = 50
                    else:
                        min_score = int(min_score)

                    max_score = item.get('max_score')
                    if max_score is None or max_score == '':
                        max_score = 100
                    else:
                        max_score = int(max_score)

                    added_to_total = bool(item.get('added_to_total', True))
                    optional = bool(item.get('optional', False))
                    is_active = bool(item.get('is_active', True))
                    note = item.get('note', '') or ''

                    # Resolve objects
                    school_sub_obj = SchoolSubject.objects.filter(id=school_sub_id).first() if school_sub_id else None
                    sub_obj = Subject.objects.filter(id=sub_id).first() if sub_id else None

                    if not sub_obj and school_sub_obj:
                        sub_obj = Subject.objects.filter(
                            Q(name_ar=school_sub_obj.name_ar) | Q(subject_code=school_sub_obj.subject_code)
                        ).first()

                    if not school_sub_obj and sub_obj:
                        school_sub_obj = SchoolSubject.objects.filter(
                            Q(name_ar=sub_obj.name_ar) | Q(subject_code=sub_obj.subject_code)
                        ).first()

                    if rec_id:
                        rec = SchoolClassSubject.objects.filter(id=rec_id).first()
                        if rec:
                            rec.min_score = min_score
                            rec.max_score = max_score
                            rec.added_to_total = added_to_total
                            rec.optional = optional
                            rec.is_active = is_active
                            rec.note = note
                            rec.is_deleted = False
                            if school_sub_obj:
                                rec.school_subject = school_sub_obj
                            if sub_obj:
                                rec.subject = sub_obj
                            rec.save()
                            continue

                    # البحث بالسجل القائم لتفادي التكرار
                    lookup = {'class_track': class_track}
                    if sub_obj:
                        lookup['subject'] = sub_obj
                    elif school_sub_obj:
                        lookup['school_subject'] = school_sub_obj

                    obj = SchoolClassSubject.objects.filter(**lookup).first()
                    if obj:
                        obj.min_score = min_score
                        obj.max_score = max_score
                        obj.added_to_total = added_to_total
                        obj.optional = optional
                        obj.is_active = is_active
                        obj.note = note
                        obj.is_deleted = False
                        if school_sub_obj:
                            obj.school_subject = school_sub_obj
                        if sub_obj:
                            obj.subject = sub_obj
                        obj.save()
                    else:
                        SchoolClassSubject.objects.create(
                            class_track=class_track,
                            school_subject=school_sub_obj,
                            subject=sub_obj,
                            min_score=min_score,
                            max_score=max_score,
                            added_to_total=added_to_total,
                            optional=optional,
                            is_active=is_active,
                            note=note
                        )
                else:
                    # إلغاء إسناد المادة (حذف السجل إذا كان مسجلاً مسبقاً)
                    if rec_id:
                        SchoolClassSubject.objects.filter(id=rec_id).delete()
                    else:
                        lookup = {'class_track': class_track}
                        if sub_id:
                            lookup['subject_id'] = sub_id
                        elif school_sub_id:
                            lookup['school_subject_id'] = school_sub_id
                        if len(lookup) > 1:
                            SchoolClassSubject.objects.filter(**lookup).delete()

        return Response({
            'success': True,
            'message': 'تم حفظ مواد مسار الصف بنجاح'
        }, status=status.HTTP_200_OK)

ClassSubjectMVS = SchoolClassSubjectMVS
