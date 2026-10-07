<template>
  <div class="template-library">
    <!-- ── Filters Bar (Exact same layout & standard as /levels) ───────── -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- 1. Search Query Input -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            label="اسم القالب أو المادة"
            placeholder="بحث باسم القالب أو المادة..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- 2. Category / Organization Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterCategory"
            :items="categoryOptions"
            item-title="text"
            item-value="value"
            label="نوع القالب / المؤسسة"
            prepend-inner-icon="mdi-domain"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- 3. Question Count Capacity Filter -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterQuestions"
            :items="questionCountOptions"
            item-title="text"
            item-value="value"
            label="سعة الأسئلة"
            prepend-inner-icon="mdi-help-circle-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- 4. Active Status Filter (Exact same as /levels) -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterActive"
            :items="activeOptions"
            item-title="text"
            item-value="value"
            label="حالة التفعيل"
            prepend-inner-icon="mdi-check-circle-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- 5. Filter Action Buttons (Exact same as /levels) -->
        <v-col cols="12" sm="6" md="2" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

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

    <!-- ── 1. TABLE VIEW (Exact custom-data-table as /levels) ─────── -->
    <div v-else-if="viewMode === 'table'">
      <custom-data-table
        v-bind="{
          items: tableItems,
          getData,
          headers,
          editItem: (item) => emit('edit', item),
          create: () => emit('create-new'),
        }"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Template Name and Subtitle -->
          <template v-if="key === 'name'">
            <div class="d-flex align-center gap-3 py-1">
              <v-avatar size="36" color="primary" variant="tonal" class="rounded-lg">
                <v-icon size="20">mdi-file-document-edit-outline</v-icon>
              </v-avatar>
              <div>
                <div class="font-weight-black text-body-2 text-primary">{{ item.name }}</div>
                <div class="text-caption text-medium-emphasis">{{ item.description || 'قالب تصحيح آلي عالي الدقة 300 DPI' }}</div>
              </div>
            </div>
          </template>

          <!-- Category / Organization -->
          <template v-else-if="key === 'category'">
            <v-chip
              size="small"
              :color="getCategoryColor(item)"
              variant="tonal"
              class="font-weight-bold"
            >
              <v-icon start size="14">{{ getCategoryIcon(item) }}</v-icon>
              {{ getCategoryLabel(item) }}
            </v-chip>
          </template>

          <!-- Questions Count -->
          <template v-else-if="key === 'total_mcq'">
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
              <v-icon start size="14">mdi-help-circle-outline</v-icon>
              {{ getQuestionsCount(item) }} سؤال
            </v-chip>
          </template>

          <!-- Columns & Layout -->
          <template v-else-if="key === 'layout'">
            <v-chip size="small" color="info" variant="tonal" class="font-weight-bold">
              <v-icon start size="14">mdi-view-column-outline</v-icon>
              {{ getColumnsCount(item) }} أعمدة ({{ getChoicesCount(item) }} خيارات)
            </v-chip>
          </template>

          <!-- Paper Size -->
          <template v-else-if="key === 'paper_size'">
            <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
              <v-icon start size="14">mdi-file-outline</v-icon>
              {{ getPaperSize(item) }}
            </v-chip>
          </template>

          <!-- Version -->
          <template v-else-if="key === 'version'">
            <v-chip size="small" color="grey-darken-2" variant="tonal" class="font-weight-bold">
              v{{ item.version || '1.0' }}
            </v-chip>
          </template>

          <!-- Is Active Status (Exact same as /levels) -->
          <template v-else-if="key === 'is_active'">
            <v-chip
              size="small"
              :color="item.is_active !== false ? 'success' : 'error'"
              variant="tonal"
              class="font-weight-bold text-white"
            >
              <v-icon start size="14">{{ item.is_active !== false ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
              {{ item.is_active !== false ? 'مفعل' : 'معطل' }}
            </v-chip>
          </template>

          <!-- Custom Actions Bar -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                is-icon
                icon="scanner"
                color="success"
                label="بدء التصحيح الضوئي بهذا القالب"
                :click="() => emit('scan', item.id)"
              />
              <custom-btn
                type="show"
                is-icon
                label="معاينة الورقة"
                :click="() => emit('preview', item)"
              />
              <custom-btn
                type="update"
                is-icon
                label="تعديل القالب"
                :click="() => emit('edit', item)"
              />
              <custom-btn
                is-icon
                icon="printer"
                color="secondary"
                label="طباعة القالب"
                :click="() => emit('print', item)"
              />
              <custom-btn
                is-icon
                icon="content-copy"
                color="info"
                label="نسخ كقالب جديد"
                :click="() => emit('duplicate', item)"
              />
              <custom-btn
                type="del"
                is-icon
                label="حذف القالب"
                :click="() => confirmDeleteTemplate(item)"
              />
            </div>
          </template>
        </template>
      </custom-data-table>
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
    <v-dialog v-model="showDeleteDialog" max-width="480">
      <v-card class="pa-6 rounded-2xl">
        <div class="d-flex align-center gap-3 mb-4">
          <v-avatar color="error" variant="tonal" size="48" rounded="xl">
            <v-icon size="28" color="error">mdi-alert-outline</v-icon>
          </v-avatar>
          <div>
            <h3 class="text-h6 font-weight-black mb-0">تأكيد حذف القالب</h3>
            <span class="text-caption text-medium-emphasis">عملية الحذف نهائية ولا يمكن التراجع عنها</span>
          </div>
        </div>
        <p class="text-body-2 mb-6">
          هل أنت متأكد من رغبتك في حذف القالب المعياري
          <strong class="text-error">«{{ templateToDelete?.name }}»</strong>؟
        </p>
        <div class="d-flex justify-end gap-2">
          <v-btn variant="text" rounded="lg" class="font-weight-bold" @click="showDeleteDialog = false">
            إلغاء
          </v-btn>
          <v-btn
            color="error"
            rounded="lg"
            class="font-weight-bold px-6"
            :loading="isDeleting"
            @click="executeDelete"
          >
            نعم، احذف القالب
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import TemplateCard from './TemplateCard.vue'

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

// View mode: 'table' (default, matches /levels) or 'cards'
const viewMode = ref<'table' | 'cards'>('table')

// Filters states (matching /levels)
const searchQuery = ref('')
const filterCategory = ref('all')
const filterQuestions = ref('all')
const filterActive = ref<boolean | null>(null)

// Dialog states
const showDeleteDialog = ref(false)
const templateToDelete = ref<any>(null)
const isDeleting = ref(false)

// Select options
const categoryOptions = [
  { text: 'كافة الأنواع (الكل)', value: 'all' },
  { text: 'وزارة التربية والتعليم', value: 'ministry' },
  { text: 'الجامعات والتعليم العالي', value: 'university' },
  { text: 'قوالب مخصصة', value: 'custom' },
]

const questionCountOptions = [
  { text: 'كافة السعات', value: 'all' },
  { text: '20 سؤال (سريع)', value: 20 },
  { text: '40 سؤال (معياري)', value: 40 },
  { text: '50 سؤال (وزاري رسمي)', value: 50 },
  { text: '60 سؤال (فصلي)', value: 60 },
  { text: '100 سؤال (نصف سنوي)', value: 100 },
  { text: '180 سؤال (جامعي شامل)', value: 180 },
]

const activeOptions = [
  { text: 'مفعل', value: true },
  { text: 'غير مفعل', value: false },
]

// Table Headers (Standard /levels specification)
const headers = computed(() => [
  { title: 'اسم القالب والنموذج', key: 'name', sortable: true },
  { title: 'نوع القالب / المؤسسة', key: 'category', sortable: true },
  { title: 'عدد الأسئلة', key: 'total_mcq', sortable: true, align: 'center' },
  { title: 'التخطيط (أعمدة / خيارات)', key: 'layout', sortable: false, align: 'center' },
  { title: 'المقاس', key: 'paper_size', sortable: false, align: 'center' },
  { title: 'الإصدار', key: 'version', sortable: true, align: 'center' },
  { title: 'الحالة', key: 'is_active', sortable: true, align: 'center' },
])

// Filtered templates list
const filteredTemplates = computed(() => {
  let list = props.templates || []

  // 1. Category filter
  if (filterCategory.value === 'ministry') {
    list = list.filter(t => {
      const name = t.name || ''
      const tid = t.template_data?.template_id || ''
      const q = getQuestionsCount(t)
      return name.includes('وزارة التربية') || name.includes('الثانوية العامة') || tid === 'YEMEN_MINISTRY_50' || tid.includes('YEMEN_MINISTRY') || q === 50
    })
  } else if (filterCategory.value === 'university') {
    list = list.filter(t => {
      const q = getQuestionsCount(t)
      return q === 180 || t.name?.includes('الجامعات') || t.name?.includes('التعليم العالي')
    })
  } else if (filterCategory.value === 'custom') {
    list = list.filter(t => {
      const q = getQuestionsCount(t)
      return q !== 50 && q !== 180
    })
  }

  // 2. Question count filter
  if (filterQuestions.value && filterQuestions.value !== 'all') {
    const targetQ = Number(filterQuestions.value)
    list = list.filter(t => getQuestionsCount(t) === targetQ)
  }

  // 3. Active status filter
  if (filterActive.value !== null && filterActive.value !== undefined) {
    list = list.filter(t => {
      const active = t.is_active !== false
      return active === filterActive.value
    })
  }

  // 4. Search query
  if (searchQuery.value && searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim()
    list = list.filter(t =>
      (t.name && t.name.toLowerCase().includes(q)) ||
      (t.description && t.description.toLowerCase().includes(q)) ||
      (String(t.id).includes(q)) ||
      (t.template_data?.template_id && t.template_data.template_id.toLowerCase().includes(q))
    )
  }

  return list
})

// Bound items for custom-data-table
const tableItems = computed(() => ({
  results: filteredTemplates.value,
  count: filteredTemplates.value.length,
}))

async function getData(params = {}) {
  return tableItems.value
}

function applyFilters() {
  // Triggers reactivity
}

function resetFilters() {
  searchQuery.value = ''
  filterCategory.value = 'all'
  filterQuestions.value = 'all'
  filterActive.value = null
}

function getQuestionsCount(item: any) {
  return (
    item.total_mcq ??
    item.template_data?.questions?.metadata?.num_questions ??
    item.template_data?.metadata?.num_questions ??
    0
  )
}

function getColumnsCount(item: any) {
  return (
    item.template_data?.questions?.layout?.columns_count ??
    item.template_data?.metadata?.columns_count ??
    item.template_data?.layout?.columns_count ??
    4
  )
}

function getChoicesCount(item: any) {
  return (
    item.template_data?.questions?.layout?.choices_count ??
    item.template_data?.metadata?.choices_count ??
    item.template_data?.layout?.choices_count ??
    4
  )
}

function getPaperSize(item: any) {
  return (
    item.template_data?.paper?.size ||
    item.template_data?.metadata?.paper_size ||
    (getQuestionsCount(item) > 100 ? 'A3' : (getQuestionsCount(item) <= 40 ? 'A5' : 'A4'))
  )
}

function getCategoryLabel(item: any) {
  const name = item.name || ''
  const tId = item.template_data?.template_id || ''
  const q = getQuestionsCount(item)
  if (name.includes('وزارة التربية') || name.includes('الثانوية العامة') || tId === 'YEMEN_MINISTRY_50' || q === 50) {
    return 'وزارة التربية والتعليم'
  }
  if (q === 180 || name.includes('الجامعات') || name.includes('التعليم العالي')) {
    return 'الجامعات والتعليم العالي'
  }
  return 'قالب مخصص'
}

function getCategoryColor(item: any) {
  const name = item.name || ''
  const tId = item.template_data?.template_id || ''
  const q = getQuestionsCount(item)
  if (name.includes('وزارة التربية') || name.includes('الثانوية العامة') || tId === 'YEMEN_MINISTRY_50' || q === 50) {
    return 'primary'
  }
  if (q === 180 || name.includes('الجامعات') || name.includes('التعليم العالي')) {
    return 'indigo'
  }
  return 'teal'
}

function getCategoryIcon(item: any) {
  const name = item.name || ''
  const tId = item.template_data?.template_id || ''
  const q = getQuestionsCount(item)
  if (name.includes('وزارة التربية') || name.includes('الثانوية العامة') || tId === 'YEMEN_MINISTRY_50' || q === 50) {
    return 'mdi-school-outline'
  }
  if (q === 180 || name.includes('الجامعات') || name.includes('التعليم العالي')) {
    return 'mdi-domain'
  }
  return 'mdi-tune-variant'
}

function confirmDeleteTemplate(t: any) {
  templateToDelete.value = t
  showDeleteDialog.value = true
}

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
