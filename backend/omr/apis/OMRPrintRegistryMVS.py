from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Min, Max, Q

from exams.models.Exam import Exam
from exams.models.StudentExamRegistration import StudentExamRegistration

class OMRPrintRegistryMVS(ViewSet):
    """
    ViewSet for tracking printed OMR sheets and batches.
    Endpoint: /api/omr/print-registry/
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """
        List print batches aggregated by Exam and print_batch.
        """
        search = request.query_params.get('search', '').strip()

        qs = StudentExamRegistration.objects.filter(
            is_deleted=False, 
            is_printed=True, 
            print_batch__isnull=False
        ).select_related('examVersion__exam', 'examVersion__exam__subject', 'student_profile')

        exam_id = request.query_params.get('exam_id')
        if exam_id and exam_id != 'all':
            qs = qs.filter(examVersion__exam_id=exam_id)

        subj_filter = request.query_params.get('subject') or request.query_params.get('subject_id')
        if subj_filter and subj_filter != 'all':
            from omr.apis.ExamGradebookMVS import ExamGradebookMVS
            s_ids, s_names = ExamGradebookMVS._resolve_subject_filter(subj_filter)
            s_q = Q(examVersion__exam__subject_id__in=s_ids)
            for sn in s_names:
                s_q |= Q(examVersion__exam__subject__name_ar__icontains=sn) | Q(examVersion__exam__subject__name_en__icontains=sn)
            qs = qs.filter(s_q)

        school_id = request.query_params.get('school_id') or request.query_params.get('school') or request.query_params.get('organization_id')
        directorate_id = request.query_params.get('directorate_id') or request.query_params.get('directorate')
        office_id = request.query_params.get('office_id') or request.query_params.get('office') or request.query_params.get('governorate') or request.query_params.get('governorate_id')

        if school_id and school_id != 'all':
            sch_ids = [int(x) for x in str(school_id).split(',') if x.strip().isdigit()]
            if sch_ids:
                qs = qs.filter(student_profile__organization_id__in=sch_ids)
        elif directorate_id and directorate_id != 'all':
            dir_ids = [int(x) for x in str(directorate_id).split(',') if x.strip().isdigit()]
            if dir_ids:
                from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
                core_dirs = CoreOrg.objects.filter(Q(id__in=dir_ids) | Q(fk_directorate_id__in=dir_ids), company_level=40)
                all_dir_ids = list(core_dirs.values_list('id', flat=True)) + list(core_dirs.exclude(fk_directorate_id__isnull=True).values_list('fk_directorate_id', flat=True)) + dir_ids
                qs = qs.filter(Q(student_profile__directorate_id__in=all_dir_ids) | Q(student_profile__organization__fk_parent_organization_id__in=core_dirs.values_list('id', flat=True)))
        elif office_id and office_id != 'all':
            off_ids = [int(x) for x in str(office_id).split(',') if x.strip().isdigit()]
            if off_ids:
                from OpenSoftCoreV41.common.models.Branch import Organization as CoreOrg
                core_offs = CoreOrg.objects.filter(Q(id__in=off_ids) | Q(fk_governorate_id__in=off_ids), company_level=30)
                child_dirs = CoreOrg.objects.filter(company_level=40, fk_parent_organization__in=core_offs.values_list('id', flat=True))
                qs = qs.filter(Q(student_profile__organization__fk_parent_organization_id__in=child_dirs.values_list('id', flat=True)) | Q(student_profile__directorate__fk_parent_organization_id__in=core_offs.values_list('id', flat=True)))

        if search:
            if search.isdigit():
                qs = qs.filter(
                    Q(print_batch__icontains=search) | 
                    Q(examVersion__exam__title__icontains=search) |
                    Q(examVersion__exam_id=int(search))
                )
            else:
                qs = qs.filter(
                    Q(print_batch__icontains=search) | 
                    Q(examVersion__exam__title__icontains=search)
                )

        # Aggregate by batch and exam
        batches = qs.values(
            'print_batch', 
            'examVersion__exam__id', 
            'examVersion__exam__title',
            'examVersion__exam__uniqueCode',
            'examVersion__exam__subject_id',
            'examVersion__exam__subject__name_ar',
            'examVersion__exam__subject__name_en'
        ).annotate(
            total_papers=Count('id'),
            first_printed=Min('printed_at'),
            last_printed=Max('printed_at')
        ).order_by('-first_printed')

        results = []
        for b in batches:
            results.append({
                "batch_id": b['print_batch'],
                "exam_id": b['examVersion__exam__id'],
                "exam_title": b['examVersion__exam__title'],
                "exam_code": b['examVersion__exam__uniqueCode'],
                "subject_id": b['examVersion__exam__subject_id'],
                "subject_name": b['examVersion__exam__subject__name_ar'] or b['examVersion__exam__subject__name_en'] or "",
                "total_papers": b['total_papers'],
                "print_date": b['first_printed'].strftime("%Y-%m-%d %H:%M") if b['first_printed'] else "",
                "status": "مكتمل"
            })

        return Response({
            "success": True,
            "count": len(results),
            "results": results
        })

    def retrieve(self, request, pk=None):
        """
        Retrieve details of a specific print batch.
        pk here refers to the batch_id.
        """
        batch_id = pk
        qs = StudentExamRegistration.objects.filter(
            is_deleted=False, 
            is_printed=True, 
            print_batch=batch_id
        ).select_related('student_profile', 'examVersion')

        students = []
        for reg in qs:
            if reg.student_profile and reg.student_profile.name_ar:
                s_name = reg.student_profile.name_ar
            elif reg.student:
                st = reg.student
                s_name = getattr(st, 'get_full_name', lambda: '')() or f"{st.first_name or ''} {st.last_name or ''}".strip() or st.username
            else:
                s_name = f"طالب ({reg.seatNumber})"
            students.append({
                "id": reg.id,
                "student_name": s_name,
                "seat_number": reg.seatNumber,
                "model_code": reg.examVersion.versionCode,
                "printed_at": reg.printed_at.strftime("%Y-%m-%d %H:%M:%S") if reg.printed_at else ""
            })

        return Response({
            "success": True,
            "batch_id": batch_id,
            "students": students
        })
