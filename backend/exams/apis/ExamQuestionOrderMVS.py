from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from exams.models.ExamQuestionOrder import ExamQuestionOrder
from exams.serializers.ExamQuestionOrder import ExamQuestionOrderSerializer

class ExamQuestionOrderMVS(AllMVS):
    queryset = ExamQuestionOrder.objects.all()
    serializer_class = ExamQuestionOrderSerializer
    enable_actions = ['all', 'select', 'list', 'second_list', 'filter', 'filter_paginate', 'create', 'update', 'destroy', 'retrieve']
