<template>
  <div class="alignment-matrix-report-page">
    <filter-fields label="معايير تصفية مصفوفة المواءمة (CLOs)" class="mb-4">
      <template #fields>
        <v-col cols="12" md="2">
          <v-select
            v-model="filters.institution_type"
            :items="[
              { text: 'الكل', value: 'all' },
              { text: 'جامعات فقط', value: 'university' },
              { text: 'مدارس فقط', value: 'school' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

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
            @update:model-value="filters.specialization = null; filters.semester_subject = null"
          />
          <auto-list
            v-model="filters.specialization"
            name="Specialization"
            :param="filters.department"
            placeholder="التخصص"
            cols="2"
            :add="false"
            :disabled="!filters.department"
            @update:model-value="filters.semester_subject = null"
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

        <template v-if="filters.institution_type !== 'university'">
          <auto-list
            v-model="filters.subject_id"
            name="Subject"
            placeholder="المادة الدراسية"
            cols="2"
            :add="false"
          />
        </template>

        <v-col cols="12" md="2">
          <v-text-field
            v-model="filters.search"
            placeholder="بحث برمز CLO أو الوصف..."
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
        <template #item.coverage_status="{ item }">
          <v-chip
            :color="item.coverage_color || 'primary'"
            size="small"
            variant="tonal"
          >
            {{ item.coverage_status }}
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
  institution_type: 'all',
  search: '',
  college: null,
  department: null,
  specialization: null,
  semester_subject: null,
  subject_id: null,
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'نوع المؤسسة', key: 'institutionType', sortable: true, align: 'center', width: '100px' },
  { title: 'رمز المخرج', key: 'code', sortable: true, width: '130px' },
  { title: 'وصف مخرج التعلم (CLO)', key: 'name_ar', sortable: true },
  { title: 'الوحدة الدراسية', key: 'unit_name', sortable: true },
  { title: 'الأسئلة المتاحة', key: 'questions_count', sortable: true, align: 'center', width: '130px' },
  { title: 'حالة التغطية', key: 'coverage_status', sortable: true, align: 'center', width: '160px' },
]

const onInstitutionTypeChange = () => {
  filters.value.college = null
  filters.value.department = null
  filters.value.specialization = null
  filters.value.semester_subject = null
  filters.value.subject_id = null
  applyFilters()
}

const buildParams = () => {
  const p = {}
  if (filters.value.institution_type && filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.college) p.college = filters.value.college
  if (filters.value.department) p.department = filters.value.department
  if (filters.value.specialization) p.specialization = filters.value.specialization
  if (filters.value.semester_subject) p.semester_subject = filters.value.semester_subject
  if (filters.value.subject_id) p.subject_id = filters.value.subject_id
  if (filters.value.search) p.search = filters.value.search
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getAlignmentMatrixReport(buildParams())
    items.value = res.clos || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    institution_type: 'all',
    search: '',
    college: null,
    department: null,
    specialization: null,
    semester_subject: null,
    subject_id: null,
  }
  applyFilters()
}

onMounted(applyFilters)
</script>
