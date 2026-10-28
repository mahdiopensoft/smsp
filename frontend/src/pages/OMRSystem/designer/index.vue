<template>
  <div class="qb-template-builder-v4" dir="rtl">
    <!-- ── Page Header ─────────────────────────────────────────── -->
    <DesignerHeader
      :page-mode="pageMode"
      :saved-db-id="savedDbId"
      :is-saving="isSaving"
      @switch-mode="pageMode = $event"
      @create-new="startNewDesignerTemplate"
      @open-import="showImportExamModal = true"
      @reset="createNewTemplate"
      @update="handleUpdateTemplate"
      @open-save-modal="showSaveModal = true"
    />

    <!-- ── Linked Exam Workflow Status Banner ──────────────────────────── -->
    <LinkedExamBanner
      v-if="linkedExam"
      :exam="linkedExam"
      :questions-count="config.questions.metadata.num_questions"
      :display-mode="config.display_mode"
      @back-to-exam="goBackToExam"
      @go-to-print="goToPrintForExam"
      @go-to-scanner="goToScannerForExam"
    />

    <!-- ── Mode Tabs Switcher ────────────────────────────────────── -->
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

    <!-- ── TAB 1: TEMPLATE LIBRARY ───────────────────────────────── -->
    <div v-if="pageMode === 'library'">
      <TemplateLibrary
        :templates="savedTemplatesList"
        :is-loading="isLoadingTemplates"
        @create-new="startNewDesignerTemplate"
        @edit="loadTemplateForEditing"
        @scan="goToScannerWithTemplate"
        @preview="openPreviewModal"
        @duplicate="duplicateTemplate"
        @print="printDirect"
        @delete="deleteTemplateById"
      />
    </div>

    <!-- ── TAB 2: VISUAL DESIGNER ─────────────────────────────────── -->
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
              <v-tab value="student" class="font-weight-bold">
                <v-icon start size="16">mdi-shield-star-outline</v-icon>
                بطاقة الطالب والشعار
              </v-tab>
              <v-tab value="questions" class="font-weight-bold">الأسئلة</v-tab>
              <v-tab value="codes" class="font-weight-bold">الباركود</v-tab>
              <v-tab value="detection" class="font-weight-bold">الذكاء الاصطناعي</v-tab>
            </v-tabs>

            <v-window v-model="designerTab">
              <v-window-item value="layout">
                <PageLayoutSettings :config="config" @preset-selected="applyPreset" />
              </v-window-item>
              <v-window-item value="student">
                <StudentCardSettings :config="config" />
              </v-window-item>
              <v-window-item value="questions">
                <SectionsManager :config="config" />
              </v-window-item>
              <v-window-item value="codes">
                <CodesSettings :config="config" />
              </v-window-item>
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

    <!-- ── Preview Modal ─────────────────────────────────────────── -->
    <PreviewSheetModal
      v-model="showPreviewModal"
      :template="previewingTemplate"
      @edit="loadTemplateForEditing"
      @scan="goToScannerWithTemplate"
    />

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

    <!-- ── Import Exam Modal ─────────────────────────────────────── -->
    <ImportExamModal
      v-model="showImportExamModal"
      @import-exam="importExamById"
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
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDesignerConfig } from './composables/useDesignerConfig'
import { useDesignerApi } from './composables/useDesignerApi'

// Subcomponents
import DesignerHeader from './components/DesignerHeader.vue'
import LinkedExamBanner from './components/LinkedExamBanner.vue'
import PreviewSheetModal from './components/PreviewSheetModal.vue'
import ImportExamModal from './components/ImportExamModal.vue'
import TemplateLibrary from './components/TemplateLibrary.vue'
import TemplateCanvas from './components/TemplateCanvas.vue'
import SaveExportModal from './components/SaveExportModal.vue'

// Panels
import PageLayoutSettings from './panels/PageLayoutSettings.vue'
import StudentCardSettings from './panels/StudentCardSettings.vue'
import SectionsManager from './panels/SectionsManager.vue'
import CodesSettings from './panels/CodesSettings.vue'
import DetectionSettings from './panels/DetectionSettings.vue'

const router = useRouter()
const route = useRoute()

// ── Composables ─────────────────────────────────────────────────
const {
  pageMode,
  designerTab,
  savedDbId,
  config,
  createNewTemplate,
  startNewDesignerTemplate,
  applyPreset,
  loadSavedTemplateState,
} = useDesignerConfig()

const {
  savedTemplatesList,
  isLoadingTemplates,
  isSaving,
  linkedExam,
  showToast,
  toastMsg,
  toastType,
  notify,
  fetchSavedTemplates,
  saveNewTemplate,
  updateTemplate,
  deleteTemplateById,
  importExamSpecs,
} = useDesignerApi()

// ── Dialog States ───────────────────────────────────────────────
const showSaveModal = ref(false)
const showImportExamModal = ref(false)
const showPreviewModal = ref(false)
const previewingTemplate = ref<any | null>(null)

// ── Actions ─────────────────────────────────────────────────────
function loadTemplateForEditing(t: any) {
  loadSavedTemplateState(t)
  showPreviewModal.value = false
  pageMode.value = 'designer'
  notify(`تم تحميل القالب «${t.name}» في المصمم بنجاح`)
}

function openPreviewModal(t: any) {
  previewingTemplate.value = t
  showPreviewModal.value = true
}

function goToScannerWithTemplate(id: number | string) {
  showPreviewModal.value = false
  router.push({ path: '/omr-scanner-lab', query: { templateId: id } })
}

function duplicateTemplate(t: any) {
  loadTemplateForEditing(t)
  savedDbId.value = null
  config.template_name = `${t.name} (نسخة)`
  notify('تم إنشاء نسخة في المصمم، يمكنك تعديلها وحفظها الآن')
}

function printDirect(t: any) {
  openPreviewModal(t)
}

function handleQuickSave() {
  if (savedDbId.value) {
    handleUpdateTemplate()
  } else {
    showSaveModal.value = true
  }
}

async function handleUpdateTemplate() {
  if (savedDbId.value) {
    await updateTemplate(config, savedDbId.value)
  }
}

async function confirmSaveTemplate(formData: any) {
  const success = await saveNewTemplate(formData, config, savedDbId)
  if (success) {
    showSaveModal.value = false
    pageMode.value = 'library'
  }
}

async function importExamById(examId: number) {
  const success = await importExamSpecs(examId, config, savedDbId)
  if (success) {
    pageMode.value = 'designer'
  }
}

// ── Navigation ──────────────────────────────────────────────────
const goBackToExam = () => {
  if (linkedExam.value?.id) {
    router.push({ path: '/omr-exams', query: { open_exam_id: linkedExam.value.id } })
  } else {
    router.push('/omr-exams')
  }
}

const goToPrintForExam = () => {
  if (linkedExam.value?.id) {
    router.push({ path: '/omr-print-registry', query: { exam_id: linkedExam.value.id } })
  } else {
    router.push('/omr-print-registry')
  }
}

const goToScannerForExam = () => {
  if (linkedExam.value?.id) {
    router.push({
      path: '/omr-scanner-lab',
      query: {
        exam_id: linkedExam.value.id,
        exam_code: linkedExam.value.uniqueCode,
        exam_title: linkedExam.value.title,
      },
    })
  } else {
    router.push('/omr-scanner-lab')
  }
}

onMounted(() => {
  fetchSavedTemplates()
  if (route.query.examId) {
    importExamById(Number(route.query.examId))
  }
})

watch(
  () => route.query.examId,
  (newId) => {
    if (newId) {
      importExamById(Number(newId))
    }
  }
)
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
