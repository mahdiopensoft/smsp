from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from submissions.models.SubmissionBatch import SubmissionBatch
from submissions.serializers.SubmissionBatch import SubmissionBatchSerializer

class SubmissionBatchMVS(AllMVS):
    queryset = SubmissionBatch.objects.all()
    serializer_class = SubmissionBatchSerializer
    enable_actions = [
        'all', 'select', 'list', 'second_list', 'filter', 'filter_paginate',
        'create', 'update', 'destroy', 'retrieve', 'partial_update'
    ]
