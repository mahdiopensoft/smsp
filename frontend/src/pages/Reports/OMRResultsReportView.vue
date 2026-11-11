<template>
  <div class="omr-results-report-page">
    <filter-fields label="معايير التصفية والبحث في نتائج التصحيح الآلي (OMR)" class="mb-4">
      <template #fields>
        <!-- اختيار نوع المؤسسة التعليمية (مدارس / جامعات / معاهد) بدون خيار الكل -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            label="نوع المؤسسة التعليمية"
            placeholder="اختر نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            clearable
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :prepend-icon="item.raw.icon" />
            </template>
          </v-select>
        </v-col>

        <auto-list
          v-model="filterExam"
          name="Exam"
          :param="examParam"
          placeholder="الاختبار"
          cols="2"
          :add="false"
          @update:model-value="filterVersion = null"
        />

        <auto-list
          v-model="filterVersion"
          name="ExamVersionByExam"
          :param="filterExam"
          placeholder="النموذج"
          cols="2"
          :add="false"
          :disabled="!filterExam"
        />

        <v-col cols="12" md="2">
          <v-select
            v-model="filterStatus"
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
            v-model="filterConfidenceMin"
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

        <v-col cols="auto" class="d-flex align-center gap-2 py-2">
          <custom-btn type="filter" :loading="loading" :click="applyFilters" />
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
import { ref, computed, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(false)
const items = ref([])

// خيارات نوع المؤسسة بدون "الكل"
const filterInstitutionType = ref(null)
const institutionTypeOptions = [
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]

const filterExam = ref(null)
const filterVersion = ref(null)
const filterStatus = ref('')
const filterConfidenceMin = ref('')

const examParam = computed(() => {
  if (filterInstitutionType.value) return { institution_type: filterInstitutionType.value }
  return null
})

const onInstitutionTypeChange = () => {
  filterExam.value = null
  filterVersion.value = null
  applyFilters()
}

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
  if (filterInstitutionType.value) {
    p.institution_type = filterInstitutionType.value
  }
  if (filterExam.value) p.exam = filterExam.value
  if (filterVersion.value) p.version = filterVersion.value
  if (filterStatus.value) p.status = filterStatus.value
  if (filterConfidenceMin.value) p.confidence_min = filterConfidenceMin.value
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
  filterInstitutionType.value = null
  filterExam.value = null
  filterVersion.value = null
  filterStatus.value = ''
  filterConfidenceMin.value = ''
  applyFilters()
}

onMounted(applyFilters)
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
