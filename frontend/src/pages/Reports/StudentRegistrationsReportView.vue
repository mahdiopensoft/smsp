<template>
  <div class="student-registrations-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في تسجيلات الطلاب في الاختبارات" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
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
          v-model="filterIsPresent"
          name="LocalTextOption"
          :objects="[
            { text: 'الكل (حضور/غياب)', value: '' },
            { text: 'حاضر', value: 'true' },
            { text: 'غائب', value: 'false' }
          ]"
          cols="3"
          label="حالة الحضور"
          icon="account-check-outline"
          :add="false"
        />

        <auto-list
          v-model="filterIsPrinted"
          name="LocalTextOption"
          :objects="[
            { text: 'الكل (حالة الطباعة)', value: '' },
            { text: 'تمت الطباعة', value: 'true' },
            { text: 'لم تطبع', value: 'false' }
          ]"
          cols="3"
          label="حالة الطباعة"
          icon="printer-outline"
          :add="false"
        />

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
          <template v-else-if="key === 'isPresent'">
            <v-chip
              :color="item.isPresent ? 'success' : 'error'"
              size="small"
              variant="tonal"
            >
              {{ item.isPresent ? 'حاضر' : 'غائب' }}
            </v-chip>
          </template>
          <template v-else-if="key === 'isPrinted'">
            <v-chip
              :color="item.isPrinted ? 'primary' : 'default'"
              size="small"
              variant="tonal"
            >
              {{ item.isPrinted ? 'مطبوع' : 'غير مطبوع' }}
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
const filterIsPresent = ref('')
const filterIsPrinted = ref('')
const filterSearch = ref('')

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
  { title: 'الرقم الأكاديمي', key: 'academicNumber', sortable: true, align: 'center' },
  { title: 'رقم الجلوس', key: 'seatNumber', sortable: true, align: 'center' },
  { title: 'الرقم السري', key: 'secretNumber', sortable: true, align: 'center' },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'النموذج', key: 'versionCode', sortable: true, align: 'center' },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'الحضور', key: 'isPresent', sortable: true, align: 'center' },
  { title: 'حالة الطباعة', key: 'isPrinted', sortable: true, align: 'center' },
  { title: 'تاريخ الطباعة', key: 'printedAt', sortable: true, align: 'center' },
]

const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }
  if (filterExam.value) p.exam = filterExam.value
  if (filterVersion.value) p.version = filterVersion.value
  if (filterIsPresent.value !== '') p.is_present = filterIsPresent.value
  if (filterIsPrinted.value !== '') p.is_printed = filterIsPrinted.value
  if (filterSearch.value) p.search = filterSearch.value
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

    const res = await reportsService.getStudentRegistrationsReport(query)
    setResponse(res)
  } catch (e) {
    console.error(e)
    setResponse({ results: [], count: 0 })
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filterInstitutionType.value = 'school'
  filterExam.value = null
  filterVersion.value = null
  filterIsPresent.value = ''
  filterIsPrinted.value = ''
  filterSearch.value = ''
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
