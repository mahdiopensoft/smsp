from rest_framework import serializers
from submissions.models.Submission import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField(read_only=True)
    seat_number = serializers.SerializerMethodField(read_only=True)
    exam_title = serializers.SerializerMethodField(read_only=True)
    exam_version_code = serializers.SerializerMethodField(read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)
    institution_type = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_control_locked = serializers.SerializerMethodField(read_only=True)
    control_receipt_no = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def get_student_name(self, obj):
        try:
            if obj.registration:
                if obj.registration.student_profile and obj.registration.student_profile.name_ar:
                    return obj.registration.student_profile.name_ar
                if obj.registration.student:
                    s = obj.registration.student
                    full_name = f"{s.first_name or ''} {s.last_name or ''}".strip()
                    if full_name:
                        return full_name
                    if s.username:
                        return s.username
            if obj.layout_result and obj.layout_result.get("student_name"):
                name = obj.layout_result.get("student_name")
                if name and name != "طالب اختبار":
                    return name
        except Exception:
            pass
        return "طالب غير محدد"

    def get_seat_number(self, obj):
        try:
            if obj.registration and obj.registration.seatNumber:
                return obj.registration.seatNumber
            if obj.layout_result and obj.layout_result.get("seat_number"):
                return str(obj.layout_result.get("seat_number"))
        except Exception:
            pass
        return "-"

    def get_exam_title(self, obj):
        try:
            return obj.exam.title
        except Exception:
            return ""

    def get_exam_version_code(self, obj):
        try:
            if obj.exam_version:
                code = getattr(obj.exam_version, 'versionCode', None) or getattr(obj.exam_version, 'version_code', None)
                if code:
                    return f"نموذج {code}"
            if obj.layout_result and obj.layout_result.get("version_code"):
                return f"نموذج {obj.layout_result.get('version_code')}"
        except Exception:
            pass
        return ""

    def get_subject_name(self, obj):
        try:
            if obj.exam and obj.exam.subject:
                return getattr(obj.exam.subject, 'name_ar', None) or getattr(obj.exam.subject, 'name_en', None) or str(obj.exam.subject)
        except Exception:
            pass
        return ""

    def get_institution_type(self, obj):
        try:
            if obj.exam:
                return obj.exam.institution_type
        except Exception:
            pass
        return "school"

    def get_is_control_locked(self, obj):
        try:
            lr = obj.layout_result or {}
            return bool(lr.get("dispatched_to_control") is True or lr.get("dispatched_to_control") == "true")
        except Exception:
            return False

    def get_control_receipt_no(self, obj):
        try:
            lr = obj.layout_result or {}
            return lr.get("control_receipt_no") or ""
        except Exception:
            return ""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            omr_res = data.get("omr_result")
            needs_enrichment = (
                isinstance(omr_res, list)
                and len(omr_res) > 0
                and isinstance(omr_res[0], dict)
                and (
                    "question_id" not in omr_res[0]
                    or "marked_choice" not in omr_res[0]
                    or "correct_choice" not in omr_res[0]
                )
            )
            if needs_enrichment:
                from omr.models.OMRQuestionResult import OMRQuestionResult
                qr_map = {
                    qr.question_number: qr
                    for qr in OMRQuestionResult.objects.filter(
                        sheet_result__submission_id=instance.id,
                        is_deleted=False,
                    ).order_by("question_number")
                }
                enriched = []
                for idx, item in enumerate(omr_res, start=1):
                    if not isinstance(item, dict):
                        enriched.append(item)
                        continue
                    q_num = item.get("question_id") or item.get("question_number") or idx
                    qr = qr_map.get(q_num)
                    marked = (
                        item.get("marked_choice")
                        or item.get("final_marked_choice")
                        or item.get("candidate_choice")
                        or (qr.final_marked_choice if qr else None)
                        or (qr.marked_choice if qr else None)
                    )
                    correct = item.get("correct_choice") or (qr.correct_choice if qr else None)
                    max_mark = (
                        item.get("max_mark")
                        or item.get("assigned_weight")
                        or (float(qr.assigned_weight) if (qr and qr.assigned_weight is not None) else 1.0)
                    )
                    if item.get("marks_awarded") is not None:
                        awarded = item.get("marks_awarded")
                    elif qr and qr.marks_awarded is not None:
                        awarded = float(qr.marks_awarded)
                    else:
                        awarded = float(max_mark) if item.get("is_correct") else 0.0

                    choices = item.get("choices")
                    if not choices:
                        m_str = str(marked or "").strip()
                        c_str = str(correct or "").strip()
                        if m_str in ("صح", "خطأ", "ص", "خ") or c_str in ("صح", "خطأ", "ص", "خ"):
                            choices = ["صح", "خطأ"]
                        elif m_str in ("1", "2", "3", "4") or c_str in ("1", "2", "3", "4"):
                            choices = ["1", "2", "3", "4"]
                        elif m_str in ("أ", "ب", "ج", "د") or c_str in ("أ", "ب", "ج", "د"):
                            choices = ["أ", "ب", "ج", "د"]
                        else:
                            choices = ["1", "2", "3", "4"]

                    merged = dict(item)
                    merged.setdefault("question_id", q_num)
                    merged.setdefault("question_number", q_num)
                    merged["marked_choice"] = marked
                    merged["final_marked_choice"] = marked
                    merged["correct_choice"] = correct
                    merged["marks_awarded"] = awarded
                    merged["max_mark"] = float(max_mark)
                    merged["choices"] = choices
                    if merged.get("final_confidence") is None and qr and qr.final_confidence is not None:
                        merged["final_confidence"] = float(qr.final_confidence)
                    if not merged.get("bubble_state") and qr and qr.bubble_state:
                        merged["bubble_state"] = qr.bubble_state
                    enriched.append(merged)
                data["omr_result"] = enriched
        except Exception:
            pass
        return data

