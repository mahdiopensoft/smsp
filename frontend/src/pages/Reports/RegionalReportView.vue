<template>
  <div class="regional-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في التقرير الإقليمي والجغرافي" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
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
          v-model="filterComparisonType"
          name="LocalTextOption"
          :objects="[
            { text: 'الكل (مدن ومناطق نائية)', value: 'all' },
            { text: 'المدن الرئيسية فقط', value: 'cities_only' },
            { text: 'المناطق النائية والريفية فقط', value: 'remote_only' }
          ]"
          cols="3"
          label="نوع المقارنة الجغرافية"
          icon="map-marker-radius-outline"
          :add="false"
          @update:model-value="applyFilters"
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
          <template v-else-if="key === 'average'">
            <span :class="getScoreClass(item.average)" class="font-weight-bold">
              {{ item.average }}%
            </span>
          </template>
          <template v-else-if="key === 'passRate'">
            <span>{{ item.passRate }}%</span>
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
const filterComparisonType = ref('all')

const onInstitutionTypeChange = () => {
  resetPagination()
  applyFilters()
}

const headers = [
  { title: 'المحافظة / المنطقة', key: 'name', sortable: true },
  { title: 'النوع', key: 'type', sortable: true, align: 'center' },
  { title: 'عدد الطلاب الممتحنين', key: 'students', sortable: true, align: 'center' },
  { title: 'المتوسط العام', key: 'average', sortable: true, align: 'center' },
  { title: 'نسبة النجاح', key: 'passRate', sortable: true, align: 'center' },
  { title: 'معامل العدالة', key: 'modifier', sortable: true, align: 'center' },
  { title: 'الاتجاه', key: 'trend', sortable: true, align: 'center' },
]

const getScoreClass = (val) => {
  if (val >= 75) return 'text-success'
  if (val >= 60) return 'text-primary'
  return 'text-error'
}

const applyFilters = async (tableParams = {}) => {
  const p = extractParams(tableParams)
  loading.value = true
  try {
    const query = {
      page: p.page,
      page_size: p.page_size,
    }
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      query.institution_type = filterInstitutionType.value
    }
    if (p.search) query.search = p.search
    if (p.sort_by) query.sort_by = p.sort_by

    const res = await reportsService.getRegionalReport(query)
    let results = res?.results || res?.governorates || (Array.isArray(res) ? res : [])
    if (filterComparisonType.value === 'cities_only') {
      results = results.filter(g => !g.isRemote)
    } else if (filterComparisonType.value === 'remote_only') {
      results = results.filter(g => g.isRemote)
    }
    setResponse({
      ...res,
      results
    })
  } catch (e) {
    console.error(e)
    setResponse({ results: [], count: 0 })
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filterInstitutionType.value = 'school'
  filterComparisonType.value = 'all'
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
