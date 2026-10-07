from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from exams.models.ExamSchedule import ExamSchedule
from exams.serializers.ExamSchedule import ExamScheduleSerializer

class ExamScheduleMVS(AllMVS):
    queryset = ExamSchedule.objects.all()
    serializer_class = ExamScheduleSerializer
    enable_actions = ['all', 'select', 'list', 'second_list', 'filter', 'filter_paginate', 'create', 'update', 'destroy', 'retrieve']
