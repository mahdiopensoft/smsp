<template>
  <div class="omr-review-questions-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في الأسئلة التي تحتاج مراجعة OMR" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
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
            v-model="filterReviewPriority"
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
            v-model="filterBubbleState"
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
            v-model="filterIsManuallyOverridden"
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
          <template v-if="key === 'index'">
            <div class="d-flex justify-center align-center">
              <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
            </div>
          </template>
          <template v-else-if="key === 'isCorrect'">
            <v-chip
              :color="item.isCorrect ? 'success' : 'error'"
              size="small"
              variant="tonal"
            >
              {{ item.isCorrect ? 'صحيح' : 'خاطئ' }}
            </v-chip>
          </template>
          <template v-else-if="key === 'needsReview'">
            <v-chip
              :color="item.needsReview ? 'warning' : 'default'"
              size="small"
              variant="tonal"
            >
              {{ item.needsReview ? 'يحتاج مراجعة' : 'لا' }}
            </v-chip>
          </template>
          <template v-else-if="key === 'reviewPriority'">
            <v-chip
              :color="getPriorityColor(item.reviewPriority)"
              size="small"
              variant="tonal"
            >
              {{ getPriorityLabel(item.reviewPriority) }}
            </v-chip>
          </template>
          <template v-else-if="key === 'isManuallyOverridden'">
            <v-chip
              :color="item.isManuallyOverridden ? 'info' : 'default'"
              size="small"
              variant="tonal"
            >
              {{ item.isManuallyOverridden ? 'نعم' : 'لا' }}
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

const loading = ref(false)
const items = ref({
  results: [],
  count: 0,
})

// خيارات نوع المؤسسة بدون "الكل"
const filterInstitutionType = ref('school')

const filterExam = ref(null)
const filterVersion = ref(null)
const filterReviewPriority = ref('')
const filterBubbleState = ref('')
const filterIsManuallyOverridden = ref('')

const examParam = computed(() => {
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') return { institution_type: filterInstitutionType.value }
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
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }
  if (filterExam.value) p.exam = filterExam.value
  if (filterVersion.value) p.version = filterVersion.value
  if (filterReviewPriority.value) p.review_priority = filterReviewPriority.value
  if (filterBubbleState.value) p.bubble_state = filterBubbleState.value
  if (filterIsManuallyOverridden.value !== '') {
    p.is_manually_overridden = filterIsManuallyOverridden.value
  }
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getOMRReviewQuestionsReport(buildParams())
    const results = Array.isArray(res) ? res : (res?.results || [])
    const count = res?.count !== undefined ? res.count : results.length
    items.value = { results, count }
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
  filterReviewPriority.value = ''
  filterBubbleState.value = ''
  filterIsManuallyOverridden.value = ''
  applyFilters()
}

onMounted(applyFilters)
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
