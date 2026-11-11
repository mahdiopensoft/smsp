<template>
  <div class="authors-report-page">
    <filter-fields label="معايير التصفية والتقرير" class="mb-4">
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
            @update:model-value="filters.department = null; filters.specialization = null"
          />
          <auto-list
            v-model="filters.department"
            name="DepartmentByCollege"
            :param="filters.college"
            placeholder="القسم الأكاديمي"
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
        </template>

        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.search"
            placeholder="بحث باسم المؤلف..."
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
        ref="table"
        :items="items"
        :headers="headers"
        :loading="loading"
        :hasFilter="false"
        :log="false"
        hover
      >
        <template #item.rank="{ index }">{{ index + 1 }}</template>
        <template #item.approvalRate="{ item }">
          <v-chip
            :color="getApprovalColor(item.approvalRate)"
            size="small"
            variant="tonal"
          >
            {{ item.approvalRate }}%
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

const institutionTypeOptions = [
  { text: 'الكل (مدارس وجامعات)', value: 'all' },
  { text: 'مدارس فقط', value: 'school' },
  { text: 'جامعات فقط', value: 'university' },
]

const filters = ref({
  institution_type: 'all',
  stage: null,
  class_track: null,
  subject: null,
  college: null,
  department: null,
  specialization: null,
  search: '',
})

const headers = computed(() => [
  { title: '#', key: 'rank', sortable: false, width: '60px' },
  { title: 'المؤلف / المعلم', key: 'name', sortable: true },
  { title: 'المادة والصف', key: 'academicInfo', sortable: false },
  { title: 'إجمالي الأسئلة', key: 'total', sortable: true, align: 'center' },
  { title: 'معتمدة', key: 'approved', sortable: true, align: 'center' },
  { title: 'قيد المراجعة', key: 'pending', sortable: true, align: 'center' },
  { title: 'مرفوضة', key: 'rejected', sortable: true, align: 'center' },
  { title: 'نسبة الاعتماد', key: 'approvalRate', sortable: true, align: 'center' },
  { title: 'آخر نشاط', key: 'lastActivity', sortable: true },
])

const getApprovalColor = (rate) => {
  if (rate >= 80) return 'success'
  if (rate >= 60) return 'warning'
  return 'error'
}

const onInstitutionTypeChange = () => {
  filters.value.stage = null
  filters.value.class_track = null
  filters.value.subject = null
  filters.value.college = null
  filters.value.department = null
  filters.value.specialization = null
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
  if (filters.value.search) p.search = filters.value.search
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getAuthorsReport(buildParams())
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
    stage: null,
    class_track: null,
    subject: null,
    college: null,
    department: null,
    specialization: null,
    search: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>
