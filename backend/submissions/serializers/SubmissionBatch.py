from rest_framework import serializers
from submissions.models.SubmissionBatch import SubmissionBatch

class SubmissionBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionBatch
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
