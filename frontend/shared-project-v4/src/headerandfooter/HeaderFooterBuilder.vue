<template>
  <div class="hf-builder" dir="rtl">
    <!-- ═══════════════════════════════════════════════════
         MAIN SCREEN: TEMPLATES TABLE VIEW (جدول قوالب الهيدر والفوتر)
    ═══════════════════════════════════════════════════ -->

    <HfTemplatesTable
      :templates="store.templates"
      :active-template-id="store.activeTemplateId"
      @select-template="onSelectTemplate"
      @edit-template="onEditTemplate"
      @duplicate-template="onDuplicateTemplate"
      @open-create="openCreateDialog"
    />

    <!-- ═══════════════════════════════════════════════════
         TEMPLATE DESIGN EDITOR DIALOG (ديالوق محرر وتصميم القالب)
    ═══════════════════════════════════════════════════ -->
    <custom-dialog v-model="editorDialog" v-if="editorDialog" fullscreen>
      <template #title>
        <v-sheet>
          <div
            class="text-subtitle-1 font-weight-black text-slate-800 d-flex align-center ga-2"
          >
            <v-icon icon="mdi-pencil-ruler" size="20" color="primary" />
            <span
              >{{ store.draftTemplate ? "تصميم قالب جديد:" : "تعديل القالب:" }}
              {{ store.activeTemplate?.name }}</span
            >
            <v-chip
              v-if="store.draftTemplate"
              size="x-small"
              color="warning"
              variant="flat"
              class="font-weight-bold"
            >
              مسودة جديدة
            </v-chip>
          </div>
        </v-sheet>
      </template>

      <!-- Dialog Editor Body Workspace -->
      <div
        class="hf-main-wrapper"
        style="flex: 1; min-height: 0; height: calc(100vh - 65px)"
      >
        <div class="hf-main" :class="`mobile-tab-${mobileTab}`">
          <!-- Mobile Navigation Switcher (Screens < 960px) -->
          <div class="hf-mobile-nav">
            <button
              type="button"
              class="hf-mobile-nav-btn"
              :class="{ active: mobileTab === 'canvas' }"
              @click="mobileTab = 'canvas'"
            >
              <v-icon icon="mdi-view-dashboard-outline" size="16" class="me-1" />
              <span>الكانفاس والمحرر</span>
            </button>
            <button
              type="button"
              class="hf-mobile-nav-btn"
              :class="{ active: mobileTab === 'sidebar' }"
              @click="mobileTab = 'sidebar'"
            >
              <v-icon icon="mdi-variable" size="16" class="me-1" />
              <span>المتغيرات والإعدادات</span>
              <span class="hf-mobile-badge">{{ store.allVariables.length }}</span>
            </button>
            <button
              type="button"
              class="hf-mobile-nav-btn"
              :class="{ active: mobileTab === 'preview' }"
              @click="mobileTab = 'preview'"
            >
              <v-icon icon="mdi-eye-outline" size="16" class="me-1" />
              <span>المعاينة الحية</span>
            </button>
          </div>

          <!-- LEFT: Variables & Options Panel -->
          <div class="hf-sidebar-container">
            <HfSidebar
              :active-template="store.activeTemplate"
              :static-variables="store.staticVariables"
              :api-variables="store.apiVariables"
              :api-loading="store.apiLoading"
              :api-error="store.apiError"
              v-model:section-tab="sectionTab"
              @insert-var="insertVarIntoEditor"
              @drag-start="onDragStart"
              @drop-to-cell="onDropToCellDirect"
              @change-columns="changeColumns"
              @update-section-style="updateSectionStyle"
              @fetch-api="store.fetchApiVariables()"
            />
          </div>

          <!-- CENTER + BOTTOM: Editor Canvas + Live Preview (All in one unified scroll body) -->
          <div class="hf-canvas-wrapper">
            <div class="hf-canvas-area-scroll">
              <!-- Canvas Breadcrumb / Back to Table bar -->
              <div
                class="hf-canvas-top-bar d-flex align-center justify-space-between mb-3 px-3 py-2 bg-white rounded-lg border"
              >
                <div class="d-flex align-center ga-2">
                  <v-chip
                    size="small"
                    variant="tonal"
                    color="info"
                    class="font-weight-bold"
                  >
                    هيدر: {{ store.activeTemplate?.header?.columns || 3 }} أعمدة
                  </v-chip>
                  <v-chip
                    size="small"
                    variant="tonal"
                    color="indigo"
                    class="font-weight-bold"
                  >
                    فوتر: {{ store.activeTemplate?.footer?.columns || 3 }} أعمدة
                  </v-chip>
                </div>
              </div>

              <!-- Editor Canvas -->
              <HfCanvas
                :active-template="store.activeTemplate"
                :active-section="activeSection"
                :active-cell-index="activeCellIndex"
                :all-variables="store.allVariables"
                @select-cell="onSelectCell"
                @drop-cell="onDropToCanvasCell"
                @remove-var="onRemoveVarFromCell"
              />

              <!-- Cell Editor (Inline Rich Toolbar & Contenteditable) -->
              <transition name="slide-up">
                <HfCellEditor
                  ref="cellEditorRef"
                  v-if="activeSection && activeCellIndex !== null"
                  :active-section="activeSection"
                  :active-cell-index="activeCellIndex"
                  :active-cell="activeCell"
                  :all-variables="store.allVariables"
                  :dragged-var="draggedVar"
                  @close="activeSection = null"
                  @update-style="onUpdateCellStyle"
                  @update-content="onUpdateCellContent"
                  @clear-content="onClearCellContent"
                />
              </transition>

              <!-- LIVE PREVIEW — Scrolling together with the canvas & editor in the body -->
              <div class="hf-preview-container mt-4">
                <HfLivePreview
                  :live-html="liveHTML"
                  :active-template="store.activeTemplate"
                  @select-cell="onSelectCell"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <template #actions>
        <custom-btn type="save" :click="saveAndCloseEditor" />
      </template>
    </custom-dialog>

    <!-- CREATE TEMPLATE WIZARD DIALOG -->
    <HfCreateDialog v-model="createDialog" @create="onCreateTemplate" />

    <!-- TEMPLATE SELECT DIALOG (Reusable Component) -->
    <HfTemplateSelectDialog
      v-model="assignDialog"
      :initial-template-id="store.activeTemplateId"
      @confirm="onTemplateSelected"
    />

    <!-- SUCCESS SNACKBAR -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      location="top"
      rounded="lg"
      :timeout="3000"
    >
      <div class="d-flex align-center ga-2">
        <v-icon :icon="snackbar.icon" color="white" size="20" />
        <span class="font-weight-bold">{{ snackbar.text }}</span>
      </div>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useCustomHeaderFooter } from "./composables/useCustomHeaderFooter";

// Subcomponents
import HfTopBar from "./components/HfTopBar.vue";
import HfTemplatesTable from "./components/HfTemplatesTable.vue";
import HfSidebar from "./components/HfSidebar.vue";
import HfCanvas from "./components/HfCanvas.vue";
import HfCellEditor from "./components/HfCellEditor.vue";
import HfLivePreview from "./components/HfLivePreview.vue";
import HfCreateDialog from "./components/HfCreateDialog.vue";
import HfTemplateSelectDialog from "./components/HfTemplateSelectDialog.vue";
import HfEmptyState from "./components/HfEmptyState.vue";

// Dedicated unified stylesheet
import "./styles/headerFooter.css";

const store = useCustomHeaderFooter();

// ── State ─────────────────────────────────────────────────────────────
const editorDialog = ref(false);
const mobileTab = ref("canvas");
const sectionTab = ref("header");
const activeSection = ref(null);
const activeCellIndex = ref(null);
const createDialog = ref(false);
const assignDialog = ref(false);
const draggedVar = ref(null);
const cellEditorRef = ref(null);
const snackbar = ref({
  show: false,
  text: "",
  color: "success",
  icon: "mdi-check-circle",
});
const savingTemplate = ref(false);

// ── Computed ──────────────────────────────────────────────────────────
const activeCell = computed(() => {
  if (!activeSection.value || activeCellIndex.value === null) return null;
  return (
    store.activeTemplate?.[activeSection.value]?.cells?.[activeCellIndex.value] || null
  );
});

const liveHTML = computed(() => {
  if (!store.activeTemplate) return { header: "", footer: "" };
  return store.generateHTML(store.activeTemplateId);
});

// ── Selection & Actions ───────────────────────────────────────────────
const selectCell = (section, idx) => {
  activeSection.value = section;
  activeCellIndex.value = idx;
  sectionTab.value = section;
};

const onSelectCell = ({ section, idx }) => {
  selectCell(section, idx);
};

const onSelectTemplate = (id) => {
  store.setActiveTemplate(id);
  activeSection.value = null;
  activeCellIndex.value = null;
  setTimeout(() => {
    selectCell("header", 0);
  }, 50);
};

const onEditTemplate = (id) => {
  store.startEditTemplate(id);
  activeSection.value = null;
  activeCellIndex.value = null;
  setTimeout(() => {
    selectCell("header", 0);
  }, 50);
  editorDialog.value = true;
};

const onDuplicateTemplate = async (id) => {
  await store.duplicateTemplate(id);
};

// ── Drag & Drop ───────────────────────────────────────────────────────
const onDragStart = (varKey) => {
  draggedVar.value = varKey;
};

const onDropToCanvasCell = ({ event, section, idx, varKey }) => {
  const finalVarKey =
    varKey ||
    event?.dataTransfer?.getData("text/plain") ||
    event?.dataTransfer?.getData("text") ||
    draggedVar.value ||
    (typeof window !== "undefined" ? window.__hfDraggedVar : null);
  if (!finalVarKey) return;
  const cell = store.activeTemplate?.[section]?.cells?.[idx];
  if (cell) {
    const newContent = (cell.content || "") + (cell.content ? " " : "") + finalVarKey;
    store.updateCellContent(store.activeTemplateId, section, idx, newContent);
    selectCell(section, idx);
    setTimeout(() => {
      if (cellEditorRef.value) {
        cellEditorRef.value.loadCellContentIntoEditor();
      }
    }, 40);
  }
};

const onDropToCellDirect = ({ section, idx, varKey }) => {
  const cell = store.activeTemplate?.[section]?.cells?.[idx];
  if (cell && varKey) {
    const newContent = (cell.content || "") + (cell.content ? " " : "") + varKey;
    store.updateCellContent(store.activeTemplateId, section, idx, newContent);
    selectCell(section, idx);
    setTimeout(() => {
      if (cellEditorRef.value) {
        cellEditorRef.value.loadCellContentIntoEditor();
      }
    }, 40);
  }
};

const onRemoveVarFromCell = ({ section, cellIdx, varKey }) => {
  const tpl = store.activeTemplate;
  if (!tpl || !tpl[section] || !tpl[section].cells[cellIdx]) return;
  const currentContent = tpl[section].cells[cellIdx].content || "";
  const cleanKey = varKey.replace(/[{}]/g, "").split("|")[0];
  const regex = new RegExp(`\\{\\{${cleanKey}(?:\\|[^}]+)?\\}\\}`, "g");
  const newContent = currentContent
    .replace(regex, "")
    .replace(/\s{2,}/g, " ")
    .trim();
  store.updateCellContent(store.activeTemplateId, section, cellIdx, newContent);

  if (
    activeSection.value === section &&
    activeCellIndex.value === cellIdx &&
    cellEditorRef.value
  ) {
    cellEditorRef.value.loadCellContentIntoEditor();
  }
};

// Insert variable via click from sidebar into rich editor
const insertVarIntoEditor = (varKey) => {
  mobileTab.value = "canvas";
  if (!activeSection.value || activeCellIndex.value === null) {
    selectCell("header", 0);
    setTimeout(() => {
      insertVarIntoEditor(varKey);
    }, 50);
    return;
  }

  if (cellEditorRef.value) {
    cellEditorRef.value.insertVariable(varKey);
  }
};

// ── Editor Handlers ───────────────────────────────────────────────────
const onUpdateCellStyle = ({ key, value }) => {
  if (!activeSection.value || activeCellIndex.value === null) return;
  store.updateCellStyle(
    store.activeTemplateId,
    activeSection.value,
    activeCellIndex.value,
    key,
    value
  );
};

const onUpdateCellContent = (rawText) => {
  if (!activeSection.value || activeCellIndex.value === null) return;
  store.updateCellContent(
    store.activeTemplateId,
    activeSection.value,
    activeCellIndex.value,
    rawText
  );
};

const onClearCellContent = () => {
  if (!activeSection.value || activeCellIndex.value === null) return;
  store.updateCellContent(
    store.activeTemplateId,
    activeSection.value,
    activeCellIndex.value,
    ""
  );
};

const changeColumns = (n) => {
  if (!store.activeTemplateId) return;
  if (sectionTab.value === "header") store.setHeaderColumns(store.activeTemplateId, n);
  else store.setFooterColumns(store.activeTemplateId, n);
  activeSection.value = null;
  activeCellIndex.value = null;
};

const updateSectionStyle = (section, prop, val) => {
  store.updateSectionStyle(store.activeTemplateId, section, prop, val);
};

// ── Template Dialogs ──────────────────────────────────────────────────
const openCreateDialog = () => {
  createDialog.value = true;
};

const onCreateTemplate = ({ name, headerColumns, footerColumns }) => {
  store.startNewTemplateDraft({
    name,
    headerColumns,
    footerColumns,
  });
  activeSection.value = null;
  activeCellIndex.value = null;
  setTimeout(() => {
    selectCell("header", 0);
  }, 50);
  editorDialog.value = true;
};

const saveAndCloseEditor = async () => {
  if (savingTemplate.value) return;
  savingTemplate.value = true;
  try {
    if (store.draftTemplate) {
      // قالب جديد → POST إلى API
      const tplName = store.draftTemplate.name;
      // أضف المسودة مؤقتاً للجدول حتى ينتهي POST
      store.commitDraftTemplate();
      const savedTpl = store.templates?.results[store.templates?.results.length - 1];

      await store.saveTemplateToApi(savedTpl);
      snackbar.value = {
        show: true,
        text: `تم حفظ وإنشاء قالب "${tplName}" بنجاح`,
        color: "success",
        icon: "mdi-check-circle",
      };
    } else {
      // تعديل قالب موجود → PUT إلى API
      const tpl = store.activeTemplate;
      store.commitEditTemplate();
      await store.updateTemplateInApi(tpl);
      snackbar.value = {
        show: true,
        text: "تم حفظ التعديلات بنجاح",
        color: "success",
        icon: "mdi-check-circle",
      };
    }
    editorDialog.value = false;
  } catch (err) {
    console.error("saveAndCloseEditor error:", err);
    snackbar.value = {
      show: true,
      text: "حدث خطأ أثناء الحفظ، يرجى المحاولة مجدداً.",
      color: "error",
      icon: "mdi-alert-circle",
    };
  } finally {
    savingTemplate.value = false;
  }
};

const closeEditorDialog = (save = false) => {
  if (save) {
    saveAndCloseEditor();
    return;
  }
  if (store.draftTemplate) {
    store.cancelDraftTemplate();
  } else {
    store.cancelEditTemplate();
  }
  editorDialog.value = false;
};

const onTemplateSelected = ({ templateId, template }) => {
  if (templateId) {
    store.setActiveTemplate(templateId);
  }
  snackbar.value = {
    show: true,
    text: `تم بنجاح اختيار وتعيين "${template?.name || "القالب"}"`,
    color: "success",
    icon: "mdi-check-circle-outline",
  };
};

// ── Initialize on Mount ───────────────────────────────────────────────
onMounted(async () => {
  store.fetchApiVariables();

  setTimeout(() => {
    selectCell("header", 0);
  }, 80);
});

// مسح جميع البيانات عند الخروج من الشاشة
onUnmounted(() => {
  store.clearTemplates();
});
</script>

<style>
@import "./styles/headerFooter.css";

.hf-table-screen {
  flex: 1;
  overflow-y: auto;
  background: #f8fafc;
  min-height: calc(100vh - 65px);
}

.hf-main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 65px);
  overflow: hidden;
}

.hf-canvas-area-scroll {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.hf-canvas-top-bar {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}
</style>
