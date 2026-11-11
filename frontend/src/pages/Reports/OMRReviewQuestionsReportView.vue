<template>
  <div class="omr-review-questions-report-page">
    <filter-fields label="معايير التصفية والبحث في الأسئلة التي تحتاج مراجعة OMR" class="mb-4">
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
const filterReviewPriority = ref('')
const filterBubbleState = ref('')
const filterIsManuallyOverridden = ref('')

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
  if (filterInstitutionType.value) {
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
