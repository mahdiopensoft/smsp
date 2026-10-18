<template>
  <div class="hf-sidebar-left">
    <!-- Main Two Tabs Switcher: المتغيرات vs خيارات القسم -->
    <div class="hf-sidebar-main-tabs">
      <button
        type="button"
        class="hf-sidebar-main-tab-btn"
        :class="{ active: activeMainTab === 'variables' }"
        @click="activeMainTab = 'variables'"
      >
        <v-icon icon="mdi-variable" size="14" class="me-1" />
        <span>المتغيرات</span>
      </button>

      <button
        type="button"
        class="hf-sidebar-main-tab-btn"
        :class="{ active: activeMainTab === 'options' }"
        @click="activeMainTab = 'options'"
      >
        <v-icon icon="mdi-tune-variant" size="14" class="me-1" />
        <span>خيارات القسم</span>
      </button>
    </div>

    <!-- TAB 1: المتغيرات المتاحة -->
    <div v-if="activeMainTab === 'variables'" class="hf-sidebar-tab-content">
      <!-- Sub-Tabs: Static vs API -->
      <div class="hf-var-tabs mb-2">
        <button
          class="hf-var-tab-btn"
          :class="{ active: varTab === 'static' }"
          @click="varTab = 'static'"
        >
          <v-icon icon="mdi-code-tags" size="13" class="me-1" />
          <span>ثابتة</span>
          <span class="hf-badge-count">{{ staticVariables.length }}</span>
        </button>

        <button
          class="hf-var-tab-btn"
          :class="{ active: varTab === 'api' }"
          @click="varTab = 'api'"
        >
          <v-icon icon="mdi-cloud-outline" size="13" class="me-1" />
          <span>متغيرات API</span>
          <span class="hf-badge-count">{{ apiVariables.length }}</span>
        </button>
      </div>

      <!-- Search Box for Variables -->
      <div class="hf-search-wrapper mb-2">
        <v-icon icon="mdi-magnify" size="14" class="hf-search-icon" />
        <input
          type="text"
          v-model="varSearch"
          class="hf-search-input"
          placeholder="بحث في المتغيرات..."
        />
        <v-icon
          v-if="varSearch"
          icon="mdi-close-circle"
          size="13"
          class="hf-search-clear"
          @click="varSearch = ''"
        />
        <v-btn
          v-if="varTab === 'api'"
          icon="mdi-refresh"
          size="small"
          variant="text"
          @click="emit('fetch-api')"
          class="ml-2 ms-2"
        />
      </div>

      <!-- API Status Banner -->
      <div
        v-if="varTab === 'api' && apiLoading"
        class="hf-api-status-banner mb-2 loading"
      >
        <v-progress-circular
          indeterminate
          size="14"
          width="2"
          color="primary"
          class="me-1"
        />
        <span>جاري جلب المتغيرات من API...</span>
      </div>
      <div
        v-else-if="varTab === 'api' && apiError"
        class="hf-api-status-banner mb-2 warning"
      >
        <v-icon icon="mdi-alert-circle-outline" size="14" color="red" class="me-1" />
        <span>{{ apiError }}</span>
        <v-btn size="small" variant="text" @click="emit('fetch-api')" class="ml-2"
          >إعادة جلب</v-btn
        >
      </div>

      <!-- Variables List -->
      <div class="hf-vars-list">
        <div
          v-for="varItem in currentTabVariables"
          :key="varItem.name_code || varItem.key"
          class="hf-var-chip"
          :class="{ 'hf-var-chip--image': !!varItem.image }"
          :draggable="true"
          @dragstart="onDragStart($event, getVarToken(varItem))"
          @dragend="onDragEnd"
          @click="onChipClick(getVarToken(varItem))"
          :title="`انقر أو اسحب لإدراج ${varItem.name_ar || varItem.label} (${
            varItem.image ? 'صورة' : 'نص'
          })`"
        >
          <!-- Image thumbnail or Icon -->
          <div class="hf-var-icon-box" :class="{ 'is-image': !!varItem.image }">
            <img
              v-if="varItem.image"
              :src="varItem.image"
              class="hf-var-thumbnail"
              alt="preview"
            />
            <v-icon
              v-else
              :icon="varItem.icon || 'mdi-variable'"
              size="14"
              :color="varItem.color || 'primary'"
            />
          </div>

          <div class="hf-var-info">
            <div class="d-flex align-center ga-1">
              <span class="hf-var-label">{{ varItem.name_ar || varItem.label }}</span>
              <span v-if="varItem.image" class="hf-image-tag">صورة</span>
            </div>
            <span
              class="text-caption text-medium-emphasis font-mono"
              style="font-size: 10px"
            >
              {{ getVarToken(varItem) }}
            </span>
          </div>

          <v-icon icon="mdi-drag" size="14" class="hf-drag-handle" />
        </div>

        <!-- Empty search state -->
        <div
          v-if="currentTabVariables.length === 0"
          class="text-center pa-4 text-caption text-medium-emphasis"
        >
          <v-icon
            icon="mdi-magnify-remove-outline"
            size="24"
            class="mb-1 d-block mx-auto opacity-50"
          />
          لا توجد متغيرات مطابقة
        </div>
      </div>
    </div>

    <!-- TAB 2: خيارات وتنسيق القسم -->
    <div
      v-else-if="activeMainTab === 'options' && activeTemplate"
      class="hf-sidebar-tab-content"
    >
      <div class="hf-section-tabs mb-3">
        <button
          class="hf-section-tab"
          :class="{ active: sectionTab === 'header' }"
          @click="$emit('update:sectionTab', 'header')"
        >
          <v-icon icon="mdi-page-layout-header" size="14" class="me-1" />
          الهيدر
        </button>
        <button
          class="hf-section-tab"
          :class="{ active: sectionTab === 'footer' }"
          @click="$emit('update:sectionTab', 'footer')"
        >
          <v-icon icon="mdi-page-layout-footer" size="14" class="me-1" />
          الفوتر
        </button>
      </div>

      <div class="hf-section-options">
        <!-- Columns Count -->
        <label class="hf-label">عدد الأعمدة</label>
        <div class="hf-col-picker mb-3">
          <button
            v-for="n in 5"
            :key="n"
            class="hf-col-btn"
            :class="{ active: activeTemplate[sectionTab]?.columns === n }"
            @click="$emit('change-columns', n)"
          >
            {{ n }}
          </button>
        </div>

        <!-- Background Color -->
        <label class="hf-label mt-2">لون الخلفية</label>
        <div class="d-flex align-center ga-2 mb-3">
          <input
            type="color"
            class="hf-color-input"
            :value="activeTemplate[sectionTab]?.backgroundColor"
            @input="
              $emit(
                'update-section-style',
                sectionTab,
                'backgroundColor',
                $event.target.value
              )
            "
          />
          <span class="text-caption text-medium-emphasis font-weight-bold">
            {{ activeTemplate[sectionTab]?.backgroundColor }}
          </span>
        </div>

        <!-- Height -->
        <label class="hf-label mt-2">الارتفاع (px)</label>
        <v-slider
          :model-value="Number(activeTemplate[sectionTab]?.height || 60)"
          @update:model-value="
            $emit('update-section-style', sectionTab, 'height', String($event))
          "
          min="30"
          max="150"
          step="5"
          color="primary"
          hide-details
          density="compact"
        >
          <template #append>
            <span class="text-caption font-weight-bold"
              >{{ activeTemplate[sectionTab]?.height }}px</span
            >
          </template>
        </v-slider>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  activeTemplate: {
    type: Object,
    default: null,
  },
  staticVariables: {
    type: Array,
    default: () => [],
  },
  apiVariables: {
    type: Array,
    default: () => [],
  },
  apiLoading: {
    type: Boolean,
    default: false,
  },
  apiError: {
    type: String,
    default: null,
  },
  sectionTab: {
    type: String,
    default: "header",
  },
});

const emit = defineEmits([
  "update:sectionTab",
  "insert-var",
  "drag-start",
  "drop-to-cell",
  "change-columns",
  "update-section-style",
  "fetch-api",
]);

const activeMainTab = ref("variables");
const varTab = ref("static");
const varSearch = ref("");

const getVarToken = (v) => {
  if (!v) return "";
  if (v.name_code) {
    const clean = String(v.name_code).replace(/[{}]/g, "").trim();
    return `{{${clean}}}`;
  }
  return v.key || "";
};

const currentTabVariables = computed(() => {
  const list = varTab.value === "static" ? props.staticVariables : props.apiVariables;
  if (!varSearch.value.trim()) return list;
  const q = varSearch.value.toLowerCase().trim();
  return list.filter(
    (v) =>
      (v.name_ar && v.name_ar.toLowerCase().includes(q)) ||
      (v.name_en && v.name_en.toLowerCase().includes(q)) ||
      (v.name_code && v.name_code.toLowerCase().includes(q)) ||
      (v.value_ar && String(v.value_ar).toLowerCase().includes(q)) ||
      (v.value_en && String(v.value_en).toLowerCase().includes(q)) ||
      (v.label && v.label.toLowerCase().includes(q)) ||
      (v.key && v.key.toLowerCase().includes(q)) ||
      (v.value && String(v.value).toLowerCase().includes(q))
  );
});

let isDragging = false;

// Native HTML5 DragStart
const onDragStart = (e, varKey) => {
  isDragging = true;
  emit("drag-start", varKey);
  if (typeof window !== "undefined") {
    window.__hfDraggedVar = varKey;
  }
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = "copy";
    e.dataTransfer.setData("text/plain", varKey);
  }
};

const onDragEnd = () => {
  setTimeout(() => {
    isDragging = false;
    if (typeof window !== "undefined") {
      window.__hfDraggedVar = null;
    }
  }, 350);
};

const onChipClick = (varKey) => {
  if (!isDragging) {
    emit("insert-var", varKey);
  }
};
</script>
