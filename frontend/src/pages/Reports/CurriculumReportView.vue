<template>
  <div class="curriculum-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل التغطية الأكاديمية" class="mb-4">
      <template #fields>
        <v-col cols="12" md="2">
          <v-select
            v-model="filters.institution_type"
            :items="institutionTypeOptions"
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

        <template v-if="filters.institution_type !== 'university'">
          <auto-list
            v-model="filters.stage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="filters.class_track = null"
          />
          <auto-list
            v-model="filters.class_track"
            name="ClassTrackByStage"
            :param="filters.stage"
            placeholder="الصف والمسار"
            cols="2"
            :add="false"
            :disabled="!filters.stage"
          />
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

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.status"
            :items="statusOptions"
            item-title="text"
            item-value="value"
            placeholder="الحالة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-text-field
            v-model="filters.search"
            placeholder="بحث باسم الدرس أو الوحدة..."
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
        <template #item.coverageStatus="{ item }">
          <v-chip
            :color="getCoverageColor(item.coverageStatus)"
            size="small"
            variant="tonal"
          >
            {{ item.coverageStatus }}
          </v-chip>
        </template>
        <template #item.isActive="{ item }">
          <v-chip
            :color="item.isActive ? 'success' : 'default'"
            size="small"
            variant="tonal"
          >
            {{ item.isActive ? 'نشط' : 'غير نشط' }}
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

const institutionTypeOptions = [
  { text: 'الكل (مدارس وجامعات)', value: 'all' },
  { text: 'مدارس فقط', value: 'school' },
  { text: 'جامعات فقط', value: 'university' },
]

const statusOptions = [
  { text: 'جميع الحالات', value: 'all' },
  { text: 'نشط', value: 'active' },
  { text: 'غير نشط', value: 'inactive' },
]

const filters = ref({
  institution_type: 'all',
  status: 'all',
  search: '',
  stage: null,
  class_track: null,
  subject: null,
  college: null,
  department: null,
  specialization: null,
  semester_subject: null,
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'نوع المؤسسة', key: 'institutionType', sortable: true, align: 'center', width: '110px' },
  { title: 'المادة / المقرر', key: 'subject', sortable: true },
  { title: 'الوحدة الدراسية', key: 'unit', sortable: true },
  { title: 'الدرس', key: 'name', sortable: true },
  { title: 'عدد الأسئلة', key: 'questionsCount', sortable: true, align: 'center' },
  { title: 'حالة التغطية', key: 'coverageStatus', sortable: true, align: 'center' },
  { title: 'الصف / التخصص', key: 'branchName', sortable: true },
  { title: 'الحالة', key: 'isActive', sortable: true, align: 'center' },
]

const getCoverageColor = (status) => {
  if (status === 'مكتمل') return 'success'
  if (status === 'جزئي') return 'warning'
  return 'error'
}

const onInstitutionTypeChange = () => {
  filters.value.stage = null
  filters.value.class_track = null
  filters.value.subject = null
  filters.value.college = null
  filters.value.department = null
  filters.value.specialization = null
  filters.value.semester_subject = null
  applyFilters()
}

const buildParams = () => {
  const p = {}
  if (filters.value.institution_type && filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.stage) p.stage = filters.value.stage
  if (filters.value.class_track) p.class_track = filters.value.class_track
  if (filters.value.subject) p.subject = filters.value.subject
  if (filters.value.college) p.college = filters.value.college
  if (filters.value.department) p.department = filters.value.department
  if (filters.value.specialization) p.specialization = filters.value.specialization
  if (filters.value.semester_subject) p.semester_subject = filters.value.semester_subject
  if (filters.value.status && filters.value.status !== 'all') p.status = filters.value.status
  if (filters.value.search) p.search = filters.value.search
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getCurriculumReport(buildParams())
    items.value = res.results || (Array.isArray(res) ? res : [])
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    institution_type: 'all',
    status: 'all',
    search: '',
    stage: null,
    class_track: null,
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
