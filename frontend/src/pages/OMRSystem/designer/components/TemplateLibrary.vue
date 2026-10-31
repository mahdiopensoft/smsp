<template>
  <div class="template-library">
    <!-- ── Filters Bar (Exact same layout & standard as students-master) ───────── -->
    <TemplateFilters
      v-model:search-query="searchQuery"
      v-model:filter-category="filterCategory"
      v-model:filter-questions="filterQuestions"
      v-model:filter-active="filterActive"
      :category-options="categoryOptions"
      :question-count-options="questionCountOptions"
      :active-options="activeOptions"
      @apply="applyFilters"
      @reset="resetFilters"
    />

    <!-- ── View Switcher & Action Header ────────────────────────── -->
    <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
      <div class="d-flex align-center gap-2">
        <v-btn-toggle
          v-model="viewMode"
          mandatory
          density="compact"
          color="primary"
          rounded="lg"
          variant="outlined"
        >
          <v-btn value="table" class="font-weight-bold px-4">
            <v-icon start size="18">mdi-table</v-icon>
            عرض الجدول (نظام القوائم)
          </v-btn>
          <v-btn value="cards" class="font-weight-bold px-4">
            <v-icon start size="18">mdi-view-grid-outline</v-icon>
            عرض البطاقات المعمارية
          </v-btn>
        </v-btn-toggle>
      </div>

      <div class="d-flex align-center gap-2">
        <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
          <v-icon start size="14">mdi-file-document-check-outline</v-icon>
          إجمالي القوالب: {{ templates.length }}
        </v-chip>
        <v-btn
          color="primary"
          rounded="lg"
          class="font-weight-bold px-4"
          prepend-icon="mdi-plus"
          @click="emit('create-new')"
        >
          تصميم قالب جديد
        </v-btn>
      </div>
    </div>

    <!-- ── Loading State ─────────────────────────────────────────── -->
    <div v-if="isLoading" class="py-16 text-center">
      <v-progress-circular indeterminate color="primary" size="48" width="4" />
      <div class="text-subtitle-1 font-weight-bold text-medium-emphasis mt-4">
        جاري مزامنة وجلب القوالب المعتمدة من الخادم...
      </div>
    </div>

    <!-- ── Empty State ───────────────────────────────────────────── -->
    <v-card v-else-if="filteredTemplates.length === 0" class="main-card pa-12 rounded-2xl text-center border elevation-0 mb-6">
      <v-avatar color="primary" variant="tonal" size="72" rounded="2xl" class="mb-4">
        <v-icon size="36">mdi-folder-open-outline</v-icon>
      </v-avatar>
      <h3 class="text-h6 font-weight-black mb-2">لا توجد قوالب تطابق شروط التصفية</h3>
      <p class="text-caption text-medium-emphasis mb-6">
        لم يتم العثور على أي قوالب تطابق معايير البحث أو خيارات التصفية المحددة حالياً.
      </p>
      <div class="d-flex justify-center gap-3">
        <v-btn variant="tonal" color="secondary" rounded="lg" class="font-weight-bold" @click="resetFilters">
          إعادة تعيين الفلاتر
        </v-btn>
        <v-btn color="primary" rounded="lg" prepend-icon="mdi-plus" class="font-weight-bold" @click="emit('create-new')">
          إنشاء قالب جديد
        </v-btn>
      </div>
    </v-card>

    <!-- ── 1. TABLE VIEW ─────────────────────────────────────────── -->
    <div v-else-if="viewMode === 'table'">
      <TemplateTable
        :table-items="tableItems"
        :headers="headers"
        :get-data="getData"
        :get-category-color="getCategoryColor"
        :get-category-icon="getCategoryIcon"
        :get-category-label="getCategoryLabel"
        :get-questions-count="getQuestionsCount"
        :get-columns-count="getColumnsCount"
        :get-choices-count="getChoicesCount"
        :get-paper-size="getPaperSize"
        @create-new="emit('create-new')"
        @edit="emit('edit', $event)"
        @scan="emit('scan', $event)"
        @preview="emit('preview', $event)"
        @duplicate="emit('duplicate', $event)"
        @print="emit('print', $event)"
        @confirm-delete="confirmDeleteTemplate"
      />
    </div>

    <!-- ── 2. CARDS GRID VIEW ────────────────────────────────────── -->
    <v-row v-else-if="viewMode === 'cards'">
      <v-col
        v-for="template in filteredTemplates"
        :key="template.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <TemplateCard
          :template="template"
          @edit="emit('edit', $event)"
          @scan="emit('scan', $event)"
          @preview="emit('preview', $event)"
          @duplicate="emit('duplicate', $event)"
          @print="emit('print', $event)"
          @delete="confirmDeleteTemplate($event)"
        />
      </v-col>
    </v-row>

    <!-- ── Delete Confirmation Dialog ────────────────────────────── -->
    <TemplateDeleteDialog
      v-model="showDeleteDialog"
      :template-to-delete="templateToDelete"
      :is-deleting="isDeleting"
      @confirm="executeDelete"
    />
  </div>
</template>

<script setup lang="ts">
import TemplateCard from './TemplateCard.vue'
import TemplateFilters from './library/TemplateFilters.vue'
import TemplateTable from './library/TemplateTable.vue'
import TemplateDeleteDialog from './library/TemplateDeleteDialog.vue'
import { useTemplateLibrary } from '../composables/useTemplateLibrary'

const props = defineProps<{
  templates: any[]
  isLoading?: boolean
}>()

const emit = defineEmits<{
  (e: 'create-new'): void
  (e: 'edit', t: any): void
  (e: 'scan', id: number | string): void
  (e: 'preview', t: any): void
  (e: 'duplicate', t: any): void
  (e: 'print', t: any): void
  (e: 'delete', id: number | string): void
}>()

const {
  viewMode,
  searchQuery,
  filterCategory,
  filterQuestions,
  filterActive,
  showDeleteDialog,
  templateToDelete,
  isDeleting,
  categoryOptions,
  questionCountOptions,
  activeOptions,
  headers,
  filteredTemplates,
  tableItems,
  getData,
  applyFilters,
  resetFilters,
  getQuestionsCount,
  getColumnsCount,
  getChoicesCount,
  getPaperSize,
  getCategoryLabel,
  getCategoryColor,
  getCategoryIcon,
  confirmDeleteTemplate,
} = useTemplateLibrary(props)

async function executeDelete() {
  if (!templateToDelete.value) return
  isDeleting.value = true
  try {
    emit('delete', templateToDelete.value.id)
    showDeleteDialog.value = false
    templateToDelete.value = null
  } finally {
    isDeleting.value = false
  }
}
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.02);
}
</style>
