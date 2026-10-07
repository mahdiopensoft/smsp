from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from OpenSoftCoreV41.utils.abstract_models.soft_delete_model import SoftDeleteModel

class AuditLog(SoftDeleteModel):
    class ActionChoices(models.TextChoices):
        CREATE = 'إنشاء', _('إنشاء')
        UPDATE = 'تعديل', _('تعديل')
        DELETE = 'حذف', _('حذف')
        APPROVE = 'اعتماد', _('اعتماد')
        REJECT = 'رفض', _('رفض')
        ARCHIVE = 'أرشفة', _('أرشفة')
        RESTORE = 'استعادة', _('استعادة')
        DUPLICATE = 'استنساخ', _('استنساخ')
        NEW_VERSION = 'إصدار جديد', _('إصدار جديد')
        IMPORT = 'استيراد جماعي', _('استيراد جماعي')
        EXPORT = 'تصدير', _('تصدير')
        PRINT = 'طباعة', _('طباعة')
        SYNC = 'مزامنة', _('مزامنة')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name=_("المستخدم المنفذ")
    )
    action = models.CharField(max_length=50, choices=ActionChoices.choices, verbose_name=_("نوع الإجراء"))
    resource_type = models.CharField(max_length=100, verbose_name=_("نوع الكيان (Resource)"))
    resource_id = models.CharField(max_length=100, verbose_name=_("معرف الكيان"))
    description = models.TextField(verbose_name=_("تفاصيل الإجراء"))
    changes = models.JSONField(null=True, blank=True, verbose_name=_("سجل التغييرات (Diff/Data)"))
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("عنوان IP"))

    class Meta:
        verbose_name = _('سجل تدقيق ورقابة')
        verbose_name_plural = _('سجلات التدقيق والرقابة')
        ordering = ['-created_at']

    def __str__(self):
        user_name = self.user.username if self.user else "System"
        return f"[{self.created_at}] {user_name} - {self.action} on {self.resource_type} #{self.resource_id}"
