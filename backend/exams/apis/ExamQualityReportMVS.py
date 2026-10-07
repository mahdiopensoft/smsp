from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Q

from exams.models.StudentExamRegistration import StudentExamRegistration
from exams.serializers.StudentExamRegistration import StudentExamRegistrationSerializer

class ExamQualityReportMVS(AllMVS):
    """
    Dedicated ModelViewSet for Exam Quality and Exam Papers Report Screen.
    Endpoint: /api/exams/exam-quality-report/
    Used by: ExamPapersReportView.vue
    """
    queryset = StudentExamRegistration.objects.filter(is_deleted=False).select_related(
        'student',
        'student_profile',
        'examVersion',
        'examVersion__exam',
        'examVersion__exam__subject',
        'examVersion__exam__governorate',
    ).prefetch_related(
        'examVersion__question_orders__question'
    ).order_by('-created_at')
    
    serializer_class = StudentExamRegistrationSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns structured student papers report with joined relations and metrics.
        """
        qs = self.get_queryset()

        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(examVersion__exam__institution_type=inst_type)

        stage_id = request.query_params.get('stageId') or request.query_params.get('stage')
        if stage_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(examVersion__exam__subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        level_id = request.query_params.get('levelId') or request.query_params.get('level')
        if level_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__class_subject__class_track__level_id=level_id) |
                Q(examVersion__exam__subject__class_subjects__class_track__level_id=level_id)
            )

        branch_id = request.query_params.get('branchId') or request.query_params.get('branch') or request.query_params.get('track')
        if branch_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__class_subject__class_track__track_id=branch_id) |
                Q(examVersion__exam__subject__class_subjects__class_track__track_id=branch_id)
            )

        class_track_id = request.query_params.get('classTrackId') or request.query_params.get('class_track')
        if class_track_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(examVersion__exam__subject__class_subjects__class_track_id=class_track_id)
            )

        # University Filters
        college_id = request.query_params.get('college') or request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(examVersion__exam__subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = request.query_params.get('department') or request.query_params.get('fk_department') or request.query_params.get('section')
        if dept_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(examVersion__exam__subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = request.query_params.get('specialization') or request.query_params.get('fk_specialization')
        if spec_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(examVersion__exam__subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = request.query_params.get('semester_subject') or request.query_params.get('fk_semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(examVersion__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(examVersion__exam__subject__semester_subjects__id=sem_sub_id)
            )

        subject_id = request.query_params.get('subjectId') or request.query_params.get('subject')
        if subject_id:
            qs = qs.filter(
                Q(examVersion__exam__subject_id=subject_id) |
                Q(examVersion__question_orders__question__lesson__unit__class_subject__subject_id=subject_id) |
                Q(examVersion__question_orders__question__lesson__unit__semester_subject__fk_subject_id=subject_id)
            )

        exam_id = request.query_params.get('examId') or request.query_params.get('exam')
        if exam_id:
            qs = qs.filter(examVersion__exam_id=exam_id)

        search = request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(seatNumber__icontains=search) |
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(student__username__icontains=search) |
                Q(student_profile__name_ar__icontains=search) |
                Q(examVersion__exam__title__icontains=search)
            )

        papers = []
        for reg in qs[:100]:
            exam = getattr(reg.examVersion, 'exam', None)
            student = reg.student
            version = reg.examVersion
            
            # Question counts and marks
            orders = version.question_orders.filter(is_deleted=False) if version else []
            questions_count = len(orders)
            total_marks = sum(getattr(o.question, 'defaultMark', 1) or 1 for o in orders)

            subject_name = (exam.subject.name_ar or exam.subject.name_en) if exam and exam.subject else "مادة عامة"
            student_name = f"{student.first_name} {student.last_name}".strip() if student and (student.first_name or student.last_name) else (student.username if student else "طالب")
            if reg.student_profile and reg.student_profile.name_ar:
                student_name = reg.student_profile.name_ar

            gov_name = exam.governorate.name if exam and exam.governorate and hasattr(exam.governorate, 'name') else ""
            
            level_name = "الصف / المستوى"
            branch_name = "القسم / التخصص"
            if orders and len(orders) > 0:
                first_q = orders[0].question
                if first_q and first_q.lesson and first_q.lesson.unit:
                    cs = getattr(first_q.lesson.unit, 'class_subject', None)
                    ss = getattr(first_q.lesson.unit, 'semester_subject', None)
                    if cs and cs.class_track:
                        level_name = cs.class_track.level.name_ar if cs.class_track.level else level_name
                        branch_name = cs.class_track.track.name_ar if cs.class_track.track else branch_name
                    elif ss:
                        if ss.fk_specialization:
                            branch_name = ss.fk_specialization.name_ar or branch_name
                        level_name = f"المستوى {ss.level}" if ss.level else level_name

            papers.append({
                "id": reg.id,
                "examId": exam.id if exam else None,
                "examTitle": exam.title if exam else "اختبار عام",
                "examCode": exam.uniqueCode if exam else "",
                "subjectName": subject_name,
                "levelName": level_name,
                "branchName": branch_name,
                "versionLabel": version.versionCode if version else "A",
                "studentName": student_name,
                "studentCode": reg.seatNumber or (student.username if student else ""),
                "institutionType": getattr(exam, 'institution_type', 'school') if exam else 'school',
                "barcodeHash": f"EXM-{exam.id if exam else 0}-STD-{student.id if student else 0}-V{version.versionCode if version else 'A'}",
                "governorateName": gov_name,
                "totalQuestions": questions_count,
                "totalMarks": total_marks,
                "isPresent": reg.isPresent
            })

        return Response({
            "results": papers,
            "count": len(papers),
            "totalCount": qs.count()
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Aggregate summary metrics for exam papers quality."""
        base_qs = StudentExamRegistration.objects.filter(is_deleted=False)
        inst_type = request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            base_qs = base_qs.filter(examVersion__exam__institution_type=inst_type)

        return Response({
            "totalPapers": base_qs.count(),
            "presentStudents": base_qs.filter(isPresent=True).count(),
            "absentStudents": base_qs.filter(isPresent=False).count(),
        })
