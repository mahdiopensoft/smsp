<template>
  <div class="students-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في الطلاب" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
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

        <template v-if="filterInstitutionType === 'school'">
          <auto-list
            v-model="filterStage"
            name="SchoolStage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
          />
        </template>

        <template v-else-if="filterInstitutionType === 'university'">
          <auto-list
            v-model="filterCollege"
            name="UniversityCollege"
            placeholder="الكلية"
            cols="2"
            :add="false"
          />
        </template>

        <template v-else-if="filterInstitutionType === 'institute'">
          <auto-list
            v-model="filterInstituteField"
            name="InstituteField"
            placeholder="المجال"
            cols="2"
            :add="false"
          />
        </template>

        <auto-list
          v-model="filterGovernorate"
          name="Governorate"
          placeholder="المحافظة"
          cols="2"
          :add="false"
          @update:model-value="filterDirectorate = null"
        />

        <auto-list
          v-model="filterDirectorate"
          name="Directorate"
          :param="filterGovernorate ? { fk_governorate: filterGovernorate } : null"
          placeholder="المديرية"
          cols="2"
          :add="false"
          :disabled="!filterGovernorate"
        />

        <v-col cols="12" md="3">
          <v-text-field
            v-model="filterSearch"
            placeholder="بحث بالاسم أو الرقم الأكاديمي..."
            density="compact"
            variant="outlined"
            prepend-inner-icon="mdi-magnify"
            hide-details
            clearable
            @keyup.enter="applyFilters"
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
              <span class="font-weight-bold text-caption text-medium-emphasis">{{ ((items?.pagination?.current_page || 1) - 1) * (items?.pagination?.page_size || 20) + (index ?? 0) + 1 }}</span>
            </div>
          </template>
          <template v-else-if="key === 'gender'">
            <v-chip
              :color="item.gender === 'ذكر' ? 'info' : 'pink'"
              size="small"
              variant="tonal"
            >
              {{ item.gender }}
            </v-chip>
          </template>
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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

const filterStage = ref(null)
const filterCollege = ref(null)
const filterInstituteField = ref(null)
const filterGovernorate = ref(null)
const filterDirectorate = ref(null)
const filterSearch = ref('')

const onInstitutionTypeChange = () => {
  filterStage.value = null
  filterCollege.value = null
  filterInstituteField.value = null
  resetPagination()
  applyFilters()
}

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'اسم الطالب', key: 'name', sortable: true },
  { title: 'الرقم الأكاديمي', key: 'academicNumber', sortable: true, align: 'center' },
  { title: 'الجنس', key: 'gender', sortable: true, align: 'center' },
  { title: 'المؤسسة التعليمية', key: 'institution', sortable: true },
  { title: 'المرحلة / المستوى', key: 'levelStage', sortable: true, align: 'center' },
  { title: 'المحافظة', key: 'governorate', sortable: true },
  { title: 'المديرية', key: 'directorate', sortable: true },
  { title: 'تاريخ الإضافة', key: 'createdAt', sortable: true, align: 'center' },
]

const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }
  if (filterStage.value) p.stage = filterStage.value
  if (filterCollege.value) p.college = filterCollege.value
  if (filterInstituteField.value) p.field = filterInstituteField.value
  if (filterGovernorate.value) p.governorate = filterGovernorate.value
  if (filterDirectorate.value) p.directorate = filterDirectorate.value
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

    const res = await reportsService.getStudentsReport(query)
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
  filterStage.value = null
  filterCollege.value = null
  filterInstituteField.value = null
  filterGovernorate.value = null
  filterDirectorate.value = null
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
