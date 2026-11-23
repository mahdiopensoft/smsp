<template>
  <custom-dialog
    :model-value="modelValue"
    :title="student?.student_name || 'معاينة ورقة الإجابة'"
    width="850"
    height="88vh"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div v-if="student">
      <!-- شريط تحذيري خاص بالمعاينة التجريبية -->
      <v-alert
        v-if="student?.is_demo"
        type="warning"
        variant="flat"
        density="compact"
        rounded="lg"
        class="text-center font-weight-black text-caption py-1.5 mb-3"
        icon="mdi-flask-outline"
      >
        نموذج معاينة تجريبية (بيانات افتراضية للاختبار فقط) — وثيقة غير رسمية ويمنع طباعتها أو توزيعها على مراكز الاختبارات
      </v-alert>

      <!-- Subheader metadata & print button -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-2 pb-3 mb-4 border-b">
        <div>
          <div class="d-flex align-center gap-2 flex-wrap">
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
      </div>

      <div class="pa-4 d-flex justify-center bg-grey-lighten-5 rounded-xl">
        <div ref="previewWrapRef" class="single-sheet-preview-wrap bg-white rounded-xl border elevation-1 pa-3">
          <YemeniAuditReportSheet
            v-if="layout === 'full_a4'"
            :hide-action-bar="true"
            :student-name="student.student_name"
            :seat-number="student.seat_number"
            :serial-number="student.secret_number || student.model_code"
            :model-code="student.model_code || 'A'"
            :form-number="student.model_code || 'A'"
            :exam-subject="exam?.subject_name || ''"
            :exam-stage-title="customStageTitle || (exam?.stage_name ? `اختبار ${exam.stage_name}` : (exam?.title || 'اختبار'))"
            :exam-year="customExamYear || exam?.year_name || ''"
            :center-name="customCenterName || student.school_name || exam?.center_name || exam?.school_name || exam?.directorate || ''"
            :center-code="student.school_id || exam?.id || ''"
            :governorate="customGovernorate || student.governorate || exam?.governorate || ''"
            :directorate="customDirectorate || student.directorate || exam?.directorate || ''"
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
            :exam-subject="exam?.subject_name || ''"
            :exam-stage-title="customStageTitle || (exam?.stage_name ? `اختبار ${exam.stage_name}` : (exam?.title || 'اختبار'))"
            :exam-year="customExamYear || exam?.year_name || ''"
            :center-name="customCenterName || student.school_name || exam?.center_name || exam?.school_name || exam?.directorate || ''"
            :governorate="customGovernorate || student.governorate || exam?.governorate || ''"
            :directorate="customDirectorate || student.directorate || exam?.directorate || ''"
            :barcode-value="student.barcode_value || `EXAM_${exam?.id}_VER_${student.model_code || 'A'}_SEAT_${student.seat_number}`"
            :qr-value="student.qr_value || `${exam?.uniqueCode}|${student.model_code || 'A'}|${student.seat_number}`"
            :total-questions="questionsCount"
            :sections="sections"
            :interactive="false"
          />
        </div>
      </div>
    </div>
  </custom-dialog>
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
