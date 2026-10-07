from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models.common.BaseSyncModel import BaseSyncModel

class SchoolClassTrack(BaseSyncModel):
    level = models.ForeignKey(
        'academic.SchoolLevel', 
        related_name='class_tracks', 
        on_delete=models.CASCADE, 
        verbose_name=_("الصف الدراسي")
    )
    track = models.ForeignKey(
        'academic.SchoolTrack', 
        related_name='track_classes', 
        on_delete=models.PROTECT, 
        verbose_name=_("المسار")
    )
    is_default = models.BooleanField(default=True, verbose_name=_("مسار افتراضي"))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("نشط"))
    note = models.TextField(max_length=250, null=True, blank=True, verbose_name=_("الملاحظة"))

    class Meta:
        db_table = 'schools_class_track'
        verbose_name = _("مسار الصف المدرسي")
        verbose_name_plural = _("مسارات الصفوف المدرسية")
        constraints = [
            models.UniqueConstraint(
                fields=['level', 'track'],
                name='unique_school_level_track_integrity',
            ),
        ]

    @property
    def full_name(self):
        class_name = getattr(self.level, 'name_ar', '') if self.level else ''
        track_name = getattr(self.track, 'name_ar', '') if self.track else ''
        if track_name:
            return f"{class_name} - {track_name}"
        return class_name

    def __str__(self):
        return self.full_name
