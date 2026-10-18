<template>
  <div v-if="activeTemplate" class="hf-canvas hf-canvas-ultra-compact" dir="rtl">
    <!-- Section Title -->
    <div class="hf-section-main-title mb-1 d-flex align-center justify-space-between">
      <div class="d-flex align-center">
        <v-icon
          icon="mdi-view-dashboard-outline"
          size="14"
          color="primary"
          class="me-1"
        />
        <span>تخطيط أعمدة الهيدر والفوتر</span>
      </div>
      <span class="text-caption text-medium-emphasis" style="font-size: 10px">
        (انقر على أي خلية لتحرير محتواها وتنسيقها)
      </span>
    </div>

    <!-- HEADER SECTION -->
    <div class="hf-compact-section mb-2">
      <div class="hf-compact-header">
        <div class="d-flex align-center ga-2">
          <div class="hf-mini-icon-box blue">
            <v-icon icon="mdi-page-layout-header" size="13" color="primary" />
          </div>
          <span
            class="text-caption font-weight-black text-slate-800"
            style="font-size: 11.5px"
            >الهيدر (Header)</span
          >
          <span class="hf-mini-cols-tag blue"
            >{{ activeTemplate?.header?.cells?.length || 3 }} أعمدة</span
          >
        </div>
        <span class="text-caption text-medium-emphasis" style="font-size: 9.5px">
          الارتفاع: {{ activeTemplate?.header?.height || 60 }}px
        </span>
      </div>

      <div
        class="hf-editor-row compact-row"
        :style="{
          backgroundColor: activeTemplate?.header?.backgroundColor || '#ffffff',
          minHeight: '34px',
          borderBottom: activeTemplate?.header?.borderBottom
            ? '2px solid rgba(37, 99, 235, 0.4)'
            : 'none',
        }"
      >
        <div
          v-for="(cell, idx) in activeTemplate?.header?.cells || []"
          :key="cell.id"
          class="hf-compact-cell"
          :class="{
            'is-active': activeSection === 'header' && activeCellIndex === idx,
            'is-dragover': dragOverCell === 'header-' + idx,
            'is-filled': hasCellContent(cell),
          }"
          :style="{ flex: 1 }"
          @click="onCellClick($event, 'header', idx)"
          @dragover.prevent="onDragOver"
          @dragenter.prevent="onDragEnter($event, 'header', idx)"
          @dragleave="onDragLeave($event, 'header', idx)"
          @drop.prevent="onDrop($event, 'header', idx)"
        >
          <div class="d-flex align-center justify-space-between w-100 px-1">
            <span class="hf-compact-label">
              <v-icon
                :icon="
                  activeSection === 'header' && activeCellIndex === idx
                    ? 'mdi-pencil'
                    : hasCellContent(cell)
                    ? 'mdi-check-circle-outline'
                    : 'mdi-cursor-default-click-outline'
                "
                size="13"
                class="me-1"
                :color="
                  activeSection === 'header' && activeCellIndex === idx
                    ? 'primary'
                    : hasCellContent(cell)
                    ? 'success'
                    : 'medium-emphasis'
                "
              />
              {{ getColLabel(idx, activeTemplate?.header?.cells?.length || 3) }}
            </span>
            <span
              v-if="activeSection === 'header' && activeCellIndex === idx"
              class="hf-status-dot active"
              title="محدد حالياً في المحرر"
            ></span>
            <span
              v-else-if="hasCellContent(cell)"
              class="hf-status-dot filled"
              title="يحتوي محتوى"
            ></span>
          </div>
        </div>
      </div>
    </div>

    <!-- FOOTER SECTION -->
    <div class="hf-compact-section">
      <div class="hf-compact-header">
        <div class="d-flex align-center ga-2">
          <div class="hf-mini-icon-box indigo">
            <v-icon icon="mdi-page-layout-footer" size="13" color="indigo" />
          </div>
          <span
            class="text-caption font-weight-black text-slate-800"
            style="font-size: 11.5px"
            >الفوتر (Footer)</span
          >
          <span class="hf-mini-cols-tag indigo"
            >{{ activeTemplate?.footer?.cells?.length || 2 }} أعمدة</span
          >
        </div>
        <span class="text-caption text-medium-emphasis" style="font-size: 9.5px">
          الارتفاع: {{ activeTemplate?.footer?.height || 60 }}px
        </span>
      </div>

      <div
        class="hf-editor-row compact-row"
        :style="{
          backgroundColor: activeTemplate?.footer?.backgroundColor || '#f8fafc',
          minHeight: '34px',
          borderTop: activeTemplate?.footer?.borderTop
            ? '2px solid rgba(79, 70, 229, 0.4)'
            : 'none',
        }"
      >
        <div
          v-for="(cell, idx) in activeTemplate?.footer?.cells || []"
          :key="cell.id"
          class="hf-compact-cell"
          :class="{
            'is-active': activeSection === 'footer' && activeCellIndex === idx,
            'is-dragover': dragOverCell === 'footer-' + idx,
            'is-filled': hasCellContent(cell),
          }"
          :style="{ flex: 1 }"
          @click="onCellClick($event, 'footer', idx)"
          @dragover.prevent="onDragOver"
          @dragenter.prevent="onDragEnter($event, 'footer', idx)"
          @dragleave="onDragLeave($event, 'footer', idx)"
          @drop.prevent="onDrop($event, 'footer', idx)"
        >
          <div class="d-flex align-center justify-space-between w-100 px-1">
            <span class="hf-compact-label">
              <v-icon
                :icon="
                  activeSection === 'footer' && activeCellIndex === idx
                    ? 'mdi-pencil'
                    : hasCellContent(cell)
                    ? 'mdi-check-circle-outline'
                    : 'mdi-cursor-default-click-outline'
                "
                size="13"
                class="me-1"
                :color="
                  activeSection === 'footer' && activeCellIndex === idx
                    ? 'indigo'
                    : hasCellContent(cell)
                    ? 'success'
                    : 'medium-emphasis'
                "
              />
              {{ getColLabel(idx, activeTemplate?.footer?.cells?.length || 2) }}
            </span>
            <span
              v-if="activeSection === 'footer' && activeCellIndex === idx"
              class="hf-status-dot active"
              title="محدد حالياً في المحرر"
            ></span>
            <span
              v-else-if="hasCellContent(cell)"
              class="hf-status-dot filled"
              title="يحتوي محتوى"
            ></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  activeTemplate: {
    type: Object,
    default: null,
  },
  activeSection: {
    type: String,
    default: null,
  },
  activeCellIndex: {
    type: Number,
    default: null,
  },
  allVariables: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["select-cell", "drop-cell", "remove-var"]);

const dragOverCell = ref(null);

// Clear position labels
const getColLabel = (idx, totalCols) => {
  if (totalCols === 3) {
    if (idx === 0) return "العمود 1 (اليمين)";
    if (idx === 1) return "العمود 2 (الوسط)";
    if (idx === 2) return "العمود 3 (اليسار)";
  } else if (totalCols === 2) {
    if (idx === 0) return "العمود 1 (اليمين)";
    if (idx === 1) return "العمود 2 (اليسار)";
  } else if (totalCols === 1) {
    return "العمود (عرض كامل)";
  }
  return `عمود ${idx + 1}`;
};

const hasCellContent = (cell) => {
  return !!(cell && cell.content && cell.content.trim());
};

const onDragOver = (e) => {
  e.preventDefault();
  if (e.dataTransfer) {
    e.dataTransfer.dropEffect = "copy";
  }
};

const onDragEnter = (e, section, idx) => {
  e.preventDefault();
  if (e.dataTransfer) {
    e.dataTransfer.dropEffect = "copy";
  }
  dragOverCell.value = `${section}-${idx}`;
};

const onDragLeave = (e, section, idx) => {
  e.preventDefault();
  if (!e.currentTarget || !e.currentTarget.contains(e.relatedTarget)) {
    if (dragOverCell.value === `${section}-${idx}`) {
      dragOverCell.value = null;
    }
  }
};

const onDrop = (e, section, idx) => {
  e.preventDefault();
  e.stopPropagation();
  dragOverCell.value = null;
  const varKey =
    e.dataTransfer?.getData("text/plain") ||
    e.dataTransfer?.getData("text") ||
    (typeof window !== "undefined" ? window.__hfDraggedVar : null);
  emit("drop-cell", { event: e, section, idx, varKey });
};

const getCellStyle = (cell) => {
  const s = cell?.style || {};
  let justify = "center";
  if (s.textAlign === "right") justify = "flex-start";
  else if (s.textAlign === "left") justify = "flex-end";

  const bg =
    s.backgroundColor === "transparent" || !s.backgroundColor
      ? "transparent"
      : s.backgroundColor;
  const fSize = parseInt(s.fontSize || 13);
  return `font-size: ${fSize}px !important; font-family: ${
    s.fontFamily || "Tajawal"
  } !important; font-weight: ${s.fontWeight || "normal"} !important; text-align: ${
    s.textAlign || "center"
  } !important; justify-content: ${justify} !important; background-color: ${bg} !important; width: 100%; min-height: 100%; box-sizing: border-box;`;
};

const onCellClick = (e, section, idx) => {
  const delBtn = e.target.closest(".hf-canvas-chip-remove");
  if (delBtn) {
    e.preventDefault();
    e.stopPropagation();
    const chip = delBtn.closest(".hf-canvas-chip");
    const token = chip?.getAttribute("data-token");
    if (token) {
      emit("remove-var", { section, cellIdx: idx, varKey: token });
      return;
    }
  }
  emit("select-cell", { section, idx });
};
</script>
