<template>
  <div class="template-canvas-container d-flex flex-column h-100">
    <!-- ── Canvas Control Toolbar ────────────────────────────────── -->
    <div class="canvas-toolbar pa-3 px-4 rounded-xl border bg-white mb-3 d-flex justify-space-between align-center flex-wrap gap-2 elevation-1">
      <div class="d-flex align-center gap-2 flex-wrap">
        <!-- View Mode -->
        <v-btn-toggle
          v-model="zoomMode"
          mandatory
          density="compact"
          color="primary"
          variant="outlined"
          rounded="lg"
          class="me-1"
        >
          <v-btn value="fit" size="small" class="font-weight-bold" prepend-icon="mdi-fit-to-screen-outline">
            ملاءمة الصفحة
          </v-btn>
          <v-btn value="actual" size="small" class="font-weight-bold" prepend-icon="mdi-image-size-select-actual">
            الحجم الفعلي 100%
          </v-btn>
        </v-btn-toggle>

        <!-- Proportional Zoom -->
        <div class="d-flex align-center bg-grey-lighten-4 rounded-lg px-1 border">
          <v-btn icon size="small" variant="text" :disabled="zoomLevel <= 0.4" @click="zoomOut">
            <v-icon size="18">mdi-magnify-minus-outline</v-icon>
          </v-btn>
          <span class="text-caption font-weight-bold px-2 font-mono" style="min-width: 44px; text-align: center;">
            {{ Math.round(currentZoomDisplay * 100) }}%
          </span>
          <v-btn icon size="small" variant="text" :disabled="zoomLevel >= 3.0" @click="zoomIn">
            <v-icon size="18">mdi-magnify-plus-outline</v-icon>
          </v-btn>
          <v-btn icon size="small" variant="text" title="إعادة ضبط" @click="resetZoom">
            <v-icon size="16">mdi-refresh</v-icon>
          </v-btn>
        </div>

        <!-- Shading Simulator Buttons -->
        <v-btn
          size="small"
          variant="tonal"
          color="info"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-dice-5-outline"
          @click="randomShade"
        >
          تظليل تجريبي
        </v-btn>
        <v-btn
          v-if="Object.keys(simulatedAnswers).length > 0"
          size="small"
          variant="text"
          color="error"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-delete-sweep-outline"
          @click="clearShade"
        >
          مسح
        </v-btn>

        <!-- Presentation / Layout Mode Switcher (For Yemeni Ministry 50) -->
        <v-btn-toggle
          v-if="isYemeniMinistryPreset"
          v-model="presentationMode"
          mandatory
          density="compact"
          color="primary"
          variant="flat"
          rounded="lg"
          class="ms-2"
        >
          <v-btn value="audit_a4" size="small" class="font-weight-bold" prepend-icon="mdi-file-document-check-outline">
            النموذج الرسمي الشامل (A4 مع الترويسة والتدقيق)
          </v-btn>
          <v-btn value="compact_a5" size="small" class="font-weight-bold" prepend-icon="mdi-file-outline">
            ورقة إجابة الطالب (A5 للاختبار)
          </v-btn>
        </v-btn-toggle>
      </div>

      <div class="d-flex align-center gap-2">
        <v-btn
          color="success"
          size="small"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-content-save"
          @click="emit('save')"
        >
          حفظ القالب
        </v-btn>
        <v-btn
          variant="tonal"
          color="indigo"
          size="small"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-code-json"
          @click="exportJson"
        >
          تصدير JSON
        </v-btn>
        <v-btn
          variant="tonal"
          color="secondary"
          size="small"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-printer"
          @click="printSheet"
        >
          طباعة
        </v-btn>
        <v-btn
          color="primary"
          size="small"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-download"
          @click="exportPNG"
        >
          تنزيل PNG عالية الدقة
        </v-btn>
      </div>
    </div>

    <!-- ── Interactive Viewport Canvas ───────────────────────────── -->
    <div
      ref="viewportRef"
      class="canvas-viewport pa-6 rounded-2xl border overflow-auto text-center position-relative flex-grow-1"
      style="min-height: 600px; max-height: calc(100vh - 260px);"
    >
      <div class="sheet-artboard-container d-inline-block rounded-lg elevation-6 bg-white position-relative" :style="containerStyle">
        
        <!-- Mode 1: Yemeni Official Electronic Audit & Correction Sheet (A4 Full) - DEFAULT -->
        <YemeniAuditReportSheet
          v-if="isYemeniMinistryPreset && presentationMode === 'audit_a4'"
          :student-name="config.header?.student_name || 'عمرو عبدالباسط عبدالله قائد الزمر'"
          :seat-number="config.header?.seat_number || '418485'"
          :serial-number="config.header?.serial_number || '148'"
          :exam-subject="config.header?.exam_name || 'القرآن الكريم'"
          :exam-year="config.metadata?.academic_year || '1444هـ-2022-2023م'"
          :center-name="config.header?.center_name || 'سالم قطن - معين'"
          :center-code="config.header?.center_code || '164'"
          :envelope-no="config.header?.envelope_no || '2'"
          :governorate="config.header?.governorate || 'أمانة العاصمة'"
          :directorate="config.header?.directorate || 'معين'"
          :barcode-value="config.barcode?.value || '41848501164148'"
          :qr-value="config.qr?.value || 'YE-MOE-1444-418485-SUB1'"
          :student-answers="simulatedAnswers"
          :mcq-bubble-type="config.questions?.layout?.bubble_type || 'numbers'"
          :tf-bubble-type="config.questions?.layout?.tf_bubble_type || 'arabic'"
          :choices-count="config.questions?.layout?.choices_count || 4"
          :bubble-radius="config.questions?.layout?.bubble_radius_mm || 2.1"
          :show-simulated-handwriting="config.instructions?.show_simulated_handwriting || false"
          :total-questions="config.questions?.metadata?.num_questions"
          :sections="config.questions?.sections"
          :columns-count="config.questions?.layout?.columns_count || 4"
          :row-spacing="config.questions?.layout?.row_spacing_mm || 5.2"
        />

        <!-- Mode 2: Student Exam Answer Sheet (A5 Compact) -->
        <YemeniMinistrySheet
          v-else-if="isYemeniMinistryPreset && presentationMode === 'compact_a5'"
          layout-mode="compact_a5"
          :republic-name="config.header?.institution_name?.split('—')[0]?.trim() || config.header?.institution_name || 'الجمهورية اليمنية'"
          :ministry-name="config.header?.institution_name?.split('—')[1]?.trim() || 'وزارة التربية والتعليم'"
          :sector-name="config.header?.sub_title || 'قطاع المناهج والتوجيه — لجان الاختبارات'"
          :exam-stage-title="config.header?.exam_stage_title || 'اختبار الشهادة الثانوية العامة (القسم العلمي)'"
          :exam-subject="config.header?.exam_name || 'القرآن الكريم'"
          :exam-year="config.metadata?.academic_year || '1444هـ — 2022-2023م'"
          :student-name="config.header?.student_name || 'عمرو عبدالباسط عبدالله قائد الزمر'"
          :seat-number="config.header?.seat_number || '418485'"
          :serial-number="config.header?.serial_number || '148'"
          :center-name="config.header?.center_name || 'سالم قطن — معين'"
          :center-code="config.header?.center_code || '164'"
          :envelope-no="config.header?.envelope_no || '2'"
          :governorate="config.header?.governorate || 'أمانة العاصمة'"
          :directorate="config.header?.directorate || 'معين'"
          :barcode-value="config.barcode?.value || '41848501164148'"
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
          :total-questions="config.questions?.metadata?.num_questions"
          :sections="config.questions?.sections"
          :columns-count="config.questions?.layout?.columns_count || 4"
          :row-spacing="config.questions?.layout?.row_spacing_mm || 5.2"
          @bubble-click="onBubbleClick"
        />

        <!-- Standard University / General Multigraphics Sheet -->
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
          :primary-color="config.header?.primary_color || '#e6007e'"
          :institution-name="config.header?.institution_name || 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'"
          :sub-title="config.header?.sub_title || 'جامعة صنعاء — الإدارة العامة للامتحانات والتقويم الآلي'"
          :exam-name="config.header?.exam_name || 'الكيمياء العامة — نموذج معاينة'"
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
import { printOmrElement } from '../../utils/omrPrint'

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

const isYemeniMinistryPreset = computed(() => {
  const tId = props.config?.template_id || ''
  const name = props.config?.template_name || ''
  return tId === 'YEMEN_MINISTRY_50' || name.includes('وزارة التربية') || name.includes('الثانوية العامة') || props.config?.questions?.metadata?.num_questions === 50
})

const presentationMode = ref<'audit_a4' | 'compact_a5'>(
  props.config?.display_mode === 'audit_a4' ? 'audit_a4' : 'compact_a5'
)

watch(() => props.config?.display_mode, (val) => {
  if (val && val !== presentationMode.value) {
    presentationMode.value = val === 'audit_a4' ? 'audit_a4' : 'compact_a5'
  }
})

watch(presentationMode, (val) => {
  if (props.config) {
    props.config.display_mode = val
    if (val === 'compact_a5') {
      props.config.paper.size = 'A5'
      props.config.paper.width_mm = 210
      props.config.paper.height_mm = 148.5
    } else {
      props.config.paper.size = 'A4'
      props.config.paper.width_mm = 210
      props.config.paper.height_mm = 297
    }
  }
})

const zoomMode = ref<'fit' | 'actual' | 'custom'>('fit')
const zoomLevel = ref(1.0)
const simulatedAnswers = ref<Record<number, any>>({})

function zoomIn() {
  if (zoomMode.value === 'fit' && isYemeniMinistryPreset.value && presentationMode.value === 'audit_a4') {
    zoomLevel.value = 0.68
  }
  zoomMode.value = 'custom'
  zoomLevel.value = Math.min(Math.round((zoomLevel.value + 0.15) * 100) / 100, 3.0)
}

function zoomOut() {
  if (zoomMode.value === 'fit' && isYemeniMinistryPreset.value && presentationMode.value === 'audit_a4') {
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
    if (isYemeniMinistryPreset.value && presentationMode.value === 'audit_a4') {
      return 0.68
    }
    return 1.0
  }
  if (zoomMode.value === 'actual') return 1.0
  return zoomLevel.value
})

const currentAspectRatio = computed(() => {
  if (isYemeniMinistryPreset.value && presentationMode.value === 'compact_a5') {
    return '210 / 148.5'
  }
  return '210 / 297'
})

const containerStyle = computed(() => {
  const ar = currentAspectRatio.value

  // معالجة هندسية خاصة لتقرير التدقيق A4 المعتمد لمنع انهيار وتداخل جداول HTML
  if (isYemeniMinistryPreset.value && presentationMode.value === 'audit_a4') {
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

async function printSheet() {
  const svgEl = (
    document.querySelector('.sheet-artboard-container svg.yemeni-ministry-sheet-svg') ||
    document.querySelector('.sheet-artboard-container svg.yemeni-sheet-svg') ||
    document.querySelector('.sheet-artboard-container svg[viewBox="0 0 210 148.5"]') ||
    document.querySelector('.sheet-artboard-container svg[viewBox="0 0 210 297"]') ||
    document.querySelector('.sheet-artboard-container svg.omr-svg') ||
    document.querySelector('.sheet-artboard-container svg')
  ) as SVGGraphicsElement

  if (svgEl) {
    await printOmrElement(svgEl, {
      title: props.config?.template_name || 'OMR_Sheet',
      isA5: presentationMode.value === 'compact_a5'
    })
  } else {
    window.print()
  }
}

async function exportPNG() {
  const svgEl = (
    document.querySelector('.sheet-artboard-container svg.yemeni-ministry-sheet-svg') ||
    document.querySelector('.sheet-artboard-container svg.yemeni-sheet-svg') ||
    document.querySelector('.sheet-artboard-container svg[viewBox="0 0 210 148.5"]') ||
    document.querySelector('.sheet-artboard-container svg[viewBox="0 0 210 297"]') ||
    document.querySelector('.sheet-artboard-container svg.omr-svg') ||
    document.querySelector('.sheet-artboard-container svg')
  ) as SVGGraphicsElement

  if (!svgEl) {
    console.error('No SVG element found to export')
    return
  }

  try {
    // 1. Clone the SVG element so we don't mutate the DOM
    const clonedSvg = svgEl.cloneNode(true) as SVGGraphicsElement

    // Ensure all required namespaces are declared on root
    clonedSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
    clonedSvg.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')

    // 2. Parse viewBox to get real millimeter dimensions
    const viewBox = svgEl.getAttribute('viewBox') || '0 0 210 148.5'
    const parts = viewBox.trim().split(/[\s,]+/).map(Number)
    const vbWidth = parts[2] || 210
    const vbHeight = parts[3] || 148.5

    // Ultra-HD 600 DPI: px = mm * (600 / 25.4) -> 4960 x 3508 for A5
    const dpi = 600
    const targetWidth = Math.round(vbWidth * (dpi / 25.4))
    const targetHeight = Math.round(vbHeight * (dpi / 25.4))

    clonedSvg.setAttribute('width', `${targetWidth}`)
    clonedSvg.setAttribute('height', `${targetHeight}`)
    clonedSvg.style.width = `${targetWidth}px`
    clonedSvg.style.height = `${targetHeight}px`

    // 3. Convert all <image> elements with relative URLs to inline Base64 Data URLs
    const images = Array.from(clonedSvg.querySelectorAll('image'))
    for (const imgEl of images) {
      const href = imgEl.getAttribute('href') || imgEl.getAttribute('xlink:href') || ''
      if (href && !href.startsWith('data:')) {
        try {
          const fullUrl = href.startsWith('http') ? href : `${window.location.origin}${href}`
          const resp = await fetch(fullUrl)
          if (resp.ok) {
            const blob = await resp.blob()
            const b64 = await new Promise<string>((resolve, reject) => {
              const reader = new FileReader()
              reader.onloadend = () => resolve(reader.result as string)
              reader.onerror = reject
              reader.readAsDataURL(blob)
            })
            imgEl.setAttribute('href', b64)
            imgEl.removeAttribute('xlink:href')
          }
        } catch (e) {
          console.warn('Could not inline image for export:', href, e)
        }
      }
    }

    // 4. Serialize to XML string and create Image blob
    const serializer = new XMLSerializer()
    let svgStr = serializer.serializeToString(clonedSvg)

    const blob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' })
    const url = URL.createObjectURL(blob)

    const img = new Image()
    img.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = targetWidth
      canvas.height = targetHeight
      const ctx = canvas.getContext('2d')
      if (ctx) {
        ctx.imageSmoothingEnabled = true
        ctx.imageSmoothingQuality = 'high'
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        ctx.drawImage(img, 0, 0, targetWidth, targetHeight)

        const pngUrl = canvas.toDataURL('image/png', 1.0)
        const a = document.createElement('a')
        a.href = pngUrl
        a.download = `${props.config?.template_name || 'OMR_Sheet'}_600DPI_UltraHD.png`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
      }
      URL.revokeObjectURL(url)
    }
    img.onerror = (e) => {
      console.error('Image load error during export:', e)
      URL.revokeObjectURL(url)
    }
    img.src = url
  } catch (err) {
    console.error('Export PNG failed:', err)
  }
}

function exportJson() {
  try {
    const jsonStr = JSON.stringify(props.config, null, 2)
    const blob = new Blob([jsonStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${props.config?.template_id || 'template'}_config.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (e) {
    console.error('Export JSON failed:', e)
  }
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
