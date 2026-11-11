<template>
  <div class="rejected-questions-report-page pa-4 pa-md-6">
    <filter-fields label="معايير التصفية والبحث في سجل الأسئلة المرفوضة" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
      <template #fields>
        <!-- 1. اختيار نوع المؤسسة التعليمية الموحد بنمط النظام -->
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

        <!-- الظهور مشروط باختيار نوع المؤسسة: إما مدارس أو جامعات أو معاهد -->
        <template v-if="filterInstitutionType === 'school' || !filterInstitutionType || filterInstitutionType === 'all'">
          <!-- 🏫 فلاتر المدارس -->
          <auto-list
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            label="المرحلة الدراسية"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            @update:model-value="onStageChange"
          />
          <auto-list
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            placeholder="الصف والمسار"
            label="الصف والمسار"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            :disabled="!filterStage"
            @update:model-value="onClassTrackChange"
          />
          <auto-list
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            placeholder="المادة الدراسية"
            label="المادة الدراسية"
            cols="12"
            sm="6"
            md="3"
            :add="false"
            @update:model-value="onSubjectChange"
          />
          <auto-list
            v-model="filterUnit"
            name="UnitBySubject"
            :param="unitFilterParam"
            placeholder="الوحدة الدراسية"
            label="الوحدة الدراسية"
            cols="12"
            sm="6"
            md="2"
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
            label="الكلية الجامعية"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            @update:model-value="onCollegeChange"
          />
          <auto-list
            v-model="filterDepartment"
            name="DepartmentByCollege"
            :param="filterCollege"
            placeholder="القسم الأكاديمي"
            label="القسم الأكاديمي"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            :disabled="!filterCollege"
            @update:model-value="onDepartmentChange"
          />
          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            :param="filterDepartment"
            placeholder="التخصص والبرنامج"
            label="التخصص والبرنامج"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            :disabled="!filterDepartment"
            @update:model-value="onSpecializationChange"
          />
          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            :param="filterSpecialization"
            placeholder="مقرر الفصل الجامعي"
            label="مقرر الفصل الجامعي"
            cols="12"
            sm="6"
            md="3"
            :add="false"
            :disabled="!filterSpecialization"
            @update:model-value="onSemesterSubjectChange"
          />
          <auto-list
            v-model="filterUnit"
            name="UnitBySubject"
            :param="unitFilterParam"
            placeholder="مفردة / موضوع المقرر"
            label="مفردة / موضوع المقرر"
            cols="12"
            sm="6"
            md="2"
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
            label="المجال المهني / التقني"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            @update:model-value="onInstituteFieldChange"
          />
          <auto-list
            v-model="filterInstituteEducationSystem"
            name="InstituteEducationSystem"
            :param="filterInstituteField"
            placeholder="نظام التعليم والتدريب"
            label="نظام التعليم والتدريب"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            :disabled="!filterInstituteField"
            @update:model-value="onInstituteEducationSystemChange"
          />
          <auto-list
            v-model="filterInstituteSpecialization"
            name="InstituteSpecialization"
            :param="instituteSpecParam"
            placeholder="التخصص المهني"
            label="التخصص المهني"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            :disabled="!filterInstituteEducationSystem"
            @update:model-value="onInstituteSpecializationChange"
          />
          <auto-list
            v-model="filterInstituteSubject"
            name="InstituteSubject"
            :param="instituteSubjectParam"
            placeholder="المادة الدراسية للمعهد"
            label="المادة الدراسية للمعهد"
            cols="12"
            sm="6"
            md="3"
            :add="false"
            @update:model-value="onInstituteSubjectChange"
          />
          <auto-list
            v-model="filterUnit"
            name="UnitBySubject"
            :param="unitFilterParam"
            placeholder="الوحدة / التدريب العملي"
            label="الوحدة / التدريب العملي"
            cols="12"
            sm="6"
            md="2"
            :add="false"
            :disabled="!filterInstituteSubject"
          />
        </template>

        <!-- فلاتر التواريخ باستخدام CustomDate الموحد -->
        <custom-date
          v-model="filterDateFrom"
          label="من تاريخ"
          cols="12"
          sm="6"
          md="2"
          hide-details
        />

        <custom-date
          v-model="filterDateTo"
          label="إلى تاريخ"
          cols="12"
          sm="6"
          md="2"
          hide-details
        />

        <!-- أزرار الإجراءات الموحدة -->
        <v-col cols="auto" class="d-flex align-center gap-2 py-2">
          <custom-btn
            type="show"
            label="تصفية النتائج"
            icon="mdi-filter"
            class="font-weight-bold px-4"
            :loading="loading"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            variant="tonal"
            color="error"
            label="تفريغ الفلاتر"
            icon="mdi-filter-off"
            class="font-weight-bold"
            :click="resetFilters"
          />
        </v-col>
      </template>
    </filter-fields>

    <!-- جدول الأسئلة المرفوضة الموحد (custom-data-table) -->
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
          <template v-else-if="key === 'rejectionReason'">
            <span class="text-error font-weight-bold">{{ item.rejectionReason || 'لم يحدد سبب' }}</span>
          </template>
          <template v-else-if="key === 'contentPreview'">
            <span class="font-weight-medium text-on-surface">{{ item.contentPreview || item.content || '—' }}</span>
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

// نوع المؤسسة التعليمية الموحد (افتراضياً مدارس التعليم العام)
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

// فلاتر مشتركة
const filterSubject = ref(null)
const filterUnit = ref(null)
const filterDateFrom = ref(null)
const filterDateTo = ref(null)

// Computed Params for AutoLists
const subjectFilterParam = computed(() => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
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

// دوال تصفير الفلاتر التابعة عند تغيير المستويات الأعلى
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

// أعمدة الجدول
const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px', align: 'center' },
  { title: 'نص السؤال (مختصر)', key: 'contentPreview', sortable: false },
  { title: 'المادة', key: 'subject', sortable: true },
  { title: 'الوحدة', key: 'unit', sortable: true },
  { title: 'الدرس', key: 'lesson', sortable: true },
  { title: 'المؤلف', key: 'author', sortable: true },
  { title: 'المراجع', key: 'reviewer', sortable: true },
  { title: 'سبب الرفض', key: 'rejectionReason', sortable: false },
  { title: 'تاريخ الإنشاء', key: 'createdAt', sortable: true },
  { title: 'تاريخ الرفض', key: 'rejectedAt', sortable: true },
]

// بناء معايير الفلترة وإرسال ما يخص النوع المحدد فقط
const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }

  if (filterInstitutionType.value === 'school' || !filterInstitutionType.value || filterInstitutionType.value === 'all') {
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

  if (filterDateFrom.value) p.date_from = filterDateFrom.value
  if (filterDateTo.value) p.date_to = filterDateTo.value
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getRejectedQuestionsReport(buildParams())
    const results = Array.isArray(res) ? res : (res?.results || [])
    const count = res?.count !== undefined ? res.count : results.length
    items.value = {
      results,
      count,
    }
  } catch (e) {
    console.error(e)
    items.value = { results: [], count: 0 }
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
  filterUnit.value = null
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
