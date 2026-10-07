from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from omr.models.OMRSheetResult import OMRSheetResult
from omr.serializers.OMRSheetResult import OMRSheetResultSerializer

class OMRSheetResultMVS(AllMVS):
    queryset = OMRSheetResult.objects.all()
    serializer_class = OMRSheetResultSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
