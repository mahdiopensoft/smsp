from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q

from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.StudentExamRegistration import StudentExamRegistration
from exams.serializers.Exam import ExamSerializer

class ExamArchiveMVS(AllMVS):
    """
    Dedicated ModelViewSet for Archived Exams View.
    Endpoint: /api/exams/exam-archive/
    Used by: ExamArchiveView.vue
    """
    queryset = Exam.objects.select_related(
        'subject', 
        'year', 
        'examSchedule',
        'examGenerationSetting'
    ).prefetch_related(
        'versions__question_orders'
    ).annotate(
        annotated_students_count=Count('versions__registered_students', filter=Q(versions__registered_students__is_deleted=False), distinct=True),
        annotated_versions_count=Count('versions', filter=Q(versions__is_deleted=False), distinct=True)
    ).distinct().order_by('-created_at')
    
    serializer_class = ExamSerializer
    filterset_fields = {
        'subject': ['exact'],
        'year': ['exact'],
        'institution_type': ['exact'],
        'examSchedule': ['exact'],
    }

    def get_queryset(self):
        qs = super().get_queryset()

        inst_type = self.request.query_params.get('institution_type')
        if inst_type and inst_type != 'all':
            qs = qs.filter(institution_type=inst_type)

        subject_id = self.request.query_params.get('subject') or self.request.query_params.get('subject_id') or self.request.query_params.get('institute_subject')
        if subject_id:
            qs = qs.filter(
                Q(subject_id=subject_id) |
                Q(versions__question_orders__question__lesson__unit__class_subject__subject_id=subject_id) |
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_subject_id=subject_id) |
                Q(versions__question_orders__question__lesson__subject_id=subject_id)
            )

        # University Filters
        college_id = self.request.query_params.get('college') or self.request.query_params.get('fk_college')
        if college_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_college_id=college_id) |
                Q(subject__semester_subjects__fk_specialization__fk_college_id=college_id)
            )

        dept_id = self.request.query_params.get('department') or self.request.query_params.get('fk_department') or self.request.query_params.get('section')
        if dept_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization__fk_section_id=dept_id) |
                Q(subject__semester_subjects__fk_specialization__fk_section_id=dept_id)
            )

        spec_id = self.request.query_params.get('specialization') or self.request.query_params.get('fk_specialization')
        if spec_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject__fk_specialization_id=spec_id) |
                Q(subject__semester_subjects__fk_specialization_id=spec_id)
            )

        sem_sub_id = self.request.query_params.get('semester_subject') or self.request.query_params.get('fk_semester_subject')
        if sem_sub_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__semester_subject_id=sem_sub_id) |
                Q(subject__semester_subjects__id=sem_sub_id)
            )

        # School Filters
        stage_id = self.request.query_params.get('stage') or self.request.query_params.get('stage_id')
        if stage_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track__level__stage_id=stage_id) |
                Q(subject__class_subjects__class_track__level__stage_id=stage_id)
            )

        class_track_id = self.request.query_params.get('class_track') or self.request.query_params.get('class_track_id')
        if class_track_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track_id=class_track_id) |
                Q(subject__class_subjects__class_track_id=class_track_id)
            )

        year_id = self.request.query_params.get('year') or self.request.query_params.get('year_id')
        if year_id:
            qs = qs.filter(year_id=year_id)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(uniqueCode__icontains=search) |
                Q(subject__name_ar__icontains=search)
            )

        return qs.order_by('-created_at').distinct()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Returns statistics for Exam Archive cards."""
        total_exams = Exam.objects.filter(is_deleted=False).count()
        total_models = ExamVersion.objects.filter(is_deleted=False).count()
        total_students = StudentExamRegistration.objects.filter(is_deleted=False).count()

        return Response({
            "totalExams": total_exams,
            "totalModels": total_models,
            "registeredStudents": total_students,
        })

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """
        Returns full detailed dashboard payload for a specific archived exam.
        """
        try:
            exam = Exam.objects.select_related('subject', 'year', 'class_track', 'examGenerationSetting', 'governorate', 'directorate').get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        versions = ExamVersion.objects.filter(exam=exam, is_deleted=False).order_by('versionCode')
        versions_list = [{"id": v.id, "versionCode": v.versionCode} for v in versions]

        first_v = versions.first()
        questions_count = first_v.question_orders.filter(is_deleted=False).count() if first_v else 0
        students_count = StudentExamRegistration.objects.filter(examVersion__exam=exam, is_deleted=False).count()

        # Class track info
        class_track_info = None
        if exam.class_track:
            class_track_info = {
                "id": exam.class_track.id,
                "name": str(exam.class_track),
            }

        # Geographic scope info
        scope_info = {
            "target_scope_level": exam.target_scope_level,
            "governorate": exam.governorate.name_ar if exam.governorate else None,
            "directorate": exam.directorate.name_ar if exam.directorate else None,
        }

        # Generation setting info
        setting_info = None
        if exam.examGenerationSetting:
            s = exam.examGenerationSetting
            setting_info = {
                "easyPercentage": s.easyPercentage,
                "mediumPercentage": s.mediumPercentage,
                "hardPercentage": s.hardPercentage,
            }

        return Response({
            "id": exam.id,
            "title": exam.title,
            "uniqueCode": exam.uniqueCode,
            "subjectName": exam.subject.name_ar if exam.subject else 'عام',
            "yearName": str(exam.year) if exam.year else '-',
            "createdAt": exam.created_at.strftime('%Y-%m-%d') if exam.created_at else '',
            "versionsCount": len(versions_list),
            "versionsList": versions_list,
            "questionsCount": questions_count,
            "studentsCount": students_count,
            "classTrack": class_track_info,
            "scope": scope_info,
            "setting": setting_info,
        })

    @action(detail=True, methods=['get'], url_path='registered-students')
    def registered_students(self, request, pk=None):
        """
        Returns registered students for a specific exam with full backend pagination,
        search, and version filtering.
        """
        try:
            exam = Exam.objects.get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        registrations = StudentExamRegistration.objects.filter(
            examVersion__exam=exam,
            is_deleted=False
        ).select_related(
            'student_profile',
            'student_profile__organization',
            'student_profile__directorate',
            'student_profile__class_track',
            'examVersion'
        )

        # 1. Filter by Version
        version = request.query_params.get('version') or request.query_params.get('versionCode')
        if version and version != 'all':
            registrations = registrations.filter(examVersion__versionCode=version)

        # 2. Search Filter
        search = request.query_params.get('search')
        if search and search.strip():
            s = search.strip()
            registrations = registrations.filter(
                Q(seatNumber__icontains=s) |
                Q(secretNumber__icontains=s) |
                Q(student_profile__name_ar__icontains=s) |
                Q(student_profile__name_en__icontains=s) |
                Q(student_profile__academic_number__icontains=s) |
                Q(student_profile__organization__name_ar__icontains=s) |
                Q(student_profile__directorate__name_ar__icontains=s)
            )

        # 3. Sorting / Ordering
        sort_by = request.query_params.get('sort_by')
        if sort_by:
            if sort_by.endswith('__display'):
                sort_by = sort_by[:-9]
            sort_map = {
                'studentName': 'student_profile__name_ar',
                '-studentName': '-student_profile__name_ar',
                'academicNumber': 'student_profile__academic_number',
                '-academicNumber': '-student_profile__academic_number',
                'seatNumber': 'seatNumber',
                '-seatNumber': '-seatNumber',
                'secretNumber': 'secretNumber',
                '-secretNumber': '-secretNumber',
                'versionCode': 'examVersion__versionCode',
                '-versionCode': '-examVersion__versionCode',
                'schoolName': 'student_profile__organization__name_ar',
                '-schoolName': '-student_profile__organization__name_ar',
                'directorateName': 'student_profile__directorate__name_ar',
                '-directorateName': '-student_profile__directorate__name_ar',
            }
            order_field = sort_map.get(sort_by, sort_by)
            try:
                registrations = registrations.order_by(order_field)
            except Exception:
                registrations = registrations.order_by('examVersion__versionCode', 'seatNumber')
        else:
            registrations = registrations.order_by('examVersion__versionCode', 'seatNumber')

        total_students_count = registrations.count()
        unique_schools_count = registrations.values('student_profile__organization').distinct().count()

        # Parse pagination parameters
        try:
            page_num = int(request.query_params.get('page', 1) or 1)
        except (ValueError, TypeError):
            page_num = 1
        try:
            page_size = int(request.query_params.get('page_size', request.query_params.get('perPage', 10)) or 10)
        except (ValueError, TypeError):
            page_size = 10

        page_size = max(1, min(page_size, 100))
        page_num = max(1, page_num)

        # 4. Backend Pagination
        page = self.paginate_queryset(registrations)
        if page is not None:
            students_data = []
            for reg in page:
                profile = reg.student_profile
                students_data.append({
                    "id": reg.id,
                    "seatNumber": reg.seatNumber,
                    "secretNumber": reg.secretNumber,
                    "isPresent": reg.isPresent,
                    "versionCode": reg.examVersion.versionCode if reg.examVersion else '-',
                    "versionId": reg.examVersion_id,
                    "studentName": profile.name_ar if profile else (str(reg.student) if reg.student else '-'),
                    "academicNumber": profile.academic_number if profile else '-',
                    "schoolName": profile.organization.name_ar if profile and profile.organization else '-',
                    "directorateName": profile.directorate.name_ar if profile and profile.directorate else '-',
                    "gender": profile.get_gender_display() if profile else '-',
                })

            resp = self.get_paginated_response(students_data)
            if isinstance(resp.data, dict):
                resp.data['examId'] = exam.id
                resp.data['examTitle'] = exam.title
                resp.data['totalStudents'] = total_students_count
                resp.data['uniqueSchoolsCount'] = unique_schools_count
                resp.data['students'] = students_data
                if 'pagination' not in resp.data:
                    num_pages = (total_students_count // page_size) + (1 if total_students_count % page_size else 0)
                    resp.data['pagination'] = {
                        'count': total_students_count,
                        'num_pages': max(1, num_pages),
                        'current_page': page_num,
                        'page_size': page_size,
                        'per_page': page_size,
                        'total': total_students_count,
                    }
            return resp

        # Fallback slicing: Ensure we NEVER return unpaginated datasets
        start = (page_num - 1) * page_size
        end = start + page_size
        paged_regs = registrations[start:end]

        students_data = []
        for reg in paged_regs:
            profile = reg.student_profile
            students_data.append({
                "id": reg.id,
                "seatNumber": reg.seatNumber,
                "secretNumber": reg.secretNumber,
                "isPresent": reg.isPresent,
                "versionCode": reg.examVersion.versionCode if reg.examVersion else '-',
                "versionId": reg.examVersion_id,
                "studentName": profile.name_ar if profile else (str(reg.student) if reg.student else '-'),
                "academicNumber": profile.academic_number if profile else '-',
                "schoolName": profile.organization.name_ar if profile and profile.organization else '-',
                "directorateName": profile.directorate.name_ar if profile and profile.directorate else '-',
                "gender": profile.get_gender_display() if profile else '-',
            })

        num_pages = (total_students_count // page_size) + (1 if total_students_count % page_size else 0)
        return Response({
            "success": True,
            "results": students_data,
            "students": students_data,
            "count": total_students_count,
            "pagination": {
                "count": total_students_count,
                "num_pages": max(1, num_pages),
                "current_page": page_num,
                "page_size": page_size,
                "per_page": page_size,
                "total": total_students_count,
            },
            "examId": exam.id,
            "examTitle": exam.title,
            "totalStudents": total_students_count,
            "uniqueSchoolsCount": unique_schools_count,
        })

