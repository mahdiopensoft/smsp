<template>
  <v-dialog :model-value="modelValue" max-width="880" scrollable @update:model-value="$emit('update:modelValue', $event)">
    <v-card class="pa-6 rounded-2xl">
      <div class="d-flex align-center justify-space-between mb-4 pb-3 border-b flex-wrap gap-2">
        <div class="d-flex align-center gap-2">
          <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
            <v-icon color="primary" size="20">mdi-eye-outline</v-icon>
          </v-avatar>
          <div>
            <h3 class="text-h6 font-weight-black mb-0">معاينة ورقة الإجابة: {{ template?.name }}</h3>
            <span class="text-caption text-medium-emphasis">مقاس A4 قياسي معتمد عالي الدقة 300 DPI</span>
          </div>
        </div>
        <div class="d-flex align-center gap-2 flex-wrap">
          <v-btn
            color="primary"
            variant="tonal"
            size="small"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-pencil-outline"
            @click="$emit('edit', template)"
          >
            فتح في المصمم
          </v-btn>
          <v-btn
            color="secondary"
            variant="outlined"
            size="small"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-printer"
            @click="handlePrint"
          >
            طباعة الورقة
          </v-btn>
          <v-btn
            color="success"
            size="small"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-scanner"
            @click="$emit('scan', template?.id)"
          >
            بدء التصحيح بهذا القالب
          </v-btn>
          <v-btn icon size="small" variant="text" @click="$emit('update:modelValue', false)">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
      </div>

      <div class="pa-4 bg-surface rounded-xl d-flex justify-center overflow-auto" style="max-height: 600px;">
        <div class="sheet-wrapper" :style="previewWrapperStyle">
          <!-- Mode 1: Yemeni Audit Report Sheet (A4 Full) -->
          <YemeniAuditReportSheet
            v-if="isYemeni && (displayMode === 'audit_a4' || !displayMode)"
            :student-name="templateData?.header?.student_name || 'عمرو عبدالباسط عبدالله قائد الزمر'"
            :seat-number="templateData?.header?.seat_number || '418485'"
            :serial-number="templateData?.header?.serial_number || '148'"
            :exam-subject="templateData?.header?.exam_name || template?.name || 'القرآن الكريم'"
            :exam-year="templateData?.metadata?.academic_year || '1444هـ-2022-2023م'"
            :center-name="templateData?.header?.center_name || 'سالم قطن - معين'"
            :center-code="templateData?.header?.center_code || '164'"
            :envelope-no="templateData?.header?.envelope_no || '2'"
            :governorate="templateData?.header?.governorate || 'أمانة العاصمة'"
            :directorate="templateData?.header?.directorate || 'معين'"
            :barcode-value="templateData?.barcode?.value || '41848501164148'"
            :qr-value="templateData?.qr?.value || 'YE-MOE-1444-418485-SUB1'"
            :mcq-bubble-type="templateData?.questions?.layout?.bubble_type || 'numbers'"
            :tf-bubble-type="templateData?.questions?.layout?.tf_bubble_type || 'arabic'"
            :choices-count="templateData?.questions?.layout?.choices_count || 4"
            :bubble-radius="templateData?.questions?.layout?.bubble_radius_mm || 2.1"
            :show-simulated-handwriting="templateData?.instructions?.show_simulated_handwriting || false"
            :total-questions="templateData?.questions?.metadata?.num_questions || template?.total_mcq || 50"
            :sections="templateData?.questions?.sections"
            :columns-count="templateData?.questions?.layout?.columns_count || 4"
            :row-spacing="templateData?.questions?.layout?.row_spacing_mm || 5.2"
          />

          <!-- Mode 2: Yemeni Ministry Student Answer Sheet (A5 Compact) -->
          <YemeniMinistrySheet
            v-else-if="isYemeni && displayMode === 'compact_a5'"
            layout-mode="compact_a5"
            :republic-name="templateData?.header?.institution_name?.split('—')[0]?.trim() || 'الجمهورية اليمنية'"
            :ministry-name="templateData?.header?.institution_name?.split('—')[1]?.trim() || 'وزارة التربية والتعليم'"
            :sector-name="templateData?.header?.sub_title || 'قطاع المناهج والتوجيه — لجان الاختبارات'"
            :exam-stage-title="templateData?.header?.exam_stage_title || 'اختبار الشهادة الثانوية العامة (القسم العلمي)'"
            :exam-subject="templateData?.header?.exam_name || template?.name || 'القرآن الكريم'"
            :exam-year="templateData?.metadata?.academic_year || '1444هـ — 2022-2023م'"
            :student-name="templateData?.header?.student_name || 'عمرو عبدالباسط عبدالله قائد الزمر'"
            :seat-number="templateData?.header?.seat_number || '418485'"
            :serial-number="templateData?.header?.serial_number || '148'"
            :label-seat-number="activeProfile.sheetLabels?.seatNumber || activeProfile.labels.seatNumber"
            :label-serial-number="activeProfile.sheetLabels?.serialNumber || activeProfile.labels.serialNumber"
            :label-subject="activeProfile.sheetLabels?.examSubject || activeProfile.labels.examSubject"
            :label-center="activeProfile.sheetLabels?.centerName || activeProfile.labels.centerName"
            :label-center-code="activeProfile.sheetLabels?.centerCode || activeProfile.labels.centerCode"
            :label-governorate="activeProfile.sheetLabels?.area1 || activeProfile.labels.area1"
            :label-directorate="activeProfile.sheetLabels?.area2 || activeProfile.labels.area2"
            :primary-color="templateData?.header?.primary_color || activeProfile.themeColor"
            :emblem-type="templateData?.header?.emblem_type || activeProfile.defaultEmblem || 'republic_eagle'"
            :custom-logo="previewEmblemLogo"
            :show-emblem="templateData?.header?.show_emblem !== false"
            :center-name="templateData?.header?.center_name || 'سالم قطن — معين'"
            :center-code="templateData?.header?.center_code || '164'"
            :envelope-no="templateData?.header?.envelope_no || '2'"
            :governorate="templateData?.header?.governorate || 'أمانة العاصمة'"
            :directorate="templateData?.header?.directorate || 'معين'"
            :barcode-value="templateData?.barcode?.value || '41848501164148'"
            :qr-value="templateData?.qr?.value || 'YE-MOE-1444-418485-SUB1'"
            :instruction1="templateData?.instructions?.rule1"
            :instruction2="templateData?.instructions?.rule2"
            :instruction3="templateData?.instructions?.rule3"
            :instruction4="templateData?.instructions?.rule4"
            :instruction-correct-label="templateData?.instructions?.correct_label"
            :total-questions="templateData?.questions?.metadata?.num_questions || template?.total_mcq || 50"
            :sections="templateData?.questions?.sections"
            :columns-count="templateData?.questions?.layout?.columns_count || 4"
            :row-spacing="templateData?.questions?.layout?.row_spacing_mm || 5.2"
            :bubble-radius="templateData?.questions?.layout?.bubble_radius_mm || 2.1"
            :mcq-bubble-type="templateData?.questions?.layout?.bubble_type || 'numbers'"
            :tf-bubble-type="templateData?.questions?.layout?.tf_bubble_type || 'arabic'"
            :choices-count="templateData?.questions?.layout?.choices_count || 4"
          />

          <!-- Mode 3: Standard University / General Multigraphics Sheet -->
          <OmrSheetMultigraphics
            v-else
            :total-questions="template?.total_mcq || templateData?.questions?.metadata?.num_questions || 180"
            :questions-per-column="templateData?.questions?.layout?.questions_per_column || Math.ceil((template?.total_mcq || 180) / (templateData?.questions?.layout?.columns_count || 4))"
            :total-columns="templateData?.questions?.layout?.columns_count || templateData?.metadata?.columns_count || 4"
            :choices-per-question="templateData?.questions?.layout?.choices_count || templateData?.metadata?.choices_count || 4"
            :primary-color="templateData?.header?.primary_color || '#e6007e'"
            :emblem-type="templateData?.header?.emblem_type || activeProfile.defaultEmblem || 'university_seal'"
            :custom-logo="previewEmblemLogo"
            :show-emblem="templateData?.header?.show_emblem !== false"
            :institution-name="templateData?.header?.institution_name || template?.name || 'نموذج اختبار معياري'"
            :sub-title="templateData?.header?.sub_title || template?.description || 'ورقة إجابة التصحيح الضوئي الآلي'"
            :exam-name="templateData?.header?.exam_name || template?.name"
            :bubble-type="templateData?.questions?.layout?.bubble_type || 'numbers'"
            :layout-direction="templateData?.questions?.layout?.layout_direction || 'rtl'"
          />
        </div>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import { printOmrElement } from '../../utils/omrPrint'
import { getProfileById } from '../composables/useInstitutionProfiles'

const props = defineProps<{
  modelValue: boolean
  template: any
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'edit', template: any): void
  (e: 'scan', templateId: number | string): void
}>()

const OmrSheetMultigraphics = defineAsyncComponent(() =>
  import('@/components/omr_templates/OmrSheetMultigraphics.vue')
)
const YemeniMinistrySheet = defineAsyncComponent(() =>
  import('@/components/omr_templates/YemeniMinistrySheet.vue')
)
const YemeniAuditReportSheet = defineAsyncComponent(() =>
  import('@/components/omr_templates/YemeniAuditReportSheet.vue')
)

const templateData = computed(() => props.template?.template_data || {})
const displayMode = computed(() => templateData.value?.display_mode)
const activeProfile = computed(() => getProfileById(templateData.value?.institution_type || props.template?.institution_type))

const previewEmblemLogo = computed<string>(() => {
  const h = templateData.value?.header
  if (!h) return ''
  const instType = templateData.value?.institution_type || props.template?.institution_type || 'school'
  if (instType === 'university' || h.emblem_type === 'university_seal') {
    return h.university_logo || ''
  }
  if (instType === 'institute' || h.emblem_type === 'institute_seal') {
    return h.institute_logo || ''
  }
  if (instType === 'school' || h.emblem_type === 'republic_eagle') {
    return h.school_logo || ''
  }
  return h.custom_logo || ''
})

const isYemeni = computed(() => {
  const t = props.template
  if (!t) return false
  const name = t.name || ''
  const tId = t.template_id || templateData.value?.template_id || ''
  return (
    name.includes('وزارة التربية') ||
    name.includes('الثانوية') ||
    tId === 'YEMEN_MINISTRY_50' ||
    t.total_mcq === 50 ||
    templateData.value?.questions?.metadata?.num_questions === 50
  )
})

const previewWrapperStyle = computed(() => {
  const isA5 = isYemeni.value && displayMode.value === 'compact_a5'
  const isAuditA4 = isYemeni.value && (displayMode.value === 'audit_a4' || !displayMode.value)
  const widthMm = isA5 ? 210 : 210
  const heightMm = isA5 ? 148.5 : 297
  const scale = isAuditA4 ? 0.72 : (isA5 ? 0.95 : 0.68)

  return {
    width: `${widthMm}mm`,
    minWidth: `${widthMm}mm`,
    height: `${heightMm}mm`,
    minHeight: `${heightMm}mm`,
    transform: `scale(${scale})`,
    transformOrigin: 'top center',
    marginBottom: `calc(-${heightMm}mm * ${1 - scale})`,
    backgroundColor: '#ffffff',
    boxShadow: '0 8px 28px rgba(0,0,0,0.12)',
    borderRadius: '4px',
    overflow: 'hidden',
  }
})

async function handlePrint() {
  const svgEl = document.querySelector('.sheet-wrapper svg') as SVGGraphicsElement
  if (svgEl) {
    await printOmrElement(svgEl, {
      title: props.template?.name || 'OMR_Sheet',
      isA5: isYemeni.value && displayMode.value === 'compact_a5',
    })
  } else {
    window.print()
  }
}
</script>
