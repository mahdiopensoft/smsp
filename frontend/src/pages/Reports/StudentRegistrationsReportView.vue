<template>
  <div class="student-registrations-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل تسجيلات الطلاب" class="mb-4">
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
            v-model="filters.is_present"
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
            v-model="filters.is_printed"
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
            v-model="filters.search"
            placeholder="بحث باسم الطالب أو رقم الجلوس..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            hide-details
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
        <template #item.isPresent="{ item }">
          <v-chip
            :color="item.isPresent ? 'success' : 'error'"
            size="small"
            variant="tonal"
          >
            {{ item.isPresent ? 'حاضر' : 'غائب' }}
          </v-chip>
        </template>
        <template #item.isPrinted="{ item }">
          <v-chip
            :color="item.isPrinted ? 'primary' : 'default'"
            size="small"
            variant="tonal"
          >
            {{ item.isPrinted ? 'مطبوع' : 'غير مطبوع' }}
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
  is_present: '',
  is_printed: '',
  search: '',
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'اسم الطالب', key: 'studentName', sortable: true },
  { title: 'الرقم الأكاديمي', key: 'academicNumber', sortable: true },
  { title: 'رقم الجلوس', key: 'seatNumber', sortable: true },
  { title: 'الرقم السري', key: 'secretNumber', sortable: true },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'النموذج', key: 'versionCode', sortable: true, align: 'center' },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'حاضر؟', key: 'isPresent', sortable: true, align: 'center' },
  { title: 'مطبوع؟', key: 'isPrinted', sortable: true, align: 'center' },
  { title: 'تاريخ الطباعة', key: 'printedAt', sortable: true },
]

const buildParams = () => {
  const p = {}
  if (filters.value.exam) p.exam = filters.value.exam
  if (filters.value.version) p.version = filters.value.version
  if (filters.value.is_present !== '') p.is_present = filters.value.is_present
  if (filters.value.is_printed !== '') p.is_printed = filters.value.is_printed
  if (filters.value.search) p.search = filters.value.search
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getStudentRegistrationsReport(buildParams())
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
    is_present: '',
    is_printed: '',
    search: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

