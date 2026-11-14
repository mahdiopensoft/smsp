<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="850px" scrollable>
    <v-card v-if="student" class="rounded-2xl overflow-hidden main-card border elevation-6">
      <!-- شريط تحذيري خاص بالمعاينة التجريبية -->
      <v-alert
        v-if="student?.is_demo"
        type="warning"
        variant="flat"
        density="compact"
        rounded="0"
        class="text-center font-weight-black text-caption py-1.5"
        icon="mdi-flask-outline"
      >
        ⚠️ نموذج معاينة تجريبية (بيانات افتراضية للاختبار فقط) — وثيقة غير رسمية ويمنع طباعتها أو توزيعها على مراكز الاختبارات
      </v-alert>

      <!-- Dialog Header -->
      <v-card-title class="d-flex align-center justify-space-between bg-surface px-6 py-4 border-b">
        <div class="d-flex align-center gap-3">
          <v-avatar :color="student?.is_demo ? 'warning' : 'primary'" variant="tonal" rounded="lg" size="44">
            <v-icon size="24" :color="student?.is_demo ? 'warning' : 'primary'">
              {{ student?.is_demo ? 'mdi-flask-outline' : 'mdi-card-account-details-outline' }}
            </v-icon>
          </v-avatar>
          <div>
            <div class="d-flex align-center gap-2 flex-wrap">
              <h3 class="text-h6 font-weight-black text-on-surface mb-0">
                {{ student.student_name || 'طالب بدون اسم' }}
              </h3>
              <v-chip
                v-if="student?.is_demo"
                size="small"
                color="warning"
                variant="flat"
                class="font-weight-black px-2.5"
              >
                معاينة تجريبية فقط
              </v-chip>
              <v-chip v-else size="small" color="primary" variant="flat" class="font-weight-bold px-2 unified-table-chip">
                رقم الجلوس: {{ student.seat_number }}
              </v-chip>
              <v-chip size="small" :color="getModelChipColor(student.model_code)" variant="tonal" class="font-weight-bold px-2.5 rounded-lg border">
                نموذج {{ student.model_code || 'A' }}
              </v-chip>
            </div>
            <p class="text-caption text-medium-emphasis mb-0 mt-1">
              {{ exam?.title || 'اختبار عام' }} • {{ student.school_name || exam?.directorate || 'المركز الاختباري' }}
            </p>
          </div>
        </div>

        <div class="d-flex align-center gap-2">
          <v-btn
            v-if="student?.is_demo"
            color="warning"
            variant="tonal"
            rounded="lg"
            size="default"
            class="font-weight-bold px-4 shadow-sm"
            prepend-icon="mdi-printer-eye"
            @click="$emit('print')"
          >
            طباعة مسودة تجريبية
          </v-btn>
          <v-btn
            v-else
            color="success"
            variant="flat"
            rounded="lg"
            size="default"
            class="font-weight-black px-4 shadow-sm"
            prepend-icon="mdi-printer"
            @click="$emit('print')"
          >
            طباعة هذه الورقة
          </v-btn>
          <v-btn icon="mdi-close" variant="text" size="small" color="medium-emphasis" @click="$emit('update:modelValue', false)" />
        </div>
      </v-card-title>

      <v-card-text class="pa-4 d-flex justify-center bg-grey-lighten-5">
        <div ref="previewWrapRef" class="single-sheet-preview-wrap bg-white rounded-xl border elevation-1 pa-3">
          <YemeniAuditReportSheet
            v-if="layout === 'full_a4'"
            :hide-action-bar="true"
            :student-name="student.student_name"
            :seat-number="student.seat_number"
            :serial-number="student.secret_number || student.model_code"
            :model-code="student.model_code || 'A'"
            :form-number="student.model_code || 'A'"
            :exam-subject="exam?.subject_name || 'الرياضيات'"
            :exam-stage-title="customStageTitle || (exam?.stage_name ? `اختبار ${exam.stage_name}` : (exam?.title || 'اختبار الشهادة العامة'))"
            :exam-year="customExamYear || exam?.year_name || '2026'"
            :center-name="customCenterName || student.school_name || exam?.directorate || 'المركز الاختباري الرئيسي'"
            :center-code="student.school_id || exam?.id || '101'"
            :governorate="customGovernorate || student.governorate || exam?.governorate || 'أمانة العاصمة'"
            :directorate="customDirectorate || student.directorate || exam?.directorate || 'السبعين'"
            :barcode-value="student.barcode_value || `EXAM_${exam?.id}_VER_${student.model_code || 'A'}_SEAT_${student.seat_number}`"
            :qr-value="student.qr_value || `${exam?.uniqueCode}|${student.model_code || 'A'}|${student.seat_number}`"
            :total-questions="questionsCount"
            :sections="sections"
          />

          <YemeniMinistrySheet
            v-else
            layout-mode="compact_a5"
            :student-name="student.student_name"
            :seat-number="student.seat_number"
            :serial-number="student.secret_number || student.model_code"
            :model-code="student.model_code || 'A'"
            :exam-subject="exam?.subject_name || 'الرياضيات'"
            :exam-stage-title="customStageTitle || (exam?.stage_name ? `اختبار ${exam.stage_name}` : (exam?.title || 'اختبار الشهادة العامة'))"
            :exam-year="customExamYear || exam?.year_name || '2026'"
            :center-name="customCenterName || student.school_name || exam?.directorate || 'المركز الامتحاني الرئيسي'"
            :governorate="customGovernorate || exam?.governorate || 'أمانة العاصمة'"
            :directorate="customDirectorate || student.directorate || exam?.directorate || 'السبعين'"
            :barcode-value="student.barcode_value || `EXAM_${exam?.id}_VER_${student.model_code || 'A'}_SEAT_${student.seat_number}`"
            :qr-value="student.qr_value || `${exam?.uniqueCode}|${student.model_code || 'A'}|${student.seat_number}`"
            :total-questions="questionsCount"
            :sections="sections"
            :interactive="false"
          />
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'
import YemeniAuditReportSheet from '@/components/omr_templates/YemeniAuditReportSheet.vue'

defineProps<{
  modelValue: boolean
  student: any
  exam: any
  layout: string
  customStageTitle?: string
  customExamYear?: string
  customCenterName?: string
  customGovernorate?: string
  customDirectorate?: string
  questionsCount?: number
  sections?: any[]
  getModelChipColor: (code?: string) => string
}>()

defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'print'): void
}>()

const previewWrapRef = ref<HTMLElement | null>(null)
defineExpose({
  previewWrapRef
})
</script>

<style scoped>
.single-sheet-preview-wrap {
  width: 100%;
  max-width: 800px;
  overflow: auto;
}
</style>
