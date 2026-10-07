<template>
  <div class="qb-template-builder-v4" dir="rtl">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">{{ pageMode === 'library' ? 'mdi-folder-multiple-outline' : 'mdi-tune-vertical' }}</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">
            {{ pageMode === 'library' ? 'مكتبة قوالب التصحيح المعيارية' : 'مصمم القوالب الهندسية المعيارية' }}
          </h1>
          <p class="text-caption text-medium-emphasis mb-0">
            {{ pageMode === 'library' ? 'استعراض وإدارة قوالب الامتحانات المعتمدة واستخدامها المباشر في التصحيح' : 'إنشاء وتخصيص وتوثيق أوراق الإجابة بدقة مليمترية معتمدة' }}
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          v-if="pageMode === 'designer'"
          variant="tonal"
          color="secondary"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-arrow-right"
          @click="pageMode = 'library'"
        >
          العودة لمكتبة القوالب
        </v-btn>

        <v-btn
          v-if="pageMode === 'library'"
          color="primary"
          rounded="lg"
          class="font-weight-bold px-5"
          prepend-icon="mdi-plus"
          @click="startNewDesignerTemplate"
        >
          تصميم قالب جديد
        </v-btn>

        <template v-if="pageMode === 'designer'">
          <v-btn
            variant="outlined"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-refresh"
            @click="createNewTemplate"
          >
            إعادة تعيين
          </v-btn>

          <v-btn
            v-if="savedDbId"
            color="success"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-content-save-check"
            :loading="isSaving"
            @click="updateExistingTemplate"
          >
            حفظ التعديلات
          </v-btn>

          <v-btn
            color="primary"
            rounded="lg"
            class="font-weight-bold px-5"
            prepend-icon="mdi-content-save-plus"
            :loading="isSaving"
            @click="showSaveModal = true"
          >
            حفظ كقالب جديد
          </v-btn>
        </template>
      </div>
    </div>

    <!-- ── Mode Tabs Switcher (Unified OpenSoftCore Standard) ──────── -->
    <v-card class="mode-tabs-card pa-1 rounded-xl mb-6 elevation-0 border">
      <v-tabs
        v-model="pageMode"
        color="primary"
        grow
        slider-color="primary"
        class="unified-mode-tabs"
      >
        <v-tab value="library" class="font-weight-black py-3 rounded-lg">
          <v-icon start size="20">mdi-folder-multiple-outline</v-icon>
          مكتبة القوالب المحفوظة
          <v-chip
            size="x-small"
            :color="pageMode === 'library' ? 'primary' : 'grey-darken-1'"
            :variant="pageMode === 'library' ? 'flat' : 'tonal'"
            class="ms-2 font-weight-bold unified-tab-badge"
          >
            {{ savedTemplatesList.length }}
          </v-chip>
        </v-tab>

        <v-tab value="designer" class="font-weight-black py-3 rounded-lg">
          <v-icon start size="20">mdi-tune-vertical</v-icon>
          مصمم القوالب والهندسة المعيارية
          <v-chip
            v-if="savedDbId"
            size="x-small"
            color="success"
            variant="tonal"
            class="ms-2 font-weight-bold unified-tab-badge"
          >
            <v-icon start size="12">mdi-pencil-outline</v-icon>
            تعديل: {{ config.template_name }}
          </v-chip>
          <v-chip
            v-else
            size="x-small"
            color="primary"
            variant="tonal"
            class="ms-2 font-weight-bold unified-tab-badge"
          >
            <v-icon start size="12">mdi-plus-circle-outline</v-icon>
            إنشاء قالب
          </v-chip>
        </v-tab>
      </v-tabs>
    </v-card>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- ── TAB 1: TEMPLATE LIBRARY                                   -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-if="pageMode === 'library'">
      <TemplateLibrary
        :templates="savedTemplatesList"
        :is-loading="isLoadingTemplates"
        @create-new="startNewDesignerTemplate"
        @edit="loadSavedTemplate"
        @scan="goToScannerWithTemplate"
        @preview="openPreviewModal"
        @duplicate="duplicateTemplate"
        @print="printDirect"
        @delete="deleteTemplate"
      />
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- ── TAB 2: VISUAL DESIGNER                                     -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-else-if="pageMode === 'designer'">
      <v-row>
        <!-- Left Side: Modular Settings Panels -->
        <v-col cols="12" md="5" lg="4">
          <v-card class="main-card pa-4 rounded-2xl border elevation-1">
            <div class="d-flex align-center justify-space-between mb-3 pb-2 border-b">
              <h2 class="text-subtitle-1 font-weight-bold d-flex align-center mb-0">
                <v-icon color="primary" class="me-2" size="20">mdi-tune</v-icon>
                لوحة الضبط الهندسي للقالب
              </h2>
            </div>

            <!-- Panels Sub-Tabs -->
            <v-tabs v-model="designerTab" density="compact" color="primary" class="mb-4 border-b" grow>
              <v-tab value="layout" class="font-weight-bold">الصفحة</v-tab>
              <v-tab value="student" class="font-weight-bold">بطاقة الطالب</v-tab>
              <v-tab value="questions" class="font-weight-bold">الأسئلة</v-tab>
              <v-tab value="codes" class="font-weight-bold">الباركود</v-tab>
              <v-tab value="detection" class="font-weight-bold">الذكاء الاصطناعي</v-tab>
            </v-tabs>

            <v-window v-model="designerTab">
              <!-- Panel 1: Page Layout -->
              <v-window-item value="layout">
                <PageLayoutSettings :config="config" @preset-selected="applyPreset" />
              </v-window-item>

              <!-- Panel 2: Student Card -->
              <v-window-item value="student">
                <StudentCardSettings :config="config" />
              </v-window-item>

              <!-- Panel 3: Questions & Sections -->
              <v-window-item value="questions">
                <SectionsManager :config="config" />
              </v-window-item>

              <!-- Panel 4: Barcodes & Codes -->
              <v-window-item value="codes">
                <CodesSettings :config="config" />
              </v-window-item>

              <!-- Panel 5: Detection & AI -->
              <v-window-item value="detection">
                <DetectionSettings :config="config" />
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>

        <!-- Right Side: Live Canvas Artboard -->
        <v-col cols="12" md="7" lg="8">
          <TemplateCanvas :config="config" @save="handleQuickSave" />
        </v-col>
      </v-row>
    </div>

    <!-- ── Fullscreen Preview Modal ──────────────────────────────── -->
    <v-dialog v-model="showPreviewModal" max-width="880" scrollable>
      <v-card class="pa-6 rounded-2xl">
        <div class="d-flex align-center justify-space-between mb-4 pb-3 border-b flex-wrap gap-2">
          <div class="d-flex align-center gap-2">
            <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
              <v-icon color="primary" size="20">mdi-eye-outline</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-h6 font-weight-black mb-0">معاينة ورقة الإجابة: {{ previewingTemplate?.name }}</h3>
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
              @click="loadSavedTemplate(previewingTemplate)"
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
              @click="printPreviewModal"
            >
              طباعة الورقة
            </v-btn>
            <v-btn
              color="success"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-scanner"
              @click="goToScannerWithTemplate(previewingTemplate?.id)"
            >
              بدء التصحيح بهذا القالب
            </v-btn>
            <v-btn icon size="small" variant="text" @click="showPreviewModal = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </div>
        </div>

        <div class="pa-4 bg-grey-lighten-4 rounded-xl d-flex justify-center overflow-auto" style="max-height: 600px;">
          <div class="sheet-wrapper" :style="previewWrapperStyle">
            <!-- Mode 1: Yemeni Audit Report Sheet (A4 Full) -->
            <YemeniAuditReportSheet
              v-if="isPreviewYemeniMinistry && (previewingTemplate?.template_data?.display_mode === 'audit_a4' || !previewingTemplate?.template_data?.display_mode)"
              :student-name="previewingTemplate?.template_data?.header?.student_name || 'عمرو عبدالباسط عبدالله قائد الزمر'"
              :seat-number="previewingTemplate?.template_data?.header?.seat_number || '418485'"
              :serial-number="previewingTemplate?.template_data?.header?.serial_number || '148'"
              :exam-subject="previewingTemplate?.template_data?.header?.exam_name || previewingTemplate?.name || 'القرآن الكريم'"
              :exam-year="previewingTemplate?.template_data?.metadata?.academic_year || '1444هـ-2022-2023م'"
              :center-name="previewingTemplate?.template_data?.header?.center_name || 'سالم قطن - معين'"
              :center-code="previewingTemplate?.template_data?.header?.center_code || '164'"
              :envelope-no="previewingTemplate?.template_data?.header?.envelope_no || '2'"
              :governorate="previewingTemplate?.template_data?.header?.governorate || 'أمانة العاصمة'"
              :directorate="previewingTemplate?.template_data?.header?.directorate || 'معين'"
              :barcode-value="previewingTemplate?.template_data?.barcode?.value || '41848501164148'"
              :qr-value="previewingTemplate?.template_data?.qr?.value || 'YE-MOE-1444-418485-SUB1'"
              :mcq-bubble-type="previewingTemplate?.template_data?.questions?.layout?.bubble_type || 'numbers'"
              :tf-bubble-type="previewingTemplate?.template_data?.questions?.layout?.tf_bubble_type || 'arabic'"
              :choices-count="previewingTemplate?.template_data?.questions?.layout?.choices_count || 4"
              :bubble-radius="previewingTemplate?.template_data?.questions?.layout?.bubble_radius_mm || 2.1"
              :show-simulated-handwriting="previewingTemplate?.template_data?.instructions?.show_simulated_handwriting || false"
              :total-questions="previewingTemplate?.template_data?.questions?.metadata?.num_questions || previewingTemplate?.total_mcq || 50"
              :sections="previewingTemplate?.template_data?.questions?.sections"
              :columns-count="previewingTemplate?.template_data?.questions?.layout?.columns_count || 4"
              :row-spacing="previewingTemplate?.template_data?.questions?.layout?.row_spacing_mm || 5.2"
            />

            <!-- Mode 2: Yemeni Ministry Student Answer Sheet (A5 Compact) -->
            <YemeniMinistrySheet
              v-else-if="isPreviewYemeniMinistry && previewingTemplate?.template_data?.display_mode === 'compact_a5'"
              layout-mode="compact_a5"
              :republic-name="previewingTemplate?.template_data?.header?.institution_name?.split('—')[0]?.trim() || 'الجمهورية اليمنية'"
              :ministry-name="previewingTemplate?.template_data?.header?.institution_name?.split('—')[1]?.trim() || 'وزارة التربية والتعليم'"
              :sector-name="previewingTemplate?.template_data?.header?.sub_title || 'قطاع المناهج والتوجيه — لجان الاختبارات'"
              :exam-stage-title="previewingTemplate?.template_data?.header?.exam_stage_title || 'اختبار الشهادة الثانوية العامة (القسم العلمي)'"
              :exam-subject="previewingTemplate?.template_data?.header?.exam_name || previewingTemplate?.name || 'القرآن الكريم'"
              :exam-year="previewingTemplate?.template_data?.metadata?.academic_year || '1444هـ — 2022-2023م'"
              :student-name="previewingTemplate?.template_data?.header?.student_name || 'عمرو عبدالباسط عبدالله قائد الزمر'"
              :seat-number="previewingTemplate?.template_data?.header?.seat_number || '418485'"
              :serial-number="previewingTemplate?.template_data?.header?.serial_number || '148'"
              :center-name="previewingTemplate?.template_data?.header?.center_name || 'سالم قطن — معين'"
              :center-code="previewingTemplate?.template_data?.header?.center_code || '164'"
              :envelope-no="previewingTemplate?.template_data?.header?.envelope_no || '2'"
              :governorate="previewingTemplate?.template_data?.header?.governorate || 'أمانة العاصمة'"
              :directorate="previewingTemplate?.template_data?.header?.directorate || 'معين'"
              :barcode-value="previewingTemplate?.template_data?.barcode?.value || '41848501164148'"
              :qr-value="previewingTemplate?.template_data?.qr?.value || 'YE-MOE-1444-418485-SUB1'"
              :instruction1="previewingTemplate?.template_data?.instructions?.rule1"
              :instruction2="previewingTemplate?.template_data?.instructions?.rule2"
              :instruction3="previewingTemplate?.template_data?.instructions?.rule3"
              :instruction4="previewingTemplate?.template_data?.instructions?.rule4"
              :instruction-correct-label="previewingTemplate?.template_data?.instructions?.correct_label"
              :total-questions="previewingTemplate?.template_data?.questions?.metadata?.num_questions || previewingTemplate?.total_mcq || 50"
              :sections="previewingTemplate?.template_data?.questions?.sections"
              :columns-count="previewingTemplate?.template_data?.questions?.layout?.columns_count || 4"
              :row-spacing="previewingTemplate?.template_data?.questions?.layout?.row_spacing_mm || 5.2"
              :bubble-radius="previewingTemplate?.template_data?.questions?.layout?.bubble_radius_mm || 2.1"
              :mcq-bubble-type="previewingTemplate?.template_data?.questions?.layout?.bubble_type || 'numbers'"
              :tf-bubble-type="previewingTemplate?.template_data?.questions?.layout?.tf_bubble_type || 'arabic'"
              :choices-count="previewingTemplate?.template_data?.questions?.layout?.choices_count || 4"
            />

            <!-- Mode 3: Standard University / General Multigraphics Sheet -->
            <OmrSheetMultigraphics
              v-else
              :total-questions="previewingTemplate?.total_mcq || previewingTemplate?.template_data?.questions?.metadata?.num_questions || 180"
              :questions-per-column="previewingTemplate?.template_data?.questions?.layout?.questions_per_column || Math.ceil((previewingTemplate?.total_mcq || 180) / (previewingTemplate?.template_data?.questions?.layout?.columns_count || 4))"
              :total-columns="previewingTemplate?.template_data?.questions?.layout?.columns_count || previewingTemplate?.template_data?.metadata?.columns_count || 4"
              :choices-per-question="previewingTemplate?.template_data?.questions?.layout?.choices_count || previewingTemplate?.template_data?.metadata?.choices_count || 4"
              :primary-color="previewingTemplate?.template_data?.header?.primary_color || '#e6007e'"
              :institution-name="previewingTemplate?.template_data?.header?.institution_name || previewingTemplate?.name || 'نموذج اختبار معياري'"
              :sub-title="previewingTemplate?.template_data?.header?.sub_title || previewingTemplate?.description || 'ورقة إجابة التصحيح الضوئي الآلي'"
              :exam-name="previewingTemplate?.template_data?.header?.exam_name || previewingTemplate?.name"
              :bubble-type="previewingTemplate?.template_data?.questions?.layout?.bubble_type || 'numbers'"
              :layout-direction="previewingTemplate?.template_data?.questions?.layout?.layout_direction || 'rtl'"
            />
          </div>
        </div>
      </v-card>
    </v-dialog>

    <!-- ── Save/Update Modal ─────────────────────────────────────── -->
    <SaveExportModal
      v-model="showSaveModal"
      :is-saving="isSaving"
      :initial-name="config.template_name"
      :initial-subject="config.header.exam_name"
      :initial-description="config.description"
      :initial-version="config.version"
      :total-questions="config.questions.metadata.num_questions"
      @save="confirmSaveTemplate"
    />

    <!-- ── Notification Snackbar ─────────────────────────────────── -->
    <v-snackbar
      v-model="showToast"
      :color="toastType === 'error' ? 'error' : 'success'"
      location="top"
      rounded="xl"
      elevation="6"
      :timeout="4500"
    >
      <div class="d-flex align-center justify-space-between gap-4 w-100">
        <div class="d-flex align-center gap-2">
          <v-icon color="white">{{ toastType === 'error' ? 'mdi-alert-circle' : 'mdi-check-circle' }}</v-icon>
          <span class="font-weight-bold text-white">{{ toastMsg }}</span>
        </div>
        <v-btn
          v-if="toastType === 'success'"
          variant="tonal"
          color="white"
          size="small"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-folder-open"
          @click="pageMode = 'library'"
        >
          عرض في المكتبة
        </v-btn>
      </div>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, defineAsyncComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

import TemplateLibrary from './components/TemplateLibrary.vue'
import TemplateCanvas from './components/TemplateCanvas.vue'
import SaveExportModal from './components/SaveExportModal.vue'
import { printOmrElement } from '../utils/omrPrint'

import PageLayoutSettings from './panels/PageLayoutSettings.vue'
import StudentCardSettings from './panels/StudentCardSettings.vue'
import SectionsManager from './panels/SectionsManager.vue'
import CodesSettings from './panels/CodesSettings.vue'
import DetectionSettings from './panels/DetectionSettings.vue'

const OmrSheetMultigraphics = defineAsyncComponent(() =>
  import('@/components/omr_templates/OmrSheetMultigraphics.vue')
)

const YemeniMinistrySheet = defineAsyncComponent(() =>
  import('@/components/omr_templates/YemeniMinistrySheet.vue')
)

const YemeniAuditReportSheet = defineAsyncComponent(() =>
  import('@/components/omr_templates/YemeniAuditReportSheet.vue')
)

const route = useRoute()
const router = useRouter()

const pageMode = ref<'library' | 'designer'>(route.query.mode === 'designer' ? 'designer' : 'library')
const designerTab = ref<'layout' | 'student' | 'questions' | 'codes' | 'detection'>('layout')

const savedTemplatesList = ref<any[]>([])
const isLoadingTemplates = ref(false)
const isSaving = ref(false)
const savedDbId = ref<number | string | null>(null)

const showSaveModal = ref(false)
const showPreviewModal = ref(false)
const previewingTemplate = ref<any>(null)

const isPreviewYemeniMinistry = computed(() => {
  const t = previewingTemplate.value
  if (!t) return false
  const name = t.name || ''
  const tId = t.template_data?.template_id || ''
  const numQ =
    t.total_mcq ||
    t.template_data?.questions?.metadata?.num_questions ||
    t.template_data?.metadata?.num_questions ||
    0
  return (
    name.includes('وزارة التربية') ||
    name.includes('الثانوية العامة') ||
    numQ === 50 ||
    tId === 'YEMEN_MINISTRY_50' ||
    tId.includes('YEMEN_MINISTRY') ||
    t.template_data?.template_name?.includes('وزارة التربية')
  )
})

const previewWrapperStyle = computed(() => {
  const isA5 = isPreviewYemeniMinistry.value && previewingTemplate.value?.template_data?.display_mode === 'compact_a5'
  const widthMm = 210
  const heightMm = isA5 ? 148.5 : 297
  const scale = isA5 ? 0.85 : 0.65
  return {
    width: `${widthMm}mm`,
    minWidth: `${widthMm}mm`,
    height: `${heightMm}mm`,
    minHeight: `${heightMm}mm`,
    aspectRatio: `${widthMm} / ${heightMm}`,
    transform: `scale(${scale})`,
    transformOrigin: 'top center',
    marginBottom: `calc(-${heightMm}mm * ${1 - scale})`,
    backgroundColor: '#ffffff',
    boxShadow: '0 8px 28px rgba(0,0,0,0.12)',
    borderRadius: '4px',
    overflow: 'hidden',
  }
})

const showToast = ref(false)
const toastMsg = ref('')
const toastType = ref<'success' | 'error'>('success')

function notify(msg: string, type: 'success' | 'error' = 'success') {
  toastMsg.value = msg
  toastType.value = type
  showToast.value = true
}

// ── Default Yemeni Ministry Configuration (50 questions hybrid) ─
const DEFAULT_CONFIG = () => ({
  template_id: 'YEMEN_MINISTRY_50',
  template_name: 'نموذج اختبار الثانوية العامة — وزارة التربية والتعليم (50 سؤال)',
  version: '1.0',
  description: 'قالب اختبار الشهادة الثانوية العامة المعتمد: 20 سؤال صح/خطأ + 30 سؤال اختيار من متعدد + بطاقة بيانات الطالب ودوائر الغياب.',
  display_mode: 'compact_a5',
  paper: {
    size: 'A5',
    width_mm: 210,
    height_mm: 148.5,
    dpi: 300,
    orientation: 'landscape'
  },
  header: {
    institution_name: 'الجمهورية اليمنية — وزارة التربية والتعليم',
    sub_title: 'قطاع المناهج والتوجيه — لجان الاختبارات',
    exam_name: 'القرآن الكريم',
    governorate: 'أمانة العاصمة',
    directorate: 'معين',
    center_name: 'سالم قطن — معين',
    center_code: '164',
    envelope_no: '2',
    student_name: 'عمرو عبدالباسط عبدالله قائد الزمر',
    seat_number: '418485',
    serial_number: '148',
    primary_color: '#000000',
  },
  metadata: {
    academic_year: '1444هـ — 2022-2023م',
  },
  student_fields: {
    enabled: true,
  },
  questions: {
    metadata: {
      num_questions: 50,
    },
    layout: {
      columns_count: 4,
      choices_count: 4,
      bubble_radius_mm: 1.8,
      row_spacing_mm: 5.2,
      bubble_type: 'numbers',
      tf_bubble_type: 'arabic',
      layout_direction: 'rtl',
    },
    sections: [
      { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'اختيار من متعدد', from_q: 21, to_q: 50, choices: ['1', '2', '3', '4'], mark: 2 },
    ]
  },
  barcode: {
    enabled: true,
    value: '41848501164148',
    format: 'CODE128',
  },
  qr: {
    enabled: true,
    value: 'YE-MOE-1444-418485-SUB1',
    ecc: 'M',
  },
  footer: {
    right_text: '',
    center_logo: '',
    left_text: '',
    document_label: '',
    show_simulated_handwriting: false,
  },
  instructions: {
    rule1: '1- يجب أن يكون تظليل الدائرة بقلم جاف أسود أو أزرق بشكل كامل مثال:',
    correct_label: 'واجب',
    rule2: '2 - تأكد من تظليل إجاباتك في الأماكن المخصصة لها.',
    rule3: '3 - يمنع استخدام المصحح.',
    rule4: '4 - لن تقبل الإجابات مالم تسجل على هذه الورقة، اترك لنفسك وقتاً كافياً لنقل الإجابات.',
    show_simulated_handwriting: false,
  },
  detection: {
    engine: 'opencv_omr',
    ai_verification: true,
    thresholds: {
      filled_min: 55,
      empty_max: 28,
    },
    tolerance_mm: 1.0,
  },
})

const config = reactive(DEFAULT_CONFIG())

function applyPreset(presetId: string) {
  if (presetId === 'YEMEN_MINISTRY_40') {
    Object.assign(config, DEFAULT_CONFIG())
    config.template_id = 'YEMEN_MINISTRY_40'
    config.template_name = 'نموذج اختبار الثانوية العامة — وزارة التربية والتعليم (40 سؤال)'
    config.questions.metadata.num_questions = 40
    config.questions.sections = [
      { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'اختيار من متعدد', from_q: 21, to_q: 40, choices: ['1', '2', '3', '4'], mark: 2 },
    ]
  } else if (presetId === 'YEMEN_MINISTRY_50') {
    Object.assign(config, DEFAULT_CONFIG())
  } else if (presetId === 'YEMEN_MINISTRY_60') {
    Object.assign(config, DEFAULT_CONFIG())
    config.template_id = 'YEMEN_MINISTRY_60'
    config.template_name = 'نموذج اختبار الثانوية العامة — وزارة التربية والتعليم (60 سؤال)'
    config.questions.metadata.num_questions = 60
    config.questions.sections = [
      { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'اختيار من متعدد', from_q: 21, to_q: 60, choices: ['1', '2', '3', '4'], mark: 1.5 },
    ]
  } else if (presetId === 'YEMEN_UNIVERSITY_180') {
    config.template_id = 'YEMEN_UNIVERSITY_180'
    config.template_name = 'نموذج الجامعات اليمنية العام (180 سؤال - 4 أعمدة)'
    config.questions.metadata.num_questions = 180
    config.questions.layout.columns_count = 4
    config.questions.layout.choices_count = 4
    config.questions.layout.bubble_radius_mm = 1.7
    config.questions.layout.row_spacing_mm = 4.2
    config.header.institution_name = 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'
    config.header.sub_title = 'جامعة صنعاء — الإدارة العامة للامتحانات والتقويم الآلي'
    config.header.primary_color = '#e6007e'
  } else if (presetId === 'GENERAL_100') {
    config.template_id = 'GENERAL_100'
    config.template_name = 'النموذج المعياري العام (100 سؤال)'
    config.questions.metadata.num_questions = 100
    config.questions.layout.columns_count = 4
    config.questions.layout.choices_count = 4
    config.questions.layout.bubble_radius_mm = 1.75
    config.questions.layout.row_spacing_mm = 4.6
  }
}

function startNewDesignerTemplate() {
  createNewTemplate()
  pageMode.value = 'designer'
}

function createNewTemplate() {
  savedDbId.value = null
  Object.assign(config, DEFAULT_CONFIG())
}

function loadSavedTemplate(t: any) {
  if (!t) return
  showPreviewModal.value = false
  savedDbId.value = t.id

  // Deep-merge template_data with DEFAULT_CONFIG to guarantee complete structure
  const defaults = DEFAULT_CONFIG()
  const td = t.template_data || {}

  Object.assign(config, defaults)
  if (td.paper) Object.assign(config.paper, td.paper)
  if (td.header) Object.assign(config.header, td.header)
  if (td.metadata) Object.assign(config.metadata, td.metadata)
  if (td.student_fields) Object.assign(config.student_fields, td.student_fields)
  if (td.questions) {
    if (td.questions.metadata) Object.assign(config.questions.metadata, td.questions.metadata)
    if (td.questions.layout) Object.assign(config.questions.layout, td.questions.layout)
    if (td.questions.sections) config.questions.sections = JSON.parse(JSON.stringify(td.questions.sections))
  }
  if (td.barcode) Object.assign(config.barcode, td.barcode)
  if (td.qr) Object.assign(config.qr, td.qr)
  if (td.footer) Object.assign(config.footer, td.footer)
  if (td.instructions) Object.assign(config.instructions, td.instructions)
  if (td.display_mode) config.display_mode = td.display_mode

  config.template_id = td.template_id || t.template_id || (t.total_mcq === 50 ? 'YEMEN_MINISTRY_50' : 'CUSTOM')
  config.template_name = t.name || config.template_name
  config.version = t.version || '1.0'
  config.description = t.description || ''
  if (config.header) {
    config.header.exam_name = td.header?.exam_name || t.name
  }

  pageMode.value = 'designer'
  notify(`تم تحميل القالب «${t.name}» في المصمم بنجاح`)
}

function openPreviewModal(t: any) {
  previewingTemplate.value = t
  showPreviewModal.value = true
}

function goToScannerWithTemplate(id: number | string) {
  showPreviewModal.value = false
  router.push({ path: '/omr/scanner', query: { templateId: id } })
}

function duplicateTemplate(t: any) {
  loadSavedTemplate(t)
  savedDbId.value = null
  config.template_name = `${t.name} (نسخة)`
  notify('تم إنشاء نسخة في المصمم، يمكنك تعديلها وحفظها الآن')
}

async function printPreviewModal() {
  const svgEl = document.querySelector('.sheet-wrapper svg') as SVGGraphicsElement
  if (svgEl) {
    await printOmrElement(svgEl, {
      title: previewingTemplate.value?.name || 'OMR_Sheet',
      isA5: isPreviewYemeniMinistry.value
    })
  } else {
    window.print()
  }
}

function printDirect(t: any) {
  openPreviewModal(t)
  setTimeout(async () => {
    await printPreviewModal()
  }, 400)
}

// ── API Communication ───────────────────────────────────────────
function extractErrorMessage(e: any): string {
  if (e.response?.data) {
    const d = e.response.data
    if (typeof d === 'string') return d
    if (d.message) return d.message
    if (d.error) return d.error
    if (d.detail) return d.detail
    if (d.non_field_errors) return Array.isArray(d.non_field_errors) ? d.non_field_errors.join(', ') : String(d.non_field_errors)
    const firstKey = Object.keys(d)[0]
    if (firstKey && Array.isArray(d[firstKey])) {
      return `${firstKey}: ${d[firstKey].join(', ')}`
    }
  }
  return e.message || 'حدث خطأ غير متوقع'
}

async function fetchSavedTemplates() {
  isLoadingTemplates.value = true
  try {
    const resp = await api.get('/api/templates-engine/', { params: { all: true, page_size: 1000 } })
    if (resp.status === 200) {
      const raw = resp.data
      const list: any[] = Array.isArray(raw) ? raw : (raw.results || raw.data || [])
      // Enrich each template with computed fields that TemplateCard needs
      savedTemplatesList.value = list.map((t: any) => {
        const td = t.template_data || {}
        const qMeta = td.questions?.metadata || td.metadata || {}
        const qLayout = td.questions?.layout || td.layout || {}
        return {
          ...t,
          total_mcq: t.total_mcq ?? qMeta.num_questions ?? 0,
          // ensure template_data has flat metadata for TemplateCard fallback paths
          template_data: td.template_id ? td : {
            ...td,
            template_id: td.template_id || t.name,
            metadata: {
              num_questions: qMeta.num_questions ?? t.total_mcq ?? 0,
              columns_count: qLayout.columns_count ?? 4,
              choices_count: qLayout.choices_count ?? 4,
              academic_year: td.metadata?.academic_year || '',
            },
            header: td.header || {},
          }
        }
      })
    }
  } catch (e: any) {
    notify('فشل في جلب قائمة القوالب: ' + extractErrorMessage(e), 'error')
  } finally {
    isLoadingTemplates.value = false
  }
}

function handleQuickSave() {
  if (savedDbId.value) {
    updateExistingTemplate()
  } else {
    showSaveModal.value = true
  }
}

async function confirmSaveTemplate(formData: any) {
  isSaving.value = true
  try {
    config.template_name = formData.name.trim()
    config.version = formData.version?.trim() || '1.0'
    config.description = formData.description?.trim() || ''
    if (config.header) {
      config.header.exam_name = formData.subject_name?.trim() || formData.name.trim()
    }

    if (!config.paper) {
      config.paper = { size: 'A4', width_mm: 210, height_mm: 297, dpi: 300, orientation: 'portrait' }
    }

    const payload = {
      name: config.template_name,
      version: config.version,
      description: config.description,
      paper_width_mm: Number(config.paper.width_mm) || 210,
      paper_height_mm: Number(config.paper.height_mm) || 297,
      dpi: Number(config.paper.dpi) || 300,
      template_data: JSON.parse(JSON.stringify(config)),
    }

    const resp = await api.post('/api/templates-engine/', payload)
    if (resp.status === 201 || resp.status === 200) {
      const saved = resp.data?.data || resp.data
      savedDbId.value = saved.id
      config.template_name = saved.name || config.template_name
      config.version = saved.version || config.version
      showSaveModal.value = false
      notify(`تم حفظ وتوثيق القالب «${config.template_name}» (إصدار ${config.version}) بنجاح!`)
      await fetchSavedTemplates()
      pageMode.value = 'library'
    }
  } catch (e: any) {
    notify('خطأ أثناء حفظ القالب: ' + extractErrorMessage(e), 'error')
  } finally {
    isSaving.value = false
  }
}

async function updateExistingTemplate() {
  if (!savedDbId.value) return
  isSaving.value = true
  try {
    if (!config.paper) {
      config.paper = { size: 'A4', width_mm: 210, height_mm: 297, dpi: 300, orientation: 'portrait' }
    }
    const payload = {
      name: config.template_name,
      version: config.version || '1.0',
      description: config.description || '',
      paper_width_mm: Number(config.paper.width_mm) || 210,
      paper_height_mm: Number(config.paper.height_mm) || 297,
      dpi: Number(config.paper.dpi) || 300,
      template_data: JSON.parse(JSON.stringify(config)),
    }
    try {
      await api.put(`/api/templates-engine/${savedDbId.value}/`, payload)
    } catch (putErr) {
      await api.patch(`/api/templates-engine/${savedDbId.value}/`, payload)
    }
    notify(`تم تحديث وحفظ القالب «${config.template_name}» بنجاح!`)
    await fetchSavedTemplates()
  } catch (e: any) {
    notify('خطأ أثناء تحديث القالب: ' + extractErrorMessage(e), 'error')
  } finally {
    isSaving.value = false
  }
}

async function deleteTemplate(id: number | string) {
  try {
    await api.delete(`/api/templates-engine/${id}/`)
    notify('تم حذف القالب بنجاح')
    if (savedDbId.value === id) {
      savedDbId.value = null
      createNewTemplate()
    }
    await fetchSavedTemplates()
  } catch (e: any) {
    notify('خطأ أثناء حذف القالب: ' + extractErrorMessage(e), 'error')
  }
}

async function loadExamIntoDesigner(examId: string | number) {
  try {
    notify('جاري استيراد مواصفات الاختبار من المولد وبناء القالب ديناميكياً...', 'success')
    const resp = await api.get(`/api/omr/exam-linking/${examId}/`)
    if (resp.status === 200 && resp.data?.success) {
      const examData = resp.data.exam || {}
      const versions = resp.data.versions || []
      const students = resp.data.registered_students || []

      // Determine questions count and sections
      let questionsCount = examData.totalQuestions || 50
      let sections: any[] = []

      // If version details available, analyze question types
      if (versions.length > 0 && versions[0].questions?.length) {
        questionsCount = versions[0].questions.length
        const qList = versions[0].questions
        
        let tfCount = 0
        let mcqCount = 0
        qList.forEach((q: any) => {
          const typeStr = String(q.questionType || '').toLowerCase()
          if (typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ')) {
            tfCount++
          } else {
            mcqCount++
          }
        })

        if (tfCount > 0 && mcqCount > 0) {
          sections = [
            { id: 'sec1', title: 'القسم الأول: صح وخطأ', from_q: 1, to_q: tfCount, choices: ['صح', 'خطأ'], mark: 1 },
            { id: 'sec2', title: 'القسم الثاني: الاختيار من متعدد', from_q: tfCount + 1, to_q: questionsCount, choices: ['1', '2', '3', '4'], mark: 2 }
          ]
        } else if (tfCount > 0 && mcqCount === 0) {
          sections = [
            { id: 'sec1', title: 'أسئلة الصح والخطأ', from_q: 1, to_q: questionsCount, choices: ['صح', 'خطأ'], mark: 1 }
          ]
        } else {
          sections = [
            { id: 'sec1', title: 'أسئلة الاختيار من متعدد', from_q: 1, to_q: questionsCount, choices: ['1', '2', '3', '4'], mark: 2 }
          ]
        }
      } else {
        // Fallback default sections based on questionsCount
        if (questionsCount <= 40) {
          sections = [
            { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: Math.min(20, Math.floor(questionsCount / 2)), choices: ['صح', 'خطأ'], mark: 1 },
            { id: 'sec2', title: 'اختيار من متعدد', from_q: Math.min(20, Math.floor(questionsCount / 2)) + 1, to_q: questionsCount, choices: ['1', '2', '3', '4'], mark: 2 }
          ]
        } else if (questionsCount === 50) {
          sections = [
            { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
            { id: 'sec2', title: 'اختيار من متعدد', from_q: 21, to_q: 50, choices: ['1', '2', '3', '4'], mark: 2 }
          ]
        } else {
          sections = [
            { id: 'sec1', title: 'صح وخطأ', from_q: 1, to_q: 20, choices: ['صح', 'خطأ'], mark: 1 },
            { id: 'sec2', title: 'اختيار من متعدد', from_q: 21, to_q: questionsCount, choices: ['1', '2', '3', '4'], mark: 2 }
          ]
        }
      }

      // Configure config dynamically
      Object.assign(config, DEFAULT_CONFIG())
      config.template_id = `EXAM_${examData.uniqueCode || examId}`
      config.template_name = `قالب ${examData.title || 'الاختبار'}`
      config.description = `قالب OMR مولد تلقائياً للاختبار: ${examData.title || ''} (${questionsCount} سؤالاً)`
      
      if (config.header) {
        config.header.exam_name = examData.subject_name || 'الامتحان النهائي'
        config.header.governorate = examData.governorate || 'أمانة العاصمة'
        config.header.directorate = examData.directorate || 'المديرية'
        if (students.length > 0) {
          config.header.student_name = students[0].student_name
          config.header.seat_number = students[0].seat_number
          config.header.center_name = students[0].school_name
          config.header.serial_number = students[0].secret_number || '101'
        }
      }

      if (config.metadata) {
        config.metadata.academic_year = examData.year_name || '2026'
      }

      config.questions.metadata.num_questions = questionsCount
      config.questions.sections = sections
      config.questions.layout.columns_count = questionsCount <= 30 ? 3 : 4
      config.questions.layout.choices_count = 4

      if (students.length > 0 && students[0].seat_number) {
        config.barcode.value = String(students[0].seat_number)
      } else {
        config.barcode.value = examData.uniqueCode || '41848501164148'
      }

      savedDbId.value = null
      pageMode.value = 'designer'
      notify(`تم استيراد مواصفات الاختبار «${examData.title}» وبناء القالب (${questionsCount} سؤالاً) ديناميكياً!`)
    }
  } catch (err: any) {
    notify('تعذر استيراد بيانات الاختبار إلى المصمم: ' + extractErrorMessage(err), 'error')
  }
}

onMounted(() => {
  fetchSavedTemplates()
  if (route.query.examId) {
    loadExamIntoDesigner(route.query.examId as string)
  }
})
</script>

<style scoped>
.qb-template-builder-v4 {
  direction: rtl;
}
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.02);
}

.mode-tabs-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.14) !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03) !important;
}

.unified-mode-tabs :deep(.v-tab) {
  border-radius: 8px !important;
  transition: all 0.2s ease;
  margin: 2px 4px;
  font-weight: 700 !important;
  letter-spacing: 0;
  text-transform: none;
}

.unified-mode-tabs :deep(.v-tab--selected) {
  background: rgba(var(--v-theme-primary), 0.08) !important;
  color: rgb(var(--v-theme-primary)) !important;
}

.unified-tab-badge {
  border-radius: 6px !important;
  font-size: 11px !important;
  font-weight: 700 !important;
}
</style>
