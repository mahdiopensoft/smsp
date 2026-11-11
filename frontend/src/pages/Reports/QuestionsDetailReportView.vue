<template>
  <div class="questions-detail-report-page">
    <filter-fields label="معايير التصفية والبحث في بنك الأسئلة التفصيلي" class="mb-4">
      <template #fields>
        <!-- اختيار نوع المؤسسة التعليمية (مدارس / جامعات / معاهد) بدون خيار الكل -->
        <v-col cols="12" sm="6" :md="filterInstitutionType ? 3 : 4">
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

        <!-- الظهور مشروط باختيار نوع المؤسسة: إما مدارس أو جامعات أو معاهد -->
        <template v-if="filterInstitutionType">
          <!-- 🏫 فلاتر المدارس -->
          <template v-if="filterInstitutionType === 'school'">
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
            <auto-list
              v-model="filterUnit"
              name="UnitBySubject"
              :param="unitFilterParam"
              placeholder="الوحدة الدراسية"
              cols="2"
              :add="false"
              :disabled="!filterSubject"
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
            <auto-list
              v-model="filterUnit"
              name="UnitBySubject"
              :param="unitFilterParam"
              placeholder="مفردة / موضوع المقرر"
              cols="2"
              :add="false"
              :disabled="!filterSemesterSubject"
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
            <auto-list
              v-model="filterUnit"
              name="UnitBySubject"
              :param="unitFilterParam"
              placeholder="الوحدة / التدريب العملي"
              cols="2"
              :add="false"
              :disabled="!filterInstituteSubject"
            />
          </template>
        </template>

        <!-- خصائص السؤال المشتركة -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterQuestionType"
            :items="questionTypeOptions"
            item-title="text"
            item-value="value"
            placeholder="نوع السؤال"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterDifficulty"
            :items="difficultyOptions"
            item-title="text"
            item-value="value"
            placeholder="مستوى الصعوبة"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterBloomLevel"
            :items="bloomOptions"
            item-title="text"
            item-value="value"
            placeholder="مستوى بلوم"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterStatus"
            :items="statusOptions"
            item-title="text"
            item-value="value"
            placeholder="حالة السؤال"
            hide-details
            density="compact"
            variant="outlined"
          />
        </v-col>

        <!-- فلاتر التواريخ باستخدام CustomDate الموحد -->
        <custom-date
          v-model="filterDateFrom"
          label="من تاريخ"
          cols="2"
          hide-details
        />

        <custom-date
          v-model="filterDateTo"
          label="إلى تاريخ"
          cols="2"
          hide-details
        />

        <!-- أزرار الإجراءات -->
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

    <!-- جدول بنك الأسئلة التفصيلي -->
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
            size="small"
            :color="getStatusColor(item.status)"
            variant="tonal"
            class="font-weight-medium"
          >
            {{ item.status || 'غير محدد' }}
          </v-chip>
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

// خيارات نوع المؤسسة التعليمية - بدون خيار "الكل"
const filterInstitutionType = ref(null)
const institutionTypeOptions = [
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]

// خيارات أنواع الأسئلة والصعوبة وبلوم والحالة
const filterQuestionType = ref('')
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

const filterDifficulty = ref('')
const difficultyOptions = [
  { text: 'جميع المستويات', value: '' },
  { text: 'سهل', value: '1' },
  { text: 'متوسط', value: '2' },
  { text: 'صعب', value: '3' },
]

const filterBloomLevel = ref('')
const bloomOptions = [
  { text: 'جميع المستويات', value: '' },
  { text: 'تذكر', value: 'تذكر' },
  { text: 'فهم', value: 'فهم' },
  { text: 'تطبيق', value: 'تطبيق' },
  { text: 'تحليل', value: 'تحليل' },
  { text: 'تقييم', value: 'تقييم' },
  { text: 'ابتكار', value: 'ابتكار' },
]

const filterStatus = ref('')
const statusOptions = [
  { text: 'جميع الحالات', value: '' },
  { text: 'مسودة', value: 'مسودة' },
  { text: 'قيد المراجعة', value: 'قيد المراجعة' },
  { text: 'معتمد', value: 'معتمد' },
  { text: 'مرفوض', value: 'مرفوض' },
  { text: 'مؤرشف', value: 'مؤرشف' },
  { text: 'معطل', value: 'معطل' },
]

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

// فلاتر مشتركة
const filterSubject = ref(null)
const filterUnit = ref(null)
const filterDateFrom = ref(null)
const filterDateTo = ref(null)

// Computed Params for AutoLists
const subjectFilterParam = computed(() => {
  const p = {}
  if (filterInstitutionType.value) {
    p.institution_type = filterInstitutionType.value
  }
  if (filterClassTrack.value) {
    p.class_track = filterClassTrack.value
  } else if (filterStage.value) {
    p.stage = filterStage.value
  }
  return Object.keys(p).length > 0 ? p : null
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

const unitFilterParam = computed(() => {
  if (filterInstitutionType.value === 'university') {
    return filterSemesterSubject.value ? { semester_subject: filterSemesterSubject.value } : null
  }
  if (filterInstitutionType.value === 'institute') {
    return filterInstituteSubject.value ? { subject: filterInstituteSubject.value } : null
  }
  return filterSubject.value || null
})

// دوال تغيير وتصفير الفلاتر التابعة
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
  filterUnit.value = null
  applyFilters()
}

const onStageChange = () => {
  filterClassTrack.value = null
  filterSubject.value = null
  filterUnit.value = null
}

const onClassTrackChange = () => {
  filterSubject.value = null
  filterUnit.value = null
}

const onSubjectChange = () => {
  filterUnit.value = null
}

const onCollegeChange = () => {
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterUnit.value = null
}

const onDepartmentChange = () => {
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterUnit.value = null
}

const onSpecializationChange = () => {
  filterSemesterSubject.value = null
  filterUnit.value = null
}

const onSemesterSubjectChange = () => {
  filterUnit.value = null
}

const onInstituteFieldChange = () => {
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  filterUnit.value = null
}

const onInstituteEducationSystemChange = () => {
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  filterUnit.value = null
}

const onInstituteSpecializationChange = () => {
  filterInstituteSubject.value = null
  filterUnit.value = null
}

const onInstituteSubjectChange = () => {
  filterUnit.value = null
}

// ألوان الحالة
const getStatusColor = (status) => {
  if (status === 'معتمد') return 'success'
  if (status === 'قيد المراجعة') return 'warning'
  if (status === 'مرفوض') return 'error'
  return 'default'
}

// أعمدة الجدول
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

// بناء معايير الفلترة وإرسال ما يخص النوع المحدد فقط
const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value) {
    p.institution_type = filterInstitutionType.value
  }

  if (filterInstitutionType.value === 'school') {
    if (filterStage.value) p.stage = filterStage.value
    if (filterClassTrack.value) p.class_track = filterClassTrack.value
    if (filterSubject.value) p.subject = filterSubject.value
    if (filterUnit.value) p.unit = filterUnit.value
  } else if (filterInstitutionType.value === 'university') {
    if (filterCollege.value) p.college = filterCollege.value
    if (filterDepartment.value) p.department = filterDepartment.value
    if (filterSpecialization.value) p.specialization = filterSpecialization.value
    if (filterSemesterSubject.value) p.semester_subject = filterSemesterSubject.value
    if (filterUnit.value) p.unit = filterUnit.value
  } else if (filterInstitutionType.value === 'institute') {
    if (filterInstituteField.value) p.field = filterInstituteField.value
    if (filterInstituteEducationSystem.value) p.education_system = filterInstituteEducationSystem.value
    if (filterInstituteSpecialization.value) p.specialization = filterInstituteSpecialization.value
    if (filterInstituteSubject.value) p.institute_subject = filterInstituteSubject.value
    if (filterUnit.value) p.unit = filterUnit.value
  }

  if (filterQuestionType.value) p.question_type = filterQuestionType.value
  if (filterDifficulty.value) p.difficulty = filterDifficulty.value
  if (filterBloomLevel.value) p.bloom_level = filterBloomLevel.value
  if (filterStatus.value) p.status = filterStatus.value
  if (filterDateFrom.value) p.date_from = filterDateFrom.value
  if (filterDateTo.value) p.date_to = filterDateTo.value
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
  filterInstitutionType.value = null
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
  filterUnit.value = null
  filterQuestionType.value = ''
  filterDifficulty.value = ''
  filterBloomLevel.value = ''
  filterStatus.value = ''
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
