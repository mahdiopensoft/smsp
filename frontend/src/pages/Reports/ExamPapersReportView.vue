<template>
  <div class="exam-papers-report-page">
    <filter-fields label="معايير التصفية والتقرير" class="mb-4">
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
            v-model="filters.stageId"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="filters.classTrackId = null"
          />
          <auto-list
            v-model="filters.classTrackId"
            name="ClassTrackByStage"
            :param="filters.stageId"
            placeholder="الصف والمسار"
            cols="2"
            :add="false"
            :disabled="!filters.stageId"
          />
          <auto-list
            v-model="filters.subjectId"
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
            @update:model-value="filters.department = null; filters.specialization = null; filters.semesterSubject = null"
          />
          <auto-list
            v-model="filters.department"
            name="DepartmentByCollege"
            :param="filters.college"
            placeholder="القسم"
            cols="2"
            :add="false"
            :disabled="!filters.college"
            @update:model-value="filters.specialization = null; filters.semesterSubject = null"
          />
          <auto-list
            v-model="filters.specialization"
            name="Specialization"
            :param="filters.department"
            placeholder="التخصص"
            cols="2"
            :add="false"
            :disabled="!filters.department"
            @update:model-value="filters.semesterSubject = null"
          />
          <auto-list
            v-model="filters.semesterSubject"
            name="SemesterSubject"
            :param="filters.specialization"
            placeholder="المقرر الجامعي"
            cols="2"
            :add="false"
            :disabled="!filters.specialization"
          />
        </template>

        <auto-list
          v-model="filters.examId"
          name="Exam"
          :param="examParam"
          :key="JSON.stringify(examParam)"
          placeholder="الاختبار المستهدف"
          cols="2"
          :add="false"
        />

        <v-col cols="12" md="2">
          <v-select
            v-model="filters.is_present"
            :items="[
              { text: 'الكل', value: '' },
              { text: 'حاضر', value: 'true' },
              { text: 'غائب', value: 'false' }
            ]"
            item-title="text"
            item-value="value"
            placeholder="حالة الحضور"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-text-field
            v-model="filters.search"
            placeholder="بحث باسم الطالب أو رقم الجلوس..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            hide-details
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
        <template #item.isPresent="{ item }">
          <v-chip
            :color="item.isPresent ? 'success' : 'error'"
            size="small"
            variant="tonal"
          >
            {{ item.isPresent ? 'حاضر' : 'غائب' }}
          </v-chip>
        </template>
        <template #item.barcodeHash="{ item }">
          <code class="text-caption font-mono">{{ item.barcodeHash }}</code>
        </template>
      </custom-data-table>
    </CustomCard>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(false)
const items = ref([])

const institutionTypeOptions = [
  { text: 'الكل (مدارس وجامعات)', value: 'all' },
  { text: 'مدارس فقط', value: 'school' },
  { text: 'جامعات فقط', value: 'university' },
]

const filters = ref({
  institution_type: 'all',
  stageId: null,
  classTrackId: null,
  subjectId: null,
  college: null,
  department: null,
  specialization: null,
  semesterSubject: null,
  examId: null,
  is_present: '',
  search: '',
})

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'اسم الطالب', key: 'studentName', sortable: true },
  { title: 'رقم الجلوس / الرقم الأكاديمي', key: 'studentCode', sortable: true },
  { title: 'الاختبار', key: 'examTitle', sortable: true },
  { title: 'النموذج', key: 'versionLabel', sortable: true, align: 'center' },
  { title: 'المادة والصف', key: 'academicInfo', sortable: false },
  { title: 'عدد الأسئلة', key: 'totalQuestions', sortable: true, align: 'center' },
  { title: 'الدرجة الكلية', key: 'totalMarks', sortable: true, align: 'center' },
  { title: 'حاضر؟', key: 'isPresent', sortable: true, align: 'center' },
  { title: 'الباركود', key: 'barcodeHash', sortable: false },
]

const examParam = computed(() => {
  const p = {}
  if (filters.value.institution_type && filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.stageId) p.stage = filters.value.stageId
  if (filters.value.classTrackId) p.class_track = filters.value.classTrackId
  if (filters.value.college) p.college = filters.value.college
  return Object.keys(p).length ? p : null
})

const onInstitutionTypeChange = () => {
  filters.value.stageId = null
  filters.value.classTrackId = null
  filters.value.subjectId = null
  filters.value.college = null
  filters.value.department = null
  filters.value.specialization = null
  filters.value.semesterSubject = null
  filters.value.examId = null
  applyFilters()
}

const buildParams = () => {
  const p = {}
  if (filters.value.institution_type && filters.value.institution_type !== 'all') {
    p.institution_type = filters.value.institution_type
  }
  if (filters.value.stageId) p.stageId = filters.value.stageId
  if (filters.value.classTrackId) p.classTrackId = filters.value.classTrackId
  if (filters.value.subjectId) p.subjectId = filters.value.subjectId
  if (filters.value.college) p.college = filters.value.college
  if (filters.value.department) p.department = filters.value.department
  if (filters.value.specialization) p.specialization = filters.value.specialization
  if (filters.value.semesterSubject) p.semester_subject = filters.value.semesterSubject
  if (filters.value.examId) p.examId = filters.value.examId
  if (filters.value.is_present !== '') p.is_present = filters.value.is_present
  if (filters.value.search) p.search = filters.value.search
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getExamQualityReport(buildParams())
    items.value = res.results || (Array.isArray(res) ? res : [])
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    institution_type: 'all',
    stageId: null,
    classTrackId: null,
    subjectId: null,
    college: null,
    department: null,
    specialization: null,
    semesterSubject: null,
    examId: null,
    is_present: '',
    search: '',
  }
  applyFilters()
}

onMounted(applyFilters)
</script>
