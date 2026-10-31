import hashlib
import json
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ExamVersion(SoftDeleteModel):
    class KeyStatus(models.TextChoices):
        DRAFT = "DRAFT", _("مسودة")
        FROZEN = "FROZEN", _("مجمد ومعتمد للتصحيح")
        INVALID = "INVALID", _("باطل أو تالف")

    exam = models.ForeignKey(
        'exams.Exam', 
        on_delete=models.CASCADE, 
        related_name='versions', 
        verbose_name=_("الاختبار الأساسي")
    )
    versionCode = models.CharField(max_length=50, verbose_name=_("رمز النموذج (A, B, C...)"))
    
    # Smart Model Difficulty Assignment
    model_group_index = models.IntegerField(
        default=0,
        verbose_name=_("رقم مجموعة النماذج"),
        help_text=_("ترتيب المجموعة التي ينتمي إليها هذا النموذج")
    )
    difficulty_profile = models.CharField(
        max_length=20,
        choices=[
            ('easy', _('سهل')),
            ('medium', _('متوسط')),
            ('hard', _('صعب')),
            ('mixed', _('مختلط'))
        ],
        default='mixed',
        verbose_name=_("ملف الصعوبة")
    )
    difficulty_distribution = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("توزيع الصعوبة التفصيلي"),
        help_text=_("مثال: {'easy': 60, 'medium': 30, 'hard': 10}")
    )

    # ── Cryptographic Answer Key Protection ──
    key_status = models.CharField(
        max_length=20,
        choices=KeyStatus.choices,
        default=KeyStatus.DRAFT,
        db_index=True,
        verbose_name=_("حالة مفتاح الإجابة")
    )
    answer_key_snapshot = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("لقطة مفتاح الإجابة المجمدة"),
        help_text=_("المصدر الوحيد للحقيقة للتصحيح بعد النشر")
    )
    answer_key_hash = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("بصمة مفتاح الإجابة (SHA-256)"),
        help_text=_("بصمة تشفيرية تضمن عدم التلاعب بلقطة المفتاح المجمدة")
    )
    key_frozen_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("تاريخ ووقت تجميد المفتاح")
    )
    key_frozen_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="frozen_exam_keys",
        verbose_name=_("المستخدم الذي جمد المفتاح")
    )

    class Meta:
        unique_together = ('exam', 'versionCode')
        verbose_name = _('نموذج اختبار')
        verbose_name_plural = _('نماذج الاختبارات')

    def __str__(self):
        return f"{self.exam.title} - {self.versionCode}"

    @staticmethod
    def calculate_snapshot_hash(snapshot: dict) -> str:
        """Calculates canonical SHA-256 hash of an answer key snapshot."""
        if not snapshot:
            return ""
        canonical_json = json.dumps(snapshot, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    def verify_key_integrity(self) -> bool:
        """
        Active cryptographic verification: returns True if key is frozen and untampered.
        """
        if self.key_status != self.KeyStatus.FROZEN or not self.answer_key_snapshot or not self.answer_key_hash:
            return False
        return self.calculate_snapshot_hash(self.answer_key_snapshot) == self.answer_key_hash

    def freeze_key(self, user=None, force: bool = False, custom_snapshot: dict = None) -> dict:
        """
        Freezes the answer key snapshot from current question orders and options,
        computes its cryptographic SHA-256 hash, and marks status as FROZEN.
        """
        if self.key_status == self.KeyStatus.FROZEN and not force:
            if not self.verify_key_integrity():
                raise ValueError(
                    f"ExamVersion {self.id} key is FROZEN but failed cryptographic integrity check!"
                )
            return self.answer_key_snapshot

        if custom_snapshot is not None:
            payload = custom_snapshot
        else:
            question_orders = self.question_orders.filter(
                is_deleted=False
            ).order_by('orderIndex').select_related('question')

            questions_data = {}
            label_map = ["A", "B", "C", "D", "E", "F"]

            for qo in question_orders:
                q = qo.question
                opts = list(q.options.filter(is_deleted=False).order_by('order_index'))

                correct_label = None
                options_list = []
                for idx, opt in enumerate(opts):
                    lbl = label_map[idx] if idx < len(label_map) else str(idx)
                    if opt.isTrue:
                        correct_label = lbl
                    options_list.append({
                        "index": idx,
                        "id": opt.id,
                        "label": lbl,
                        "is_correct": bool(opt.isTrue)
                    })

                weight = float(getattr(q, 'defaultMark', None) or getattr(q, 'assigned_weight', 1.0) or 1.0)
                questions_data[str(qo.orderIndex)] = {
                    "question_id": q.id,
                    "correct_choice": correct_label,
                    "assigned_weight": weight,
                    "options": options_list
                }

            payload = {
                "exam_id": self.exam_id,
                "version_id": self.id,
                "version_code": self.versionCode,
                "total_questions": len(questions_data),
                "questions": questions_data
            }

        snapshot_hash = self.calculate_snapshot_hash(payload)
        self.answer_key_snapshot = payload
        self.answer_key_hash = snapshot_hash
        self.key_status = self.KeyStatus.FROZEN
        self.key_frozen_at = timezone.now()
        self.key_frozen_by = user
        self.save(update_fields=['key_status', 'answer_key_snapshot', 'answer_key_hash', 'key_frozen_at', 'key_frozen_by'])
        return payload

    def get_answer_key_and_weights(self) -> tuple:
        """
        Returns (answer_key, marks_map) strictly from the frozen snapshot.
        If frozen, performs active cryptographic verification (verify_key_integrity).
        If verification fails, raises ValueError(CRITICAL_INTEGRITY_VIOLATION).
        If not frozen, freezes the key snapshot automatically first.
        """
        if self.key_status == self.KeyStatus.FROZEN:
            if not self.verify_key_integrity():
                raise ValueError(
                    f"CRITICAL_INTEGRITY_VIOLATION: ExamVersion {self.id} ({self.versionCode}) "
                    "answer key snapshot failed cryptographic SHA-256 integrity verification!"
                )
            snapshot = self.answer_key_snapshot
        else:
            snapshot = self.freeze_key()

        answer_key = {}
        marks_map = {}
        for q_num_str, q_info in snapshot.get("questions", {}).items():
            answer_key[str(q_num_str)] = q_info.get("correct_choice") or "A"
            marks_map[str(q_num_str)] = float(q_info.get("assigned_weight", 1.0) or 1.0)

        return answer_key, marks_map
