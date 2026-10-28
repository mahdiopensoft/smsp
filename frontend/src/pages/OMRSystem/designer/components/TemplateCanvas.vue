<template>
  <div class="template-canvas-container d-flex flex-column h-100">
    <!-- ── Canvas Control Toolbar ────────────────────────────────── -->
    <CanvasToolbar
      :zoom-mode="zoomMode"
      :zoom-level="zoomLevel"
      :current-zoom-display="currentZoomDisplay"
      :presentation-mode="presentationMode"
      :has-simulated-answers="Object.keys(simulatedAnswers).length > 0"
      @update:zoom-mode="zoomMode = $event"
      @update:presentation-mode="presentationMode = $event"
      @zoom-in="zoomIn"
      @zoom-out="zoomOut"
      @reset-zoom="resetZoom"
      @random-shade="randomShade"
      @clear-shade="clearShade"
      @save="emit('save')"
      @export-json="exportJson(config)"
      @print="printSheet(config, presentationMode)"
      @export-png="exportPNG(config)"
    />

    <!-- ── Interactive Viewport Canvas ───────────────────────────── -->
    <div
      ref="viewportRef"
      class="canvas-viewport pa-6 rounded-2xl border overflow-auto text-center position-relative flex-grow-1"
      style="min-height: 600px; max-height: calc(100vh - 260px);"
    >
      <div class="sheet-artboard-container d-inline-block rounded-lg elevation-6 bg-white position-relative" :style="containerStyle">
        <!-- Mode 1: Yemeni Official Electronic Audit Sheet (A4 Full) -->
        <YemeniAuditReportSheet
          v-if="presentationMode === 'audit_a4'"
          :student-name="config.header?.student_name || '................................'"
          :seat-number="config.header?.seat_number || '418485'"
          :serial-number="config.header?.serial_number || '101'"
          :model-code="config.header?.model_code || '1'"
          :form-number="config.header?.model_code || '1'"
          :exam-subject="config.header?.exam_name || 'الرياضيات'"
          :exam-stage-title="config.header?.sub_title || 'اختبار الشهادة العامة'"
          :exam-year="config.metadata?.academic_year || '2026'"
          :center-name="config.header?.center_name || 'المركز الاختباري الرئيسي'"
          :center-code="config.header?.center_code || '101'"
          :envelope-no="config.header?.envelope_no || '1'"
          :governorate="config.header?.governorate || 'أمانة العاصمة'"
          :directorate="config.header?.directorate || 'السبعين'"
          :barcode-value="config.barcode?.value || '41848501164148'"
          :qr-value="config.qr?.value || 'YE-MOE-1444-418485-SUB1'"
          :student-answers="simulatedAnswers"
          :mcq-bubble-type="config.questions?.layout?.bubble_type || 'numbers'"
          :tf-bubble-type="config.questions?.layout?.tf_bubble_type || 'arabic'"
          :choices-count="config.questions?.layout?.choices_count || 4"
          :bubble-radius="config.questions?.layout?.bubble_radius_mm || 2.1"
          :show-simulated-handwriting="config.instructions?.show_simulated_handwriting || false"
          :total-questions="config.questions?.metadata?.num_questions || 50"
          :sections="config.questions?.sections"
          :columns-count="config.questions?.layout?.columns_count || 4"
          :row-spacing="config.questions?.layout?.row_spacing_mm || 5.2"
        />

        <!-- Mode 2: Student Exam Answer Sheet (A5 Compact) -->
        <YemeniMinistrySheet
          v-else-if="presentationMode === 'compact_a5'"
          layout-mode="compact_a5"
          :republic-name="config.header?.institution_name?.split('—')[0]?.trim() || config.header?.institution_name || 'الجمهورية اليمنية'"
          :ministry-name="config.header?.institution_name?.split('—')[1]?.trim() || 'وزارة التربية والتعليم'"
          :sector-name="config.header?.sub_title || 'قطاع المناهج والتوجيه — لجان الاختبارات'"
          :exam-stage-title="config.header?.exam_stage_title || 'اختبار الشهادة العامة'"
          :exam-subject="config.header?.exam_name || 'الرياضيات'"
          :exam-year="config.metadata?.academic_year || '2026'"
          :student-name="config.header?.student_name || '................................'"
          :seat-number="config.header?.seat_number || '418485'"
          :serial-number="config.header?.serial_number || '101'"
          :label-seat-number="activeProfile.sheetLabels?.seatNumber || activeProfile.labels.seatNumber"
          :label-serial-number="activeProfile.sheetLabels?.serialNumber || activeProfile.labels.serialNumber"
          :label-subject="activeProfile.sheetLabels?.examSubject || activeProfile.labels.examSubject"
          :label-center="activeProfile.sheetLabels?.centerName || activeProfile.labels.centerName"
          :label-center-code="activeProfile.sheetLabels?.centerCode || activeProfile.labels.centerCode"
          :label-governorate="activeProfile.sheetLabels?.area1 || activeProfile.labels.area1"
          :label-directorate="activeProfile.sheetLabels?.area2 || activeProfile.labels.area2"
          :primary-color="config.header?.primary_color || activeProfile.themeColor"
          :emblem-type="config.header?.emblem_type || activeProfile.defaultEmblem || 'republic_eagle'"
          :custom-logo="activeEmblemLogo"
          :show-emblem="config.header?.show_emblem !== false"
          :model-code="config.header?.model_code || '1'"
          :center-name="config.header?.center_name || 'المركز الاختباري الرئيسي'"
          :center-code="config.header?.center_code || '101'"
          :envelope-no="config.header?.envelope_no || '1'"
          :governorate="config.header?.governorate || 'أمانة العاصمة'"
          :directorate="config.header?.directorate || 'السبعين'"
          :barcode-value="config.barcode?.value || '41848501164148'"
          :qr-value="config.qr?.value || 'YE-MOE-1444-418485-SUB1'"
          :student-answers="simulatedAnswers"
          :interactive="true"
          :mcq-bubble-type="config.questions?.layout?.bubble_type || 'numbers'"
          :tf-bubble-type="config.questions?.layout?.tf_bubble_type || 'arabic'"
          :choices-count="config.questions?.layout?.choices_count || 4"
          :bubble-radius="config.questions?.layout?.bubble_radius_mm || 2.1"
          :instruction1="config.instructions?.rule1"
          :instruction2="config.instructions?.rule2"
          :instruction3="config.instructions?.rule3"
          :instruction4="config.instructions?.rule4"
          :instruction-correct-label="config.instructions?.correct_label"
          :show-simulated-handwriting="config.instructions?.show_simulated_handwriting || false"
          :total-questions="config.questions?.metadata?.num_questions || 50"
          :sections="config.questions?.sections"
          :columns-count="config.questions?.layout?.columns_count || 4"
          :row-spacing="config.questions?.layout?.row_spacing_mm || 5.2"
          @bubble-click="onBubbleClick"
        />

        <!-- Mode 3: Standard University / General Multigraphics Sheet -->
        <OmrSheetMultigraphics
          v-else
          :total-questions="config.questions?.metadata?.num_questions || 180"
          :questions-per-column="config.questions?.layout?.questions_per_column || 45"
          :total-columns="config.questions?.layout?.columns_count || 4"
          :row-spacing="config.questions?.layout?.row_spacing_mm || 4.2"
          :bubble-radius="config.questions?.layout?.bubble_radius_mm || 1.7"
          :choices-per-question="config.questions?.layout?.choices_count || 4"
          :bubble-type="config.questions?.layout?.bubble_type || 'numbers'"
          :layout-direction="config.questions?.layout?.layout_direction || 'rtl'"
          :primary-color="config.header?.primary_color || '#1976D2'"
          :emblem-type="config.header?.emblem_type || activeProfile.defaultEmblem || 'university_seal'"
          :custom-logo="activeEmblemLogo"
          :show-emblem="config.header?.show_emblem !== false"
          :institution-name="config.header?.institution_name || 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'"
          :sub-title="config.header?.sub_title || 'الإدارة العامة للامتحانات والتقويم الآلي'"
          :exam-name="config.header?.exam_name || 'اختبار نهائي'"
          :student-name="config.header?.student_name || 'طالب اختبار معياري'"
          :barcode-value="config.barcode?.value || '41848501164148'"
          :student-answers="simulatedAnswers"
          :interactive="true"
          @bubble-click="onBubbleClick"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent, watch } from 'vue'
import CanvasToolbar from './canvas/CanvasToolbar.vue'
import { useCanvasExport } from '../composables/useCanvasExport'
import { getProfileById } from '../composables/useInstitutionProfiles'

const props = defineProps<{
  config: any
}>()

const emit = defineEmits<{
  (e: 'save'): void
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

const { printSheet, exportPNG, exportJson } = useCanvasExport()

const activeProfile = computed(() => getProfileById(props.config?.institution_type))

const activeEmblemLogo = computed<string>(() => {
  const h = props.config?.header
  if (!h) return ''
  const instType = props.config?.institution_type || 'school'
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

const presentationMode = ref<'audit_a4' | 'compact_a5' | 'university_180'>(
  props.config?.display_mode === 'compact_a5'
    ? 'compact_a5'
    : props.config?.display_mode === 'university_180'
    ? 'university_180'
    : 'audit_a4'
)

watch(
  () => props.config?.display_mode,
  (val) => {
    if (val && val !== presentationMode.value) {
      presentationMode.value = val as any
    }
  }
)

watch(presentationMode, (val) => {
  if (props.config) {
    props.config.display_mode = val
    if (val === 'compact_a5') {
      props.config.paper.size = 'A5'
      props.config.paper.width_mm = 210
      props.config.paper.height_mm = 148.5
      props.config.paper.orientation = 'landscape'
    } else {
      props.config.paper.size = 'A4'
      props.config.paper.width_mm = 210
      props.config.paper.height_mm = 297
      props.config.paper.orientation = 'portrait'
    }
  }
})

const zoomMode = ref<'fit' | 'actual' | 'custom'>('fit')
const zoomLevel = ref(1.0)
const simulatedAnswers = ref<Record<number, any>>({})

function zoomIn() {
  if (zoomMode.value === 'fit' && presentationMode.value === 'audit_a4') {
    zoomLevel.value = 0.68
  }
  zoomMode.value = 'custom'
  zoomLevel.value = Math.min(Math.round((zoomLevel.value + 0.15) * 100) / 100, 3.0)
}

function zoomOut() {
  if (zoomMode.value === 'fit' && presentationMode.value === 'audit_a4') {
    zoomLevel.value = 0.68
  }
  zoomMode.value = 'custom'
  zoomLevel.value = Math.max(Math.round((zoomLevel.value - 0.15) * 100) / 100, 0.4)
}

function resetZoom() {
  zoomMode.value = 'fit'
  zoomLevel.value = 1.0
}

watch(zoomMode, (mode) => {
  if (mode === 'fit' || mode === 'actual') {
    zoomLevel.value = 1.0
  }
})

const currentZoomDisplay = computed(() => {
  if (zoomMode.value === 'fit') {
    if (presentationMode.value === 'audit_a4') return 0.68
    return 1.0
  }
  if (zoomMode.value === 'actual') return 1.0
  return zoomLevel.value
})

const currentAspectRatio = computed(() => {
  if (presentationMode.value === 'compact_a5') return '210 / 148.5'
  return '210 / 297'
})

const containerStyle = computed(() => {
  const ar = currentAspectRatio.value
  if (presentationMode.value === 'audit_a4') {
    const scaleFactor = zoomMode.value === 'fit' ? 0.68 : (zoomMode.value === 'actual' ? 1.0 : zoomLevel.value)
    return {
      width: '210mm',
      minWidth: '210mm',
      minHeight: '297mm',
      transform: `scale(${scaleFactor})`,
      transformOrigin: 'top center',
      margin: '0 auto',
      marginBottom: `calc(-297mm * ${Math.max(0, 1 - scaleFactor)})`,
      boxShadow: '0 12px 36px rgba(0,0,0,0.14)',
      transition: 'transform 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
    }
  }

  if (zoomMode.value === 'fit') {
    return {
      width: 'auto',
      maxWidth: '100%',
      height: 'calc(100vh - 320px)',
      maxHeight: '780px',
      aspectRatio: ar,
      margin: '0 auto',
      boxShadow: '0 12px 36px rgba(0,0,0,0.14)',
      transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
    }
  } else if (zoomMode.value === 'actual') {
    return {
      width: '860px',
      height: 'auto',
      aspectRatio: ar,
      margin: '0 auto',
      boxShadow: '0 12px 36px rgba(0,0,0,0.14)',
      transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
    }
  } else {
    return {
      width: `${Math.round(860 * zoomLevel.value)}px`,
      height: 'auto',
      aspectRatio: ar,
      margin: '0 auto',
      boxShadow: '0 12px 36px rgba(0,0,0,0.14)',
      transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
    }
  }
})

function onBubbleClick(q: number, choice: string) {
  const current = simulatedAnswers.value[q]
  if (current === choice) {
    const updated = { ...simulatedAnswers.value }
    delete updated[q]
    simulatedAnswers.value = updated
  } else {
    simulatedAnswers.value = {
      ...simulatedAnswers.value,
      [q]: choice,
    }
  }
}

function randomShade() {
  const total = props.config.questions?.metadata?.num_questions || 50
  const sections = props.config.questions?.sections || []
  const answers: Record<number, any> = {}

  for (let q = 1; q <= total; q++) {
    const sec = sections.find((s: any) => q >= (s.from_q || 1) && q <= (s.to_q || s.from_q || 1))
    const isTf = sec ? (sec.type === 'true_false') : (q <= 20)
    if (isTf) {
      const tfChoices = sec?.choices || ['صح', 'خطأ']
      answers[q] = tfChoices[Math.floor(Math.random() * tfChoices.length)]
    } else {
      const choices = sec?.choices || ['1', '2', '3', '4']
      answers[q] = choices[Math.floor(Math.random() * choices.length)]
    }
  }
  simulatedAnswers.value = answers
}

function clearShade() {
  simulatedAnswers.value = {}
}
</script>

<style scoped>
.canvas-viewport {
  background: radial-gradient(circle at center, #f8fafc 0%, #edf2f7 100%);
}

.sheet-artboard-container {
  max-width: 100%;
}
</style>
