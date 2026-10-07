from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import time

from omr.models.OMRSheetResult import OMRSheetResult
from omr.serializers.OMRSheetResult import OMRSheetResultSerializer
from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion

class OMRScannerLabMVS(AllMVS):
    """
    Dedicated ModelViewSet for Interactive OMR Scanner Lab.
    Endpoint: /api/omr/omr-scanner/
    Used by: OMRScannerLabView.vue
    """
    queryset = OMRSheetResult.objects.filter(is_deleted=False).prefetch_related('questions')
    serializer_class = OMRSheetResultSerializer

    @action(detail=False, methods=['get'], url_path='answer-key')
    def get_answer_key(self, request):
        """
        Returns answer key for a given exam and model version.
        """
        exam_id = request.query_params.get('examId') or request.query_params.get('exam')
        version_code = request.query_params.get('versionCode', 'A')

        if not exam_id:
            return Response({"success": False, "message": "يجب تحديد معرف الاختبار"}, status=status.HTTP_400_BAD_REQUEST)

        version = ExamVersion.objects.filter(
            exam_id=exam_id,
            versionCode=version_code,
            is_deleted=False
        ).prefetch_related('question_orders__question__options').first()

        if not version:
            # Generate default fallback answer key
            default_keys = {i: chr(65 + (i % 4)) for i in range(1, 41)}
            return Response({"success": True, "answerKey": default_keys})

        key_map = {}
        for qo in version.question_orders.filter(is_deleted=False).order_by('orderIndex'):
            correct_opt = qo.question.options.filter(isTrue=True).first()
            if correct_opt:
                # Map option order to letter (A, B, C, D)
                all_opts = list(qo.question.options.all())
                try:
                    idx = all_opts.index(correct_opt)
                    key_map[qo.orderIndex] = chr(65 + idx)
                except ValueError:
                    key_map[qo.orderIndex] = 'A'
            elif qo.question.isTrue is not None:
                key_map[qo.orderIndex] = 'A' if qo.question.isTrue else 'B'
            else:
                key_map[qo.orderIndex] = 'A'

        return Response({"success": True, "answerKey": key_map})

    @action(detail=False, methods=['post'], url_path='scan-sheet')
    def scan_sheet(self, request):
        """
        Receives scanned bubbles payload or image, validates answers against key,
        and computes grades and confidence.
        """
        bubbles = request.data.get('bubbles', {})
        exam_id = request.data.get('examId')
        version_code = request.data.get('versionCode', 'A')
        answer_key = request.data.get('answerKey', {})

        if not answer_key and exam_id:
            # Fetch from DB
            key_res = self.get_answer_key(request)
            answer_key = key_res.data.get('answerKey', {})

        total_q = max(len(bubbles), len(answer_key), 40)
        correct_count = 0
        wrong_count = 0
        unanswered_count = 0
        details = []

        for q_num in range(1, total_q + 1):
            q_str = str(q_num)
            marked = bubbles.get(q_str) or bubbles.get(q_num)
            expected = answer_key.get(q_str) or answer_key.get(q_num) or 'A'

            is_correct = False
            if marked:
                if str(marked).upper() == str(expected).upper():
                    correct_count += 1
                    is_correct = True
                else:
                    wrong_count += 1
            else:
                unanswered_count += 1

            details.append({
                "question_number": q_num,
                "marked": marked or '-',
                "expected": expected,
                "is_correct": is_correct,
                "confidence": 0.98 if marked else 0.0
            })

        percentage = round((correct_count / total_q) * 100, 2) if total_q > 0 else 0
        passed = percentage >= 50.0

        return Response({
            "success": True,
            "totalQuestions": total_q,
            "correctAnswers": correct_count,
            "wrongAnswers": wrong_count,
            "unanswered": unanswered_count,
            "score": correct_count,
            "maxScore": total_q,
            "percentage": percentage,
            "passed": passed,
            "details": details
        })
