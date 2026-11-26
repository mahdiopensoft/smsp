<template>
  <div class="omr-review-questions-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في الأسئلة التي تحتاج مراجعة OMR" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
      <template #fields>
        <!-- 1. اختيار نوع المؤسسة التعليمية الموحد -->
        <v-col cols="3">
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
          cols="3"
          :add="false"
          @update:model-value="filterVersion = null"
        />

        <auto-list
          v-model="filterVersion"
          name="ExamVersionByExam"
          :param="filterExam"
          placeholder="النموذج"
          cols="3"
          :add="false"
          :disabled="!filterExam"
        />

        <auto-list
          v-model="filterReviewPriority"
          name="LocalTextOption"
          :objects="[
            { text: 'جميع الأولويات', value: '' },
            { text: 'حرج', value: 'CRITICAL' },
            { text: 'عالي', value: 'HIGH' },
            { text: 'متوسط', value: 'MEDIUM' },
            { text: 'لا يتطلب', value: 'NONE' }
          ]"
          cols="3"
          label="أولوية المراجعة"
          icon="alert-circle-outline"
          :add="false"
        />

        <auto-list
          v-model="filterBubbleState"
          name="LocalTextOption"
          :objects="[
            { text: 'جميع الحالات', value: '' },
            { text: 'ملتبس', value: 'ambiguous' },
            { text: 'تظليل متعدد', value: 'multiple' },
            { text: 'فارغ', value: 'empty' },
            { text: 'ممسوح', value: 'erased' }
          ]"
          cols="3"
          label="حالة الدائرة"
          icon="radiobox-marked"
          :add="false"
        />

        <auto-list
          v-model="filterIsManuallyOverridden"
          name="LocalTextOption"
          :objects="[
            { text: 'الكل', value: '' },
            { text: 'معدّل يدوياً', value: 'true' },
            { text: 'غير معدّل', value: 'false' }
          ]"
          cols="3"
          label="تعديل يدوي"
          icon="pencil-outline"
          :add="false"
        />

        <v-col cols="auto" class="d-flex align-center gap-2 mb-6">
          <custom-btn type="show" label="عرض" color="primary" class="font-weight-bold px-5" :loading="loading" :click="applyFilters" />
          <custom-btn
            type="cancel_filter"
            color="error"
            variant="tonal"
            :click="resetFilters"
            label="إلغاء الفلترة"
            class="font-weight-bold"
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
            <span class="font-weight-bold text-body-2" :class="`text-${getPriorityColor(item.reviewPriority)}`">
              {{ getPriorityLabel(item.reviewPriority) }}
            </span>
          </template>
          <template v-else-if="key === 'isManuallyOverridden'">
            <span class="font-weight-medium text-body-2" :class="item.isManuallyOverridden ? 'text-info' : 'text-medium-emphasis'">
              {{ item.isManuallyOverridden ? 'نعم' : 'لا' }}
            </span>
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
}

const headers = [
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

    const res = await reportsService.getOMRReviewQuestionsReport(query)
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
  filterReviewPriority.value = ''
  filterBubbleState.value = ''
  filterIsManuallyOverridden.value = ''
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
