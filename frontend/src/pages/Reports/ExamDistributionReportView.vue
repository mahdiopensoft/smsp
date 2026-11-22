<template>
  <div class="exam-distribution-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في توزيع وإرسال الاختبارات" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
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
          v-model="filterExam"
          name="Exam"
          placeholder="الاختبار"
          cols="3"
          :add="false"
        />

        <v-col cols="12" md="2">
          <v-select
            v-model="filterStatus"
            :items="[
              { text: 'جميع الحالات', value: '' },
              { text: 'مجدول', value: 'scheduled' },
              { text: 'تم الإرسال', value: 'dispatched' },
              { text: 'مكتمل', value: 'completed' },
              { text: 'ملغي', value: 'cancelled' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="الحالة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filterDeliveryMode"
            :items="[
              { text: 'جميع الطرق', value: '' },
              { text: 'إلكتروني', value: 'online' },
              { text: 'ورقي (مطبوع)', value: 'paper' },
              { text: 'مدمج', value: 'hybrid' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="طريقة التسليم"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <custom-date-picker
            v-model="filterDateFrom"
            label="من تاريخ الإرسال"
            density="compact"
            variant="outlined"
            hide-details
          />
        </v-col>

        <v-col cols="12" md="2">
          <custom-date-picker
            v-model="filterDateTo"
            label="إلى تاريخ الإرسال"
            density="compact"
            variant="outlined"
            hide-details
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
          <template v-if="key === 'numbering'">
            <div class="d-flex justify-center align-center">
              <span class="font-weight-bold text-caption text-medium-emphasis">{{ ((items?.pagination?.current_page || 1) - 1) * (items?.pagination?.page_size || 20) + (index ?? 0) + 1 }}</span>
            </div>
          </template>
          <template v-else-if="key === 'status'">
            <v-chip
              :color="getStatusColor(item.status)"
              size="small"
              variant="tonal"
            >
              {{ getStatusLabel(item.status) }}
            </v-chip>
          </template>
          <template v-else-if="key === 'deliveryMode'">
            <span>{{ getDeliveryLabel(item.deliveryMode) }}</span>
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

const filterExam = ref(null)
const filterStatus = ref('')
const filterDeliveryMode = ref('')
const filterDateFrom = ref(null)
const filterDateTo = ref(null)

const headers = [
  { title: 'عنوان الإرسال', key: 'title', sortable: true },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'المستوى المستهدف', key: 'targetLevel', sortable: true, align: 'center' },
  { title: 'طريقة التسليم', key: 'deliveryMode', sortable: true, align: 'center' },
  { title: 'الحالة', key: 'status', sortable: true, align: 'center' },
  { title: 'تاريخ الإرسال', key: 'dispatchAt', sortable: true, align: 'center' },
  { title: 'بدء الاختبار', key: 'examStartAt', sortable: true, align: 'center' },
  { title: 'نهاية الاختبار', key: 'examEndAt', sortable: true, align: 'center' },
]

const getStatusColor = (status) => {
  const map = {
    scheduled: 'info',
    dispatched: 'primary',
    completed: 'success',
    cancelled: 'error',
  }
  return map[status] || 'default'
}

const getStatusLabel = (status) => {
  const map = {
    scheduled: 'مجدول',
    dispatched: 'تم الإرسال',
    completed: 'مكتمل',
    cancelled: 'ملغي',
  }
  return map[status] || status
}

const getDeliveryLabel = (mode) => {
  const map = {
    online: 'إلكتروني',
    paper: 'ورقي',
    hybrid: 'مدمج',
  }
  return map[mode] || mode
}

const onInstitutionTypeChange = () => {
  filterExam.value = null
  resetPagination()
  applyFilters()
}

const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }
  if (filterExam.value) p.exam = filterExam.value
  if (filterStatus.value) p.status = filterStatus.value
  if (filterDeliveryMode.value) p.delivery_mode = filterDeliveryMode.value
  if (filterDateFrom.value) p.date_from = filterDateFrom.value
  if (filterDateTo.value) p.date_to = filterDateTo.value
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

    const res = await reportsService.getExamDistributionReport(query)
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
  filterExam.value = null
  filterStatus.value = ''
  filterDeliveryMode.value = ''
  filterDateFrom.value = null
  filterDateTo.value = null
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
