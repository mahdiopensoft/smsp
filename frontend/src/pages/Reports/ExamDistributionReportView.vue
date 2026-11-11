<template>
  <div class="exam-distribution-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل توزيع وإرسال الاختبارات" class="mb-4">
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
            @update:model-value="onInstitutionTypeChange"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :prepend-icon="item.raw.icon" />
            </template>
          </v-select>
        </v-col>

        <auto-list
          v-model="filterExam"
          name="Exam"
          placeholder="الاختبار"
          cols="2"
          :add="false"
        />

        <v-col cols="12" md="2">
          <v-select
            v-model="filterStatus"
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
            v-model="filterDeliveryMode"
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

        <!-- فلاتر التواريخ باستخدام CustomDate الموحد -->
        <custom-date
          v-model="filterDateFrom"
          label="من تاريخ الإرسال"
          cols="2"
          hide-details
        />

        <custom-date
          v-model="filterDateTo"
          label="إلى تاريخ الإرسال"
          cols="2"
          hide-details
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

// خيارات نوع المؤسسة بدون "الكل"
const filterInstitutionType = ref(null)
const institutionTypeOptions = [
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]

const filterExam = ref(null)
const filterStatus = ref('')
const filterDeliveryMode = ref('')
const filterDateFrom = ref(null)
const filterDateTo = ref(null)

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

const onInstitutionTypeChange = () => {
  filterExam.value = null
  applyFilters()
}

const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value) {
    p.institution_type = filterInstitutionType.value
  }
  if (filterExam.value) p.exam = filterExam.value
  if (filterStatus.value) p.status = filterStatus.value
  if (filterDeliveryMode.value) p.delivery_mode = filterDeliveryMode.value
  if (filterDateFrom.value) p.date_from = filterDateFrom.value
  if (filterDateTo.value) p.date_to = filterDateTo.value
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
  filterInstitutionType.value = null
  filterExam.value = null
  filterStatus.value = ''
  filterDeliveryMode.value = ''
  filterDateFrom.value = null
  filterDateTo.value = null
  applyFilters()
}

onMounted(applyFilters)
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
