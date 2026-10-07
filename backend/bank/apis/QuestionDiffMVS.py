import difflib
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils.html import strip_tags
from bank.models.Question import Question
from bank.models.QuestionVersion import QuestionVersion
from bank.models.Answer import Answer

def generate_word_diff_html(text1, text2):
    """Generate HTML with <ins> (green) and <del> (red) word differences."""
    words1 = strip_tags(text1 or '').split()
    words2 = strip_tags(text2 or '').split()
    
    matcher = difflib.SequenceMatcher(None, words1, words2)
    result = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            result.append(" ".join(words1[i1:i2]))
        elif tag == 'delete':
            deleted_text = " ".join(words1[i1:i2])
            result.append(f'<span class="diff-del px-1 rounded text-red font-weight-bold" style="background: rgba(239, 68, 68, 0.15); text-decoration: line-through;">{deleted_text}</span>')
        elif tag == 'insert':
            inserted_text = " ".join(words2[j1:j2])
            result.append(f'<span class="diff-ins px-1 rounded text-green font-weight-bold" style="background: rgba(34, 197, 94, 0.15);">{inserted_text}</span>')
        elif tag == 'replace':
            deleted_text = " ".join(words1[i1:i2])
            inserted_text = " ".join(words2[j1:j2])
            result.append(f'<span class="diff-del px-1 rounded text-red font-weight-bold" style="background: rgba(239, 68, 68, 0.15); text-decoration: line-through;">{deleted_text}</span> <span class="diff-ins px-1 rounded text-green font-weight-bold" style="background: rgba(34, 197, 94, 0.15);">{inserted_text}</span>')
            
    return " ".join(result)

class QuestionDiffMVS(ViewSet):
    """
    Dedicated ViewSet for Question Versions Comparison & Visual Diff View.
    Endpoint: /api/bank/question-diff/
    Used by: QuestionDiffDialog.vue / ReviewQueueView.vue
    """

    @action(detail=False, methods=['get'])
    def compare(self, request):
        """
        Compare two question versions.
        Query params:
            v1: id of first question (older)
            v2: id of second question (newer)
        """
        v1_id = request.query_params.get('v1')
        v2_id = request.query_params.get('v2')

        if not v1_id or not v2_id:
            return Response({"error": "يرجى تحديد معرف السؤالين للمقارنة (v1, v2)"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            q1 = Question.objects.select_related('lesson', 'learningOutcome').prefetch_related('options').get(id=v1_id)
            q2 = Question.objects.select_related('lesson', 'learningOutcome').prefetch_related('options').get(id=v2_id)
        except Question.DoesNotExist:
            return Response({"error": "أحد السؤالين غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        # Field comparisons
        fields_diff = []

        # 1. Content
        content_changed = strip_tags(q1.content) != strip_tags(q2.content)
        fields_diff.append({
            'field': 'content',
            'label': 'نص السؤال',
            'v1_value': q1.content,
            'v2_value': q2.content,
            'diff_html': generate_word_diff_html(q1.content, q2.content),
            'changed': content_changed
        })

        # 2. Difficulty
        fields_diff.append({
            'field': 'difficulty',
            'label': 'مستوى الصعوبة',
            'v1_value': q1.get_difficulty_display() if hasattr(q1, 'get_difficulty_display') else q1.difficulty,
            'v2_value': q2.get_difficulty_display() if hasattr(q2, 'get_difficulty_display') else q2.difficulty,
            'changed': q1.difficulty != q2.difficulty
        })

        # 3. Bloom Level
        fields_diff.append({
            'field': 'bloomLevel',
            'label': 'مستوى بلوم',
            'v1_value': q1.bloomLevel,
            'v2_value': q2.bloomLevel,
            'changed': q1.bloomLevel != q2.bloomLevel
        })

        # 4. Default Mark
        fields_diff.append({
            'field': 'defaultMark',
            'label': 'الدرجة الافتراضية',
            'v1_value': q1.defaultMark,
            'v2_value': q2.defaultMark,
            'changed': q1.defaultMark != q2.defaultMark
        })

        # 5. Question Type
        fields_diff.append({
            'field': 'questionType',
            'label': 'نوع السؤال',
            'v1_value': q1.questionType,
            'v2_value': q2.questionType,
            'changed': q1.questionType != q2.questionType
        })

        # Options comparison
        opts1 = list(q1.options.all())
        opts2 = list(q2.options.all())
        options_diff = []

        max_len = max(len(opts1), len(opts2))
        for idx in range(max_len):
            opt1 = opts1[idx] if idx < len(opts1) else None
            opt2 = opts2[idx] if idx < len(opts2) else None
            
            t1 = opt1.text if opt1 else ''
            t2 = opt2.text if opt2 else ''
            c1 = opt1.isTrue if opt1 else False
            c2 = opt2.isTrue if opt2 else False

            options_diff.append({
                'index': idx + 1,
                'v1_text': t1,
                'v2_text': t2,
                'v1_is_correct': c1,
                'v2_is_correct': c2,
                'text_changed': t1 != t2,
                'correctness_changed': c1 != c2,
                'diff_html': generate_word_diff_html(t1, t2) if t1 != t2 else t1
            })

        return Response({
            "version_1": {
                "id": q1.id,
                "version_number": q1.version_number,
                "status": q1.status,
                "created_at": q1.created_at,
            },
            "version_2": {
                "id": q2.id,
                "version_number": q2.version_number,
                "status": q2.status,
                "created_at": q2.created_at,
            },
            "fields_diff": fields_diff,
            "options_diff": options_diff,
            "has_changes": any(f['changed'] for f in fields_diff) or any(o['text_changed'] or o['correctness_changed'] for o in options_diff)
        })

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get the version chain/tree for a question."""
        question_id = request.query_params.get('question_id')
        if not question_id:
            return Response({"error": "يرجى تحديد معرف السؤال"}, status=status.HTTP_400_BAD_REQUEST)

        versions = QuestionVersion.objects.filter(
            original_question_id=question_id
        ).select_related('version_question', 'createdBy').order_by('version_number')

        return Response([
            {
                'version_number': v.version_number,
                'question_id': v.version_question_id,
                'change_reason': v.change_reason,
                'created_at': v.created_at,
                'author': v.createdBy.username if v.createdBy else 'مستخدم'
            }
            for v in versions
        ])
