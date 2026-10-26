<template>
  <div class="student-card-settings">
    <!-- Student Card Toggle -->
    <div class="pa-4 rounded-xl border bg-surface mb-4 d-flex justify-space-between align-center">
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
      <!-- ── Dynamic Institution Identity Switcher (School vs University vs Institute) ── -->
      <div class="pa-4 rounded-xl border bg-surface mb-4">
        <div class="d-flex align-center justify-space-between mb-2">
          <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
            <v-icon color="primary" size="20">mdi-domain-switch</v-icon>
            نمط ونطاق حقول هوية الطالب:
          </label>
          <v-chip size="x-small" :color="activeProfile.color" variant="flat" class="font-weight-bold">
            {{ activeProfile.name }}
          </v-chip>
        </div>

        <!-- Dynamic Switcher Buttons from Registry -->
        <v-btn-toggle
          v-model="currentInstitutionType"
          mandatory
          color="primary"
          density="comfortable"
          rounded="lg"
          grow
          class="w-100 mb-2"
          @update:model-value="onInstitutionChange"
        >
          <v-btn
            v-for="profile in INSTITUTION_PROFILES"
            :key="profile.id"
            :value="profile.id"
            class="font-weight-bold"
          >
            <v-icon start size="18">{{ profile.icon }}</v-icon>
            {{ profile.name }}
          </v-btn>
        </v-btn-toggle>

        <div class="d-flex align-center justify-space-between text-caption text-medium-emphasis">
          <span>{{ activeProfile.fullName }}</span>
          <v-btn
            size="x-small"
            variant="text"
            color="primary"
            prepend-icon="mdi-restore"
            class="font-weight-bold"
            @click="applyProfileDefaults(activeProfile)"
          >
            استعادة نموذج {{ activeProfile.name }}
          </v-btn>
        </div>
      </div>

      <!-- Institutional Header & Seal (Dynamic Labels) -->
      <div class="pa-4 rounded-xl border bg-surface mb-4">
        <label class="text-subtitle-2 font-weight-bold mb-2 d-block">
          الترويسة والشعار — {{ activeProfile.fullName }}
        </label>
        <v-text-field
          v-model="config.header.institution_name"
          :label="activeProfile.labels.institution"
          variant="outlined"
          density="compact"
          rounded="lg"
          class="mb-3"
          hide-details
        />
        <v-text-field
          v-model="config.header.sub_title"
          :label="activeProfile.labels.subTitle"
          variant="outlined"
          density="compact"
          rounded="lg"
          class="mb-3"
          hide-details
        />
        <v-row dense>
          <v-col cols="6">
            <v-text-field
              v-model="config.header.exam_stage_title"
              :label="activeProfile.labels.examStage"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="config.metadata.academic_year"
              :label="activeProfile.labels.academicYear"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
        </v-row>
      </div>

      <!-- Exam & Subject Information (Dynamic Labels) -->
      <div class="pa-4 rounded-xl border bg-surface mb-4">
        <label class="text-subtitle-2 font-weight-bold mb-2 d-block">بيانات المقرر وموقع الاختبار</label>
        <v-text-field
          v-model="config.header.exam_name"
          :label="activeProfile.labels.examSubject"
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
              :label="activeProfile.labels.area1"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="config.header.directorate"
              :label="activeProfile.labels.area2"
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
              :label="activeProfile.labels.centerName"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="config.header.center_code"
              :label="activeProfile.labels.centerCode"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
        </v-row>
      </div>

      <!-- Student Identifier & Serial Box (Dynamic Labels) -->
      <div class="pa-4 rounded-xl border bg-surface mb-4">
        <label class="text-subtitle-2 font-weight-bold mb-2 d-block">
          صندوق {{ activeProfile.labels.seatNumber }} والرقم التسلسلي
        </label>
        <v-row dense>
          <v-col cols="7">
            <v-text-field
              v-model="config.header.seat_number"
              :label="activeProfile.labels.seatNumber"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
          <v-col cols="5">
            <v-text-field
              v-model="config.header.serial_number"
              :label="activeProfile.labels.serialNumber"
              variant="outlined"
              density="compact"
              rounded="lg"
              hide-details
            />
          </v-col>
        </v-row>
      </div>

      <!-- Absence & Violations Section -->
      <div class="pa-4 rounded-xl border bg-surface">
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
import { ref, computed } from 'vue'
import { INSTITUTION_PROFILES, getProfileById, type InstitutionProfile } from '../composables/useInstitutionProfiles'

const props = defineProps<{
  config: any
}>()

const currentInstitutionType = ref<string>(
  props.config?.institution_type ||
  (props.config?.header?.institution_name?.includes('التعليم العالي')
    ? 'university'
    : props.config?.header?.institution_name?.includes('التعليم الفني') || props.config?.header?.institution_name?.includes('المعهد')
    ? 'institute'
    : 'school')
)

const activeProfile = computed<InstitutionProfile>(() => {
  return getProfileById(currentInstitutionType.value)
})

function onInstitutionChange(typeId: string) {
  currentInstitutionType.value = typeId
  if (props.config) {
    props.config.institution_type = typeId
  }
  const prof = getProfileById(typeId)
  applyProfileDefaults(prof)
}

function applyProfileDefaults(prof: InstitutionProfile) {
  if (!props.config) return
  props.config.institution_type = prof.id
  if (props.config.header) {
    props.config.header.institution_name = prof.defaults.institution_name
    props.config.header.sub_title = prof.defaults.sub_title
    props.config.header.exam_stage_title = prof.defaults.exam_stage_title
    props.config.header.governorate = prof.defaults.governorate
    props.config.header.directorate = prof.defaults.directorate
    props.config.header.center_name = prof.defaults.center_name
    props.config.header.center_code = prof.defaults.center_code
    if (prof.defaults.primary_color) {
      props.config.header.primary_color = prof.defaults.primary_color
    }
  }
  if (props.config.metadata) {
    props.config.metadata.academic_year = prof.defaults.academic_year
  }
}
</script>
