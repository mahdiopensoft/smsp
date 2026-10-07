from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from exams.models.TableOfSpecifications import TableOfSpecifications
from exams.serializers.TableOfSpecifications import TableOfSpecificationsSerializer
from bank.models.AuditLog import AuditLog
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Q

class TableOfSpecificationsMVS(AllMVS):
    """
    Dedicated ModelViewSet for Table of Specifications (TOS / جدول المواصفات).
    Endpoint: /api/exams/table-of-specifications/
    Used by: TableOfSpecificationsView.vue / ExamCreateView.vue
    """
    queryset = TableOfSpecifications.objects.select_related('subject', 'level', 'createdBy').all().distinct()
    serializer_class = TableOfSpecificationsSerializer
    filterset_fields = {
        'subject': ['exact'],
        'level': ['exact'],
        'institution_type': ['exact'],
        'is_active': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)
        
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(level__stage_id=stage_id)

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(level_id=level_id)

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            from academic.models.schools.SchoolClassTrack import SchoolClassTrack
            try:
                ct = SchoolClassTrack.objects.get(id=class_track_id)
                if ct.level_id:
                    qs = qs.filter(level_id=ct.level_id)
            except Exception:
                pass

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id')
        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        institute_subject_id = self.request.query_params.get('institute_subject') or self.request.query_params.get('institute_subject_id')
        if institute_subject_id:
            from academic.models.institutes.InstituteSubject import InstituteSubject
            try:
                isub = InstituteSubject.objects.get(id=institute_subject_id)
                qs = qs.filter(subject__name_ar=isub.name_ar)
            except Exception:
                pass

        semester_subject_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('semester_subject_id')
        if semester_subject_id:
            from academic.models.universities.UniversitySemesterSubject import UniversitySemesterSubject
            try:
                ss = UniversitySemesterSubject.objects.get(id=semester_subject_id)
                if ss.fk_subject_id:
                    qs = qs.filter(subject_id=ss.fk_subject_id)
            except Exception:
                pass

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(subject__name_ar__icontains=search) |
                Q(subject__name_en__icontains=search) |
                Q(level__name_ar__icontains=search)
            )

        return qs.order_by('-created_at').distinct()

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        inst_type = serializer.validated_data.get('institution_type')
        subject = serializer.validated_data.get('subject')

        if inst_type == 'institute' and not subject:
            institute_sub_id = self.request.data.get('institute_subject') or self.request.data.get('instituteSubject')
            if institute_sub_id:
                from academic.models.institutes.InstituteSubject import InstituteSubject
                from academic.models.common.Subject import Subject
                try:
                    isub = InstituteSubject.objects.get(id=institute_sub_id)
                    sub = Subject.objects.filter(name_ar=isub.name_ar).first()
                    if not sub:
                        sub = Subject.objects.create(name_ar=isub.name_ar, subject_code=isub.subject_code or f"INST_{isub.id}")
                    serializer.validated_data['subject'] = sub
                except Exception:
                    pass

        instance = serializer.save(createdBy=user)
        
        AuditLog.objects.create(
            user=user,
            action=AuditLog.ActionChoices.CREATE,
            resource_type='TableOfSpecifications',
            resource_id=str(instance.id),
            description=f"إنشاء جدول مواصفات جديد: '{instance.name}' لمادة ({instance.subject_id})"
        )

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        instance = serializer.save()
        
        AuditLog.objects.create(
            user=user,
            action=AuditLog.ActionChoices.UPDATE,
            resource_type='TableOfSpecifications',
            resource_id=str(instance.id),
            description=f"تحديث جدول المواصفات: '{instance.name}'"
        )

    def perform_destroy(self, instance):
        user = self.request.user if self.request.user.is_authenticated else None
        instance_id = instance.id
        instance_name = instance.name
        instance.delete()

        AuditLog.objects.create(
            user=user,
            action=AuditLog.ActionChoices.DELETE,
            resource_type='TableOfSpecifications',
            resource_id=str(instance_id),
            description=f"حذف جدول المواصفات: '{instance_name}'"
        )

    @action(detail=True, methods=['get'])
    def blueprint(self, request, pk=None):
        """
        Mathematical Blueprint Generator Algorithm:
        Calculates exact number of questions required for each Unit x Bloom cell
        based on the matrix percentage distribution and total target questions count.
        Guarantees exact integer rounding distribution so that sum(counts) == total_questions.
        """
        tos = self.get_object()
        total_questions = tos.total_questions_count or 30
        matrix = tos.matrix_data or []

        bloom_keys = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']
        bloom_arabic_labels = {
            'remember': 'تذكر',
            'understand': 'فهم',
            'apply': 'تطبيق',
            'analyze': 'تحليل',
            'evaluate': 'تقييم',
            'create': 'ابتكار'
        }

        # 1. First pass: calculate fractional questions and take integer floor
        raw_blueprint = []
        allocated_total = 0
        remainders = []

        for row_idx, row in enumerate(matrix):
            unit_id = row.get('unit_id')
            unit_name = row.get('unit_name', '')
            weights = row.get('weights', {})

            cell_counts = {}
            for k in bloom_keys:
                pct = float(weights.get(k, 0) or 0)
                exact_val = (pct / 100.0) * total_questions
                int_val = int(exact_val)
                rem = exact_val - int_val

                cell_counts[k] = int_val
                allocated_total += int_val
                if rem > 0:
                    remainders.append((rem, row_idx, k))

            raw_blueprint.append({
                'unit_id': unit_id,
                'unit_name': unit_name,
                'weights': weights,
                'bloom_counts': cell_counts
            })

        # 2. Second pass: distribute shortfall based on largest fractional remainders
        shortfall = total_questions - allocated_total
        if shortfall > 0:
            remainders.sort(key=lambda x: x[0], reverse=True)
            for i in range(min(shortfall, len(remainders))):
                _, r_idx, b_key = remainders[i]
                raw_blueprint[r_idx]['bloom_counts'][b_key] += 1

        # 3. Compute Bloom summary totals
        bloom_totals = {k: sum(r['bloom_counts'][k] for r in raw_blueprint) for k in bloom_keys}
        bloom_totals_display = {bloom_arabic_labels[k]: bloom_totals[k] for k in bloom_keys}

        return Response({
            "tos_id": tos.id,
            "tos_name": tos.name,
            "subject_name": tos.subject.name_ar if tos.subject else '',
            "total_questions": total_questions,
            "total_marks": tos.total_marks,
            "bloom_totals": bloom_totals_display,
            "blueprint": raw_blueprint
        })
