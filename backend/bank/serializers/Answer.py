from rest_framework import serializers
from bank.models.Answer import Answer
from bank.serializers.Base64ImageField import Base64ImageField

class AnswerSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']
