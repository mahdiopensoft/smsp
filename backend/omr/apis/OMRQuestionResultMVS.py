from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from omr.models.OMRQuestionResult import OMRQuestionResult
from omr.serializers.OMRQuestionResult import OMRQuestionResultSerializer

class OMRQuestionResultMVS(AllMVS):
    queryset = OMRQuestionResult.objects.all()
    serializer_class = OMRQuestionResultSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
