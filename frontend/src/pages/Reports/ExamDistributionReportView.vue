<template>
  <div class="exam-distribution-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل توزيع وإرسال الاختبارات" class="mb-4">
      <template #fields>
        <auto-list
          v-model="filters.exam"
          name="Exam"
          placeholder="الاختبار"
          cols="2"
          :add="false"
        />

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.status"
            :items="statusOptions"
            item-title="text"
            item-value="value"
            placeholder="حالة التوزيع"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.delivery_mode"
            :items="[
              { text: 'الكل', value: '' },
              { text: 'ورقي', value: 'printed_omr' },
              { text: 'إلكتروني', value: 'cbt_online' },
              { text: 'مزدوج', value: 'hybrid' }
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
          <v-text-field
            v-model="filters.date_from"
            type="date"
            label="من تاريخ الإرسال"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-text-field
            v-model="filters.date_to"
            type="date"
            label="إلى تاريخ الإرسال"
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
        <template #item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            size="small"
            variant="tonal"
          >
            {{ getStatusLabel(item.status) }}
          </v-chip>
        </template>
        <template #item.deliveryMode="{ item }">
          <span>{{ getDeliveryLabel(item.deliveryMode) }}</span>
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

const statusOptions = [
  { text: 'جميع الحالات', value: '' },
  { text: 'مسودة', value: 'draft' },
  { text: 'مجدول', value: 'scheduled' },
  { text: 'مُرسَل', value: 'dispatched' },
  { text: 'متاح للطباعة', value: 'accessible' },
  { text: 'جارٍ حالياً', value: 'in_progress' },
  { text: 'مكتمل', value: 'completed' },
  { text: 'ملغي', value: 'cancelled' },
]

const filters = ref({
  exam: null,
  status: '',
  delivery_mode: '',
  date_from: '',
  date_to: '',
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'عنوان التوزيع', key: 'title', sortable: true },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'المستوى المستهدف', key: 'targetLevel', sortable: true },
  { title: 'طريقة التسليم', key: 'deliveryMode', sortable: true, align: 'center' },
  { title: 'الحالة', key: 'status', sortable: true, align: 'center' },
  { title: 'تاريخ الإرسال المجدول', key: 'dispatchAt', sortable: true },
  { title: 'تاريخ الإتاحة', key: 'accessibleFrom', sortable: true },
  { title: 'بداية الاختبار', key: 'examStartAt', sortable: true },
  { title: 'نهاية الاختبار', key: 'examEndAt', sortable: true },
]

const getStatusColor = (status) => {
  const map = {
    completed: 'success',
    in_progress: 'info',
    dispatched: 'primary',
    accessible: 'teal',
    scheduled: 'warning',
    cancelled: 'error',
    draft: 'default',
  }
  return map[status] || 'default'
}

const getStatusLabel = (status) => {
  const map = {
    draft: 'مسودة',
    scheduled: 'مجدول',
    dispatched: 'مُرسَل',
    accessible: 'متاح للطباعة',
    in_progress: 'جارٍ حالياً',
    completed: 'مكتمل',
    cancelled: 'ملغي',
  }
  return map[status] || status
}

const getDeliveryLabel = (mode) => {
  const map = {
    printed_omr: 'طباعة OMR',
    cbt_online: 'إلكتروني CBT',
    hybrid: 'مزدوج',
  }
  return map[mode] || mode
}

const buildParams = () => {
  const p = {}
  if (filters.value.exam) p.exam = filters.value.exam
  if (filters.value.status) p.status = filters.value.status
  if (filters.value.delivery_mode) p.delivery_mode = filters.value.delivery_mode
  if (filters.value.date_from) p.date_from = filters.value.date_from
  if (filters.value.date_to) p.date_to = filters.value.date_to
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getExamDistributionReport(buildParams())
    items.value = res.results || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    exam: null,
    status: '',
    delivery_mode: '',
    date_from: '',
    date_to: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

