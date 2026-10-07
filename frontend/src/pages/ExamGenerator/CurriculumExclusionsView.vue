<template>
  <div class="qb-curriculum-exclusions-v4 pa-4 pa-md-8">
    <!-- Header Section -->
    <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-6">
      <div class="d-flex align-center">
        <v-avatar size="50" color="error" variant="tonal" class="me-4 rounded-2xl">
          <v-icon size="28">mdi-book-remove-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-slate-800 mb-1">المحذوفات من المنهج والمقررات</h1>
          <span class="text-caption text-medium-emphasis">
            تحديد الوحدات والدروس المستبعدة من بنك الأسئلة وتوليد الاختبارات سنوياً بقرار وزاري أو أكاديمي
          </span>
        </div>
      </div>

      <!-- Tab Toggle -->
      <div class="d-flex align-center gap-2">
        <v-btn-toggle
          v-model="currentViewTab"
          mandatory
          density="compact"
          color="primary"
          rounded="lg"
          variant="outlined"
        >
          <v-btn value="manage">
            <v-icon start size="16">mdi-format-list-checks</v-icon>
            تحديد المحذوفات
          </v-btn>
          <v-btn value="list">
            <v-icon start size="16">mdi-archive-outline</v-icon>
            سجل المحذوفات المعتمدة
          </v-btn>
        </v-btn-toggle>
      </div>
    </div>

    <!-- TAB 1: MANAGE EXCLUSIONS -->
    <div v-if="currentViewTab === 'manage'">
      <!-- Institution Type & Academic Year Toggle Bar -->
      <v-card class="main-card pa-5 rounded-2xl border-subtle mb-6" elevation="0">
        <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-4 pb-4 border-b">
          <div class="d-flex align-center gap-3 flex-wrap">
            <span class="text-subtitle-2 font-weight-bold text-slate-700">نوع المؤسسة التعليمية:</span>
            <v-btn-toggle
              v-model="institutionType"
              mandatory
              density="compact"
              color="primary"
              rounded="lg"
              variant="outlined"
              @update:model-value="onInstitutionTypeChange"
            >
              <v-btn value="school">
                <v-icon start size="16">mdi-school-outline</v-icon>
                مدارس (التعليم العام)
              </v-btn>
              <v-btn value="university">
                <v-icon start size="16">mdi-town-hall</v-icon>
                جامعات وكليات
              </v-btn>
              <v-btn value="institute">
                <v-icon start size="16">mdi-tools</v-icon>
                معاهد وتدريب مهني
              </v-btn>
            </v-btn-toggle>
          </div>

          <div style="min-width: 250px;">
            <auto-list
              v-model="selectedYearId"
              name="AcademicYear"
              placeholder="العام الدراسي *"
              cols="12"
              :add="false"
              @update:model-value="onYearOrSubjectChange"
            />
          </div>
        </div>

        <!-- Cascading Filter Controls -->
        <v-row dense class="align-center">
          <!-- 🏫 SCHOOL SELECTORS -->
          <template v-if="institutionType === 'school'">
            <auto-list
              v-model="selectedStageId"
              name="EducationalStage"
              placeholder="المرحلة الدراسية"
              cols="4"
              :add="false"
              @update:model-value="() => { selectedClassTrackId = null; selectedSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedClassTrackId"
              name="SchoolClassTrack"
              :param="selectedStageId"
              placeholder="الصف والمسار الدراسي *"
              cols="4"
              :add="false"
              :disabled="!selectedStageId"
              @update:model-value="() => { selectedSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedSubjectId"
              name="Subject"
              :param="selectedClassTrackId"
              placeholder="المادة الدراسية *"
              cols="4"
              :add="false"
              :disabled="!selectedClassTrackId"
              @update:model-value="onYearOrSubjectChange"
            />
          </template>

          <!-- 🎓 UNIVERSITY SELECTORS -->
          <template v-if="institutionType === 'university'">
            <auto-list
              v-model="selectedCollegeId"
              name="College"
              placeholder="الكلية"
              cols="3"
              :add="false"
              @update:model-value="() => { selectedDepartmentId = null; selectedSpecializationId = null; selectedSemesterSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedDepartmentId"
              name="DepartmentByCollege"
              :param="selectedCollegeId"
              placeholder="القسم الأكاديمي"
              cols="3"
              :add="false"
              :disabled="!selectedCollegeId"
              @update:model-value="() => { selectedSpecializationId = null; selectedSemesterSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedSpecializationId"
              name="Specialization"
              :param="selectedDepartmentId"
              placeholder="التخصص"
              cols="3"
              :add="false"
              :disabled="!selectedDepartmentId"
              @update:model-value="() => { selectedSemesterSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedSemesterSubjectId"
              name="SemesterSubject"
              :param="selectedSpecializationId"
              placeholder="مقرر الفصل الجامعي *"
              cols="3"
              :add="false"
              :disabled="!selectedSpecializationId"
              @update:model-value="onYearOrSubjectChange"
            />
          </template>

          <!-- 🏢 INSTITUTE SELECTORS -->
          <template v-if="institutionType === 'institute'">
            <auto-list
              v-model="selectedInstituteFieldId"
              name="InstituteField"
              placeholder="المجال المهني"
              cols="2"
              :add="false"
              @update:model-value="() => { selectedInstituteEducationSystemId = null; selectedInstituteSpecializationId = null; selectedInstituteCurriculumId = null; selectedInstituteSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedInstituteEducationSystemId"
              name="InstituteEducationSystem"
              :param="selectedInstituteFieldId"
              placeholder="نظام التعليم"
              cols="2"
              :add="false"
              :disabled="!selectedInstituteFieldId"
              @update:model-value="() => { selectedInstituteSpecializationId = null; selectedInstituteCurriculumId = null; selectedInstituteSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedInstituteSpecializationId"
              name="InstituteSpecialization"
              :param="{ field: selectedInstituteFieldId, education_system: selectedInstituteEducationSystemId }"
              placeholder="التخصص المهني"
              cols="3"
              :add="false"
              :disabled="!selectedInstituteEducationSystemId"
              @update:model-value="() => { selectedInstituteCurriculumId = null; selectedInstituteSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedInstituteCurriculumId"
              name="InstituteCurriculum"
              :param="selectedInstituteSpecializationId"
              placeholder="الخطة التدريبية"
              cols="2"
              :add="false"
              :disabled="!selectedInstituteSpecializationId"
              @update:model-value="() => { selectedInstituteSubjectId = null; onYearOrSubjectChange(); }"
            />
            <auto-list
              v-model="selectedInstituteSubjectId"
              name="InstituteSubject"
              :param="selectedInstituteCurriculumId"
              placeholder="المادة التدريبية *"
              cols="3"
              :add="false"
              :disabled="!selectedInstituteCurriculumId"
              @update:model-value="onYearOrSubjectChange"
            />
          </template>
        </v-row>

        <!-- Reason / Decree Text Input -->
        <div class="mt-4 pt-3 border-t">
          <v-text-field
            v-model="decreeReason"
            label="مبرر أو رقم قرار الحذف (تعميم وزاري / مجلس الكلية)"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-file-certificate-outline"
            placeholder="مثال: تعميم وزاري رقم (14) للعام الدراسي 2025/2026 باستبعاد الموضوعات الإثرائية"
            hide-details
          />
        </div>
      </v-card>

      <!-- Loading State -->
      <div v-if="loadingTree" class="text-center py-12 main-card rounded-2xl">
        <v-progress-circular indeterminate color="primary" size="48" class="mb-3" />
        <p class="text-subtitle-1 font-weight-bold">جاري تحميل موضوعات ووحدات المنهج...</p>
      </div>

      <!-- No Selection Prompt -->
      <div v-else-if="!isSubjectSelected" class="text-center py-12 main-card rounded-2xl border-subtle">
        <v-avatar size="64" color="slate-100" class="mb-3">
          <v-icon size="36" color="slate-400">mdi-cursor-default-click-outline</v-icon>
        </v-avatar>
        <h3 class="text-h6 font-weight-bold text-slate-700 mb-1">يرجى تحديد المادة أو المقرر الدراسي</h3>
        <p class="text-body-2 text-medium-emphasis">
          اختر العام الدراسي والمقرر لعرض قائمة الوحدات والدروس وتحديد المستبعد منها لهذا العام.
        </p>
      </div>

      <!-- Empty Units State -->
      <div v-else-if="treeData.length === 0" class="text-center py-12 main-card rounded-2xl border-subtle">
        <v-avatar size="64" color="amber-lighten-5" class="mb-3">
          <v-icon size="36" color="amber-darken-3">mdi-folder-alert-outline</v-icon>
        </v-avatar>
        <h3 class="text-h6 font-weight-bold text-slate-800 mb-1">لا توجد وحدات أو دروس مسجلة لهذا المقرر</h3>
        <p class="text-body-2 text-medium-emphasis">
          تأكد من إدخال الوحدات والدروس التابعة لهذه المادة في النظام الأكاديمي أولاً.
        </p>
      </div>

      <!-- Curriculum Tree Interactive Panel -->
      <div v-else>
        <!-- KPI Summary Cards & Bulk Actions -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
          <div class="d-flex align-center gap-2 flex-wrap">
            <v-chip color="primary" variant="tonal" class="font-weight-bold">
              {{ treeData.length }} وحدات دراسية
            </v-chip>
            <v-chip :color="excludedUnitsCount > 0 ? 'error' : 'slate-500'" variant="tonal" class="font-weight-bold">
              <v-icon start size="16">mdi-folder-remove</v-icon>
              {{ excludedUnitsCount }} وحدات محذوفة بالكامل
            </v-chip>
            <v-chip color="indigo" variant="tonal" class="font-weight-bold">
              {{ totalLessonsCount }} دروس / موضوعات
            </v-chip>
            <v-chip :color="excludedLessonsCount > 0 ? 'error' : 'slate-500'" variant="tonal" class="font-weight-bold">
              <v-icon start size="16">mdi-book-cancel</v-icon>
              {{ excludedLessonsCount }} دروس محذوفة
            </v-chip>
          </div>

          <div class="d-flex align-center gap-2">
            <custom-btn
              label="حذف كافة الوحدات"
              variant="outlined"
              color="error"
              size="small"
              class="font-weight-bold"
              :click="excludeAll"
            />
            <custom-btn
              label="تضمين الكل (إلغاء الحذف)"
              variant="outlined"
              color="success"
              size="small"
              class="font-weight-bold"
              :click="includeAll"
            />
          </div>
        </div>

        <!-- Units & Lessons Cards -->
        <div class="d-flex flex-column gap-4 mb-8">
          <v-card
            v-for="unit in treeData"
            :key="unit.id"
            class="main-card rounded-2xl border-subtle overflow-hidden"
            :class="{ 'border-error-subtle bg-red-lighten-5': unit.is_excluded }"
            elevation="0"
          >
            <!-- Unit Header -->
            <div class="pa-4 d-flex align-center justify-space-between flex-wrap gap-3 bg-surface-variant border-b">
              <div class="d-flex align-center gap-3">
                <v-avatar size="36" :color="unit.is_excluded ? 'error' : 'primary'" class="text-white font-weight-bold">
                  {{ unit.order || '#' }}
                </v-avatar>
                <div>
                  <h3 class="text-subtitle-1 font-weight-black mb-0" :class="{ 'text-error': unit.is_excluded }">
                    {{ unit.name }}
                  </h3>
                  <span class="text-caption text-medium-emphasis">
                    تحتوي على {{ unit.lessons ? unit.lessons.length : 0 }} دروس وموضوعات فرعية
                  </span>
                </div>
              </div>

              <!-- Unit Full Exclusion Toggle -->
              <div class="d-flex align-center gap-2">
                <v-switch
                  v-model="unit.is_excluded"
                  color="error"
                  density="compact"
                  hide-details
                  :label="unit.is_excluded ? 'الوحدة محذوفة بالكامل' : 'استبعاد كامل الوحدة'"
                  class="font-weight-bold"
                  @update:model-value="(val) => onUnitToggle(unit, val)"
                />
              </div>
            </div>

            <!-- Lessons List Inside Unit -->
            <div class="pa-4">
              <div v-if="!unit.lessons || unit.lessons.length === 0" class="text-center py-4 text-medium-emphasis text-caption">
                لا توجد دروس مدخلة تحت هذه الوحدة.
              </div>
              <v-row dense v-else>
                <v-col
                  v-for="lesson in unit.lessons"
                  :key="lesson.id"
                  cols="12"
                  md="6"
                >
                  <div
                    class="pa-3 rounded-xl border d-flex align-center justify-space-between gap-2 transition-all"
                    :class="{
                      'bg-red-lighten-5 border-error text-error': lesson.is_excluded || unit.is_excluded,
                      'bg-surface border-subtle': !lesson.is_excluded && !unit.is_excluded
                    }"
                  >
                    <div class="d-flex align-center gap-2 overflow-hidden">
                      <v-icon size="18" :color="lesson.is_excluded || unit.is_excluded ? 'error' : 'slate-400'">
                        {{ lesson.is_excluded || unit.is_excluded ? 'mdi-close-circle-outline' : 'mdi-checkbox-blank-circle-outline' }}
                      </v-icon>
                      <div class="text-truncate">
                        <div class="text-body-2 font-weight-bold text-truncate">{{ lesson.name }}</div>
                        <span v-if="lesson.reason" class="text-caption text-error d-block text-truncate">
                          سبب: {{ lesson.reason }}
                        </span>
                      </div>
                    </div>

                    <div class="d-flex align-center gap-2 flex-shrink-0">
                      <v-chip
                        size="x-small"
                        :color="lesson.is_excluded || unit.is_excluded ? 'error' : 'emerald'"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        {{ lesson.is_excluded || unit.is_excluded ? 'محذوف من الاختبارات' : 'مشمول' }}
                      </v-chip>

                      <v-checkbox-btn
                        v-model="lesson.is_excluded"
                        :disabled="unit.is_excluded"
                        color="error"
                        density="compact"
                        hide-details
                      />
                    </div>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-card>
        </div>

        <!-- Sticky Bottom Save Bar -->
        <div class="sticky-save-bar pa-4 rounded-2xl main-card border-subtle d-flex align-center justify-space-between flex-wrap gap-3">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary">mdi-shield-check-outline</v-icon>
            <span class="text-body-2 font-weight-bold">
              سيتم اعتماد المحذوفات تلقائياً ومنع سحب أسئلتها في معالج توليد الاختبارات للعام الدراسي المحدد.
            </span>
          </div>

          <custom-btn
            type="add"
            label="حفظ واعتماد المحذوفات لهذا العام"
            icon="mdi-content-save-check"
            color="primary"
            class="px-8 font-weight-bold shadow-md"
            :loading="saving"
            :click="saveExclusions"
          />
        </div>
      </div>
    </div>

    <!-- TAB 2: ACTIVE EXCLUSIONS ARCHIVE TABLE -->
    <div v-else-if="currentViewTab === 'list'">
      <v-card class="main-card pa-5 rounded-2xl border-subtle mb-4" elevation="0">
        <v-row dense class="align-center">
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchExclusionsQuery"
              label="بحث في المحذوفات المعتمدة..."
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              hide-details
              clearable
              @update:model-value="loadExclusionsList"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="filterListInstType"
              :items="[
                { value: 'all', title: 'كافة المؤسسات (مدارس / جامعات / معاهد)' },
                { value: 'school', title: 'مدارس فقط' },
                { value: 'university', title: 'جامعات فقط' },
                { value: 'institute', title: 'معاهد وتدريب مهني فقط' }
              ]"
              label="نوع المؤسسة"
              variant="outlined"
              density="compact"
              hide-details
              @update:model-value="loadExclusionsList"
            />
          </v-col>
          <v-col cols="12" md="4" class="d-flex justify-end">
            <custom-btn
              type="refresh"
              label="تحديث السجل"
              color="primary"
              variant="tonal"
              :click="loadExclusionsList"
            />
          </v-col>
        </v-row>
      </v-card>

      <div class="main-card rounded-2xl overflow-hidden border-subtle">
        <custom-data-table
          :headers="exclusionsTableHeaders"
          :items="exclusionsTableItems"
          :loading="loadingList"
          :hasFilter="false"
          :log="false"
          :restore="false"
          :showSelect="false"
          @update:options="loadExclusionsList"
        >
          <template v-slot:item-slot="{ item, key }">
            <template v-if="key === 'institution_type'">
              <v-chip
                size="x-small"
                :color="item.institution_type === 'institute' ? 'warning' : item.institution_type === 'university' ? 'info' : 'emerald'"
                variant="tonal"
                class="font-weight-bold"
              >
                {{ item.institution_type_display || item.institution_type }}
              </v-chip>
            </template>

            <template v-else-if="key === 'target_name'">
              <div class="font-weight-bold">
                <v-icon size="14" color="error" class="me-1">
                  {{ item.exclusion_type === 'unit' ? 'mdi-folder-remove' : 'mdi-book-cancel' }}
                </v-icon>
                <span>{{ item.exclusion_type === 'unit' ? item.unit_name : item.lesson_name }}</span>
                <span class="text-caption text-medium-emphasis ms-2" v-if="item.exclusion_type === 'lesson' && item.unit_name">
                  (الوحدة: {{ item.unit_name }})
                </span>
              </div>
            </template>

            <template v-else-if="key === 'subject_display'">
              <span class="font-weight-medium">
                {{ item.subject_name || item.semester_subject_name || item.institute_subject_name || '-' }}
              </span>
            </template>

            <template v-else-if="key === 'actions'">
              <custom-btn
                type="delete"
                label="حذف وإعادة التضمين"
                color="error"
                variant="tonal"
                size="x-small"
                class="font-weight-bold"
                :click="() => deleteExclusionItem(item.id)"
              />
            </template>
          </template>
        </custom-data-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, getCurrentInstance } from 'vue'
import { examsService } from '@/services/examsService'

const { proxy } = getCurrentInstance()

// Navigation & Tab State
const currentViewTab = ref('manage') // 'manage' | 'list'
const institutionType = ref('school') // 'school' | 'university' | 'institute'
const selectedYearId = ref(null)

// School Hierarchy State
const selectedStageId = ref(null)
const selectedClassTrackId = ref(null)
const selectedSubjectId = ref(null)

// University Hierarchy State
const selectedCollegeId = ref(null)
const selectedDepartmentId = ref(null)
const selectedSpecializationId = ref(null)
const selectedSemesterSubjectId = ref(null)

// Institute Hierarchy State
const selectedInstituteFieldId = ref(null)
const selectedInstituteEducationSystemId = ref(null)
const selectedInstituteSpecializationId = ref(null)
const selectedInstituteCurriculumId = ref(null)
const selectedInstituteSubjectId = ref(null)

// General Decree / Reason
const decreeReason = ref('')

// Tree State
const loadingTree = ref(false)
const saving = ref(false)
const treeData = ref([])

// Archive List State
const loadingList = ref(false)
const exclusionsList = ref([])
const searchExclusionsQuery = ref('')
const filterListInstType = ref('all')

const isSubjectSelected = computed(() => {
  if (institutionType.value === 'school') return Boolean(selectedSubjectId.value)
  if (institutionType.value === 'university') return Boolean(selectedSemesterSubjectId.value)
  if (institutionType.value === 'institute') return Boolean(selectedInstituteSubjectId.value)
  return false
})

const excludedUnitsCount = computed(() => {
  return treeData.value.filter(u => u.is_excluded).length
})

const totalLessonsCount = computed(() => {
  return treeData.value.reduce((acc, u) => acc + (u.lessons?.length || 0), 0)
})

const excludedLessonsCount = computed(() => {
  let count = 0
  for (const u of treeData.value) {
    if (u.is_excluded) {
      count += u.lessons?.length || 0
    } else {
      count += u.lessons?.filter(l => l.is_excluded).length || 0
    }
  }
  return count
})

// Table Headers for Active Exclusions
const exclusionsTableHeaders = [
  { title: 'العام الدراسي', key: 'academic_year_name', sortable: true },
  { title: 'المؤسسة', key: 'institution_type', sortable: true },
  { title: 'المادة / المقرر', key: 'subject_display', sortable: true },
  { title: 'نطاق الحذف', key: 'exclusion_type_display', sortable: true },
  { title: 'المحتوى المستبعد', key: 'target_name', sortable: true },
  { title: 'قرار / مبرر الحذف', key: 'reason', sortable: false },
  { title: 'إجراءات', key: 'actions', sortable: false, align: 'center' },
]

const exclusionsTableItems = computed(() => ({
  results: exclusionsList.value,
  count: exclusionsList.value.length,
  pagination: {
    count: exclusionsList.value.length,
    current_page: 1,
    num_pages: 1,
  }
}))

onMounted(async () => {
  await loadExclusionsList()
})

function onInstitutionTypeChange() {
  selectedStageId.value = null
  selectedClassTrackId.value = null
  selectedSubjectId.value = null
  selectedCollegeId.value = null
  selectedDepartmentId.value = null
  selectedSpecializationId.value = null
  selectedSemesterSubjectId.value = null
  selectedInstituteFieldId.value = null
  selectedInstituteEducationSystemId.value = null
  selectedInstituteSpecializationId.value = null
  selectedInstituteCurriculumId.value = null
  selectedInstituteSubjectId.value = null
  treeData.value = []
}

async function onYearOrSubjectChange() {
  if (!isSubjectSelected.value) {
    treeData.value = []
    return
  }

  loadingTree.value = true
  try {
    const params = {
      year_id: selectedYearId.value,
      institution_type: institutionType.value,
      subject_id: selectedSubjectId.value,
      stage_id: selectedStageId.value,
      class_track_id: selectedClassTrackId.value,
      semester_subject_id: selectedSemesterSubjectId.value,
      institute_subject_id: selectedInstituteSubjectId.value,
    }

    const res = await examsService.getCurriculumTreeForSubject(params)
    if (res && res.success) {
      treeData.value = res.tree || []
      // If any existing exclusion has a reason, pre-fill decreeReason
      const firstReason = res.tree.find(u => u.reason)?.reason || res.tree.flatMap(u => u.lessons || []).find(l => l.reason)?.reason
      if (firstReason && !decreeReason.value) {
        decreeReason.value = firstReason
      }
    } else {
      treeData.value = []
    }
  } catch (err) {
    console.error('فشل جلب وحدات المنهج:', err)
    treeData.value = []
  } finally {
    loadingTree.value = false
  }
}

function onUnitToggle(unit, val) {
  if (unit.lessons) {
    unit.lessons.forEach(l => {
      l.is_excluded = val
    })
  }
}

function excludeAll() {
  treeData.value.forEach(u => {
    u.is_excluded = true
    if (u.lessons) {
      u.lessons.forEach(l => { l.is_excluded = true })
    }
  })
}

function includeAll() {
  treeData.value.forEach(u => {
    u.is_excluded = false
    if (u.lessons) {
      u.lessons.forEach(l => { l.is_excluded = false })
    }
  })
}

async function saveExclusions() {
  if (!selectedYearId.value) {
    if (proxy?.$alert) proxy.$alert('errorData', { message: 'يرجى تحديد العام الدراسي أولاً' })
    return
  }

  saving.value = true
  try {
    const excluded_unit_ids = []
    const excluded_lesson_ids = []
    const scope_unit_ids = treeData.value.map(u => u.id)

    for (const u of treeData.value) {
      if (u.is_excluded) {
        excluded_unit_ids.push(u.id)
      } else if (u.lessons) {
        for (const l of u.lessons) {
          if (l.is_excluded) {
            excluded_lesson_ids.push(l.id)
          }
        }
      }
    }

    const payload = {
      academic_year_id: selectedYearId.value,
      institution_type: institutionType.value,
      scope_unit_ids,
      excluded_unit_ids,
      excluded_lesson_ids,
      reason: decreeReason.value,
      stage_id: selectedStageId.value,
      class_track_id: selectedClassTrackId.value,
      subject_id: selectedSubjectId.value,
      college_id: selectedCollegeId.value,
      department_id: selectedDepartmentId.value,
      specialization_id: selectedSpecializationId.value,
      semester_subject_id: selectedSemesterSubjectId.value,
      institute_field_id: selectedInstituteFieldId.value,
      institute_education_system_id: selectedInstituteEducationSystemId.value,
      institute_specialization_id: selectedInstituteSpecializationId.value,
      institute_curriculum_id: selectedInstituteCurriculumId.value,
      institute_subject_id: selectedInstituteSubjectId.value,
    }

    const res = await examsService.syncCurriculumExclusions(payload)
    if (res && res.success) {
      if (proxy?.$alert) {
        proxy.$alert('success', {
          title: 'تم الاعتماد بنجاح',
          message: `تم حفظ المحذوفات بنجاح (${excluded_unit_ids.length} وحدات و ${excluded_lesson_ids.length} دروس). لن تدخل في أي اختبار لهذا العام.`
        })
      }
      await loadExclusionsList()
    }
  } catch (err) {
    console.error('فشل حفظ المحذوفات:', err)
    if (proxy?.$alert) {
      proxy.$alert('errorData', { message: err?.response?.data?.message || err.message || 'فشل حفظ المحذوفات' })
    }
  } finally {
    saving.value = false
  }
}

async function loadExclusionsList() {
  loadingList.value = true
  try {
    const params = {}
    if (searchExclusionsQuery.value) params.search = searchExclusionsQuery.value
    if (filterListInstType.value && filterListInstType.value !== 'all') {
      params.institution_type = filterListInstType.value
    }
    const res = await examsService.getCurriculumExclusions(params)
    exclusionsList.value = res?.results || (Array.isArray(res) ? res : [])
  } catch (err) {
    console.error('فشل جلب سجل المحذوفات:', err)
  } finally {
    loadingList.value = false
  }
}

async function deleteExclusionItem(id) {
  try {
    await examsService.deleteCurriculumExclusion(id)
    if (proxy?.$alert) {
      proxy.$alert('success', { message: 'تم إلغاء الحذف وإعادة تضمين المحتوى في المنهج بنجاح' })
    }
    await loadExclusionsList()
    if (isSubjectSelected.value) {
      await onYearOrSubjectChange()
    }
  } catch (err) {
    console.error('فشل حذف سجل الاستبعاد:', err)
  }
}
</script>

<style scoped>
.qb-curriculum-exclusions-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.border-subtle {
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.border-error-subtle {
  border: 1.5px solid rgba(var(--v-theme-error), 0.35) !important;
}

.sticky-save-bar {
  position: sticky;
  bottom: 16px;
  z-index: 10;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12) !important;
}
</style>
