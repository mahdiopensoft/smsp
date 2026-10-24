<template>
  <drawer :data="data" :getData="handleDrawerSubmit" click="api/academic/academic-years/">
    <template v-slot>
      <v-row>
        <fields :data="data" url="academic-years" :attr="fieldsAttr" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddAcademicYears',
  props: {
    data: Object,
    items: [Array, Object],
    getData: Function,
  },
  computed: {
    existingItems() {
      if (Array.isArray(this.items)) return this.items;
      if (this.items && Array.isArray(this.items.data)) return this.items.data;
      if (this.items && Array.isArray(this.items.results)) return this.items.results;
      return [];
    },
    isOriginallyCurrent() {
      if (!this.data?.id) return false;
      const found = this.existingItems.find((i) => i.id === this.data.id);
      return Boolean(found?.is_current);
    },
    fieldsAttr() {
      return {
        hijri_year: {
          placeholder: 'مثال: 1446 أو 1445-1446',
          hint: 'أدخل السنة الهجرية بأرقام صحيحة (مثال: 1446 أو 1445-1446)',
          persistentHint: true,
          rules: [
            (v) => (!!v && !!String(v).trim()) || 'السنة الهجرية مطلوبة',
            (v) => this.validateYearFormat(v, 'hijri'),
            (v) => this.checkUnique(v, 'hijri_year', 'السنة الهجرية مسجلة مسبقاً في النظام'),
          ],
          update: (val) => {
            if (val && typeof val === 'string') {
              const converted = this.normalizeDigits(val);
              if (converted !== val) {
                this.data.hijri_year = converted;
              }
            }
          },
        },
        gregorian_year: {
          placeholder: 'مثال: 2024-2025 أو 2025',
          hint: 'أدخل السنة الميلادية بأرقام صحيحة (مثال: 2024-2025 أو 2025)',
          persistentHint: true,
          rules: [
            (v) => (!!v && !!String(v).trim()) || 'السنة الميلادية مطلوبة',
            (v) => this.validateYearFormat(v, 'gregorian'),
            (v) => this.checkUnique(v, 'gregorian_year', 'السنة الميلادية مسجلة مسبقاً في النظام'),
          ],
          update: (val) => {
            if (val && typeof val === 'string') {
              const converted = this.normalizeDigits(val);
              if (converted !== val) {
                this.data.gregorian_year = converted;
              }
            }
          },
        },
        is_current: {
          label: 'السنة الحالية',
          disabled: this.isOriginallyCurrent,
          hint: this.isOriginallyCurrent
            ? 'هذا هو العام الدراسي الحالي النشط في النظام، ولا يمكن إلغاؤه مباشرة؛ لتغيير العام الحالي قم بتفعيل عام دراسي آخر بدلاً منه.'
            : 'تفعيل هذا الخيار سيجعل هذا العام هو العام الدراسي الحالي ويغلق الأعوام الأخرى تلقائياً.',
          persistentHint: true,
          rules: [
            (v) => {
              if (this.isOriginallyCurrent && !v) {
                return 'لا يمكن إلغاء العام الدراسي الحالي؛ يجب تفعيل عام دراسي آخر بدلاً منه.';
              }
              return true;
            },
          ],
        },
        is_active: {
          depend: false,
        },
      };
    },
  },
  methods: {
    async handleDrawerSubmit(params) {
      if (this.data?.is_current) {
        const currentId = this.data.id;
        this.existingItems.forEach((item) => {
          if (!currentId || item.id !== currentId) {
            item.is_current = false;
          }
        });
      }
      if (typeof this.getData === 'function') {
        await this.getData(params);
      }
    },
    normalizeDigits(val) {
      if (!val) return '';
      const arabicNumbers = '٠١٢٣٤٥٦٧٨٩';
      return String(val)
        .replace(/[٠-٩]/g, (d) => arabicNumbers.indexOf(d))
        .trim();
    },
    normalizeYearForComparison(val) {
      if (!val) return '';
      return this.normalizeDigits(val)
        .replace(/\//g, '-')
        .replace(/\s+/g, '');
    },
    validateYearFormat(val, type = 'hijri') {
      if (!val) return true;
      const v = this.normalizeDigits(val);
      const isHijri = type === 'hijri';
      const label = isHijri ? 'الهجرية' : 'الميلادية';
      const example = isHijri ? '1446 أو 1445-1446' : '2024-2025 أو 2025';
      const min = isHijri ? 1300 : 1900;
      const max = isHijri ? 1600 : 2150;

      // Check split year (YYYY-YYYY or YYYY/YYYY or YYYY-YY)
      const splitMatch = v.match(/^(\d{4})\s*[-/]\s*(\d{2,4})$/);
      // Check single year (YYYY)
      const singleMatch = v.match(/^(\d{4})$/);

      if (splitMatch) {
        const y1 = parseInt(splitMatch[1], 10);
        let y2 = parseInt(splitMatch[2], 10);
        if (splitMatch[2].length === 2) {
          const century = Math.floor(y1 / 100) * 100;
          y2 = century + y2;
        }

        if (y1 < min || y1 > max) {
          return `السنة ${label} (${y1}) يجب أن تكون بين ${min} و ${max}`;
        }
        if (y2 !== y1 + 1) {
          return `السنة الثانية (${y2}) يجب أن تلي الأولى (${y1}) مباشرة (مثال: ${example})`;
        }
        return true;
      }

      if (singleMatch) {
        const y = parseInt(singleMatch[1], 10);
        if (y < min || y > max) {
          return `السنة ${label} (${y}) يجب أن تكون بين ${min} و ${max}`;
        }
        return true;
      }

      return `صيغة السنة ${label} غير صحيحة، يرجى كتابتها بالأرقام مثل (${example})`;
    },
    checkUnique(val, fieldName, errorMsg) {
      if (!val) return true;
      const normalizedInput = this.normalizeYearForComparison(val);
      if (!normalizedInput) return true;
      const currentId = this.data?.id;

      const duplicate = this.existingItems.find((item) => {
        if (currentId && item.id === currentId) return false;
        const itemVal = item[fieldName];
        return itemVal && this.normalizeYearForComparison(itemVal) === normalizedInput;
      });

      return duplicate ? errorMsg : true;
    },
  },
};
</script>
