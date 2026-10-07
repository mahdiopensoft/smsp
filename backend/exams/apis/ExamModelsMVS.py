from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import random

from exams.models.Exam import Exam
from exams.models.ExamVersion import ExamVersion
from exams.models.ExamQuestionOrder import ExamQuestionOrder
from exams.serializers.Exam import ExamSerializer

class ExamModelsMVS(AllMVS):
    """
    Dedicated ModelViewSet for Exam Models Management.
    Endpoint: /api/exams/exam-models/
    Used by: ExamModelsView.vue
    """
    queryset = Exam.objects.select_related('subject', 'year').prefetch_related('versions')
    serializer_class = ExamSerializer

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """
        Get full detailed structure of an exam and its models (versions)
        with all question orders, options, correct answers and marks.
        """
        try:
            exam = Exam.objects.select_related('subject', 'year').get(pk=pk, is_deleted=False)
        except Exam.DoesNotExist:
            return Response({"success": False, "message": "الاختبار غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        versions = ExamVersion.objects.filter(
            exam=exam,
            is_deleted=False
        ).prefetch_related(
            'question_orders__question__options',
            'question_orders__question__lesson__unit'
        ).order_by('versionCode')

        enriched_versions = []
        for v in versions:
            q_orders = v.question_orders.filter(is_deleted=False).order_by('orderIndex')
            questions_data = []
            for qo in q_orders:
                q = qo.question
                options_data = [
                    {
                        "id": opt.id,
                        "text": opt.text,
                        "isTrue": opt.isTrue,
                        "image": opt.image.url if opt.image else None,
                        "latex": opt.latex,
                    }
                    for opt in q.options.filter(is_deleted=False)
                ]

                unit_name = 'عام'
                lesson_name = 'عام'
                if q.lesson:
                    lesson_name = q.lesson.name_ar
                    if hasattr(q.lesson, 'unit') and q.lesson.unit:
                        unit_name = q.lesson.unit.name_ar

                questions_data.append({
                    "id": q.id,
                    "orderId": qo.id,
                    "orderIndex": qo.orderIndex,
                    "content": q.content,
                    "questionType": q.questionType,
                    "difficulty": q.difficulty,
                    "bloomLevel": q.bloomLevel,
                    "assignedMark": q.defaultMark or 1.0,
                    "unitName": unit_name,
                    "lessonName": lesson_name,
                    "options": options_data,
                    "isTrue": q.isTrue,
                    "answerText": q.answerText,
                })

            enriched_versions.append({
                "id": v.id,
                "versionCode": v.versionCode,
                "model_group_index": getattr(v, 'model_group_index', 0),
                "difficulty_profile": getattr(v, 'difficulty_profile', 'mixed'),
                "difficulty_profile_display": v.get_difficulty_profile_display() if hasattr(v, 'get_difficulty_profile_display') else getattr(v, 'difficulty_profile', 'mixed'),
                "difficulty_distribution": getattr(v, 'difficulty_distribution', None),
                "questions": questions_data
            })

        return Response({
            "id": exam.id,
            "title": exam.title,
            "institution_type": exam.institution_type,
            "uniqueCode": exam.uniqueCode,
            "subjectName": exam.subject.name_ar if exam.subject else 'عام',
            "versions": enriched_versions
        })

    @action(detail=False, methods=['post'], url_path='shuffle')
    def shuffle_version(self, request):
        """
        Shuffles the question order of a specific model version atomically.
        """
        version_id = request.data.get('versionId') or request.data.get('version_id')
        if not version_id:
            return Response({"success": False, "message": "يجب تحديد معرف النموذج"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            orders = list(ExamQuestionOrder.objects.filter(examVersion_id=version_id, is_deleted=False).select_related('question'))
            if not orders:
                return Response({"success": False, "message": "لا توجد أسئلة في هذا النموذج"}, status=status.HTTP_400_BAD_REQUEST)

            def is_tf(qo):
                t = str(getattr(qo.question, 'questionType', '') or '').lower()
                return 'true' in t or 'false' in t or 'صح' in t or 'خطأ' in t

            tf_orders = [qo for qo in orders if is_tf(qo)]
            mcq_orders = [qo for qo in orders if not is_tf(qo)]

            random.shuffle(tf_orders)
            random.shuffle(mcq_orders)

            combined = tf_orders + mcq_orders
            with transaction.atomic():
                # Step 1: Use temporary negative indices to prevent unique collisions
                for idx, qo in enumerate(combined, start=1):
                    qo.orderIndex = -idx
                    qo.save(update_fields=['orderIndex'])
                # Step 2: Set final positive indices
                for idx, qo in enumerate(combined, start=1):
                    qo.orderIndex = idx
                    qo.save(update_fields=['orderIndex'])

            return Response({"success": True, "message": "تم خلط ترتيب الأسئلة بنجاح مع الحفاظ على الأقسام"})
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='reorder')
    def reorder_version(self, request):
        """
        Reorders questions in a version according to a provided array of orders.
        """
        orders_payload = request.data.get('orders', [])
        if not orders_payload:
            return Response({"success": False, "message": "لا توجد بيانات ترتيب"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for item in orders_payload:
                    order_id = item.get('orderId') or item.get('id')
                    new_idx = item.get('orderIndex')
                    if order_id and new_idx is not None:
                        ExamQuestionOrder.objects.filter(id=order_id).update(orderIndex=new_idx)

            return Response({"success": True, "message": "تم تحديث ترتيب الأسئلة بنجاح"})
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='remove-question')
    def remove_question(self, request):
        """
        Removes a question from a version and re-indexes remaining questions.
        """
        order_id = request.data.get('orderId') or request.data.get('id')
        if not order_id:
            return Response({"success": False, "message": "يجب تحديد معرف السؤال"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            qo = ExamQuestionOrder.objects.get(id=order_id)
            version_id = qo.examVersion_id
            deleted_idx = qo.orderIndex
            
            with transaction.atomic():
                qo.delete()
                # Shift subsequent indices down
                ExamQuestionOrder.objects.filter(
                    examVersion_id=version_id,
                    orderIndex__gt=deleted_idx,
                    is_deleted=False
                ).update(orderIndex=models.F('orderIndex') - 1)

            return Response({"success": True, "message": "تم حذف السؤال من النموذج بنجاح"})
        except ExamQuestionOrder.DoesNotExist:
            return Response({"success": False, "message": "السؤال غير موجود في النموذج"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
