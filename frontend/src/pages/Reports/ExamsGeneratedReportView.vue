<template>
  <div class="exams-generated-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل الاختبارات المولدة" class="mb-4">
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
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <auto-list
          v-model="filters.year"
          name="AcademicYear"
          placeholder="العام الدراسي"
          cols="2"
          :add="false"
        />

        <template v-if="filters.institution_type !== 'university'">
          <auto-list
            v-model="filters.stage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="filters.class_track = null"
          />
          <auto-list
            v-model="filters.class_track"
            name="ClassTrackByStage"
            :param="filters.stage"
            placeholder="الصف والمسار"
            cols="2"
            :add="false"
            :disabled="!filters.stage"
          />
          <auto-list
            v-model="filters.subject"
            name="Subject"
            placeholder="المادة الدراسية"
            cols="2"
            :add="false"
          />
        </template>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.is_approved"
            :items="[
              { text: 'الكل', value: '' },
              { text: 'معتمد', value: 'true' },
              { text: 'غير معتمد', value: 'false' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="حالة الاعتماد"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-text-field
            v-model="filters.date_from"
            type="date"
            label="من تاريخ"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-text-field
            v-model="filters.date_to"
            type="date"
            label="إلى تاريخ"
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
        <template #item.isApproved="{ item }">
          <v-chip
            :color="item.isApproved ? 'success' : 'warning'"
            size="small"
            variant="tonal"
          >
            {{ item.isApproved ? 'معتمد' : 'غير معتمد' }}
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
  year: null,
  stage: null,
  class_track: null,
  subject: null,
  is_approved: '',
  date_from: '',
  date_to: '',
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'عنوان الاختبار', key: 'title', sortable: true },
  { title: 'الكود الفريد', key: 'uniqueCode', sortable: true, width: '120px' },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'الصف / المسار', key: 'classTrack', sortable: true },
  { title: 'العام الدراسي', key: 'year', sortable: true, align: 'center' },
  { title: 'عدد النماذج', key: 'versionsCount', sortable: true, align: 'center' },
  { title: 'عدد الأسئلة', key: 'totalQuestions', sortable: true, align: 'center' },
  { title: 'الدرجة الكلية', key: 'totalMarks', sortable: true, align: 'center' },
  { title: 'حالة الاعتماد', key: 'isApproved', sortable: true, align: 'center' },
  { title: 'المعتمد بواسطة', key: 'approvedBy', sortable: true },
  { title: 'تاريخ الإنشاء', key: 'createdAt', sortable: true },
]

const onInstitutionTypeChange = () => {
  filters.value.stage = null
  filters.value.class_track = null
  filters.value.subject = null
  applyFilters()
}

const buildParams = () => {
  const p = {}
  if (filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.year) p.year = filters.value.year
  if (filters.value.stage) p.stage = filters.value.stage
  if (filters.value.class_track) p.class_track = filters.value.class_track
  if (filters.value.subject) p.subject = filters.value.subject
  if (filters.value.is_approved !== '') p.is_approved = filters.value.is_approved
  if (filters.value.date_from) p.date_from = filters.value.date_from
  if (filters.value.date_to) p.date_to = filters.value.date_to
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getExamsGeneratedReport(buildParams())
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
    year: null,
    stage: null,
    class_track: null,
    subject: null,
    is_approved: '',
    date_from: '',
    date_to: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

