<template>
  <div class="omr-results-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في نتائج التصحيح الآلي (OMR)" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
      <template #fields>
        <!-- 1. اختيار نوع المؤسسة التعليمية الموحد -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filterInstitutionType"
            name="InstitutionType"
            label="نوع المؤسسة التعليمية"
            placeholder="نوع المؤسسة التعليمية"
            cols="12"
            :add="false"
            @update:model-value="onInstitutionTypeChange"
          />
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
              { text: 'بانتظار مراجعة', value: 'needs_review' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="الحالة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filterConfidenceMin"
            :items="[
              { text: 'أي دقة', value: '' },
              { text: 'أعلى من 90%', value: '0.90' },
              { text: 'أعلى من 80%', value: '0.80' },
              { text: 'أقل من 80%', value: '0.79' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="الحد الأدنى للثقة"
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

    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <custom-data-table
        :items="items"
        :headers="headers"
        :getData="applyFilters"
        :customLoading="loading"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :actions="false"
        :search="true"
        :numbering="true"
        class="bg-transparent"
      >
        <template v-slot:item-slot="{ item, key, index }">
          <template v-if="key === 'numbering'">
            <div class="d-flex justify-center align-center">
              <span class="font-weight-bold text-caption text-medium-emphasis">{{ ((items?.pagination?.current_page || 1) - 1) * (items?.pagination?.page_size || 20) + (index ?? 0) + 1 }}</span>
            </div>
          </template>
          <template v-else-if="key === 'confidence'">
            <v-chip
              :color="item.confidence >= 90 ? 'success' : (item.confidence >= 70 ? 'warning' : 'error')"
              size="small"
              variant="tonal"
            >
              {{ item.confidence }}%
            </v-chip>
          </template>
          <template v-else-if="key === 'status'">
            <v-chip
              :color="item.status === 'success' ? 'success' : 'warning'"
              size="small"
              variant="tonal"
            >
              {{ item.status === 'success' ? 'ناجح' : (item.status === 'needs_review' ? 'بانتظار مراجعة' : item.status) }}
            </v-chip>
          </template>
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'
import { useReportPagination } from '@/composables/useReportPagination'

const {
  loading,
  items,
  extractParams,
  setResponse,
  resetPagination
} = useReportPagination(20)

// خيارات نوع المؤسسة بدون "الكل"
const filterInstitutionType = ref('school')

const filterExam = ref(null)
const filterVersion = ref(null)
const filterStatus = ref('')
const filterConfidenceMin = ref('')

const examParam = computed(() => {
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') return { institution_type: filterInstitutionType.value }
  return null
})

const onInstitutionTypeChange = () => {
  filterExam.value = null
  filterVersion.value = null
  resetPagination()
  applyFilters()
}

const headers = [
  { title: 'اسم الطالب', key: 'studentName', sortable: true },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'النموذج', key: 'versionCode', sortable: true, align: 'center' },
  { title: 'إجمالي الأسئلة', key: 'totalQuestions', sortable: true, align: 'center' },
  { title: 'الإجابات الصحيحة', key: 'correctAnswers', sortable: true, align: 'center' },
  { title: 'الإجابات الخاطئة', key: 'wrongAnswers', sortable: true, align: 'center' },
  { title: 'الدرجة المحسوبة', key: 'mcqScore', sortable: true, align: 'center' },
  { title: 'دقة القراءة', key: 'confidence', sortable: true, align: 'center' },
  { title: 'الحالة', key: 'status', sortable: true, align: 'center' },
]

const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }
  if (filterExam.value) p.exam = filterExam.value
  if (filterVersion.value) p.version = filterVersion.value
  if (filterStatus.value) p.status = filterStatus.value
  if (filterConfidenceMin.value) p.confidence_min = filterConfidenceMin.value
  return p
}

const applyFilters = async (tableParams = {}) => {
  const p = extractParams(tableParams)
  loading.value = true
  try {
    const query = {
      ...buildParams(),
      page: p.page,
      page_size: p.page_size,
    }
    if (p.search) query.search = p.search
    if (p.sort_by) query.sort_by = p.sort_by

    const res = await reportsService.getOMRResultsReport(query)
    setResponse(res)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filterInstitutionType.value = 'school'
  filterExam.value = null
  filterVersion.value = null
  filterStatus.value = ''
  filterConfidenceMin.value = ''
  resetPagination()
  applyFilters()
}

onMounted(applyFilters)
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
