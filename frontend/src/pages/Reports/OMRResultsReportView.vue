<template>
  <div class="omr-results-report-page">
    <filter-fields label="معايير التصفية والبحث في نتائج التصحيح الآلي (OMR)" class="mb-4">
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
            v-model="filters.status"
            :items="[
              { text: 'جميع الحالات', value: '' },
              { text: 'ناجح', value: 'success' },
              { text: 'بانتظار المراجعة', value: 'needs_review' },
              { text: 'خطأ', value: 'error' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="حالة المعالجة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.confidence_min"
            :items="[
              { text: 'جميع مستويات الثقة', value: '' },
              { text: 'أكثر من 90%', value: '0.90' },
              { text: 'أكثر من 70%', value: '0.70' },
              { text: 'أقل من 70%', value: '0' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="مستوى الثقة"
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
        <template #item.confidence="{ item }">
          <v-chip
            :color="item.confidence >= 90 ? 'success' : (item.confidence >= 70 ? 'warning' : 'error')"
            size="small"
            variant="tonal"
          >
            {{ item.confidence }}%
          </v-chip>
        </template>
        <template #item.status="{ item }">
          <v-chip
            :color="item.status === 'success' ? 'success' : 'warning'"
            size="small"
            variant="tonal"
          >
            {{ item.status === 'success' ? 'ناجح' : (item.status === 'needs_review' ? 'بانتظار مراجعة' : item.status) }}
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
  status: '',
  confidence_min: '',
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'اسم الطالب', key: 'studentName', sortable: true },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'النموذج', key: 'versionCode', sortable: true, align: 'center' },
  { title: 'إجمالي الأسئلة', key: 'totalQuestions', sortable: true, align: 'center' },
  { title: 'الصحيحة', key: 'correctAnswers', sortable: true, align: 'center' },
  { title: 'الخاطئة', key: 'wrongAnswers', sortable: true, align: 'center' },
  { title: 'غير المجابة', key: 'unanswered', sortable: true, align: 'center' },
  { title: 'الملتبسة', key: 'ambiguousCount', sortable: true, align: 'center' },
  { title: 'الدرجة', key: 'mcqScore', sortable: true, align: 'center' },
  { title: 'الدرجة العظمى', key: 'mcqMaxScore', sortable: true, align: 'center' },
  { title: 'نسبة الثقة', key: 'confidence', sortable: true, align: 'center' },
  { title: 'حالة المعالجة', key: 'status', sortable: true, align: 'center' },
]

const buildParams = () => {
  const p = {}
  if (filters.value.exam) p.exam = filters.value.exam
  if (filters.value.version) p.version = filters.value.version
  if (filters.value.status) p.status = filters.value.status
  if (filters.value.confidence_min) p.confidence_min = filters.value.confidence_min
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getOMRResultsReport(buildParams())
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
    status: '',
    confidence_min: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

