from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from exams.models.ExamGenerationSetting import ExamGenerationSetting
from exams.serializers.ExamGenerationSetting import ExamGenerationSettingSerializer

class ExamGenerationSettingMVS(AllMVS):
    queryset = ExamGenerationSetting.objects.all()
    serializer_class = ExamGenerationSettingSerializer
    enable_actions = ['all', 'select', 'list', 'second_list', 'filter', 'filter_paginate', 'create', 'update', 'destroy', 'retrieve']
