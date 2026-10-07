<template>
  <div class="qb-exam-papers-report-v4">
    <!-- Filters Section -->
    <filter-fields :label="'معايير التصفية والتقرير'" class="mb-4">
      <template #fields>
        <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            placeholder="نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            class="mb-6"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- 🏫 School Filters -->
        <template v-if="filterInstitutionType === 'school'">
          <!-- Stage Filter -->
          <auto-list
            v-model="filter_fields.stageId"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="onStageChange"
          />

          <!-- ClassTrack Filter (الصف والمسار) -->
          <auto-list
            v-model="filter_fields.classTrackId"
            name="ClassTrackByStage"
            :param="filter_fields.stageId"
            placeholder="الصف والمسار"
            cols="2"
            :add="false"
            :disabled="!filter_fields.stageId"
          />
        </template>

        <!-- 🎓 University Filters -->
        <template v-if="filterInstitutionType === 'university'">
          <auto-list
            v-model="filter_fields.college"
            name="College"
            placeholder="الكلية الجامعية"
            cols="2"
            :add="false"
            @update:model-value="onCollegeChange"
          />
          <auto-list
            v-model="filter_fields.department"
            name="DepartmentByCollege"
            :param="filter_fields.college"
            placeholder="القسم الأكاديمي"
            cols="2"
            :add="false"
            :disabled="!filter_fields.college"
            @update:model-value="filter_fields.specialization = null"
          />
          <auto-list
            v-model="filter_fields.specialization"
            name="Specialization"
            :param="filter_fields.department"
            placeholder="التخصص والبرنامج"
            cols="2"
            :add="false"
            :disabled="!filter_fields.department"
          />
          <auto-list
            v-model="filter_fields.semesterSubject"
            name="SemesterSubject"
            :param="filter_fields.specialization"
            placeholder="مقرر الفصل الجامعي"
            cols="2"
            :add="false"
          />
        </template>

        <!-- Subject Filter (Schools only) -->
        <auto-list
          v-if="filterInstitutionType !== 'university'"
          v-model="filter_fields.subjectId"
          name="Subject"
          placeholder="المادة الدراسية"
          cols="2"
          :add="false"
        />

        <!-- Exam Filter -->
        <auto-list
          v-model="filter_fields.examId"
          name="Exam"
          :param="examFilterParam"
          :key="JSON.stringify(examFilterParam)"
          placeholder="الاختبار المستهدف"
          cols="2"
          :add="false"
        />

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="2">
          <v-text-field
            v-model="filter_fields.search"
            :placeholder="filterInstitutionType === 'university' ? 'بحث باسم الطالب أو الرقم الأكاديمي...' : 'بحث باسم الطالب أو رقم الجلوس...'"
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
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
            class="font-weight-bold rounded-lg px-6"
            label="إعادة ضبط"
            icon="mdi-refresh"
          />
        </v-col>
      </template>
    </filter-fields>

    <!-- Data Table -->
    <CustomCard class="glass-card rounded-xl overflow-hidden" elevation="0">
      <custom-data-table
        ref="table"
        v-bind="{
          items: filteredPapers,
          headers,
        }"
        hover
        class="bg-transparent"
        :items-per-page="15"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :customLoading="loading"
      >
        <!-- Student Name -->
        <template v-slot:item.studentName="{ item }">
          <div class="d-flex align-center py-2">
            <v-avatar size="36" color="primary" variant="tonal" class="me-3 font-weight-bold">
              <v-icon size="20">mdi-account</v-icon>
            </v-avatar>
            <div>
              <div class="font-weight-bold text-body-1">{{ item.studentName }}</div>
              <div class="text-caption text-medium-emphasis" v-if="item.governorateName">
                <v-icon size="12" class="me-1">mdi-map-marker</v-icon>{{ item.governorateName }}
              </div>
            </div>
          </div>
        </template>

        <!-- Student Code -->
        <template v-slot:item.studentCode="{ item }">
          <v-chip size="small" variant="outlined" color="primary" class="font-weight-bold font-mono">
            {{ item.studentCode || 'غير محدد' }}
          </v-chip>
        </template>

        <!-- Version / Model -->
        <template v-slot:item.versionLabel="{ item }">
          <v-chip size="small" :color="getVersionColor(item.versionLabel)" variant="tonal" class="font-weight-bold px-3">
            نموذج {{ item.versionLabel }}
          </v-chip>
        </template>

        <!-- Academic Info -->
        <template v-slot:item.academicInfo="{ item }">
          <div>
            <div class="font-weight-bold text-primary">{{ item.subjectName }}</div>
            <div class="text-caption text-medium-emphasis">{{ item.levelName }} - {{ item.branchName }}</div>
          </div>
        </template>

        <!-- Exam Title -->
        <template v-slot:item.examTitle="{ item }">
          <div class="d-flex align-center gap-1.5 flex-wrap">
            <v-chip
              size="x-small"
              :color="item.institutionType === 'university' ? 'deep-purple' : 'teal'"
              variant="tonal"
              class="font-weight-bold"
            >
              {{ item.institutionType === 'university' ? '🎓 جامعي' : '🏫 مدرسي' }}
            </v-chip>
            <span class="font-weight-medium">{{ item.examTitle }}</span>
          </div>
        </template>

        <!-- Questions Count -->
        <template v-slot:item.totalQuestions="{ item }">
          <v-chip color="indigo" variant="tonal" size="small" class="font-weight-bold px-3">
            {{ item.totalQuestions }} سؤال
          </v-chip>
        </template>

        <!-- Total Marks -->
        <template v-slot:item.totalMarks="{ item }">
          <v-chip color="emerald" variant="tonal" size="small" class="font-weight-bold px-3 text-success">
            {{ item.totalMarks }} درجة
          </v-chip>
        </template>

        <!-- Barcode -->
        <template v-slot:item.barcodeHash="{ item }">
          <div class="d-flex align-center font-mono text-caption text-medium-emphasis">
            <v-icon size="16" class="me-1">mdi-barcode</v-icon>
            <span>{{ item.barcodeHash ? item.barcodeHash.substring(0, 12) + '...' : '-' }}</span>
          </div>
        </template>
      </custom-data-table>
    </CustomCard>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(false)
const studentPapers = ref([])

// ──────────────────────────────────────────────────
// INSTITUTION & FILTERS STATE
// ──────────────────────────────────────────────────
const filterInstitutionType = ref('all')
const institutionTypeOptions = [
  { text: "الكل (مدارس وجامعات)", value: "all" },
  { text: "🏫 مدارس فقط", value: "school" },
  { text: "🎓 جامعات فقط", value: "university" },
]

const filter_fields = ref({
  stageId: null,
  classTrackId: null,
  college: null,
  department: null,
  specialization: null,
  semesterSubject: null,
  subjectId: null,
  examId: null,
  search: '',
})

const onInstitutionTypeChange = () => {
  filter_fields.value.stageId = null
  filter_fields.value.classTrackId = null
  filter_fields.value.college = null
  filter_fields.value.department = null
  filter_fields.value.specialization = null
  filter_fields.value.semesterSubject = null
  filter_fields.value.subjectId = null
  filter_fields.value.examId = null
  applyFilters()
}

const onStageChange = () => {
  filter_fields.value.classTrackId = null
}

const onCollegeChange = () => {
  filter_fields.value.department = null
  filter_fields.value.specialization = null
  filter_fields.value.semesterSubject = null
}

const examFilterParam = computed(() => {
  if (filterInstitutionType.value === 'university') {
    const p = { institution_type: 'university' }
    if (filter_fields.value.college) p.college = filter_fields.value.college
    if (filter_fields.value.department) p.department = filter_fields.value.department
    if (filter_fields.value.specialization) p.specialization = filter_fields.value.specialization
    if (filter_fields.value.semesterSubject) p.semester_subject = filter_fields.value.semesterSubject
    return p
  } else if (filterInstitutionType.value === 'school') {
    const p = { institution_type: 'school' }
    if (filter_fields.value.stageId) p.stage = filter_fields.value.stageId
    if (filter_fields.value.classTrackId) p.class_track = filter_fields.value.classTrackId
    if (filter_fields.value.subjectId) p.subject = filter_fields.value.subjectId
    return p
  }
  return filter_fields.value.subjectId ? filter_fields.value.subjectId : null
})

const applyFilters = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      params.institution_type = filterInstitutionType.value
    }
    if (filter_fields.value.stageId) params.stageId = filter_fields.value.stageId
    if (filter_fields.value.classTrackId) params.classTrackId = filter_fields.value.classTrackId
    if (filter_fields.value.college) params.college = filter_fields.value.college
    if (filter_fields.value.department) params.department = filter_fields.value.department
    if (filter_fields.value.specialization) params.specialization = filter_fields.value.specialization
    if (filter_fields.value.semesterSubject) params.semester_subject = filter_fields.value.semesterSubject
    if (filter_fields.value.subjectId) params.subjectId = filter_fields.value.subjectId
    if (filter_fields.value.examId) params.examId = filter_fields.value.examId
    if (filter_fields.value.search) params.search = filter_fields.value.search

    const res = await reportsService.getExamQualityReport(params)
    studentPapers.value = res.results || (Array.isArray(res) ? res : [])
  } catch (err) {
    console.error('Error loading exam papers report data:', err)
  } finally {
    loading.value = false
  }
}

const resetFilters = async () => {
  filterInstitutionType.value = 'all'
  filter_fields.value = {
    stageId: null,
    classTrackId: null,
    college: null,
    department: null,
    specialization: null,
    semesterSubject: null,
    subjectId: null,
    examId: null,
    search: '',
  }
  await applyFilters()
}

// Filtered items for DataTable
const filteredPapers = computed(() => {
  return studentPapers.value
})

// Table Headers (Dynamic by Institution Type)
const headers = computed(() => {
  const isUniv = filterInstitutionType.value === 'university'
  return [
    { title: 'اسم الطالب', key: 'studentName', sortable: true },
    { title: isUniv ? 'الرقم الأكاديمي' : 'رقم الجلوس', key: 'studentCode', sortable: true },
    { title: 'النموذج', key: 'versionLabel', sortable: true },
    { title: isUniv ? 'المقرر والتخصص' : 'المادة والصف', key: 'academicInfo', sortable: false },
    { title: 'الاختبار', key: 'examTitle', sortable: true },
    { title: 'عدد الأسئلة', key: 'totalQuestions', sortable: true },
    { title: 'الدرجة الكلية', key: 'totalMarks', sortable: true },
    { title: 'الباركود', key: 'barcodeHash', sortable: false },
  ]
})

// Version badge colors
const getVersionColor = (label) => {
  const map = { A: 'indigo', B: 'purple', C: 'amber', D: 'teal', 'أ': 'indigo', 'ب': 'purple', 'ج': 'amber', 'د': 'teal' }
  return map[label] || 'primary'
}

// Backend Data Fetching
onMounted(async () => {
  await applyFilters()
})
</script>

<style scoped>
.qb-exam-papers-report-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.glass-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.font-mono {
  font-family: monospace;
}
</style>
