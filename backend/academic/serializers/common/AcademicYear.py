import re
from django.db import transaction
from rest_framework import serializers
from academic.models.common.AcademicYear import AcademicYear
from django.utils.translation import gettext_lazy as _
from config.imports.viewmodel_core import DynamicFieldsModelSerializer


def normalize_digits(text: str) -> str:
    if not text:
        return ""
    arabic_to_eng = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    return str(text).translate(arabic_to_eng).strip()


def normalize_year_str(val: str) -> str:
    if not val:
        return ""
    v = normalize_digits(val)
    return v.replace('/', '-').replace(' ', '')


def validate_and_normalize_year(raw_val: str, year_type: str = 'hijri') -> str:
    val = normalize_digits(raw_val)
    label = "الهجرية" if year_type == 'hijri' else "الميلادية"
    min_year = 1300 if year_type == 'hijri' else 1900
    max_year = 1600 if year_type == 'hijri' else 2150
    example_single = "1446" if year_type == 'hijri' else "2025"
    example_split = "1445-1446" if year_type == 'hijri' else "2024-2025"

    pattern_split = r'^(\d{4})\s*[-/]\s*(\d{2,4})$'
    pattern_single = r'^(\d{4})$'

    m_split = re.match(pattern_split, val)
    m_single = re.match(pattern_single, val)

    if m_split:
        y1_str, y2_str = m_split.groups()
        y1 = int(y1_str)
        if len(y2_str) == 2:
            century = (y1 // 100) * 100
            y2 = century + int(y2_str)
        else:
            y2 = int(y2_str)

        if not (min_year <= y1 <= max_year):
            raise serializers.ValidationError(
                f"السنة {label} ({y1}) غير صحيحة، يجب أن تكون بين {min_year} و {max_year}."
            )

        if y2 != y1 + 1:
            raise serializers.ValidationError(
                f"صيغة السنة {label} غير صحيحة: السنة الثانية ({y2}) يجب أن تلي السنة الأولى ({y1}) مباشرة، مثال: {example_split}."
            )

        return f"{y1}-{y2}"

    elif m_single:
        y = int(m_single.group(1))
        if not (min_year <= y <= max_year):
            raise serializers.ValidationError(
                f"السنة {label} ({y}) غير صحيحة، يجب أن تكون بين {min_year} و {max_year}."
            )
        return str(y)

    else:
        raise serializers.ValidationError(
            f"صيغة السنة {label} غير صحيحة. يرجى إدخال أرقام صحيحة بالصيغة ({example_split} أو {example_single})."
        )


class AcademicYearSerializer(DynamicFieldsModelSerializer):
    name = serializers.SerializerMethodField()
    name_ar = serializers.SerializerMethodField()

    class Meta:
        model = AcademicYear
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'is_current' in self.fields:
            self.fields['is_current'].validators = [
                v for v in self.fields['is_current'].validators
                if not isinstance(v, serializers.UniqueValidator)
            ]

    def get_validators(self):
        validators = super().get_validators()
        filtered = []
        for v in validators:
            fields = getattr(v, 'fields', None)
            if fields:
                field_list = list(fields) if isinstance(fields, (list, tuple, set)) else [fields]
                if 'is_current' in field_list:
                    continue
            if getattr(v, 'field_name', None) == 'is_current':
                continue
            constraint = getattr(v, 'constraint', None)
            if constraint:
                c_fields = getattr(constraint, 'fields', [])
                if 'is_current' in c_fields or getattr(constraint, 'name', '') == 'unique_single_current_academic_year_no_deleted':
                    continue
            filtered.append(v)
        return filtered

    def get_name(self, obj):
        return str(obj)

    def get_name_ar(self, obj):
        return str(obj)

    def validate_hijri_year(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError(_("السنة الهجرية مطلوبة."))

        normalized = validate_and_normalize_year(value, year_type='hijri')
        norm_key = normalize_year_str(normalized)

        # Uniqueness check for Hijri year
        qs = AcademicYear.objects.filter(is_deleted=False)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        for rec in qs:
            if rec.hijri_year and normalize_year_str(rec.hijri_year) == norm_key:
                raise serializers.ValidationError(_("السنة الهجرية مسجلة مسبقاً في النظام."))

        return normalized

    def validate_gregorian_year(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError(_("السنة الميلادية مطلوبة."))

        normalized = validate_and_normalize_year(value, year_type='gregorian')
        norm_key = normalize_year_str(normalized)

        # Uniqueness check for Gregorian year
        qs = AcademicYear.objects.filter(is_deleted=False)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        for rec in qs:
            if rec.gregorian_year and normalize_year_str(rec.gregorian_year) == norm_key:
                raise serializers.ValidationError(_("السنة الميلادية مسجلة مسبقاً في النظام."))

        return normalized

    def validate(self, attrs):
        attrs = super().validate(attrs)

        # Prevent deactivating the only current academic year directly
        if self.instance and self.instance.is_current:
            is_current_val = attrs.get('is_current')
            if is_current_val is False:
                other_current = AcademicYear.objects.filter(
                    is_current=True, is_deleted=False
                ).exclude(id=self.instance.id).exists()
                if not other_current:
                    raise serializers.ValidationError({
                        "is_current": _("لا يمكن إلغاء العام الدراسي الحالي مباشرة؛ يجب تفعيل عام دراسي آخر بدلاً منه.")
                    })

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['is_active'] = True
            # If no current year exists yet, make this new year current
            has_current = AcademicYear.objects.filter(is_current=True, is_deleted=False).exists()
            if not has_current or validated_data.get('is_current'):
                validated_data['is_current'] = True
                AcademicYear.objects.filter(is_current=True, is_deleted=False).update(is_current=False)
            return super().create(validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data['is_active'] = True
            if validated_data.get('is_current'):
                AcademicYear.objects.filter(is_current=True, is_deleted=False).exclude(id=instance.id).update(is_current=False)
            return super().update(instance, validated_data)
