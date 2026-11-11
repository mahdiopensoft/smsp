<template>
  <div class="rejected-questions-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل الأسئلة المرفوضة" class="mb-4">
      <template #fields>
        <v-col cols="12" md="2">
          <v-select
            v-model="filters.institution_type"
            :items="[
              { text: 'الكل', value: 'all' },
              { text: 'مدارس فقط', value: 'school' },
              { text: 'جامعات فقط', value: 'university' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="نوع المؤسسة"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <template v-if="filters.institution_type !== 'university'">
          <auto-list
            v-model="filters.subject"
            name="Subject"
            placeholder="المادة الدراسية"
            cols="2"
            :add="false"
          />
        </template>

        <template v-if="filters.institution_type !== 'school'">
          <auto-list
            v-model="filters.college"
            name="College"
            placeholder="الكلية"
            cols="2"
            :add="false"
            @update:model-value="filters.department = null; filters.specialization = null; filters.semester_subject = null"
          />
          <auto-list
            v-model="filters.department"
            name="DepartmentByCollege"
            :param="filters.college"
            placeholder="القسم"
            cols="2"
            :add="false"
            :disabled="!filters.college"
            @update:model-value="filters.specialization = null"
          />
          <auto-list
            v-model="filters.specialization"
            name="Specialization"
            :param="filters.department"
            placeholder="التخصص"
            cols="2"
            :add="false"
            :disabled="!filters.department"
          />
          <auto-list
            v-model="filters.semester_subject"
            name="SemesterSubject"
            :param="filters.specialization"
            placeholder="المقرر الجامعي"
            cols="2"
            :add="false"
            :disabled="!filters.specialization"
          />
        </template>

        <v-col cols="12" md="2">
          <v-text-field
            v-model="filters.date_from"
            type="date"
            label="من تاريخ"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-text-field
            v-model="filters.date_to"
            type="date"
            label="إلى تاريخ"
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
        <template #item.rejectionReason="{ item }">
          <span class="text-error font-weight-medium">{{ item.rejectionReason || 'لم يحدد سبب' }}</span>
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
  institution_type: 'all',
  date_from: '',
  date_to: '',
  subject: null,
  college: null,
  department: null,
  specialization: null,
  semester_subject: null,
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'نص السؤال (مختصر)', key: 'contentPreview', sortable: false },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'الوحدة', key: 'unit', sortable: true },
  { title: 'الدرس', key: 'lesson', sortable: true },
  { title: 'المؤلف', key: 'author', sortable: true },
  { title: 'المراجع', key: 'reviewer', sortable: true },
  { title: 'سبب الرفض', key: 'rejectionReason', sortable: false },
  { title: 'تاريخ الإنشاء', key: 'createdAt', sortable: true },
  { title: 'تاريخ الرفض', key: 'rejectedAt', sortable: true },
]

const onInstitutionTypeChange = () => {
  filters.value.subject = null
  filters.value.college = null
  filters.value.department = null
  filters.value.specialization = null
  filters.value.semester_subject = null
  applyFilters()
}

const buildParams = () => {
  const p = {}
  if (filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.subject) p.subject = filters.value.subject
  if (filters.value.college) p.college = filters.value.college
  if (filters.value.department) p.department = filters.value.department
  if (filters.value.specialization) p.specialization = filters.value.specialization
  if (filters.value.semester_subject) p.semester_subject = filters.value.semester_subject
  if (filters.value.date_from) p.date_from = filters.value.date_from
  if (filters.value.date_to) p.date_to = filters.value.date_to
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getRejectedQuestionsReport(buildParams())
    items.value = res.results || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    institution_type: 'all',
    date_from: '',
    date_to: '',
    subject: null,
    college: null,
    department: null,
    specialization: null,
    semester_subject: null,
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

