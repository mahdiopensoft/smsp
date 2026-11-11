<template>
  <div class="questions-detail-report-page">
    <filter-fields label="معايير التصفية والبحث في بنك الأسئلة التفصيلي" class="mb-4">
      <template #fields>
        <v-col cols="12" md="2">
          <v-select
            v-model="filters.institution_type"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            placeholder="نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

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

        <template v-if="filters.institution_type !== 'school'">
          <auto-list
            v-model="filters.college"
            name="College"
            placeholder="الكلية"
            cols="2"
            :add="false"
            @update:model-value="filters.department = null; filters.specialization = null; filters.semester_subject = null"
          />
          <auto-list
            v-model="filters.department"
            name="DepartmentByCollege"
            :param="filters.college"
            placeholder="القسم"
            cols="2"
            :add="false"
            :disabled="!filters.college"
            @update:model-value="filters.specialization = null; filters.semester_subject = null"
          />
          <auto-list
            v-model="filters.specialization"
            name="Specialization"
            :param="filters.department"
            placeholder="التخصص"
            cols="2"
            :add="false"
            :disabled="!filters.department"
            @update:model-value="filters.semester_subject = null"
          />
          <auto-list
            v-model="filters.semester_subject"
            name="SemesterSubject"
            :param="filters.specialization"
            placeholder="المقرر الجامعي"
            cols="2"
            :add="false"
            :disabled="!filters.specialization"
          />
        </template>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.question_type"
            :items="questionTypeOptions"
            item-title="text"
            item-value="value"
            placeholder="نوع السؤال"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.difficulty"
            :items="difficultyOptions"
            item-title="text"
            item-value="value"
            placeholder="مستوى الصعوبة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.bloom_level"
            :items="bloomOptions"
            item-title="text"
            item-value="value"
            placeholder="مستوى بلوم"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.status"
            :items="statusOptions"
            item-title="text"
            item-value="value"
            placeholder="حالة السؤال"
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
        <template #item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            size="small"
            variant="tonal"
          >
            {{ item.status }}
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

const institutionTypeOptions = [
  { text: 'الكل', value: 'all' },
  { text: 'مدارس فقط', value: 'school' },
  { text: 'جامعات فقط', value: 'university' },
]

const questionTypeOptions = [
  { text: 'جميع الأنواع', value: '' },
  { text: 'اختيار من متعدد', value: 'Single Choice' },
  { text: 'اختيار متعدد الإجابات', value: 'Multiple Choice' },
  { text: 'صح وخطأ', value: 'True/False' },
  { text: 'مقالي', value: 'Essay' },
  { text: 'ملء الفراغ', value: 'Fill in the Blanks' },
  { text: 'توافق', value: 'Matching' },
  { text: 'ترتيب', value: 'Ordering' },
  { text: 'دراسة حالة', value: 'Case Study' },
]

const difficultyOptions = [
  { text: 'جميع المستويات', value: '' },
  { text: 'سهل', value: '1' },
  { text: 'متوسط', value: '2' },
  { text: 'صعب', value: '3' },
]

const bloomOptions = [
  { text: 'جميع المستويات', value: '' },
  { text: 'تذكر', value: 'تذكر' },
  { text: 'فهم', value: 'فهم' },
  { text: 'تطبيق', value: 'تطبيق' },
  { text: 'تحليل', value: 'تحليل' },
  { text: 'تقييم', value: 'تقييم' },
  { text: 'ابتكار', value: 'ابتكار' },
]

const statusOptions = [
  { text: 'جميع الحالات', value: '' },
  { text: 'مسودة', value: 'مسودة' },
  { text: 'قيد المراجعة', value: 'قيد المراجعة' },
  { text: 'معتمد', value: 'معتمد' },
  { text: 'مرفوض', value: 'مرفوض' },
  { text: 'مؤرشف', value: 'مؤرشف' },
  { text: 'معطل', value: 'معطل' },
]

const filters = ref({
  institution_type: 'all',
  question_type: '',
  difficulty: '',
  bloom_level: '',
  status: '',
  date_from: '',
  date_to: '',
  stage: null,
  class_track: null,
  subject: null,
  college: null,
  department: null,
  specialization: null,
  semester_subject: null,
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'نص السؤال (مختصر)', key: 'contentPreview', sortable: false },
  { title: 'نوع السؤال', key: 'questionType', sortable: true, align: 'center' },
  { title: 'الصعوبة', key: 'difficultyLabel', sortable: true, align: 'center' },
  { title: 'مستوى بلوم', key: 'bloomLevel', sortable: true, align: 'center' },
  { title: 'الحالة', key: 'status', sortable: true, align: 'center' },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'الوحدة', key: 'unit', sortable: true },
  { title: 'الدرس', key: 'lesson', sortable: true },
  { title: 'المؤلف', key: 'author', sortable: true },
  { title: 'تاريخ الإنشاء', key: 'createdAt', sortable: true },
  { title: 'تاريخ الاعتماد', key: 'approvedAt', sortable: true },
]

const getStatusColor = (status) => {
  if (status === 'معتمد') return 'success'
  if (status === 'قيد المراجعة') return 'warning'
  if (status === 'مرفوض') return 'error'
  return 'default'
}

const onInstitutionTypeChange = () => {
  filters.value.stage = null
  filters.value.class_track = null
  filters.value.subject = null
  filters.value.college = null
  filters.value.department = null
  filters.value.specialization = null
  filters.value.semester_subject = null
  applyFilters()
}

const buildParams = () => {
  const p = {}
  if (filters.value.institution_type && filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.stage) p.stage = filters.value.stage
  if (filters.value.class_track) p.class_track = filters.value.class_track
  if (filters.value.subject) p.subject = filters.value.subject
  if (filters.value.college) p.college = filters.value.college
  if (filters.value.department) p.department = filters.value.department
  if (filters.value.specialization) p.specialization = filters.value.specialization
  if (filters.value.semester_subject) p.semester_subject = filters.value.semester_subject
  if (filters.value.question_type) p.question_type = filters.value.question_type
  if (filters.value.difficulty) p.difficulty = filters.value.difficulty
  if (filters.value.bloom_level) p.bloom_level = filters.value.bloom_level
  if (filters.value.status) p.status = filters.value.status
  if (filters.value.date_from) p.date_from = filters.value.date_from
  if (filters.value.date_to) p.date_to = filters.value.date_to
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getQuestionsDetailReport(buildParams())
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
    question_type: '',
    difficulty: '',
    bloom_level: '',
    status: '',
    date_from: '',
    date_to: '',
    stage: null,
    class_track: null,
    subject: null,
    college: null,
    department: null,
    specialization: null,
    semester_subject: null,
  }
  applyFilters()
}

onMounted(applyFilters)
</script>

