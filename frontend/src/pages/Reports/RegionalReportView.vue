<template>
  <div class="regional-report-page">
    <filter-fields label="خيارات تصفية التقرير الإقليمي والجغرافي" class="mb-4">
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
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="loadReport"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.comparisonType"
            :items="[
              { text: 'جميع المحافظات', value: 'all' },
              { text: 'المدن الرئيسية فقط', value: 'cities_only' },
              { text: 'المناطق النائية فقط', value: 'remote_only' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="نطاق المقارنة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="auto">
          <custom-btn type="filter" :loading="loading" :click="loadReport" />
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
        :items="filteredItems"
        :headers="headers"
        :loading="loading"
        :hasFilter="false"
        hover
      >
        <template #item.index="{ index }">{{ index + 1 }}</template>
        <template #item.average="{ item }">
          <span :class="getScoreClass(item.average)" class="font-weight-bold">
            {{ item.average }}%
          </span>
        </template>
        <template #item.passRate="{ item }">
          <span>{{ item.passRate }}%</span>
        </template>
      </custom-data-table>
    </CustomCard>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(false)
const allItems = ref([])

const filters = ref({
  institution_type: 'all',
  comparisonType: 'all',
})

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
  if (filters.value.comparisonType === 'cities_only') {
    return allItems.value.filter(g => !g.isRemote)
  }
  if (filters.value.comparisonType === 'remote_only') {
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
    if (filters.value.institution_type !== 'all') {
      params.institution_type = filters.value.institution_type
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
  filters.value = { institution_type: 'all', comparisonType: 'all' }
  loadReport()
}

onMounted(loadReport)
</script>
