<template>
  <div class="curriculum-exclusions-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل المحذوفات من المنهج" class="mb-4">
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
          />
        </v-col>

        <auto-list
          v-model="filters.academic_year"
          name="AcademicYear"
          placeholder="العام الدراسي"
          cols="2"
          :add="false"
        />

        <auto-list
          v-model="filters.stage"
          name="Stage"
          placeholder="المرحلة الدراسية"
          cols="2"
          :add="false"
        />

        <auto-list
          v-model="filters.subject"
          name="Subject"
          placeholder="المادة الدراسية"
          cols="2"
          :add="false"
        />

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.exclusion_type"
            :items="[
              { text: 'الكل', value: '' },
              { text: 'وحدة كاملة', value: 'unit' },
              { text: 'درس محدد', value: 'lesson' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="نوع الاستبعاد"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.is_active"
            :items="[
              { text: 'الكل', value: '' },
              { text: 'نشط', value: 'true' },
              { text: 'غير نشط', value: 'false' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="الحالة"
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
        <template #item.exclusionType="{ item }">
          <v-chip size="small" variant="tonal" color="primary">
            {{ item.exclusionType === 'unit' ? 'وحدة كاملة' : 'درس محدد' }}
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

const filters = ref({
  institution_type: 'all',
  academic_year: null,
  stage: null,
  subject: null,
  exclusion_type: '',
  is_active: '',
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'العام الدراسي', key: 'academicYear', sortable: true },
  { title: 'نوع المؤسسة', key: 'institutionType', sortable: true, align: 'center' },
  { title: 'المرحلة', key: 'stage', sortable: true },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'نوع الاستبعاد', key: 'exclusionType', sortable: true, align: 'center' },
  { title: 'الوحدة', key: 'unit', sortable: true },
  { title: 'الدرس', key: 'lesson', sortable: true },
  { title: 'السبب / التعميم', key: 'reason', sortable: false },
  { title: 'الحالة', key: 'isActive', sortable: true, align: 'center' },
  { title: 'تاريخ الإنشاء', key: 'createdAt', sortable: true },
]

const buildParams = () => {
  const p = {}
  if (filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.academic_year) p.academic_year = filters.value.academic_year
  if (filters.value.stage) p.stage = filters.value.stage
  if (filters.value.subject) p.subject = filters.value.subject
  if (filters.value.exclusion_type) p.exclusion_type = filters.value.exclusion_type
  if (filters.value.is_active !== '') p.is_active = filters.value.is_active
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getCurriculumExclusionsReport(buildParams())
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
    academic_year: null,
    stage: null,
    subject: null,
    exclusion_type: '',
    is_active: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

