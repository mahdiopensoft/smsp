<template>
  <!-- حقل التاريخ الهجري -->
  <date-picker
    v-model="localHijri"
    :label="$t ? $t('date_hai') : 'التاريخ الهجري'"
    :cols="cols"
    :rules="rules"
  />

  <!-- حقل التاريخ الميلادي -->
  <custom-date
    v-model="localGregorian"
    :label="$t ? $t('date_m') : 'التاريخ الميلادي'"
    :cols="cols"
    :rules="rules"
  />
</template>

<script>
import moment from 'moment-hijri';

export default {
  name: 'DualDatePicker',
  props: {
    gregorian: { type: String, default: '' },
    hijri:     { type: String, default: '' },
    cols:      { type: [String, Number], default: 12 },
    rules:     { type: Array, default: () => [] }
  },
  emits: ['update:gregorian', 'update:hijri'],
  computed: {
    // ── التاريخ الميلادي ─────────────────────────────
    localGregorian: {
      get() {
        const val = this.gregorian || '';
        if (!val) return '';
        // date-picker يستخدم new Date(val) داخلياً —
        // القيمة 'YYYY-MM-DD' تُفسَّر كـ UTC منتصف الليل مما يُظهر اليوم الخاطئ
        // في المناطق الزمنية السالبة (UTC-7).
        // الحل: نُمرّر 'YYYY-MM-DDT00:00:00' لإجبار التوقيت المحلي
        // دون المساس بالمكوّن الأصلي DatePicker.vue
        return val.includes('T') ? val : val + 'T00:00:00';
      },
      set(val) {
        // date-picker يُرسل 'YYYY-MM-DD' — نُنظّفها من T إن وُجد
        const clean = val ? val.split('T')[0] : '';

        // 1) أرسل قيمة الميلادي النظيفة للأب
        this.$emit('update:gregorian', clean);

        // 2) حوّل وأرسل الهجري للأب
        // moment.utc() يجعل التحويل مستقلاً عن المنطقة الزمنية للمتصفح
        if (clean) {
          const m = moment.utc(clean, 'YYYY-MM-DD');
          if (m.isValid()) {
            this.$emit('update:hijri', m.format('iYYYY-iMM-iDD'));
          }
        } else {
          this.$emit('update:hijri', '');
        }
      }
    },

    // ── التاريخ الهجري ───────────────────────────────
    localHijri: {
      get() {
        return this.hijri || '';
      },
      set(val) {
        // 1) أرسل قيمة الهجري للأب
        this.$emit('update:hijri', val);

        // 2) حوّل وأرسل الميلادي للأب
        if (val) {
          const m = moment.utc(val, 'iYYYY-iMM-iDD');
          if (m.isValid()) {
            this.$emit('update:gregorian', m.format('YYYY-MM-DD'));
          }
        } else {
          this.$emit('update:gregorian', '');
        }
      }
    }
  }
};
</script>
