from django.db import models
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class BaseSyncModel(SoftDeleteModel):
    """
    النموذج الأساسي لجميع كيانات النظام الأكاديمي.
    يدعم الحذف المرن وتتبع مزامنة السجلات مع البوابة المركزية.
    """
    portal_id = models.BigIntegerField(
        null=True, 
        blank=True, 
        verbose_name=_('معرف البوابة'),
        help_text=_('المعرف الفريد للسجل في نظام البوابة')
    )
    source_system = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('نظام المصدر'),
        help_text=_('النظام الذي جاءت منه البيانات (portal, school, university, institute)')
    )
    last_synced_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name=_('تاريخ آخر مزامنة')
    )

    class Meta:
        abstract = True
