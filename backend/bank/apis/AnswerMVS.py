from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.Answer import Answer
from bank.serializers.Answer import AnswerSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class AnswerMVS(AllMVS):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request, *args, **kwargs):
        # Allow payload to be either a list directly, or a dict containing {'answers': [...]}
        data = request.data.get('answers', request.data) if isinstance(request.data, dict) else request.data
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        serializer.save()
