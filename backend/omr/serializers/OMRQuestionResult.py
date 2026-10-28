from rest_framework import serializers
from omr.models.OMRQuestionResult import OMRQuestionResult

class OMRQuestionResultSerializer(serializers.ModelSerializer):
    question_type = serializers.SerializerMethodField()
    is_true_false = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    correct_choice_display = serializers.SerializerMethodField()
    marked_choice_display = serializers.SerializerMethodField()

    class Meta:
        model = OMRQuestionResult
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def _is_tf(self, obj):
        # 1. Check choice_confidences
        if isinstance(obj.choice_confidences, dict):
            keys = set(obj.choice_confidences.keys())
            if any(k in keys for k in ['صح', 'خطأ', 'ص', 'خ']):
                return True
        # 2. Check marked or correct choice
        if obj.marked_choice in ['صح', 'خطأ', 'ص', 'خ', 'True', 'False', 'T', 'F']:
            return True
        if obj.correct_choice in ['صح', 'خطأ', 'ص', 'خ']:
            return True
        # 3. Standard Yemeni 50-q sheet convention: 1-20 is True/False
        total_q = getattr(obj.sheet_result, 'total_questions', 50) or 50
        if total_q >= 20 and 1 <= obj.question_number <= 20:
            return True
        return False

    def get_is_true_false(self, obj):
        return self._is_tf(obj)

    def get_question_type(self, obj):
        return "true_false" if self._is_tf(obj) else "mcq"

    def get_options(self, obj):
        if self._is_tf(obj):
            return ["صح", "خطأ"]
        return ["1", "2", "3", "4"]

    def get_correct_choice_display(self, obj):
        ch = obj.correct_choice
        if not ch:
            return "لم تُحدد"
        if self._is_tf(obj):
            c_upper = str(ch).strip().upper()
            if c_upper in ["A", "1", "صح", "ص", "T", "TRUE"]:
                return "صح"
            if c_upper in ["B", "2", "خطأ", "خ", "F", "FALSE"]:
                return "خطأ"
        return str(ch)

    def get_marked_choice_display(self, obj):
        ch = obj.marked_choice
        if not ch or ch == "لم يُجب (فارغ)":
            return "لم يُجب (فارغ)"
        if self._is_tf(obj):
            c_upper = str(ch).strip().upper()
            if c_upper in ["A", "1", "صح", "ص", "T", "TRUE"]:
                return "صح"
            if c_upper in ["B", "2", "خطأ", "خ", "F", "FALSE"]:
                return "خطأ"
        return str(ch)

