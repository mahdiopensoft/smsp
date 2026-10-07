from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.Question import Question
from bank.models.Answer import Answer
from bank.serializers.Question import QuestionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class QuestionFastEntryMVS(AllMVS):
    """
    Dedicated ModelViewSet for Fast Multi-Question Entry.
    Endpoint: /api/bank/question-fast-entry/
    Used by: QuestionFastEntryView.vue
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        # Support direct POST to endpoint as well as bulk_create_full
        return self._process_bulk_create(request)

    @action(detail=False, methods=['post'])
    def bulk_create_full(self, request):
        return self._process_bulk_create(request)

    def _process_bulk_create(self, request):
        lesson_id = request.data.get('lesson') or request.data.get('fk_lesson')
        questions_data = request.data.get('questions', [])
        
        if not questions_data:
            return Response(
                {"success": False, "message": "لا يوجد أسئلة للحفظ", "code": "NO_DATA"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not lesson_id:
            return Response(
                {"success": False, "message": "يجب تحديد الدرس الأكاديمي المشترك للأسئلة", "code": "NO_LESSON"},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_by = request.user if request.user and request.user.is_authenticated else None
        created_count = 0
        all_answers_to_create = []
        
        try:
            with transaction.atomic():
                for q_data in questions_data:
                    # Create question
                    learning_outcome_id = (
                        q_data.get('learningOutcome') or 
                        q_data.get('learning_outcome_id') or 
                        request.data.get('learningOutcome') or 
                        request.data.get('learning_outcome_id')
                    )
                    institution_type = q_data.get('institution_type') or request.data.get('institution_type', 'school')

                    # Process helper image if present
                    image_file = None
                    raw_image = q_data.get('image')
                    if raw_image and isinstance(raw_image, str) and raw_image.startswith('data:image'):
                        try:
                            import base64
                            import uuid
                            from django.core.files.base import ContentFile
                            format_part, imgstr = raw_image.split(';base64,')
                            ext = format_part.split('/')[-1]
                            if ext == 'jpeg':
                                ext = 'jpg'
                            file_name = f"{uuid.uuid4()}.{ext}"
                            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)
                        except Exception:
                            image_file = None

                    q = Question.objects.create(
                        content=q_data.get('content', ''),
                        image=image_file,
                        questionType=q_data.get('questionType') or q_data.get('question_type', 'Single Choice'),
                        difficulty=q_data.get('difficulty', 2),
                        bloomLevel=q_data.get('bloomLevel') or q_data.get('bloom_level', 'تطبيق'),
                        defaultMark=q_data.get('defaultMark') or q_data.get('default_mark', 1),
                        expected_time_minutes=q_data.get('expected_time_minutes') or q_data.get('expectedTimeMinutes', 1),
                        status=q_data.get('status', 'قيد المراجعة'),
                        institution_type=institution_type,
                        lesson_id=lesson_id,
                        learningOutcome_id=learning_outcome_id,
                        createdBy=created_by
                    )
                    
                    # Prepare answers
                    answers_data = q_data.get('answers') or q_data.get('options', [])
                    for a_data in answers_data:
                        if isinstance(a_data, dict):
                            text = a_data.get('text') or a_data.get('content') or ''
                            is_true = a_data.get('isTrue') if 'isTrue' in a_data else a_data.get('is_correct', False)
                        else:
                            text = str(a_data)
                            is_true = False
                            
                        all_answers_to_create.append(Answer(
                            question=q,
                            text=text,
                            isTrue=is_true
                        ))
                    
                    created_count += 1
                
                if all_answers_to_create:
                    Answer.objects.bulk_create(all_answers_to_create)
                    
            return Response({
                "success": True,
                "message": f"تم حفظ {created_count} أسئلة بنجاح",
                "count": created_count
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
