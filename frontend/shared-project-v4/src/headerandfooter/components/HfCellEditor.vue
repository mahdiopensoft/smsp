<template>
  <div class="hf-cell-editor" v-if="activeSection && activeCellIndex !== null">
    <!-- Header -->
    <div class="hf-cell-editor-header">
      <div class="d-flex align-center ga-2">
        <v-icon icon="mdi-square-edit-outline" size="18" color="primary" />
        <span class="font-weight-bold">محرر محتوى الخلية</span>
        <span class="hf-editor-badge">
          {{ activeSection === "header" ? "الهيدر" : "الفوتر" }} — عمود
          {{ activeCellIndex + 1 }}
        </span>
      </div>

      <v-btn
        icon="mdi-close"
        size="small"
        class="ms-auto"
        variant="text"
        @click="$emit('close')"
      />
    </div>

    <!-- Structured Toolbar -->
    <div class="hf-toolbar">
      <!-- Group 1: Font & Size -->
      <div class="hf-toolbar-group">
        <!-- Font Family Dropdown -->
        <div class="hf-font-dropdown-wrapper" ref="fontDropdownRef">
          <button
            type="button"
            class="hf-font-activator"
            :class="{ active: fontsMenuOpen }"
            @mousedown.prevent="saveSelection"
            @click.stop="toggleFontMenu"
            :title="'نوع الخط: ' + currentFontFamily"
          >
            <span :style="{ fontFamily: currentFontFamily }">
              {{ currentFontFamily }}
            </span>
            <v-icon
              :icon="fontsMenuOpen ? 'mdi-chevron-up' : 'mdi-chevron-down'"
              size="12"
            />
          </button>

          <!-- Dropdown Menu -->
          <div v-if="fontsMenuOpen" class="hf-font-menu" @click.stop>
            <button
              v-for="f in FONTS"
              :key="f"
              type="button"
              class="hf-font-menu-item"
              :class="{ active: currentFontFamily === f }"
              :style="{ fontFamily: f }"
              @mousedown.prevent
              @click="pickFont(f)"
            >
              {{ f }}
            </button>
          </div>
        </div>

        <!-- Font Size +/- with Quick Presets -->
        <div class="hf-size-control" ref="sizeDropdownRef">
          <button
            type="button"
            class="hf-size-btn"
            @mousedown.prevent
            @click="adjustFontSize(-1)"
            title="تصغير الخط (−2px)"
          >
            −
          </button>
          <button
            type="button"
            class="hf-size-value-btn"
            @mousedown.prevent
            @click.stop="toggleSizeMenu"
            :title="`الحجم الحالي: ${currentFontSize}px (انقر لاختيار حجم محدد)`"
          >
            {{ currentFontSize }}
          </button>
          <button
            type="button"
            class="hf-size-btn"
            @mousedown.prevent
            @click="adjustFontSize(+1)"
            title="تكبير الخط (+2px)"
          >
            +
          </button>

          <!-- Size Presets Dropdown -->
          <div v-if="sizeMenuOpen" class="hf-size-menu" @click.stop>
            <button
              v-for="sz in FONT_SIZES"
              :key="sz"
              type="button"
              class="hf-size-menu-item"
              :class="{ active: Number(currentFontSize) === Number(sz) }"
              @mousedown.prevent
              @click="pickFontSize(Number(sz))"
            >
              {{ sz }}
            </button>
          </div>
        </div>
      </div>

      <div class="hf-toolbar-sep" />

      <!-- Group 2: Text Formatting (Bold, Italic, Underline) -->
      <div class="hf-toolbar-group">
        <button
          type="button"
          class="hf-toolbar-btn"
          :class="{ active: isFormatActive('bold', 'fontWeight', 'bold') }"
          title="غامق (Bold)"
          @mousedown.prevent
          @click="applyFormat('bold', 'fontWeight', 'bold', 'normal')"
        >
          <b>B</b>
        </button>
        <button
          type="button"
          class="hf-toolbar-btn"
          :class="{ active: isFormatActive('italic', 'fontStyle', 'italic') }"
          title="مائل (Italic)"
          @mousedown.prevent
          @click="applyFormat('italic', 'fontStyle', 'italic', 'normal')"
        >
          <i>I</i>
        </button>
        <button
          type="button"
          class="hf-toolbar-btn"
          :class="{ active: isFormatActive('underline', 'textDecoration', 'underline') }"
          title="تسطير (Underline)"
          @mousedown.prevent
          @click="applyFormat('underline', 'textDecoration', 'underline', 'none')"
        >
          <u>U</u>
        </button>
      </div>

      <div class="hf-toolbar-sep" />

      <!-- Group 3: Text Alignment -->
      <div class="hf-toolbar-group">
        <button
          v-for="align in ['right', 'center', 'left']"
          :key="align"
          type="button"
          class="hf-toolbar-btn"
          :class="{ active: (activeCell?.style?.textAlign || 'right') === align }"
          :title="`محاذاة ${
            align === 'right' ? 'يمين' : align === 'center' ? 'وسط' : 'يسار'
          }`"
          @click="$emit('update-style', { key: 'textAlign', value: align })"
        >
          <v-icon :icon="ALIGN_ICONS[align]" size="14" />
        </button>
      </div>

      <div class="hf-toolbar-sep" />

      <!-- Group 4: Colors (Text Color & Fill Color) -->
      <div class="hf-toolbar-group">
        <div class="hf-color-wrapper" title="لون النص" @mousedown="saveSelection">
          <v-icon icon="mdi-format-color-text" size="14" />
          <input
            type="color"
            class="hf-color-overlay"
            :value="activeCell?.style?.color || '#000000'"
            @input="applyTextColor($event.target.value)"
          />
        </div>

        <div class="hf-color-wrapper" title="لون خلفية الخلية">
          <v-icon icon="mdi-format-color-fill" size="14" />
          <input
            type="color"
            class="hf-color-overlay"
            :value="
              activeCell?.style?.backgroundColor === 'transparent'
                ? '#ffffff'
                : activeCell?.style?.backgroundColor || '#ffffff'
            "
            @input="
              $emit('update-style', {
                key: 'backgroundColor',
                value: $event.target.value,
              })
            "
          />
        </div>
      </div>

      <!-- Group 5: Clear Button -->
      <div class="ms-auto d-flex align-center ga-1">
        <button
          type="button"
          class="hf-clear-cell-btn"
          title="مسح محتوى الخلية"
          @click="clearCell"
        >
          <v-icon icon="mdi-trash-can-outline" size="13" class="me-1" />
          مسح
        </button>
      </div>

      <!-- Visual Selection Indicator -->
      <template v-if="selectedTextPreview">
        <div class="hf-toolbar-sep" />
        <div class="hf-selection-indicator" title="التنسيق سيطبق على هذا النص المحدد فقط">
          <v-icon icon="mdi-format-paint" size="12" color="primary" />
          <span>
            تعديل المحدد: "<b>{{
              selectedTextPreview.length > 14
                ? selectedTextPreview.substring(0, 14) + "..."
                : selectedTextPreview
            }}</b
            >"
          </span>
          <button
            type="button"
            class="hf-selection-clear-btn"
            title="إلغاء تحديد الكلمة"
            @click.stop="clearSelection"
          >
            ✕
          </button>
        </div>
      </template>
    </div>

    <!-- Content Area -->
    <div
      class="hf-content-area"
      @dragover.prevent="onEditorDragOver"
      @drop.prevent="onDropToEditor"
    >
      <!-- The Rich Editor Contenteditable Box -->
      <div
        ref="richEditorRef"
        class="hf-rich-editor"
        contenteditable="true"
        dir="rtl"
        :style="`font-family: ${baseFontFamily} !important; font-size: ${baseFontSize}px !important; text-align: ${
          activeCell?.style?.textAlign || 'right'
        } !important; color: ${
          activeCell?.style?.color || '#000000'
        } !important; font-weight: ${
          activeCell?.style?.fontWeight || 'normal'
        } !important; font-style: ${
          activeCell?.style?.fontStyle || 'normal'
        } !important; text-decoration: ${
          activeCell?.style?.textDecoration || 'none'
        } !important;`"
        @keydown="onEditorKeyDown"
        @input="onEditorInput"
        @mousedown="onEditorMouseDown"
        @click="onEditorClick"
        @mouseup="saveSelection"
        @keyup="saveSelection"
        @focus="saveSelection"
        @dragover.prevent="onEditorDragOver"
        @dragenter.prevent
        @drop.prevent="onDropToEditor"
        data-placeholder="اكتب هنا بحرية... أو اسحب المتغيرات والصور وأفلتها في هذا المحرر مباشرة"
      ></div>
    </div>

    <!-- Image Template & Size Customization Dialog -->
    <v-dialog v-model="imageDialog" max-width="580" persistent>
      <v-card class="rounded-xl overflow-hidden" elevation="8">
        <!-- 1. Fixed Header Title -->
        <v-card-title
          class="d-flex align-center justify-space-between px-4 py-3 border-b bg-surface"
        >
          <div class="d-flex align-center ga-2">
            <v-icon icon="mdi-image-edit-outline" color="primary" size="20" />
            <span class="text-subtitle-1 font-weight-bold">تعديل قالب وشكل الصورة</span>
          </div>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            @click="imageDialog = false"
          />
        </v-card-title>

        <!-- 2. Fixed Top Visual Live Preview Box -->
        <div class="px-4 py-3 border-b" style="background: #f8fafc">
          <div
            class="d-flex flex-column align-center justify-center pa-3 rounded-lg"
            style="background: #ffffff; border: 1px solid #e2e8f0; min-height: 120px"
          >
            <div
              :class="`shape-${selectedShape}`"
              :style="`width: ${Math.min(selectedWidth, 180)}px; height: ${
                selectedShape === 'circle' || selectedShape === 'stamp-double'
                  ? `${Math.min(selectedWidth, 180)}px`
                  : `${Math.min(selectedHeight, 130)}px`
              }; opacity: ${
                selectedOpacity / 100
              }; transition: all 0.2s; overflow: hidden; display: flex; align-items: center; justify-content: center;`"
            >
              <img
                v-if="previewImgSrc"
                :src="previewImgSrc"
                :style="`width: 100%; height: 100%; display: block; object-fit: ${selectedFit} !important;`"
                alt="preview"
              />
              <div
                v-else
                class="d-flex flex-column align-center justify-center pa-2 rounded"
                style="
                  background: #f1f5f9;
                  border: 1.5px dashed #cbd5e1;
                  width: 100%;
                  height: 100%;
                "
              >
                <v-icon
                  icon="mdi-image-off-outline"
                  size="26"
                  color="grey-darken-1"
                  class="mb-1"
                />
                <span
                  class="text-caption text-medium-emphasis font-weight-bold"
                  style="font-size: 11px !important"
                  >لا توجد صورة</span
                >
              </div>
            </div>
            <span class="text-caption font-weight-bold mt-2 text-medium-emphasis">
              {{ previewLabel }} — {{ selectedWidth }} × {{ selectedHeight }} px
              <span v-if="selectedOpacity < 100" class="text-primary font-weight-black"
                >({{ selectedOpacity }}% شفافية)</span
              >
              <span class="text-primary font-weight-bold"> — ({{ selectedFit }})</span>
            </span>
          </div>
        </div>

        <!-- 3. Unified Scrollable Controls Body (Templates + Width + Opacity all scrolling together) -->
        <div class="hf-dialog-scroll-body">
          <!-- Choose Shape Template -->
          <label class="hf-label mb-2 d-block font-weight-bold"
            >اختر قالب وشكل العرض</label
          >
          <div class="hf-shape-grid mb-4">
            <div
              v-for="shp in IMAGE_SHAPES"
              :key="shp.key"
              class="hf-shape-card"
              :class="{ active: selectedShape === shp.key }"
              @click="selectedShape = shp.key"
            >
              <v-icon
                :icon="shp.icon"
                size="22"
                :color="selectedShape === shp.key ? 'primary' : 'grey-darken-1'"
              />
              <span
                class="text-caption font-weight-bold mt-1"
                style="font-size: 11.5px !important"
                >{{ shp.label }}</span
              >
              <span
                class="text-caption text-medium-emphasis"
                style="font-size: 9.5px !important"
                >{{ shp.desc }}</span
              >
            </div>
          </div>

          <!-- Image Width & Height Controls (حجم وأبعاد الصورة) -->
          <div class="d-flex align-center justify-space-between mb-2 pt-2 border-t">
            <div class="d-flex align-center ga-1">
              <v-icon icon="mdi-aspect-ratio" size="16" color="primary" />
              <label class="hf-label font-weight-bold"
                >أبعاد الصورة (العرض والارتفاع)</label
              >
            </div>
            <span class="text-caption font-weight-bold text-primary"
              >{{ selectedWidth }} × {{ selectedHeight }} px</span
            >
          </div>

          <!-- Dual Compact Manual Input Fields -->
          <div class="d-flex align-center ga-2 mb-3">
            <!-- Width Input Field -->
            <div class="flex-1 d-flex flex-column ga-1">
              <span
                class="text-caption text-medium-emphasis font-weight-bold"
                style="font-size: 11px"
                >العرض (Width)</span
              >
              <v-text-field
                v-model.number="selectedWidth"
                type="number"
                min="20"
                max="600"
                step="5"
                density="compact"
                variant="outlined"
                hide-details
                suffix="px"
                prepend-inner-icon="mdi-arrow-expand-horizontal"
                @update:model-value="onWidthInput"
              />
            </div>

            <!-- Aspect Ratio Link / Lock Toggle Button -->
            <div class="d-flex flex-column align-center justify-end pb-1">
              <v-btn
                :icon="lockRatio ? 'mdi-link' : 'mdi-link-off'"
                size="small"
                variant="tonal"
                :color="lockRatio ? 'primary' : 'grey-darken-1'"
                :title="lockRatio ? 'قفل تناسب الأبعاد مفعل' : 'تناسب الأبعاد حر'"
                @click="lockRatio = !lockRatio"
                class="mt-4"
              />
            </div>

            <!-- Height Input Field -->
            <div class="flex-1 d-flex flex-column ga-1">
              <span
                class="text-caption text-medium-emphasis font-weight-bold"
                style="font-size: 11px"
                >الارتفاع (Height)</span
              >
              <v-text-field
                v-model.number="selectedHeight"
                type="number"
                min="20"
                max="600"
                step="5"
                density="compact"
                variant="outlined"
                hide-details
                suffix="px"
                prepend-inner-icon="mdi-arrow-expand-vertical"
                @update:model-value="onHeightInput"
              />
            </div>
          </div>

          <!-- Quick Size Chips -->
          <div class="d-flex ga-2 mb-3">
            <v-chip
              v-for="preset in [50, 80, 120, 160, 220]"
              :key="preset"
              size="small"
              variant="outlined"
              :color="
                selectedWidth === preset && selectedHeight === preset
                  ? 'primary'
                  : undefined
              "
              @click="applySizePreset(preset)"
            >
              {{ preset }}px
            </v-chip>
          </div>

          <!-- Slider for Width -->
          <v-slider
            v-model="selectedWidth"
            min="20"
            max="350"
            step="5"
            color="primary"
            hide-details
            density="compact"
            class="mb-4"
            @update:model-value="onWidthInput"
          />

          <!-- Image Opacity Controls (شفافية الصورة) -->
          <div class="d-flex align-center justify-space-between mb-1 pt-2 border-t">
            <div class="d-flex align-center ga-1">
              <v-icon icon="mdi-opacity" size="16" color="primary" />
              <label class="hf-label font-weight-bold">شفافية الصورة (Opacity)</label>
            </div>
            <span class="text-caption font-weight-bold text-primary"
              >{{ selectedOpacity }}%</span
            >
          </div>

          <!-- Quick Opacity Chips -->
          <div class="d-flex ga-2 mb-3">
            <v-chip
              v-for="opPreset in [20, 40, 60, 80, 100]"
              :key="opPreset"
              size="small"
              variant="outlined"
              :color="selectedOpacity === opPreset ? 'primary' : undefined"
              @click="selectedOpacity = opPreset"
            >
              {{ opPreset }}%
            </v-chip>
          </div>

          <!-- Slider for Opacity -->
          <v-slider
            v-model="selectedOpacity"
            min="10"
            max="100"
            step="5"
            color="primary"
            hide-details
            density="compact"
            class="mb-4"
          />

          <!-- Image Object-Fit Controls (ملاءمة الصورة) -->
          <div class="d-flex align-center justify-space-between mb-2 pt-2 border-t">
            <div class="d-flex align-center ga-1">
              <v-icon icon="mdi-fit-to-page-outline" size="16" color="primary" />
              <label class="hf-label font-weight-bold">ملاءمة الصورة (Object-fit)</label>
            </div>
            <span class="text-caption font-weight-bold text-primary">{{
              selectedFit
            }}</span>
          </div>

          <div class="hf-fit-grid mb-2">
            <div
              v-for="fitItem in IMAGE_FITS"
              :key="fitItem.key"
              class="hf-fit-card"
              :class="{ active: selectedFit === fitItem.key }"
              @click="selectedFit = fitItem.key"
            >
              <v-icon
                :icon="fitItem.icon"
                size="20"
                :color="selectedFit === fitItem.key ? 'primary' : 'grey-darken-1'"
              />
              <span
                class="text-caption font-weight-bold"
                style="font-size: 11px !important"
                >{{ fitItem.label }}</span
              >
              <span
                class="text-caption text-medium-emphasis"
                style="font-size: 9px !important"
                >{{ fitItem.desc }}</span
              >
            </div>
          </div>
        </div>

        <!-- 4. Fixed Actions Footer -->
        <v-card-actions class="px-4 py-3 border-t bg-surface">
          <v-spacer />
          <v-btn variant="text" @click="imageDialog = false">إلغاء</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            class="px-6 rounded-lg font-weight-bold"
            @click="applyImageDialog"
          >
            تطبيق التعديلات
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { FONTS, FONT_SIZES, ALIGN_ICONS } from "../constants";
import {
  IMAGE_SHAPES,
  IMAGE_FITS,
  createChipHTML,
  templateToEditorHTML,
  editorHTMLToTemplate,
} from "../utils/chipUtils";

const props = defineProps({
  activeSection: {
    type: String,
    default: null,
  },
  activeCellIndex: {
    type: Number,
    default: null,
  },
  activeCell: {
    type: Object,
    default: null,
  },
  allVariables: {
    type: Array,
    default: () => [],
  },
  draggedVar: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(["close", "update-style", "update-content", "clear-content"]);

const richEditorRef = ref(null);
const isInternalUpdate = ref(false);
const savedRange = ref(null);
const selectedTextPreview = ref("");

// Dropdown UI states
const fontsMenuOpen = ref(false);
const sizeMenuOpen = ref(false);
const fontDropdownRef = ref(null);
const sizeDropdownRef = ref(null);

// Specific styles detected on the current selection (if any)
const selectedFontSize = ref(null);
const selectedFontFamily = ref(null);

// Local reactive fallback for instant whole-cell updates
const localFontSize = ref(null);
const localFontFamily = ref(null);

// Check if user currently has active selected text inside the editor
const hasSelectedText = () => {
  if (selectedTextPreview.value && selectedTextPreview.value.trim().length > 0)
    return true;
  if (savedRange.value) {
    try {
      const txt = savedRange.value.toString().trim();
      if (txt.length > 0) return true;
    } catch {}
  }
  return false;
};

// Base cell font size & family (does NOT jump when a word is selected)
const baseFontSize = computed(() => {
  if (localFontSize.value) return parseInt(localFontSize.value);
  return parseInt(props.activeCell?.style?.fontSize || 14);
});

const baseFontFamily = computed(() => {
  if (localFontFamily.value) return localFontFamily.value;
  return props.activeCell?.style?.fontFamily || "Tajawal";
});

// Current active font size for toolbar display
const currentFontSize = computed(() => {
  if (hasSelectedText() && selectedFontSize.value) {
    return parseInt(selectedFontSize.value);
  }
  return baseFontSize.value;
});

// Current active font family for toolbar display
const currentFontFamily = computed(() => {
  if (hasSelectedText() && selectedFontFamily.value) {
    return selectedFontFamily.value;
  }
  return baseFontFamily.value;
});

// Inspect the selected text node in DOM to detect its current fontSize & fontFamily
const detectSelectionStyles = (range) => {
  if (!range) return;
  let node = range.startContainer;
  let el = node.nodeType === 3 ? node.parentElement : node;
  if (el && richEditorRef.value?.contains(el)) {
    const computedStyle = window.getComputedStyle(el);

    // Detect font size
    const px = parseFloat(computedStyle.fontSize);
    if (!isNaN(px) && px > 0) {
      selectedFontSize.value = Math.round(px);
    }

    // Detect font family
    const family = computedStyle.fontFamily || "";
    const matched = FONTS.find((f) => family.toLowerCase().includes(f.toLowerCase()));
    if (matched) {
      selectedFontFamily.value = matched;
    } else {
      selectedFontFamily.value = props.activeCell?.style?.fontFamily || "Tajawal";
    }
  }
};

// Toggle Dropdown Menus
const toggleFontMenu = () => {
  fontsMenuOpen.value = !fontsMenuOpen.value;
  sizeMenuOpen.value = false;
};

const toggleSizeMenu = () => {
  sizeMenuOpen.value = !sizeMenuOpen.value;
  fontsMenuOpen.value = false;
};

// Close menus when clicking outside
const onDocumentClick = (e) => {
  if (fontDropdownRef.value && !fontDropdownRef.value.contains(e.target)) {
    fontsMenuOpen.value = false;
  }
  if (sizeDropdownRef.value && !sizeDropdownRef.value.contains(e.target)) {
    sizeMenuOpen.value = false;
  }
};

// Save selection range inside the editor
const saveSelection = () => {
  const sel = window.getSelection();
  if (!sel || sel.rangeCount === 0 || !richEditorRef.value) return;

  const range = sel.getRangeAt(0);
  const isInside =
    richEditorRef.value.contains(range.commonAncestorContainer) ||
    range.commonAncestorContainer === richEditorRef.value;

  if (isInside) {
    if (!range.collapsed) {
      const txt = range.toString().trim();
      if (txt.length > 0) {
        savedRange.value = range.cloneRange();
        selectedTextPreview.value = txt;
        detectSelectionStyles(range);
        return;
      }
    } else {
      // Clicked without drag or cursor collapsed: reset selection state
      savedRange.value = null;
      selectedTextPreview.value = "";
      selectedFontSize.value = null;
      selectedFontFamily.value = null;
    }
  }
};

const handleGlobalSelectionChange = () => {
  const sel = window.getSelection();
  if (!sel || sel.rangeCount === 0 || !richEditorRef.value) return;
  const range = sel.getRangeAt(0);
  const isInside =
    richEditorRef.value.contains(range.commonAncestorContainer) ||
    range.commonAncestorContainer === richEditorRef.value;

  if (isInside && !range.collapsed) {
    saveSelection();
  }
};

const clearSelection = () => {
  savedRange.value = null;
  selectedTextPreview.value = "";
  selectedFontSize.value = null;
  selectedFontFamily.value = null;
  const sel = window.getSelection();
  if (sel) sel.removeAllRanges();
};

// Convert Rich Editor DOM back to clean template string
const syncEditorToStore = () => {
  if (!richEditorRef.value) return;
  const rawText = editorHTMLToTemplate(richEditorRef.value);
  emit("update-content", rawText);
};

// Load active cell content into rich editor
const loadCellContentIntoEditor = () => {
  if (!richEditorRef.value || !props.activeCell) return;
  isInternalUpdate.value = true;
  richEditorRef.value.innerHTML = templateToEditorHTML(
    props.activeCell.content || "",
    props.allVariables
  );
  savedRange.value = null;
  selectedTextPreview.value = "";
  selectedFontSize.value = null;
  selectedFontFamily.value = null;
  localFontSize.value = null;
  localFontFamily.value = null;
  isInternalUpdate.value = false;
};

watch(
  () => [props.activeSection, props.activeCellIndex],
  () => {
    setTimeout(loadCellContentIntoEditor, 30);
  }
);

const onEditorKeyDown = (e) => {
  // If Enter is pressed, insert clean <br>
  if (e.key === "Enter") {
    e.preventDefault();
    const sel = window.getSelection();
    if (sel && sel.rangeCount > 0) {
      const range = sel.getRangeAt(0);
      range.deleteContents();
      const br = document.createElement("br");
      range.insertNode(br);
      const textNode = document.createTextNode("\u200B");
      if (br.nextSibling) {
        br.parentNode.insertBefore(textNode, br.nextSibling);
      } else {
        br.parentNode.appendChild(textNode);
      }
      range.setStart(textNode, 1);
      range.setEnd(textNode, 1);
      sel.removeAllRanges();
      sel.addRange(range);
      savedRange.value = null;
      selectedTextPreview.value = "";
      syncEditorToStore();
    }
    return;
  }

  // Handle typing characters (including space) at the end boundary of any styled span
  if (
    e.key &&
    !e.ctrlKey &&
    !e.metaKey &&
    !e.altKey &&
    ![
      "Shift",
      "Control",
      "Alt",
      "Meta",
      "CapsLock",
      "Escape",
      "ArrowLeft",
      "ArrowRight",
      "ArrowUp",
      "ArrowDown",
    ].includes(e.key)
  ) {
    const sel = window.getSelection();
    if (!sel || !sel.isCollapsed || !richEditorRef.value) return;

    let node = sel.anchorNode;
    let offset = sel.anchorOffset;
    if (!node) return;

    let spanEl =
      node.nodeType === 3 ? node.parentElement : node.tagName === "SPAN" ? node : null;

    if (
      spanEl &&
      spanEl.tagName === "SPAN" &&
      !spanEl.classList.contains("hf-canvas-chip") &&
      !spanEl.closest(".hf-canvas-chip") &&
      richEditorRef.value.contains(spanEl)
    ) {
      const isAtEnd =
        (node.nodeType === 3 &&
          offset >= node.textContent.length &&
          spanEl.lastChild === node) ||
        (node === spanEl && offset >= spanEl.childNodes.length);

      if (isAtEnd) {
        // ALWAYS ensure cursor is sitting in a clean text node OUTSIDE this styled span
        let next = spanEl.nextSibling;
        if (!next || next.nodeType !== 3) {
          next = document.createTextNode("");
          spanEl.parentNode.insertBefore(next, spanEl.nextSibling);
        }

        // Place cursor at the start of the next clean text node
        const newRange = document.createRange();
        newRange.setStart(next, 0);
        newRange.setEnd(next, 0);
        sel.removeAllRanges();
        sel.addRange(newRange);
        savedRange.value = null;
        selectedTextPreview.value = "";
        // Normal typing continues naturally in the plain text node
      }
    }
  }
};

const onEditorInput = () => {
  if (isInternalUpdate.value || !richEditorRef.value) return;
  saveSelection();
  syncEditorToStore();
};

// Robust In-Place DOM Range Styling (prevents nested spans)
const applyStyleToSelection = (styleProp, styleValue) => {
  if (!richEditorRef.value || !hasSelectedText()) return false;

  let range = savedRange.value;
  // If range was lost due to input focus, look up span matching selectedTextPreview
  if (!range || range.collapsed) {
    const spans = richEditorRef.value.querySelectorAll("span");
    for (const sp of spans) {
      if (
        !sp.classList.contains("hf-canvas-chip") &&
        !sp.closest(".hf-canvas-chip") &&
        sp.textContent.trim() === selectedTextPreview.value.trim()
      ) {
        const r = document.createRange();
        r.selectNodeContents(sp);
        range = r;
        savedRange.value = r;
        break;
      }
    }
  }

  if (!range) return false;
  const textContent = selectedTextPreview.value || range.toString();
  if (!textContent || textContent.trim().length === 0) return false;

  // Check if selection is already inside an existing editable styling SPAN
  let parentSpan = null;
  let container = range.commonAncestorContainer;
  let el = container.nodeType === 3 ? container.parentElement : container;

  if (
    el &&
    el.tagName === "SPAN" &&
    !el.classList.contains("hf-canvas-chip") &&
    !el.closest(".hf-canvas-chip") &&
    richEditorRef.value.contains(el)
  ) {
    if (el.textContent.trim() === textContent.trim()) {
      parentSpan = el;
    }
  }

  const kebabProp = styleProp.replace(/([A-Z])/g, "-$1").toLowerCase();

  if (parentSpan) {
    // Directly update existing span style with !important
    parentSpan.style.setProperty(kebabProp, styleValue, "important");
    const newRange = document.createRange();
    newRange.selectNodeContents(parentSpan);
    savedRange.value = newRange;
  } else {
    // Wrap selection with new span with !important
    const span = document.createElement("span");
    span.style.setProperty(kebabProp, styleValue, "important");

    try {
      range.surroundContents(span);
    } catch {
      const fragment = range.extractContents();
      span.appendChild(fragment);
      range.insertNode(span);
    }

    const newRange = document.createRange();
    newRange.selectNodeContents(span);
    savedRange.value = newRange;
  }

  // Always ensure a clean sibling text node exists after the styled span
  const targetEl =
    parentSpan || (savedRange.value ? savedRange.value.commonAncestorContainer : null);
  const actualSpan =
    targetEl && targetEl.nodeType === 3 ? targetEl.parentElement : targetEl;
  if (actualSpan && actualSpan.tagName === "SPAN" && actualSpan.parentNode) {
    let next = actualSpan.nextSibling;
    if (!next || next.nodeType !== 3) {
      next = document.createTextNode("");
      actualSpan.parentNode.insertBefore(next, actualSpan.nextSibling);
    }
  }

  syncEditorToStore();
  return true;
};

// Universal Font Size Application (Selection or Whole Cell)
const applyFontSize = (newSize) => {
  if (hasSelectedText()) {
    selectedFontSize.value = newSize;
    applyStyleToSelection("fontSize", `${newSize}px`);
  } else {
    localFontSize.value = newSize;
    emit("update-style", { key: "fontSize", value: String(newSize) });
    if (richEditorRef.value) {
      richEditorRef.value.style.setProperty("font-size", `${newSize}px`, "important");
      syncEditorToStore();
    }
  }
};

// Font Size Adjustment (+ / -)
const adjustFontSize = (delta) => {
  const cur = currentFontSize.value;
  const newSize = Math.max(8, Math.min(96, cur + delta * 2));
  applyFontSize(newSize);
};

// Quick Font Size Picker
const pickFontSize = (newSize) => {
  sizeMenuOpen.value = false;
  applyFontSize(newSize);
};

// Font Family Picker
const pickFont = (fontName) => {
  fontsMenuOpen.value = false;
  const fallback =
    fontName.includes("serif") || fontName.includes("sans")
      ? fontName
      : `'${fontName}', sans-serif`;

  if (hasSelectedText()) {
    selectedFontFamily.value = fontName;
    applyStyleToSelection("fontFamily", fallback);
  } else {
    localFontFamily.value = fontName;
    emit("update-style", { key: "fontFamily", value: fontName });
    if (richEditorRef.value) {
      richEditorRef.value.style.setProperty("font-family", fallback, "important");
      syncEditorToStore();
    }
  }
};

// Formatting Active State Helper
const isFormatActive = (command, styleKey, onVal) => {
  if (hasSelectedText() && savedRange.value) {
    try {
      let node = savedRange.value.startContainer;
      let el = node.nodeType === 3 ? node.parentElement : node;
      if (el && richEditorRef.value?.contains(el)) {
        const computedStyle = window.getComputedStyle(el);
        if (command === "bold")
          return (
            computedStyle.fontWeight === "bold" ||
            parseInt(computedStyle.fontWeight) >= 700
          );
        if (command === "italic") return computedStyle.fontStyle === "italic";
        if (command === "underline")
          return (
            computedStyle.textDecorationLine?.includes("underline") ||
            computedStyle.textDecoration?.includes("underline")
          );
      }
    } catch {}
  }
  return props.activeCell?.style?.[styleKey] === onVal;
};

const toggleFormatOnSelection = (formatType) => {
  if (!savedRange.value || savedRange.value.collapsed) return false;
  if (!richEditorRef.value) return false;

  const range = savedRange.value;
  const textContent = range.toString();
  if (!textContent || textContent.trim().length === 0) return false;

  let prop = "";
  let onVal = "";
  let offVal = "";
  if (formatType === "bold") {
    prop = "font-weight";
    onVal = "bold";
    offVal = "normal";
  } else if (formatType === "italic") {
    prop = "font-style";
    onVal = "italic";
    offVal = "normal";
  } else if (formatType === "underline") {
    prop = "text-decoration";
    onVal = "underline";
    offVal = "none";
  }

  let parentSpan = null;
  let container = range.commonAncestorContainer;
  let el = container.nodeType === 3 ? container.parentElement : container;
  if (
    el &&
    el.tagName === "SPAN" &&
    !el.classList.contains("hf-canvas-chip") &&
    !el.closest(".hf-canvas-chip") &&
    richEditorRef.value.contains(el)
  ) {
    if (el.textContent.trim() === textContent.trim()) {
      parentSpan = el;
    }
  }

  if (parentSpan) {
    const current = parentSpan.style.getPropertyValue(prop);
    parentSpan.style.setProperty(prop, current === onVal ? offVal : onVal, "important");
    const newRange = document.createRange();
    newRange.selectNodeContents(parentSpan);
    savedRange.value = newRange;
  } else {
    const span = document.createElement("span");
    span.style.setProperty(prop, onVal, "important");
    try {
      range.surroundContents(span);
    } catch {
      const fragment = range.extractContents();
      span.appendChild(fragment);
      range.insertNode(span);
    }
    const newRange = document.createRange();
    newRange.selectNodeContents(span);
    savedRange.value = newRange;
  }

  const targetEl = parentSpan || span;
  if (targetEl && targetEl.parentNode) {
    let next = targetEl.nextSibling;
    if (!next || next.nodeType !== 3) {
      next = document.createTextNode("");
      targetEl.parentNode.insertBefore(next, targetEl.nextSibling);
    }
  }

  const sel = window.getSelection();
  if (sel && savedRange.value) {
    sel.removeAllRanges();
    sel.addRange(savedRange.value);
  }

  syncEditorToStore();
  return true;
};

const applyFormat = (command, styleKey, onVal, offVal) => {
  if (hasSelectedText()) {
    toggleFormatOnSelection(command);
  } else {
    const current = props.activeCell?.style?.[styleKey];
    const nextVal = current === onVal ? offVal : onVal;
    emit("update-style", { key: styleKey, value: nextVal });
    if (richEditorRef.value) {
      const kebab = styleKey.replace(/([A-Z])/g, "-$1").toLowerCase();
      richEditorRef.value.style.setProperty(kebab, nextVal, "important");
      syncEditorToStore();
    }
  }
};

// Text Color
const applyTextColor = (color) => {
  if (hasSelectedText()) {
    applyStyleToSelection("color", color);
  } else {
    emit("update-style", { key: "color", value: color });
    if (richEditorRef.value) {
      richEditorRef.value.style.setProperty("color", color, "important");
      syncEditorToStore();
    }
  }
};

// Image Template Dialog State
const imageDialog = ref(false);
const editingImageBox = ref(null);
const selectedShape = ref("default");
const selectedWidth = ref(80);
const selectedHeight = ref(80);
const lockRatio = ref(true);
const selectedOpacity = ref(100);
const selectedFit = ref("contain");
const previewImgSrc = ref("");
const previewLabel = ref("");

const onWidthInput = (val) => {
  const num = parseInt(val) || 20;
  if (lockRatio.value) {
    selectedHeight.value = num;
  }
};

const onHeightInput = (val) => {
  const num = parseInt(val) || 20;
  if (lockRatio.value) {
    selectedWidth.value = num;
  }
};

const applySizePreset = (preset) => {
  selectedWidth.value = preset;
  if (lockRatio.value) {
    selectedHeight.value = preset;
  }
};

const openImageDialog = (chipEl) => {
  editingImageBox.value = chipEl;
  selectedShape.value = chipEl.getAttribute("data-shape") || "default";
  selectedWidth.value = parseInt(chipEl.getAttribute("data-width")) || 80;
  selectedHeight.value =
    parseInt(chipEl.getAttribute("data-height")) || selectedWidth.value;
  selectedOpacity.value = parseInt(chipEl.getAttribute("data-opacity")) || 100;
  selectedFit.value = chipEl.getAttribute("data-fit") || "contain";
  previewImgSrc.value =
    chipEl.getAttribute("data-img") || chipEl.querySelector("img")?.src || "";
  previewLabel.value =
    chipEl.querySelector(".hf-canvas-chip-label")?.textContent || "صورة";
  imageDialog.value = true;
};

const applyImageDialog = () => {
  if (editingImageBox.value) {
    editingImageBox.value.setAttribute("data-shape", selectedShape.value);
    editingImageBox.value.setAttribute("data-width", String(selectedWidth.value));
    editingImageBox.value.setAttribute("data-height", String(selectedHeight.value));
    editingImageBox.value.setAttribute("data-opacity", String(selectedOpacity.value));
    editingImageBox.value.setAttribute("data-fit", selectedFit.value);

    // Update or create size tag badge on the chip
    let sizeTag = editingImageBox.value.querySelector(".hf-chip-size-tag");
    const dimText =
      selectedWidth.value === selectedHeight.value
        ? `${selectedWidth.value}px`
        : `${selectedWidth.value}×${selectedHeight.value}px`;
    if (
      selectedWidth.value !== 80 ||
      selectedHeight.value !== 80 ||
      selectedShape.value !== "default" ||
      selectedOpacity.value !== 100 ||
      selectedFit.value !== "contain"
    ) {
      if (!sizeTag) {
        sizeTag = document.createElement("span");
        sizeTag.className = "hf-chip-size-tag";
        const editBtn = editingImageBox.value.querySelector(".hf-canvas-chip-edit");
        if (editBtn) editingImageBox.value.insertBefore(sizeTag, editBtn);
        else editingImageBox.value.appendChild(sizeTag);
      }
      sizeTag.textContent =
        selectedOpacity.value < 100 ? `${dimText} / ${selectedOpacity.value}%` : dimText;
    } else if (sizeTag) {
      sizeTag.remove();
    }

    // Apply opacity and fit preview on the thumbnail inside the chip
    const thumbImg = editingImageBox.value.querySelector("img.hf-canvas-chip-thumb");
    if (thumbImg) {
      thumbImg.style.opacity = selectedOpacity.value / 100;
      thumbImg.style.objectFit = selectedFit.value;
    }

    syncEditorToStore();
  }
  imageDialog.value = false;
};

const onEditorMouseDown = () => {
  // Let default editor selection run naturally
};

const onEditorClick = (e) => {
  // 1. Edit image template button clicked
  const editBtn =
    e.target.closest(".hf-canvas-chip-edit") || e.target.closest(".hf-image-edit-btn");
  if (editBtn) {
    e.preventDefault();
    e.stopPropagation();
    const chip =
      editBtn.closest(".hf-canvas-chip") || editBtn.closest(".hf-resizable-image");
    if (chip) {
      openImageDialog(chip);
    }
    return;
  }

  // 2. Delete chip button clicked
  const delBtn =
    e.target.closest(".hf-canvas-chip-remove") ||
    e.target.closest(".hf-chip-del") ||
    e.target.closest(".hf-image-del-btn");
  if (delBtn) {
    e.preventDefault();
    e.stopPropagation();
    const chip =
      delBtn.closest(".hf-canvas-chip") ||
      delBtn.closest(".hf-editor-chip") ||
      delBtn.closest(".hf-resizable-image");
    if (chip) {
      chip.remove();
      savedRange.value = null;
      selectedTextPreview.value = "";
      selectedFontSize.value = null;
      selectedFontFamily.value = null;
      syncEditorToStore();
    }
    return;
  }

  setTimeout(() => {
    const sel = window.getSelection();
    if (sel && sel.isCollapsed) {
      savedRange.value = null;
      selectedTextPreview.value = "";
      selectedFontSize.value = null;
      selectedFontFamily.value = null;
    }
  }, 120);
};

const insertChipAtSelection = (chipHTML) => {
  if (!richEditorRef.value) return;
  richEditorRef.value.focus();
  const sel = window.getSelection();
  if (sel.rangeCount && richEditorRef.value.contains(sel.getRangeAt(0).startContainer)) {
    const range = sel.getRangeAt(0);
    range.deleteContents();
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = chipHTML;
    const frag = document.createDocumentFragment();
    let node;
    let lastNode;
    while ((node = tempDiv.firstChild)) {
      lastNode = frag.appendChild(node);
    }
    range.insertNode(frag);
    if (lastNode) {
      range.setStartAfter(lastNode);
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);
    }
  } else {
    richEditorRef.value.insertAdjacentHTML("beforeend", chipHTML);
  }
};

const insertVariable = (varKey) => {
  const chipHTML = createChipHTML(varKey, props.allVariables, true);
  insertChipAtSelection(chipHTML);
  syncEditorToStore();
};

const onEditorDragOver = (e) => {
  e.preventDefault();
  if (e.dataTransfer) {
    e.dataTransfer.dropEffect = "copy";
  }
};

const onDropToEditor = (e) => {
  e.preventDefault();
  e.stopPropagation();
  const varKey =
    e.dataTransfer?.getData("text/plain") ||
    e.dataTransfer?.getData("text") ||
    props.draggedVar ||
    (typeof window !== "undefined" ? window.__hfDraggedVar : null);
  if (!varKey) return;

  let dropRange = null;
  if (document.caretRangeFromPoint) {
    dropRange = document.caretRangeFromPoint(e.clientX, e.clientY);
  } else if (document.caretPositionFromPoint) {
    const pos = document.caretPositionFromPoint(e.clientX, e.clientY);
    if (pos) {
      dropRange = document.createRange();
      dropRange.setStart(pos.offsetNode, pos.offset);
      dropRange.collapse(true);
    }
  }

  const chipHTML = createChipHTML(varKey, props.allVariables, true);

  if (
    dropRange &&
    richEditorRef.value &&
    richEditorRef.value.contains(dropRange.startContainer)
  ) {
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = chipHTML;
    const frag = document.createDocumentFragment();
    let node;
    let lastNode;
    while ((node = tempDiv.firstChild)) {
      lastNode = frag.appendChild(node);
    }
    dropRange.deleteContents();
    dropRange.insertNode(frag);
    if (lastNode) {
      dropRange.setStartAfter(lastNode);
      dropRange.collapse(true);
      const sel = window.getSelection();
      if (sel) {
        sel.removeAllRanges();
        sel.addRange(dropRange);
      }
    }
  } else {
    insertChipAtSelection(chipHTML);
  }

  syncEditorToStore();
};

const clearCell = () => {
  emit("clear-content");
  if (richEditorRef.value) {
    richEditorRef.value.innerHTML = "";
  }
  savedRange.value = null;
  selectedTextPreview.value = "";
  selectedFontSize.value = null;
  selectedFontFamily.value = null;
  localFontSize.value = null;
  localFontFamily.value = null;
};

onMounted(() => {
  document.addEventListener("selectionchange", handleGlobalSelectionChange);
  document.addEventListener("click", onDocumentClick);
  setTimeout(loadCellContentIntoEditor, 80);
});

onBeforeUnmount(() => {
  document.removeEventListener("selectionchange", handleGlobalSelectionChange);
  document.removeEventListener("click", onDocumentClick);
});

defineExpose({
  insertVariable,
  loadCellContentIntoEditor,
});
</script>
