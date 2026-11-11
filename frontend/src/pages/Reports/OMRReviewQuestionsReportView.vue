<template>
  <div class="omr-review-questions-report-page">
    <filter-fields label="معايير التصفية والبحث في الأسئلة التي تحتاج مراجعة OMR" class="mb-4">
      <template #fields>
        <auto-list
          v-model="filters.exam"
          name="Exam"
          placeholder="الاختبار"
          cols="2"
          :add="false"
          @update:model-value="filters.version = null"
        />

        <auto-list
          v-model="filters.version"
          name="ExamVersionByExam"
          :param="filters.exam"
          placeholder="النموذج"
          cols="2"
          :add="false"
          :disabled="!filters.exam"
        />

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.review_priority"
            :items="[
              { text: 'جميع الأولويات', value: '' },
              { text: 'حرج', value: 'CRITICAL' },
              { text: 'عالي', value: 'HIGH' },
              { text: 'متوسط', value: 'MEDIUM' },
              { text: 'لا يتطلب', value: 'NONE' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="أولوية المراجعة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.bubble_state"
            :items="[
              { text: 'جميع الحالات', value: '' },
              { text: 'ملتبس', value: 'ambiguous' },
              { text: 'تظليل متعدد', value: 'multiple' },
              { text: 'فارغ', value: 'empty' },
              { text: 'ممسوح', value: 'erased' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="حالة الدائرة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.is_manually_overridden"
            :items="[
              { text: 'الكل', value: '' },
              { text: 'معدّل يدوياً', value: 'true' },
              { text: 'غير معدّل', value: 'false' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="تعديل يدوي"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="auto">
          <custom-btn type="filter" :loading="loading" :click="applyFilters" />
        </v-col>
        <v-col cols="auto">
          <custom-btn
            color="primary"
            variant="tonal"
            :click="resetFilters"
            label="إعادة ضبط"
            icon="mdi-refresh"
          />
        </v-col>
      </template>
    </filter-fields>

    <CustomCard elevation="0" class="rounded-xl overflow-hidden">
      <custom-data-table
        :items="items"
        :headers="headers"
        :loading="loading"
        :hasFilter="false"
        hover
      >
        <template #item.index="{ index }">{{ index + 1 }}</template>
        <template #item.isCorrect="{ item }">
          <v-chip
            :color="item.isCorrect ? 'success' : 'error'"
            size="small"
            variant="tonal"
          >
            {{ item.isCorrect ? 'صحيح' : 'خاطئ' }}
          </v-chip>
        </template>
        <template #item.needsReview="{ item }">
          <v-chip
            :color="item.needsReview ? 'warning' : 'default'"
            size="small"
            variant="tonal"
          >
            {{ item.needsReview ? 'يحتاج مراجعة' : 'لا' }}
          </v-chip>
        </template>
        <template #item.reviewPriority="{ item }">
          <v-chip
            :color="getPriorityColor(item.reviewPriority)"
            size="small"
            variant="tonal"
          >
            {{ getPriorityLabel(item.reviewPriority) }}
          </v-chip>
        </template>
        <template #item.isManuallyOverridden="{ item }">
          <v-chip
            :color="item.isManuallyOverridden ? 'info' : 'default'"
            size="small"
            variant="tonal"
          >
            {{ item.isManuallyOverridden ? 'نعم' : 'لا' }}
          </v-chip>
        </template>
      </custom-data-table>
    </CustomCard>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(false)
const items = ref([])

const filters = ref({
  exam: null,
  version: null,
  review_priority: '',
  bubble_state: '',
  is_manually_overridden: '',
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'اسم الطالب', key: 'studentName', sortable: true },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'رقم السؤال', key: 'questionNumber', sortable: true, align: 'center' },
  { title: 'الخيار المظلل', key: 'markedChoice', sortable: true, align: 'center' },
  { title: 'الخيار الصحيح', key: 'correctChoice', sortable: true, align: 'center' },
  { title: 'صحيح؟', key: 'isCorrect', sortable: true, align: 'center' },
  { title: 'حالة الدائرة', key: 'bubbleState', sortable: true, align: 'center' },
  { title: 'يحتاج مراجعة؟', key: 'needsReview', sortable: true, align: 'center' },
  { title: 'أولوية المراجعة', key: 'reviewPriority', sortable: true, align: 'center' },
  { title: 'معدّل يدوياً؟', key: 'isManuallyOverridden', sortable: true, align: 'center' },
]

const getPriorityColor = (priority) => {
  const map = {
    CRITICAL: 'error',
    HIGH: 'warning',
    MEDIUM: 'info',
    NONE: 'default',
  }
  return map[priority] || 'default'
}

const getPriorityLabel = (priority) => {
  const map = {
    CRITICAL: 'حرج',
    HIGH: 'عالي',
    MEDIUM: 'متوسط',
    NONE: 'لا يتطلب',
  }
  return map[priority] || priority
}

const buildParams = () => {
  const p = {}
  if (filters.value.exam) p.exam = filters.value.exam
  if (filters.value.version) p.version = filters.value.version
  if (filters.value.review_priority) p.review_priority = filters.value.review_priority
  if (filters.value.bubble_state) p.bubble_state = filters.value.bubble_state
  if (filters.value.is_manually_overridden !== '') {
    p.is_manually_overridden = filters.value.is_manually_overridden
  }
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getOMRReviewQuestionsReport(buildParams())
    items.value = res.results || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    exam: null,
    version: null,
    review_priority: '',
    bubble_state: '',
    is_manually_overridden: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

