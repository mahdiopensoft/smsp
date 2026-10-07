<template>
  <div class="student-card-settings">
    <!-- Student Card Toggle -->
    <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4 d-flex justify-space-between align-center">
      <div>
        <label class="text-subtitle-2 font-weight-bold d-block">بطاقة بيانات الطالب الرسمية المدمجة</label>
        <span class="text-caption text-medium-emphasis">تتضمن الترويسة والشعار والهوية المؤسسية والدوائر الأمنية</span>
      </div>
      <v-switch
        v-model="config.student_fields.enabled"
        color="primary"
        hide-details
        density="compact"
      />
    </div>

    <template v-if="config.student_fields.enabled">
      <!-- ── Fast Institution Identity Switcher (School vs University) ── -->
      <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
        <div class="d-flex align-center justify-space-between mb-2">
          <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
            <v-icon color="primary" size="20">mdi-domain-switch</v-icon>
            نمط ونطاق حقول هوية الطالب:
          </label>
          <v-chip size="x-small" :color="currentInstitutionType === 'university' ? 'purple' : 'primary'" variant="flat" class="font-weight-bold">
            {{ currentInstitutionType === 'university' ? '🎓 جامعي' : '🏫 مدرسي' }}
          </v-chip>
        </div>

        <!-- Quick Switcher Button Toggle -->
        <v-btn-toggle
          v-model="currentInstitutionType"
          mandatory
          color="primary"
          density="comfortable"
          rounded="lg"
          grow
          class="w-100"
          @update:model-value="onInstitutionChange"
        >
          <v-btn value="school" class="font-weight-bold">
            <v-icon start size="18">mdi-school</v-icon>
            🏫 مدرسي
          </v-btn>
          <v-btn value="university" class="font-weight-bold">
            <v-icon start size="18">mdi-domain</v-icon>
            🎓 جامعي
          </v-btn>
        </v-btn-toggle>
      </div>

      <!-- Institutional Header & Seal -->
      <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
        <label class="text-subtitle-2 font-weight-bold mb-2 d-block">
          {{ currentInstitutionType === 'university' ? 'الترويسة والشعار — التعليم الجامعي والأكاديمي' : 'الترويسة والشعار — التعليم الأساسي والثانوي' }}
        </label>
        <v-text-field
          v-model="config.header.institution_name"
          :label="currentInstitutionType === 'university' ? 'اسم الدولة والجامعة' : 'اسم الدولة والوزارة'"
          variant="outlined"
          density="compact"
          rounded="lg"
          class="mb-3"
          hide-details
        />
        <v-text-field
          v-model="config.header.sub_title"
          :label="currentInstitutionType === 'university' ? 'الكلية / نيابة شؤون الطلاب والامتحانات' : 'القطاع / لجنة الاختبارات'"
          variant="outlined"
          density="compact"
          rounded="lg"
          class="mb-3"
          hide-details
        />
        <v-text-field
          v-model="config.metadata.academic_year"
          :label="currentInstitutionType === 'university' ? 'العام الجامعي / الفصل' : 'العام الدراسي'"
          variant="outlined"
          density="compact"
          rounded="lg"
          hide-details
        />
      </div>

      <!-- Exam & Subject Information -->
      <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
        <label class="text-subtitle-2 font-weight-bold mb-2 d-block">بيانات المادة وموقع الاختبار</label>
        <v-text-field
          v-model="config.header.exam_name"
          :label="currentInstitutionType === 'university' ? 'اسم المقرر الأكاديمي' : 'اسم المادة الدراسية'"
          variant="outlined"
          density="compact"
          rounded="lg"
          class="mb-3"
          hide-details
        />
        <v-row dense class="mb-2">
          <v-col cols="6">
            <v-text-field
              v-model="config.header.governorate"
              :label="currentInstitutionType === 'university' ? 'المدينة / الحرم الجامعي' : 'المحافظة'"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="config.header.directorate"
              :label="currentInstitutionType === 'university' ? 'المبنى / القاعة' : 'المديرية'"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="6">
            <v-text-field
              v-model="config.header.center_name"
              :label="currentInstitutionType === 'university' ? 'الكلية / المعمل' : 'اسم المركز الاختباري'"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="config.header.center_code"
              :label="currentInstitutionType === 'university' ? 'رقم القاعة / الشعبة' : 'رقم المركز'"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
        </v-row>
      </div>

      <!-- Student Identifier & Serial Box -->
      <div class="pa-4 rounded-xl border bg-grey-lighten-5 mb-4">
        <label class="text-subtitle-2 font-weight-bold mb-2 d-block">
          {{ currentInstitutionType === 'university' ? 'صندوق الرقم الأكاديمي / القيد' : 'صندوق رقم الجلوس والرقم التسلسلي' }}
        </label>
        <v-row dense>
          <v-col cols="7">
            <v-text-field
              v-model="config.header.seat_number"
              :label="currentInstitutionType === 'university' ? 'الرقم الأكاديمي / القيد' : 'رقم الجلوس'"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
          <v-col cols="5">
            <v-text-field
              v-model="config.header.serial_number"
              label="الرقم التسلسلي"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
        </v-row>
      </div>

      <!-- Absence & Violations Section -->
      <div class="pa-4 rounded-xl border bg-grey-lighten-5">
        <div class="d-flex align-center justify-space-between mb-2">
          <label class="text-subtitle-2 font-weight-bold">دوائر الملاحظة ولجنة النظام والمراقبة</label>
          <v-chip size="x-small" color="warning" variant="tonal" class="font-weight-bold">5 حالات معتمدة</v-chip>
        </div>
        <p class="text-caption text-medium-emphasis mb-3">
          يتم تضمين دوائر تظليل الحالات الخاصة لتمكين رئيس المركز ولجنة المراقبة من رصد الغياب أو المخالفات آلياً:
        </p>
        <div class="d-flex gap-1 flex-wrap">
          <v-chip size="small" variant="outlined" color="primary">غائب</v-chip>
          <v-chip size="small" variant="outlined" color="error">غش</v-chip>
          <v-chip size="small" variant="outlined" color="error">شغب</v-chip>
          <v-chip size="small" variant="outlined" color="warning">تلفون</v-chip>
          <v-chip size="small" variant="outlined" color="grey-darken-1">أخرى</v-chip>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  config: any
}>()

// Determine current institution type based on config
const currentInstitutionType = ref<string>(
  props.config?.institution_type ||
  (props.config?.header?.institution_name?.includes('التعليم العالي') ? 'university' : 'school')
)

function onInstitutionChange(typeId: string) {
  currentInstitutionType.value = typeId
  if (props.config) {
    props.config.institution_type = typeId
  }
  if (typeId === 'university') {
    if (props.config?.header) {
      props.config.header.institution_name = 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'
      props.config.header.sub_title = 'جامعة صنعاء — كلية الحاسوب وتكنولوجيا المعلومات'
      if (props.config.metadata) {
        props.config.metadata.academic_year = 'العام الجامعي 2024-2025م'
      }
      props.config.header.governorate = 'صنعاء'
      props.config.header.directorate = 'الحرم الجامعي'
      props.config.header.center_name = 'قاعة الاختبارات المركزية'
      props.config.header.center_code = 'A1'
    }
  } else {
    if (props.config?.header) {
      props.config.header.institution_name = 'الجمهورية اليمنية — وزارة التربية والتعليم'
      props.config.header.sub_title = 'قطاع المناهج والتوجيه — لجان الاختبارات'
      if (props.config.metadata) {
        props.config.metadata.academic_year = '1444هـ — 2022-2023م'
      }
      props.config.header.governorate = 'أمانة العاصمة'
      props.config.header.directorate = 'معين'
      props.config.header.center_name = 'سالم قطن — معين'
      props.config.header.center_code = '164'
    }
  }
}
</script>
