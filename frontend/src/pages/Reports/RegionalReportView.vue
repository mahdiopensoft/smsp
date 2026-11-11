<template>
  <div class="regional-report-page">
    <filter-fields label="خيارات تصفية التقرير الإقليمي والجغرافي" class="mb-4">
      <template #fields>
        <!-- اختيار نوع المؤسسة التعليمية (مدارس / جامعات / معاهد) بدون خيار الكل -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            label="نوع المؤسسة التعليمية"
            placeholder="اختر نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            clearable
            density="compact"
            variant="outlined"
            @update:model-value="loadReport"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :prepend-icon="item.raw.icon" />
            </template>
          </v-select>
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

// خيارات نوع المؤسسة بدون "الكل"
const filterInstitutionType = ref(null)
const institutionTypeOptions = [
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]

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
    if (filterInstitutionType.value) {
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
  filterInstitutionType.value = null
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
