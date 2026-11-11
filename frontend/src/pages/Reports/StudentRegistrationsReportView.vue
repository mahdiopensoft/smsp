<template>
  <div class="student-registrations-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في سجل تسجيلات الطلاب" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
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
            v-model="filterIsPresent"
            :items="[
              { text: 'الكل', value: '' },
              { text: 'حاضر', value: 'true' },
              { text: 'غائب', value: 'false' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="حالة الحضور"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filterIsPrinted"
            :items="[
              { text: 'الكل', value: '' },
              { text: 'مطبوع', value: 'true' },
              { text: 'غير مطبوع', value: 'false' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="حالة الطباعة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="3">
          <v-text-field
            v-model="filterSearch"
            placeholder="بحث باسم الطالب أو رقم الجلوس..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            hide-details
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

const loading = ref(false)
const items = ref({
  results: [],
  count: 0,
})

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
  applyFilters()
}

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'اسم الطالب', key: 'studentName', sortable: true },
  { title: 'الرقم الأكاديمي', key: 'academicNumber', sortable: true },
  { title: 'رقم الجلوس', key: 'seatNumber', sortable: true },
  { title: 'الرقم السري', key: 'secretNumber', sortable: true },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'النموذج', key: 'versionCode', sortable: true, align: 'center' },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'الصف / التخصص', key: 'classTrack', sortable: true },
  { title: 'حالة الحضور', key: 'isPresent', sortable: true, align: 'center' },
  { title: 'حالة الطباعة', key: 'isPrinted', sortable: true, align: 'center' },
  { title: 'تاريخ التسجيل', key: 'createdAt', sortable: true },
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

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getStudentRegistrationsReport(buildParams())
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
  filterIsPresent.value = ''
  filterIsPrinted.value = ''
  filterSearch.value = ''
  applyFilters()
}

onMounted(applyFilters)
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
