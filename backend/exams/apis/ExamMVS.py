from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from exams.models.Exam import Exam
from exams.serializers.Exam import ExamSerializer
from django.db.models import Q

class ExamMVS(AllMVS):
    queryset = Exam.objects.select_related('subject', 'year', 'examSchedule', 'examGenerationSetting').all().distinct()
    serializer_class = ExamSerializer
    enable_actions = ['all', 'select', 'list', 'second_list', 'filter', 'filter_paginate', 'create', 'update', 'destroy', 'retrieve']
    filterset_fields = {
        'subject': ['exact'],
        'year': ['exact'],
        'institution_type': ['exact'],
        'examSchedule': ['exact'],
        'country': ['exact'],
        'governorate': ['exact'],
        'directorate': ['exact'],
        'region': ['exact'],
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

        level_id = self.request.query_params.get('level') or self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track__level_id=level_id) |
                Q(subject__class_subjects__class_track__level_id=level_id)
            )

        track_id = self.request.query_params.get('track') or self.request.query_params.get('track_id') or self.request.query_params.get('branch')
        if track_id:
            qs = qs.filter(
                Q(versions__question_orders__question__lesson__unit__class_subject__class_track__track_id=track_id) |
                Q(subject__class_subjects__class_track__track_id=track_id)
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

        return qs.order_by('-id').distinct()
