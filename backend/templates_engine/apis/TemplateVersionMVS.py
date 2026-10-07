from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from templates_engine.models.TemplateVersion import TemplateVersion
from templates_engine.serializers.TemplateVersion import TemplateVersionSerializer

class TemplateVersionMVS(AllMVS):
    queryset = TemplateVersion.objects.all()
    serializer_class = TemplateVersionSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
