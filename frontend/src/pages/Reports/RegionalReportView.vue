<template>
  <div class="regional-report-page pa-4 pa-md-6">
    <filter-fields label="خيارات تصفية التقرير الإقليمي والجغرافي" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
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

        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterComparisonType"
            :items="[
              { text: 'جميع المحافظات', value: 'all' },
              { text: 'المدن الرئيسية فقط', value: 'cities_only' },
              { text: 'المناطق النائية فقط', value: 'remote_only' }
            ]"
            item-title="text"
            item-value="value"
            label="نطاق المقارنة"
            placeholder="نطاق المقارنة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="auto" class="d-flex align-center gap-2 py-2">
          <custom-btn type="filter" :loading="loading" :click="loadReport" />
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
        :items="filteredItems"
        :headers="headers"
        :getData="loadReport"
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
import { ref, computed, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(false)
const allItems = ref([])

// خيارات نوع المؤسسة بدون "الكل"
const filterInstitutionType = ref('school')

const filterComparisonType = ref('all')

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'المحافظة / المنطقة', key: 'name', sortable: true },
  { title: 'النوع', key: 'type', sortable: true, align: 'center' },
  { title: 'عدد الطلاب الممتحنين', key: 'students', sortable: true, align: 'center' },
  { title: 'المتوسط العام', key: 'average', sortable: true, align: 'center' },
  { title: 'نسبة النجاح', key: 'passRate', sortable: true, align: 'center' },
  { title: 'معامل العدالة', key: 'modifier', sortable: true, align: 'center' },
  { title: 'الاتجاه', key: 'trend', sortable: true, align: 'center' },
]

const filteredItems = computed(() => {
  if (filterComparisonType.value === 'cities_only') {
    return allItems.value.filter(g => !g.isRemote)
  }
  if (filterComparisonType.value === 'remote_only') {
    return allItems.value.filter(g => g.isRemote)
  }
  return allItems.value
})

const getScoreClass = (val) => {
  if (val >= 75) return 'text-success'
  if (val >= 60) return 'text-primary'
  return 'text-error'
}

const loadReport = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      params.institution_type = filterInstitutionType.value
    }
    const res = await reportsService.getRegionalReport(params)
    allItems.value = res.governorates || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filterInstitutionType.value = 'school'
  filterComparisonType.value = 'all'
  loadReport()
}

onMounted(loadReport)
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
