from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from exams.models.ExamVersion import ExamVersion
from exams.serializers.ExamVersion import ExamVersionSerializer

class ExamVersionMVS(AllMVS):
    queryset = ExamVersion.objects.all()
    serializer_class = ExamVersionSerializer
    enable_actions = ['all', 'select', 'list', 'second_list', 'filter', 'filter_paginate', 'create', 'update', 'destroy', 'retrieve']
