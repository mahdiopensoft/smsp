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
        ).select_related('examVersion__exam')

        exam_id = request.query_params.get('exam_id')
        if exam_id:
            qs = qs.filter(examVersion__exam_id=exam_id)

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
        batches = qs.values('print_batch', 'examVersion__exam__id', 'examVersion__exam__title').annotate(
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
                s_name = reg.student.get_full_name() or reg.student.username
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
