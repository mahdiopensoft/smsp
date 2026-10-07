
import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from utils.core.base_sync_model import BaseSyncModel,models
# from portals.coordination_acceptance.models.Institution import Institution
class MetaDataTable(BaseSyncModel):
    # fk_institution = models.ForeignKey(
    #     Institution,
    #     related_name="institution_metadata",
    #     on_delete=models.CASCADE,
    #     verbose_name=_('المؤسسة الفرعية'),
    #     help_text=_('المؤسسةالفرعية المرتبطة بحساب المؤسسة الرئيسية'),
    #     null=True,
    #     blank=True,
    # )

    title = models.CharField(
        max_length=500,
        verbose_name=_('العنوان'),
        help_text=_('اسم أو وصف السجل كما هو في النظام المصدري'),
    )
    name_table = models.CharField(
        max_length=255,
        verbose_name=_('اسم الجدول المصدري'),
        help_text=_('اسم الجدول الأصلي مثل'),
    )

    class Meta:
        verbose_name = _('جدول البيانات الوصفية')
        verbose_name_plural = _('جداول البيانات الوصفية')
        ordering = ['name_table', 'title']
        constraints = [
            models.UniqueConstraint(
                fields=['external_id', 'source_system', 'name_table'],
                condition=Q(is_deleted=False),
                name='unique_metadata_external_source_table',
            ),
        ]

    def __str__(self):
        return f'{self.name_table}: {self.title}'
