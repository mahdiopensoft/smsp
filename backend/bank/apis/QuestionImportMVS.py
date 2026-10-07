from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.Question import Question
from bank.models.Answer import Answer
from bank.serializers.Question import QuestionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import pandas as pd

class QuestionImportMVS(AllMVS):
    """
    Dedicated ModelViewSet for Excel/CSV Question Importing.
    Endpoint: /api/bank/question-import/
    Used by: QuestionImportView.vue
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        return self._process_excel_import(request)

    @action(detail=False, methods=['post'], url_path='import-excel')
    def import_excel(self, request):
        return self._process_excel_import(request)

    def _process_excel_import(self, request):
        lesson_id = request.data.get('fk_lesson') or request.data.get('lesson')
        learning_outcome_id = (
            request.data.get('fk_learning_outcome') or 
            request.data.get('learning_outcome') or 
            request.data.get('learningOutcome')
        )
        file = request.FILES.get('file')
        
        if not file or not lesson_id:
            return Response(
                {"success": False, "message": "يجب توفير ملف الإكسل ومعرف الدرس الأكاديمي"},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_by = request.user if request.user and request.user.is_authenticated else None
        
        try:
            df = pd.read_excel(file)
            created_count = 0
            all_answers_to_create = []
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    question_text = str(row.iloc[0]).strip()
                    if not question_text or question_text.lower() == 'nan' or question_text.startswith('نص السؤال'):
                        continue
                        
                    # Create question
                    institution_type = request.data.get('institution_type', 'school')
                    q = Question.objects.create(
                        content=question_text,
                        questionType='Single Choice',
                        difficulty=2,
                        bloomLevel='تطبيق',
                        defaultMark=1.0,
                        expected_time_minutes=1,
                        status='قيد المراجعة',
                        institution_type=institution_type,
                        lesson_id=lesson_id,
                        learningOutcome_id=learning_outcome_id,
                        createdBy=created_by
                    )
                    
                    # Extract options (cols 1 to 4)
                    options = []
                    for i in range(1, 5):
                        try:
                            opt_text = str(row.iloc[i]).strip()
                        except IndexError:
                            opt_text = ''
                        if opt_text and opt_text.lower() != 'nan':
                            options.append((i, opt_text))
                            
                    # Detect correct option (col 5)
                    raw_correct = ''
                    try:
                        raw_correct = str(row.iloc[5]).strip()
                    except IndexError:
                        raw_correct = '1'
                        
                    correct_index = 1
                    letter_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'أ': 1, 'ب': 2, 'ج': 3, 'د': 4}
                    if raw_correct.lower() in letter_map:
                        correct_index = letter_map[raw_correct.lower()]
                    else:
                        try:
                            correct_index = int(float(raw_correct))
                        except (ValueError, TypeError):
                            # Try to match text
                            matched = next((opt_num for opt_num, opt_val in options if opt_val == raw_correct), 1)
                            correct_index = matched
                            
                    for opt_num, opt_val in options:
                        is_true = (opt_num == correct_index)
                        all_answers_to_create.append(Answer(
                            question=q,
                            text=opt_val,
                            isTrue=is_true
                        ))
                        
                    created_count += 1
                    
                if all_answers_to_create:
                    Answer.objects.bulk_create(all_answers_to_create)
                        
            return Response({
                "success": True,
                "count": created_count,
                "message": f"تم استيراد {created_count} أسئلة بنجاح"
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"success": False, "message": f"فشل في استيراد الملف: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
