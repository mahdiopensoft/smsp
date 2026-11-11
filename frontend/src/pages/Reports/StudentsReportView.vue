<template>
  <div class="students-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل الطلاب" class="mb-4">
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
          v-model="filters.governorate"
          name="Governorate"
          placeholder="المحافظة"
          cols="2"
          :add="false"
          @update:model-value="filters.directorate = null"
        />

        <auto-list
          v-model="filters.directorate"
          name="DirectorateByGovernorate"
          :param="filters.governorate"
          placeholder="المديرية"
          cols="2"
          :add="false"
          :disabled="!filters.governorate"
        />

        <auto-list
          v-model="filters.stage"
          name="Stage"
          placeholder="المرحلة الدراسية"
          cols="2"
          :add="false"
        />

        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.search"
            placeholder="بحث باسم الطالب أو الرقم الأكاديمي..."
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
        <template #item.gender="{ item }">
          <v-chip
            :color="item.gender === 'ذكر' ? 'info' : 'pink'"
            size="small"
            variant="tonal"
          >
            {{ item.gender }}
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
  governorate: null,
  directorate: null,
  stage: null,
  search: '',
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'اسم الطالب', key: 'name', sortable: true },
  { title: 'الرقم الأكاديمي', key: 'academicNumber', sortable: true },
  { title: 'الجنس', key: 'gender', sortable: true, align: 'center' },
  { title: 'المؤسسة التعليمية', key: 'institution', sortable: true },
  { title: 'المرحلة / المستوى', key: 'levelStage', sortable: true },
  { title: 'المحافظة', key: 'governorate', sortable: true },
  { title: 'المديرية', key: 'directorate', sortable: true },
  { title: 'تاريخ التسجيل', key: 'createdAt', sortable: true },
]

const buildParams = () => {
  const p = {}
  if (filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.governorate) p.governorate = filters.value.governorate
  if (filters.value.directorate) p.directorate = filters.value.directorate
  if (filters.value.stage) p.stage = filters.value.stage
  if (filters.value.search) p.search = filters.value.search
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getStudentsReport(buildParams())
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
    governorate: null,
    directorate: null,
    stage: null,
    search: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

