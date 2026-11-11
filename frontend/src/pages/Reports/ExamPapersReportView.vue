<template>
  <div class="exam-papers-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والتقرير" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
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

        <!-- الظهور مشروط باختيار نوع المؤسسة -->
        <!-- الظهور مشروط باختيار نوع المؤسسة -->
        <template v-if="filterInstitutionType === 'school' || !filterInstitutionType || filterInstitutionType === 'all'">
          <!-- 🏫 فلاتر المدارس -->
            <auto-list
              v-model="filterStage"
              name="Stage"
              placeholder="المرحلة الدراسية"
              cols="2"
              :add="false"
              @update:model-value="onStageChange"
            />
            <auto-list
              v-model="filterClassTrack"
              name="ClassTrackByStage"
              :param="filterStage"
              placeholder="الصف والمسار"
              cols="2"
              :add="false"
              :disabled="!filterStage"
              @update:model-value="onClassTrackChange"
            />
            <auto-list
              v-model="filterSubject"
              name="Subject"
              :param="subjectFilterParam"
              placeholder="المادة الدراسية"
              cols="2"
              :add="false"
              @update:model-value="onSubjectChange"
            />
          </template>

          <!-- 🎓 فلاتر الجامعات -->
          <template v-if="filterInstitutionType === 'university'">
            <auto-list
              v-model="filterCollege"
              name="College"
              placeholder="الكلية الجامعية"
              cols="2"
              :add="false"
              @update:model-value="onCollegeChange"
            />
            <auto-list
              v-model="filterDepartment"
              name="DepartmentByCollege"
              :param="filterCollege"
              placeholder="القسم الأكاديمي"
              cols="2"
              :add="false"
              :disabled="!filterCollege"
              @update:model-value="onDepartmentChange"
            />
            <auto-list
              v-model="filterSpecialization"
              name="Specialization"
              :param="filterDepartment"
              placeholder="التخصص والبرنامج"
              cols="2"
              :add="false"
              :disabled="!filterDepartment"
              @update:model-value="onSpecializationChange"
            />
            <auto-list
              v-model="filterSemesterSubject"
              name="SemesterSubject"
              :param="filterSpecialization"
              placeholder="مقرر الفصل الجامعي"
              cols="2"
              :add="false"
              :disabled="!filterSpecialization"
              @update:model-value="onSemesterSubjectChange"
            />
          </template>

          <!-- 🏢 فلاتر المعاهد والتدريب المهني -->
          <template v-if="filterInstitutionType === 'institute'">
            <auto-list
              v-model="filterInstituteField"
              name="InstituteField"
              placeholder="المجال المهني / التقني"
              cols="2"
              :add="false"
              @update:model-value="onInstituteFieldChange"
            />
            <auto-list
              v-model="filterInstituteEducationSystem"
              name="InstituteEducationSystem"
              :param="filterInstituteField"
              placeholder="نظام التعليم والتدريب"
              cols="2"
              :add="false"
              :disabled="!filterInstituteField"
              @update:model-value="onInstituteEducationSystemChange"
            />
            <auto-list
              v-model="filterInstituteSpecialization"
              name="InstituteSpecialization"
              :param="instituteSpecParam"
              placeholder="التخصص المهني"
              cols="2"
              :add="false"
              :disabled="!filterInstituteEducationSystem"
              @update:model-value="onInstituteSpecializationChange"
            />
            <auto-list
              v-model="filterInstituteSubject"
              name="InstituteSubject"
              :param="instituteSubjectParam"
              placeholder="المادة الدراسية للمعهد"
              cols="2"
              :add="false"
              @update:model-value="onInstituteSubjectChange"
            />
          </template>

        <auto-list
          v-model="filterExamId"
          name="Exam"
          :param="examParam"
          :key="JSON.stringify(examParam)"
          placeholder="الاختبار المستهدف"
          cols="2"
          :add="false"
        />

        <v-col cols="12" md="2">
          <v-select
            v-model="filterIsPresent"
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
            v-model="filterSearch"
            placeholder="بحث باسم الطالب أو رقم الجلوس..."
            prepend-inner-icon="mdi-magnify"
            clearable
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
          <template v-if="key === 'index'">
            <div class="d-flex justify-center align-center">
              <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
            </div>
          </template>
          <template v-else-if="key === 'isPresent'">
            <v-chip
              :color="item.isPresent ? 'success' : 'error'"
              size="small"
              variant="tonal"
            >
              {{ item.isPresent ? 'حاضر' : 'غائب' }}
            </v-chip>
          </template>
          <template v-else-if="key === 'barcodeHash'">
            <code class="text-caption font-mono">{{ item.barcodeHash }}</code>
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
const items = ref({
  results: [],
  count: 0,
})

// المؤسسة التعليمية
const filterInstitutionType = ref('school')

// فلاتر المدارس
const filterStage = ref(null)
const filterClassTrack = ref(null)

// فلاتر الجامعات
const filterCollege = ref(null)
const filterDepartment = ref(null)
const filterSpecialization = ref(null)
const filterSemesterSubject = ref(null)

// فلاتر المعاهد
const filterInstituteField = ref(null)
const filterInstituteEducationSystem = ref(null)
const filterInstituteSpecialization = ref(null)
const filterInstituteSubject = ref(null)

// فلاتر عامة
const filterSubject = ref(null)
const filterExamId = ref(null)
const filterIsPresent = ref('')
const filterSearch = ref('')

const subjectFilterParam = computed(() => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') p.institution_type = filterInstitutionType.value
  if (filterClassTrack.value) p.class_track = filterClassTrack.value
  else if (filterStage.value) p.stage = filterStage.value
  return Object.keys(p).length ? p : null
})

const instituteSpecParam = computed(() => {
  const p = {}
  if (filterInstituteField.value) p.field = filterInstituteField.value
  if (filterInstituteEducationSystem.value) p.education_system = filterInstituteEducationSystem.value
  return Object.keys(p).length ? p : null
})

const instituteSubjectParam = computed(() => {
  if (filterInstituteField.value) return { field: filterInstituteField.value }
  return null
})

const examParam = computed(() => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') p.institution_type = filterInstitutionType.value
  if (filterStage.value) p.stage = filterStage.value
  if (filterClassTrack.value) p.class_track = filterClassTrack.value
  if (filterCollege.value) p.college = filterCollege.value
  if (filterSemesterSubject.value) p.semester_subject = filterSemesterSubject.value
  return Object.keys(p).length ? p : null
})

const onInstitutionTypeChange = () => {
  filterStage.value = null
  filterClassTrack.value = null
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterInstituteField.value = null
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  filterSubject.value = null
  filterExamId.value = null
  applyFilters()
}

const onStageChange = () => {
  filterClassTrack.value = null
  filterSubject.value = null
  filterExamId.value = null
}

const onClassTrackChange = () => {
  filterSubject.value = null
  filterExamId.value = null
}

const onSubjectChange = () => {
  filterExamId.value = null
}

const onCollegeChange = () => {
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterExamId.value = null
}

const onDepartmentChange = () => {
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterExamId.value = null
}

const onSpecializationChange = () => {
  filterSemesterSubject.value = null
  filterExamId.value = null
}

const onSemesterSubjectChange = () => {
  filterExamId.value = null
}

const onInstituteFieldChange = () => {
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  filterExamId.value = null
}

const onInstituteEducationSystemChange = () => {
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  filterExamId.value = null
}

const onInstituteSpecializationChange = () => {
  filterInstituteSubject.value = null
  filterExamId.value = null
}

const onInstituteSubjectChange = () => {
  filterExamId.value = null
}

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

const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }

  if (filterInstitutionType.value === 'school' || !filterInstitutionType.value || filterInstitutionType.value === 'all') {
    if (filterStage.value) p.stageId = filterStage.value
    if (filterClassTrack.value) p.classTrackId = filterClassTrack.value
    if (filterSubject.value) p.subjectId = filterSubject.value
  } else if (filterInstitutionType.value === 'university') {
    if (filterCollege.value) p.college = filterCollege.value
    if (filterDepartment.value) p.department = filterDepartment.value
    if (filterSpecialization.value) p.specialization = filterSpecialization.value
    if (filterSemesterSubject.value) p.semester_subject = filterSemesterSubject.value
  } else if (filterInstitutionType.value === 'institute') {
    if (filterInstituteField.value) p.field = filterInstituteField.value
    if (filterInstituteEducationSystem.value) p.education_system = filterInstituteEducationSystem.value
    if (filterInstituteSpecialization.value) p.specialization = filterInstituteSpecialization.value
    if (filterInstituteSubject.value) p.subjectId = filterInstituteSubject.value
  }

  if (filterExamId.value) p.examId = filterExamId.value
  if (filterIsPresent.value !== '') p.is_present = filterIsPresent.value
  if (filterSearch.value) p.search = filterSearch.value
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
  filterInstitutionType.value = 'school'
  filterStage.value = null
  filterClassTrack.value = null
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterInstituteField.value = null
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  filterSubject.value = null
  filterExamId.value = null
  filterIsPresent.value = ''
  filterSearch.value = ''
  applyFilters()
}

onMounted(applyFilters)
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
