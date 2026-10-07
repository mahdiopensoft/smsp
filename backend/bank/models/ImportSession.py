import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class ImportSession(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_subject = models.ForeignKey(
        'academic.SchoolClassSubject', 
        on_delete=models.CASCADE, 
        related_name='import_sessions',
        verbose_name=_("مادة مسار الصف"),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _("جلسة استيراد")
        verbose_name_plural = _("جلسات الاستيراد")

    def __str__(self):
        return f"ImportSession {self.id} - {self.class_subject}"
