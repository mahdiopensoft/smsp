<template>
  <div class="qb-exam-create-v4 position-relative">

    <!-- Top Subtle Linear Progress during Edit Loading -->
    <v-progress-linear
      v-if="isLoadingForEdit"
      indeterminate
      color="primary"
      height="3"
      rounded
      class="mb-3"
    />

    <!-- Lightweight Formal Transparent Overlay -->
    <v-fade-transition>
      <div v-if="isLoadingForEdit" class="formal-loading-overlay">
        <div class="formal-loading-pill d-flex align-center gap-3 pa-3 px-5 rounded-pill elevation-3">
          <v-progress-circular
            indeterminate
            color="primary"
            size="22"
            width="2.5"
          />
          <span class="text-caption font-weight-bold text-high-emphasis">
            جاري استرجاع بيانات الاختبار...
          </span>
        </div>
      </div>
    </v-fade-transition>

    <!-- Active Editing Draft Mode Banner (Zero Gray executive design) -->
    <div
      v-if="isEditing && !isLoadingForEdit"
      class="editing-mode-banner mb-6 pa-4 rounded-2xl d-flex align-center justify-space-between flex-wrap gap-3"
    >
      <div class="d-flex align-center gap-3">
        <v-avatar color="warning" size="44" class="font-weight-black text-white shadow-sm">
          <v-icon color="white" size="24">mdi-pencil-box-multiple</v-icon>
        </v-avatar>
        <div>
          <div class="d-flex align-center gap-2 flex-wrap">
            <h3 class="text-subtitle-1 font-weight-black mb-0 text-warning">
              تعديل مسودة الاختبار: {{ exam.title || editingExamCode }}
            </h3>
            <v-chip size="x-small" color="warning" variant="flat" class="font-weight-black text-white">
              مسودة غير معتمدة
            </v-chip>
            <span class="text-caption font-mono font-weight-bold opacity-80">({{ editingExamCode }})</span>
          </div>
          <p class="text-caption font-weight-medium text-medium-emphasis mb-0">
            أنت الآن تقوم بتعديل معايير وتوزيعات الاختبار الحالية. يمكنك تعديل أي خطوة وإعادة توليد وتحديث الاختبار.
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <v-btn
          variant="tonal"
          color="warning"
          size="small"
          class="font-weight-bold rounded-xl text-none"
          prepend-icon="mdi-plus"
          @click="exitEditMode"
        >
          إنشاء اختبار جديد بدلاً من التعديل
        </v-btn>
      </div>
    </div>

    <!-- Main Stepper Wizard Window Content -->
    <div
      class="main-card rounded-2xl mb-8"
      :class="{ 'content-loading-blur': isLoadingForEdit }"
    >

      <!-- Premium Connected Wizard Stepper Pipeline (دوائر تفاعلية مع خطوط توصيل وحالات نجاح/فشل صريحة) -->
      <ExamWizardStepper
        :current-step="step"
        :wizard-steps="wizardSteps"
        :wizard-progress-percentage="wizardProgressPercentage"
        :get-step-node-classes="getStepNodeClasses"
        :get-step-status="getStepStatus"
        @step-click="handleStepClick"
      />

      <div class="pa-6">
        <v-window v-model="step" class="bg-transparent">
          <!-- ════════════════════════════════════════════════════════════════ -->
          <!-- STEP 1: SETTINGS (GROUPED SECTIONS) -->
          <v-window-item :value="1">
            <Step1ExamSettings
              ref="step1ComponentRef"
              :exam="exam"
              v-model:active-step1-section="activeStep1Section"
              :validated-once="validatedOnce"
              :invalid-sections-count="invalidSectionsCount"
              :is-section-valid="isSectionValid"
              :step1-nav-items="step1NavItems"
              :is-loading-for-edit="isLoadingForEdit"
              :required-rule="requiredRule"
              :models-mode="modelsMode"
              :total-models-count="totalModelsCount"
              :model-groups="modelGroups"
              :difficulty-items="difficultyItems"
              :difficulty-profiles="difficultyProfiles"
              :governorates-list="governoratesList"
              :loading-geo-data="loadingGeoData"
              :loading-schools="loadingSchools"
              :on-institution-type-toggle="onInstitutionTypeToggle"
              :set-models-mode="setModelsMode"
              :set-models-count="setModelsCount"
              :add-model-group="addModelGroup"
              :remove-model-group="removeModelGroup"
              :apply-difficulty-preset="applyDifficultyPreset"
              :update-group-diff="updateGroupDiff"
              :step-group-diff="stepGroupDiff"
              :group-diff-total="groupDiffTotal"
              :on-group-scope-level-change="onGroupScopeLevelChange"
              :on-group-filter-gov-for-school="onGroupFilterGovForSchool"
              :on-group-filter-dir-for-school="onGroupFilterDirForSchool"
              :get-directorates-for-group="getDirectoratesForGroup"
              :get-directorates-for-filter-gov="getDirectoratesForFilterGov"
              :is-group-school-disabled="isGroupSchoolDisabled"
            />
          </v-window-item>

          <!-- ════════════════════════════════════════════════════════════════ -->
          <!-- STEP 2: BLUEPRINT MATRIX (SEGMENTED CONTROL OVERHAUL) -->
          <v-window-item :value="2">
            <Step2SpecificationsMatrix
              :exam="exam"
              v-model:active-tab="activeTab"
              :matrix-tab-items="matrixTabItems"
              :blueprint="blueprint"
              :models-mode="modelsMode"
              :model-groups="modelGroups"
              v-model:bloom-enabled="bloomEnabled"
              :theme="theme"
              v-model:active-unit-group-index="activeUnitGroupIndex"
              :current-unit-group="currentUnitGroup"
              :current-group-units-total="currentGroupUnitsTotal"
              :current-active-units-list="currentActiveUnitsList"
              v-model:active-type-group-index="activeTypeGroupIndex"
              :current-type-group="currentTypeGroup"
              :current-group-types-total="currentGroupTypesTotal"
              :current-group-distributed-marks="currentGroupDistributedMarks"
              :current-active-types-list="currentActiveTypesList"
              :total-difficulty-percentage="totalDifficultyPercentage"
              :total-bloom-percentage="totalBloomPercentage"
              :has-term-separation="hasTermSeparation"
              :is-unit-in-term="isUnitInTerm"
              :select-unit-group="selectUnitGroup"
              :select-type-group="selectTypeGroup"
              :get-group-version-codes="getGroupVersionCodes"
              :get-group-target-names="getGroupTargetNames"
              :get-group-units-total="getGroupUnitsTotal"
              :get-group-types-total="getGroupTypesTotal"
              :get-unit-lessons-count="getUnitLessonsCount"
              :get-unit-approved-questions-count="getUnitApprovedQuestionsCount"
              :get-unit-required-questions="getUnitRequiredQuestions"
              :get-unit-remaining-questions="getUnitRemainingQuestions"
              :adjust-unit-percentage="adjustUnitPercentage"
              :update-unit-percentage="updateUnitPercentage"
              :auto-distribute-current-group-units="autoDistributeCurrentGroupUnits"
              :auto-distribute-all-groups-units="autoDistributeAllGroupsUnits"
              :copy-current-group-units-to-all="copyCurrentGroupUnitsToAll"
              :adjust-type-percentage="adjustTypePercentage"
              :update-type-percentage="updateTypePercentage"
              :adjust-type-mark="adjustTypeMark"
              :set-total-marks="setTotalMarks"
              :auto-balance-marks="autoBalanceMarks"
              :get-type-questions-count="getTypeQuestionsCount"
              :get-type-total-marks="getTypeTotalMarks"
              :auto-distribute-current-group-types="autoDistributeCurrentGroupTypes"
              :auto-distribute-all-groups-types="autoDistributeAllGroupsTypes"
              :copy-current-group-types-to-all="copyCurrentGroupTypesToAll"
              :update-distribution="updateDistribution"
              :auto-distribute="autoDistribute"
              :open-unit-details="openUnitDetails"
            />
          </v-window-item>

          <!-- ════════════════════════════════════════════════════════════════ -->
          <!-- STEP 3: PREVIEW & CONFIRMATION (EXECUTIVE DASHBOARD) -->
          <v-window-item :value="3">
            <Step3PreviewConfirmation
              :exam="exam"
              :bloom-enabled="bloomEnabled"
              :models-mode="modelsMode"
              :total-models-count="totalModelsCount"
              :model-groups="modelGroups"
              :is-all-groups-all-regions="isAllGroupsAllRegions"
              :total-unique-assigned-targets-count="totalUniqueAssignedTargetsCount"
              :blueprint="blueprint"
              :staging-loading="stagingLoading"
              :get-group-version-codes="getGroupVersionCodes"
              :get-group-target-names="getGroupTargetNames"
              :get-group-units-total="getGroupUnitsTotal"
              @next-step="nextStep"
            />
          </v-window-item>

          <!-- STEP 4: INTERACTIVE EXAM STAGING & MODEL COMPOSER -->
          <v-window-item :value="4">
            <Step4ModelsReview
              :staging-loading="stagingLoading"
              :generating="generating"
              :staged-models="stagedModels"
              v-model:active-staged-model-index="activeStagedModelIndex"
              :total-marks="exam.totalMarks"
              v-model:show-correct-answers="showCorrectAnswers"
              @prepare-staging-and-proceed="prepareStagingAndProceed"
              @commit-final-exam="commitFinalExam"
              @go-to-step="step = $event"
              @quick-auto-swap="quickAutoSwap($event.question, $event.modelIndex)"
              @open-swap-dialog="openSwapDialog($event.question, $event.modelIndex)"
              @open-quick-create-dialog="openQuickCreateDialog($event.question, $event.modelIndex)"
            />
          </v-window-item>
        </v-window>
      </div>

      <!-- Stepper Action Buttons Footer (Sticky) -->
      <div class="px-6 py-4 border-t border-subtle d-flex align-center justify-space-between wizard-footer"
        style="position: sticky; bottom: 0; background: rgb(var(--v-theme-surface)); z-index: 99; box-shadow: 0 -10px 30px rgba(0,0,0,0.05); border-bottom-left-radius: 16px; border-bottom-right-radius: 16px;">
        <v-btn variant="tonal" color="medium-emphasis" class="font-weight-bold px-5" rounded="lg" :disabled="step === 1 || generating"
          @click="step--">
          <v-icon start size="18">mdi-arrow-right</v-icon>
          السابق
        </v-btn>

        <div class="d-none d-sm-flex align-center gap-2">
          <span class="text-caption font-weight-bold text-medium-emphasis">
            خطوة {{ step }} من 4
          </span>
        </div>

        <v-btn
          v-if="step < 3"
          color="primary"
          class="font-weight-bold px-8"
          rounded="lg"
          elevation="2"
          @click="nextStep"
        >
          <v-icon start size="20">mdi-arrow-left</v-icon>
          التالي
        </v-btn>

        <v-btn
          v-else-if="step === 3"
          color="primary"
          class="font-weight-bold px-8"
          rounded="lg"
          elevation="2"
          :loading="stagingLoading"
          @click="nextStep"
        >
          <v-icon start size="20">mdi-file-document-edit-outline</v-icon>
          الانتقال لمسودة واستعراض النماذج
        </v-btn>

        <v-btn
          v-else-if="step === 4"
          color="success"
          class="font-weight-bold px-8 shadow-success"
          rounded="lg"
          elevation="3"
          size="large"
          :loading="generating"
          @click="commitFinalExam"
        >
          <v-icon start size="20">mdi-check-decagram</v-icon>
          اعتماد وتوليد الاختبار النهائي (تثبيت رسمي)
        </v-btn>
      </div>
    </div>
    <!-- DIALOG COMPONENTS -->
    <ShortageReportDialog
      v-model="shortageDialog"
      :shortage-report="shortageReport"
      @go-to-matrix="shortageDialog = false; step = 2"
      @go-to-add-question="goToAddQuestion()"
    />

    <QuestionSelectorDialog
      v-model="swapDialog"
      :target-swap-question="targetSwapQuestion"
      :swap-loading="swapLoading"
      :swap-candidates="swapCandidates"
      :swap-scope="swapScope"
      v-model:swap-search-query="swapSearchQuery"
      @set-scope="setSwapScope"
      @search="searchSwapCandidates"
      @open-quick-create="openQuickCreateFromSwap"
      @apply-replacement="applyReplacement"
    />

    <QuickCreateQuestionDialog
      v-model="quickCreateDialog"
      :form="quickCreateForm"
      :loading="quickCreateLoading"
      @submit="submitQuickCreateQuestion"
    />

    <UnitDetailsDialog
      v-model="unitDetailsDialog.show"
      :unit-details="unitDetailsDialog"
      :institution-type="exam.institution_type"
      :expanded-lesson-id="expandedLessonId"
      :lesson-questions-loading="lessonQuestionsLoading"
      :lesson-questions-list="lessonQuestionsList"
      @toggle-lesson-questions="toggleLessonQuestions"
      @go-to-add-question="goToAddQuestion($event.unitId, $event.lessonId)"
      @go-to-edit-question="goToEditQuestion"
      @open-in-question-bank="openInQuestionBank"
    />


  </div>
</template>

<script setup>
import Step2SpecificationsMatrix from './components/exam_create/Step2SpecificationsMatrix.vue'
import Step1ExamSettings from './components/exam_create/Step1ExamSettings.vue'
import ExamWizardStepper from './components/exam_create/ExamWizardStepper.vue'
import Step3PreviewConfirmation from './components/exam_create/Step3PreviewConfirmation.vue'
import Step4ModelsReview from './components/exam_create/Step4ModelsReview.vue'
import ShortageReportDialog from './components/dialogs/ShortageReportDialog.vue'
import QuestionSelectorDialog from './components/dialogs/QuestionSelectorDialog.vue'
import QuickCreateQuestionDialog from './components/dialogs/QuickCreateQuestionDialog.vue'
import UnitDetailsDialog from './components/dialogs/UnitDetailsDialog.vue'
import { ref, reactive, computed, watch, onMounted, getCurrentInstance, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDataStore } from '@/stores/dataStore'
import { useTheme } from 'vuetify'
import { rules } from '@/utils/validations'
import { examsService } from '@/services/examsService'
import { academicService } from '@/services/academicService'
import api from '@/services/api'

const { proxy } = getCurrentInstance()
const router = useRouter()
const route = useRoute()

// Edit Exam Mode States
const isEditing = ref(false)
const editingExamId = ref(null)
const editingExamCode = ref('')
const isLoadingForEdit = ref(Boolean(route.query.edit_exam_id))
const store = useDataStore()
const theme = useTheme()

const requiredRule = [rules.required]

// Stepper Step Indicator Config - NOW 3 STEPS
const step = ref(1)
const step1Form = ref(null)
const step1ComponentRef = ref(null)
const generating = ref(false)

const wizardSteps = [
  { value: 1, title: 'إعدادات الاختبار', subtitle: 'البيانات والنطاق والنماذج', icon: 'mdi-tune-variant' },
  { value: 2, title: 'مصفوفة المعايير', subtitle: 'الوحدات والصعوبة والدرجات', icon: 'mdi-chart-pie' },
  { value: 3, title: 'المعاينة والتأكيد', subtitle: 'مطابقة ملخص المواصفات', icon: 'mdi-clipboard-check-outline' },
  { value: 4, title: 'استعراض وضبط النماذج', subtitle: 'المسودة التفاعلية والتحكيم', icon: 'mdi-file-document-edit-outline' },
]

const validatedStep2Once = ref(false)

const wizardProgressPercentage = computed(() => {
  return ((step.value - 1) / (wizardSteps.length - 1)) * 100
})

function getStepStatus(sValue) {
  // ── Step 1: إعدادات الاختبار ──
  if (sValue === 1) {
    if (step.value === 1) {
      if (validatedOnce.value && invalidSectionsCount.value > 0) {
        return {
          type: 'error',
          badge: 'تنبيه',
          text: `فشل: ${invalidSectionsCount.value} أقسام غير مكتملة`,
          statusIcon: 'mdi-alert-circle',
        }
      }
      return {
        type: 'active',
        badge: 'قيد الإعداد',
        text: 'جاري ضبط الإعدادات...',
        statusIcon: 'mdi-record-circle-outline',
      }
    }
    if (invalidSectionsCount.value > 0) {
      return {
        type: 'error',
        badge: 'تنبيه',
        text: 'فشل: حقول مطلوبة غير مكتملة',
        statusIcon: 'mdi-alert-circle',
      }
    }
    return {
      type: 'completed',
      badge: 'نجاح',
      text: 'تم بنجاح (مكتمل)',
      statusIcon: 'mdi-check-bold',
    }
  }

  // ── Step 2: مصفوفة المعايير ──
  if (sValue === 2) {
    const isStep2Valid = modelsMode.value === 'advanced'
      ? (Array.isArray(modelGroups.value) && modelGroups.value.length > 0 && modelGroups.value.every(g => getGroupUnitsTotal(g) === 100 && getGroupTypesTotal(g) === 100))
      : (totalUnitsPercentage.value === 100 && totalTypesPercentage.value === 100)

    if (step.value === 2) {
      if (validatedStep2Once.value && !isStep2Valid) {
        return {
          type: 'error',
          badge: 'غير متطابق',
          text: `فشل: الأوزان ${totalUnitsPercentage.value}% (المطلوب 100%)`,
          statusIcon: 'mdi-alert-circle',
        }
      }
      return {
        type: 'active',
        badge: 'قيد الضبط',
        text: isStep2Valid ? 'المصفوفة متوازنة (جاهزة)' : 'جاري موازنة النسب...',
        statusIcon: 'mdi-record-circle-outline',
      }
    }
    if (step.value > 2) {
      if (!isStep2Valid) {
        return {
          type: 'error',
          badge: 'تنبيه',
          text: 'فشل: المصفوفة غير متوازنة',
          statusIcon: 'mdi-alert-circle',
        }
      }
      return {
        type: 'completed',
        badge: 'نجاح',
        text: 'تم بنجاح (المصفوفة متطابقة)',
        statusIcon: 'mdi-check-bold',
      }
    }
    return {
      type: 'pending',
      badge: 'في الانتظار',
      text: 'في الانتظار',
      statusIcon: 'mdi-clock-outline',
    }
  }

  // ── Step 3: المعاينة والتأكيد ──
  if (sValue === 3) {
    if (step.value === 3) {
      if (shortageReport.value && shortageReport.value.totalMissing > 0) {
        return {
          type: 'error',
          badge: 'عجز بالأسئلة',
          text: `فشل: عجز ${shortageReport.value.totalMissing} سؤال`,
          statusIcon: 'mdi-alert-circle',
        }
      }
      return {
        type: 'active',
        badge: 'قيد الفحص',
        text: 'جاري مطابقة الملخص والمواصفات...',
        statusIcon: 'mdi-record-circle-outline',
      }
    }
    if (step.value > 3) {
      return {
        type: 'completed',
        badge: 'نجاح',
        text: 'تم الاعتماد والتأكيد بنجاح',
        statusIcon: 'mdi-check-bold',
      }
    }
    return {
      type: 'pending',
      badge: 'في الانتظار',
      text: 'في الانتظار',
      statusIcon: 'mdi-clock-outline',
    }
  }

  // ── Step 4: استعراض وضبط النماذج ──
  if (sValue === 4) {
    if (step.value === 4) {
      if (generating.value) {
        return {
          type: 'active',
          badge: 'جاري التوليد',
          text: 'جاري بناء النماذج وسحب الأسئلة...',
          statusIcon: 'mdi-loading',
        }
      }
      if (stagedModels.value && stagedModels.value.length > 0) {
        return {
          type: 'completed',
          badge: 'نجاح',
          text: `تم بنجاح (${stagedModels.value.length} نماذج جاهزة)`,
          statusIcon: 'mdi-check-bold',
        }
      }
      return {
        type: 'active',
        badge: 'قيد الاستعراض',
        text: 'معاينة النماذج والتحكيم',
        statusIcon: 'mdi-record-circle-outline',
      }
    }
    return {
      type: 'pending',
      badge: 'في الانتظار',
      text: 'في الانتظار',
      statusIcon: 'mdi-clock-outline',
    }
  }

  return {
    type: 'pending',
    badge: 'في الانتظار',
    text: 'في الانتظار',
    statusIcon: 'mdi-clock-outline',
  }
}

function getStepNodeClasses(sVal) {
  const status = getStepStatus(sVal).type
  return {
    'is-active': status === 'active',
    'is-completed': status === 'completed',
    'is-error': status === 'error',
    'is-pending': status === 'pending',
  }
}

const handleStepClick = (stepVal) => {
  if (stepVal < step.value) {
    step.value = stepVal
  } else if (stepVal === step.value + 1) {
    nextStep()
  } else if (isEditing.value) {
    step.value = stepVal
  }
}

// State declarations
const modelsMode = ref('uniform')
const bloomEnabled = ref(false)

// Exam Settings
const exam = ref({
  title: '',
  institution_type: 'school',
  subjectId: null,
  classTrackId: null,
  stageId: null,
  collegeId: null,
  departmentId: null,
  specializationId: null,
  semesterSubjectId: null,
  instituteFieldId: null,
  instituteEducationSystemId: null,
  instituteSpecializationId: null,
  instituteCurriculumId: null,
  instituteSubjectId: null,
  yearId: null,
  examPeriodId: null,
  organizationId: null,
  countryId: null,
  governorateId: null,
  directorateId: null,
  regionId: null,
  questionsCount: 20,
  modelsCount: 2,
  totalMarks: 100,
  target_scope_level: 'all',
  exclude_previously_used: false,
})

const examTotalScore = computed(() => Number(exam.value?.totalMarks) || 100)

// Matrix Inner Tabs Items
const activeTab = ref(0)
const instituteSpecParam = computed(() => {
  const p = {}
  if (exam.value.instituteFieldId) p.field = exam.value.instituteFieldId
  if (exam.value.instituteEducationSystemId) p.education_system = exam.value.instituteEducationSystemId
  return Object.keys(p).length ? p : null
})

const matrixTabItems = computed(() => [
  { label: modelsMode.value === 'advanced' ? 'توزيع الوحدات (حسب المجموعات)' : 'توزيع الوحدات', icon: 'mdi-book-open-page-variant' },
  { label: modelsMode.value === 'advanced' ? 'مستويات الصعوبة (متقدم)' : 'مستويات الصعوبة', icon: 'mdi-speedometer' },
  { label: bloomEnabled.value ? 'مستويات بلوم' : 'مستويات بلوم (معطّل)', icon: 'mdi-brain' },
  { label: modelsMode.value === 'advanced' ? 'أنواع الأسئلة (حسب المجموعات)' : 'أنواع الأسئلة', icon: 'mdi-shape' },
])

// Shortage Dialog State
const shortageDialog = ref(false)
const shortageReport = ref({
  mcq: { required: 0, available: 0, missing: 0 },
  tf: { required: 0, available: 0, missing: 0 },
  easy: { required: 0, available: 0, missing: 0 },
  medium: { required: 0, available: 0, missing: 0 },
  hard: { required: 0, available: 0, missing: 0 },
  totalMissing: 0
})

// Quick Selection Helpers

const setModelsCount = (num) => {
  exam.value.modelsCount = num
}
const setTargetScopeLevel = (lvl) => {
  exam.value.target_scope_level = lvl
  if (lvl === 'all') {
    selectedTargetIds.value = []
  }
}

const setModelsMode = (mode) => {
  modelsMode.value = mode
}

// ⭐ Advanced Model Groups
const modelGroups = ref([
  {
    name: 'المجموعة 1',
    count: 2,
    difficulty_profile: 'hard',
    difficulty_distribution: { easy: 10, medium: 30, hard: 60 },
    questions_variation: 'same_scrambled',
    scope_level: 'governorate',
    target_ids: [],
    units: [],
    types: [],
    filter_governorate_id: null,
    filter_directorate_id: null,
    availableSchools: [],
    loadingSchools: false,
  },
  {
    name: 'المجموعة 2',
    count: 2,
    difficulty_profile: 'easy',
    difficulty_distribution: { easy: 60, medium: 30, hard: 10 },
    questions_variation: 'same_scrambled',
    scope_level: 'governorate',
    target_ids: [],
    units: [],
    types: [],
    filter_governorate_id: null,
    filter_directorate_id: null,
    availableSchools: [],
    loadingSchools: false,
  },
])

// ⭐ Geographic Targeting & Organizations (Loaded from dedicated APIs)
const selectedTargetIds = ref([])
const selectedGovernorateForFilter = ref(null)
const selectedDirectorateForFilter = ref(null)

const educationalOrgsList = ref([])
const allSchoolsList = ref([])

const loadingGeoData = ref(false)
const loadingSchools = ref(false)

const loadEducationalHierarchy = async () => {
  loadingGeoData.value = true
  try {
    const res = await examsService.getEducationalHierarchy()
    const data = res?.data || res?.results || (Array.isArray(res) ? res : [])
    educationalOrgsList.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Error loading educational hierarchy:', err)
  } finally {
    loadingGeoData.value = false
  }
}

const governoratesList = computed(() => {
  return educationalOrgsList.value
    .filter(o => o.company_level === 30)
    .map(o => ({
      id: o.id,
      name: o.name_ar,
      name_ar: o.name_ar,
      name_en: o.name_en,
      branch_no: o.branch_no,
      fk_parent_organization: o.fk_parent_organization
    }))
})

const allDirectoratesList = computed(() => {
  return educationalOrgsList.value
    .filter(o => o.company_level === 40)
    .map(o => ({
      id: o.id,
      name: o.name_ar,
      name_ar: o.name_ar,
      name_en: o.name_en,
      branch_no: o.branch_no,
      fk_parent_organization: o.fk_parent_organization
    }))
})

const directoratesList = computed(() => {
  if (!selectedGovernorateForFilter.value) return allDirectoratesList.value
  return allDirectoratesList.value.filter(d => d.fk_parent_organization === selectedGovernorateForFilter.value)
})

const filteredDirectoratesForSchool = computed(() => {
  if (!selectedGovernorateForFilter.value) return []
  return allDirectoratesList.value.filter(d => d.fk_parent_organization === selectedGovernorateForFilter.value)
})

const loadGovernorates = async () => {
  await loadEducationalHierarchy()
}

const loadDirectorates = async () => {}
const loadDirectoratesForSchoolFilter = async () => {}

const isTargetInstitutionsDisabled = computed(() => {
  const instType = exam.value.institution_type || 'school'
  if (instType === 'school') {
    return !selectedGovernorateForFilter.value || !selectedDirectorateForFilter.value
  }
  return !selectedGovernorateForFilter.value
})

const targetInstitutionsPlaceholder = computed(() => {
  const instType = exam.value.institution_type || 'school'
  if (instType === 'school') {
    if (!selectedGovernorateForFilter.value) return 'اختر المحافظة أولاً...'
    if (!selectedDirectorateForFilter.value) return 'اختر المديرية أولاً...'
    return 'ابحث بالاسم للمدرسة...'
  }
  if (!selectedGovernorateForFilter.value) return 'اختر المحافظة أولاً...'
  return instType === 'university'
    ? 'ابحث بالاسم للجامعة أو الكلية...'
    : 'ابحث بالاسم للمعهد...'
})

const loadOrganizations = async (params = {}) => {
  const instType = exam.value.institution_type || 'school'
  if (instType === 'school' && (!params.governorate || !params.directorate)) {
    allSchoolsList.value = []
    return
  }
  if ((instType === 'university' || instType === 'institute') && !params.governorate) {
    allSchoolsList.value = []
    return
  }

  loadingSchools.value = true
  try {
    const queryParts = [`institution_type=${instType}`]
    if (params.governorate) queryParts.push(`governorate=${params.governorate}`)
    if (params.directorate) queryParts.push(`directorate=${params.directorate}`)
    const res = await api.get(`api/academic/organizations/all/?${queryParts.join('&')}`)
    const data = res.data?.data || res.data?.results || res.data || []
    allSchoolsList.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error("Error loading organizations:", e)
    allSchoolsList.value = []
  } finally {
    loadingSchools.value = false
  }
}

const loadGeographicOrgs = async () => {
  await loadEducationalHierarchy()
}

const onFilterGovForDirectorates = (val) => {
  selectedGovernorateForFilter.value = val
  selectedTargetIds.value = []
}

const onFilterGovForSchoolChange = (val) => {
  selectedGovernorateForFilter.value = val
  selectedDirectorateForFilter.value = null
  selectedTargetIds.value = []
  allSchoolsList.value = []
  const instType = exam.value.institution_type || 'school'
  if (val && instType !== 'school') {
    loadOrganizations({ governorate: val })
  }
}

const onFilterDirForSchoolChange = (val) => {
  selectedDirectorateForFilter.value = val
  selectedTargetIds.value = []
  if (val && selectedGovernorateForFilter.value) {
    loadOrganizations({ governorate: selectedGovernorateForFilter.value, directorate: val })
  } else {
    allSchoolsList.value = []
  }
}

// ⭐ STRICT FILTERING: Only the entities chosen in Section 4 are available for model groups
const targetOptionsForGroups = computed(() => {
  if (exam.value.target_scope_level === 'all' || !selectedTargetIds.value || selectedTargetIds.value.length === 0) {
    return []
  }

  const selectedIds = new Set(selectedTargetIds.value)
  let sourceList = []
  if (exam.value.target_scope_level === 'governorate') {
    sourceList = governoratesList.value
  } else if (exam.value.target_scope_level === 'directorate') {
    sourceList = directoratesList.value
  } else if (exam.value.target_scope_level === 'school') {
    sourceList = allSchoolsList.value
  }

  return sourceList
    .filter(item => selectedIds.has(item.id))
    .map(item => ({
      id: item.id,
      name: item.name_ar || item.name || `هدف #${item.id}`
    }))
})

// Clean up group assignments if target scope or selection changes
watch(selectedTargetIds, (newIds) => {
  if (isLoadingForEdit.value) return
  const validIds = new Set(newIds || [])
  modelGroups.value.forEach(group => {
    if (group.assigned_target_ids && group.assigned_target_ids.length > 0) {
      group.assigned_target_ids = group.assigned_target_ids.filter(id => validIds.has(id))
    }
  })
}, { deep: true })

const getAssignedTargetNames = (ids) => {
  if (!ids || !ids.length) return '—'
  const names = ids.map(id => {
    const opt = targetOptionsForGroups.value.find(o => o.id === id)
    if (opt) return opt.name
    const found = governoratesList.value.find(o => o.id === id) ||
                  directoratesList.value.find(o => o.id === id) ||
                  allSchoolsList.value.find(o => o.id === id)
    return found ? (found.name_ar || found.name) : `#${id}`
  })
  return names.join('، ')
}

const onGroupScopeLevelChange = (group) => {
  group.target_ids = []
  group.filter_governorate_id = null
  group.filter_directorate_id = null
  group.availableSchools = []
}

const getDirectoratesForGroup = (group) => {
  if (!group || !group.filter_governorate_id) return allDirectoratesList.value
  return allDirectoratesList.value.filter(d => d.fk_parent_organization === group.filter_governorate_id)
}

const getDirectoratesForFilterGov = (govId) => {
  if (!govId) return []
  return allDirectoratesList.value.filter(d => d.fk_parent_organization === govId)
}

const isGroupSchoolDisabled = (group) => {
  const instType = exam.value.institution_type || 'school'
  if (instType === 'school') {
    return !group.filter_governorate_id || !group.filter_directorate_id
  }
  return !group.filter_governorate_id
}

const onGroupFilterGovForSchool = (group) => {
  group.filter_directorate_id = null
  group.target_ids = []
  group.availableSchools = []
  const instType = exam.value.institution_type || 'school'
  if (group.filter_governorate_id && instType !== 'school') {
    loadSchoolsForGroup(group)
  }
}

const onGroupFilterDirForSchool = (group) => {
  group.target_ids = []
  if (group.filter_directorate_id && group.filter_governorate_id) {
    loadSchoolsForGroup(group)
  } else {
    group.availableSchools = []
  }
}

const loadSchoolsForGroup = async (group) => {
  const instType = exam.value.institution_type || 'school'
  group.loadingSchools = true
  try {
    const queryParts = [`institution_type=${instType}`]
    if (group.filter_governorate_id) queryParts.push(`governorate=${group.filter_governorate_id}`)
    if (group.filter_directorate_id) queryParts.push(`directorate=${group.filter_directorate_id}`)
    const res = await api.get(`api/academic/organizations/all/?${queryParts.join('&')}`)
    const data = res.data?.data || res.data?.results || res.data || []
    group.availableSchools = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('Error loading schools for group:', e)
    group.availableSchools = []
  } finally {
    group.loadingSchools = false
  }
}

const getGroupTargetNames = (group) => {
  if (!group) return '—'
  if ((group.scope_level || 'all') === 'all') return 'كافة المناطق (عام)'
  if (!group.target_ids || !group.target_ids.length) return 'غير محدد'

  if (group.scope_level === 'governorate') {
    const names = group.target_ids
      .map(id => governoratesList.value.find(g => g.id === id)?.name_ar)
      .filter(Boolean)
    return names.length ? names.join('، ') : `${group.target_ids.length} محافظة`
  }

  if (group.scope_level === 'directorate') {
    const names = group.target_ids
      .map(id => allDirectoratesList.value.find(d => d.id === id)?.name_ar)
      .filter(Boolean)
    return names.length ? names.join('، ') : `${group.target_ids.length} مديرية`
  }

  if (group.scope_level === 'school') {
    if (group.availableSchools && group.availableSchools.length) {
      const names = group.target_ids
        .map(id => group.availableSchools.find(s => s.id === id)?.name_ar)
        .filter(Boolean)
      if (names.length) return names.join('، ')
    }
    return `${group.target_ids.length} مؤسسة / مدرسة`
  }

  return `${group.target_ids.length} جهة`
}

const isAllGroupsAllRegions = computed(() => {
  if (!modelGroups.value || !modelGroups.value.length) return true
  return modelGroups.value.every(g => (g.scope_level || 'all') === 'all')
})

const totalUniqueAssignedTargetsCount = computed(() => {
  if (!modelGroups.value) return 0
  const allIds = new Set()
  modelGroups.value.forEach(g => {
    if ((g.scope_level || 'all') !== 'all' && Array.isArray(g.target_ids)) {
      g.target_ids.forEach(id => allIds.add(id))
    }
  })
  return allIds.size
})

const scopeLevelOptions = [
  { value: 'all', label: 'الكل (بدون تحديد)' },
  { value: 'governorate', label: 'محافظات محددة' },
  { value: 'directorate', label: 'مديريات محددة' },
  { value: 'school', label: 'مدارس محددة' },
]

const difficultyProfiles = [
  { value: 'easy', label: 'سهل' },
  { value: 'medium', label: 'متوسط' },
  { value: 'hard', label: 'صعب' },
  { value: 'mixed', label: 'مختلط' },
  { value: 'custom', label: 'مخصص' },
]

const difficultyItems = [
  { key: 'easy', label: 'سهل', color: 'success' },
  { key: 'medium', label: 'متوسط', color: 'warning' },
  { key: 'hard', label: 'صعب', color: 'error' },
]

const difficultyColor = (profile) => {
  const map = { 
    easy: 'success', 1: 'success', '1': 'success', 'سهل': 'success',
    medium: 'warning', 2: 'warning', '2': 'warning', 'متوسط': 'warning',
    hard: 'error', 3: 'error', '3': 'error', 'صعب': 'error',
    mixed: 'info', custom: 'deep-purple' 
  }
  return map[profile] || 'info'
}

const difficultyLabel = (profile) => {
  const map = { 
    easy: 'سهل', 1: 'سهل', '1': 'سهل', 'سهل': 'سهل',
    medium: 'متوسط', 2: 'متوسط', '2': 'متوسط', 'متوسط': 'متوسط',
    hard: 'صعب', 3: 'صعب', '3': 'صعب', 'صعب': 'صعب',
    mixed: 'مختلط', custom: 'مخصص' 
  }
  return map[profile] || profile
}

const applyDifficultyPreset = (group) => {
  if (group.difficulty_profile === 'custom') return
  const presets = {
    easy: { easy: 60, medium: 30, hard: 10 },
    medium: { easy: 20, medium: 60, hard: 20 },
    hard: { easy: 10, medium: 30, hard: 60 },
    mixed: { easy: 30, medium: 40, hard: 30 },
  }
  group.difficulty_distribution = { ...presets[group.difficulty_profile] || presets.mixed }
}

const groupDiffTotal = (group) => {
  const d = group.difficulty_distribution || {}
  return (Number(d.easy) || 0) + (Number(d.medium) || 0) + (Number(d.hard) || 0)
}

const getGroupDiffMax = (group, key) => {
  const dist = group.difficulty_distribution || {}
  const currentVal = Number(dist[key]) || 0
  const othersSum = (Number(dist.easy) || 0) + (Number(dist.medium) || 0) + (Number(dist.hard) || 0) - currentVal
  return Math.max(0, 100 - othersSum)
}

const updateGroupDiff = (group, key, newVal) => {
  const dist = group.difficulty_distribution
  if (!dist) return
  const currentVal = Number(dist[key]) || 0
  const othersSum = (Number(dist.easy) || 0) + (Number(dist.medium) || 0) + (Number(dist.hard) || 0) - currentVal
  const maxAllowed = Math.max(0, 100 - othersSum)

  if (newVal > maxAllowed) {
    if (dist[key] !== maxAllowed) {
      dist[key] = maxAllowed
    } else {
      // Force Vue reactivity tick so slider resets internal thumb position
      dist[key] = maxAllowed - 0.001
      nextTick(() => {
        dist[key] = maxAllowed
      })
    }
  } else {
    dist[key] = Math.max(0, newVal)
  }
  syncDifficultyProfile(group)
}

const stepGroupDiff = (group, key, delta) => {
  const dist = group.difficulty_distribution
  if (!dist) return
  const currentVal = Number(dist[key]) || 0
  const othersSum = (Number(dist.easy) || 0) + (Number(dist.medium) || 0) + (Number(dist.hard) || 0) - currentVal
  const maxAllowed = Math.max(0, 100 - othersSum)

  if (delta > 0) {
    dist[key] = Math.min(currentVal + delta, maxAllowed)
  } else {
    dist[key] = Math.max(0, currentVal + delta)
  }
  syncDifficultyProfile(group)
}

const syncDifficultyProfile = (group) => {
  const dist = group.difficulty_distribution || {}
  const presets = {
    easy: { easy: 60, medium: 30, hard: 10 },
    medium: { easy: 20, medium: 60, hard: 20 },
    hard: { easy: 10, medium: 30, hard: 60 },
    mixed: { easy: 30, medium: 40, hard: 30 },
  }
  for (const [profileKey, p] of Object.entries(presets)) {
    if (dist.easy === p.easy && dist.medium === p.medium && dist.hard === p.hard) {
      group.difficulty_profile = profileKey
      return
    }
  }
  group.difficulty_profile = 'custom'
}

const addModelGroup = () => {
  const nextNum = modelGroups.value.length + 1
  const initialUnits = blueprint.value.units ? JSON.parse(JSON.stringify(blueprint.value.units)) : []
  const initialTypes = blueprint.value.types ? JSON.parse(JSON.stringify(blueprint.value.types)) : []
  modelGroups.value.push({
    name: `المجموعة ${nextNum}`,
    count: 2,
    difficulty_profile: 'medium',
    difficulty_distribution: { easy: 20, medium: 60, hard: 20 },
    questions_variation: 'same_scrambled',
    scope_level: 'all',
    target_ids: [],
    units: initialUnits,
    types: initialTypes,
    filter_governorate_id: null,
    filter_directorate_id: null,
    availableSchools: [],
    loadingSchools: false,
  })
}

const removeModelGroup = (idx) => {
  modelGroups.value.splice(idx, 1)
  if (activeUnitGroupIndex.value >= modelGroups.value.length) {
    activeUnitGroupIndex.value = Math.max(0, modelGroups.value.length - 1)
  }
}

const totalModelsCount = computed(() => {
  if (modelsMode.value === 'advanced') {
    return modelGroups.value.reduce((sum, g) => sum + (g.count || 0), 0)
  }
  return exam.value.modelsCount || 2
})

const getGroupVersionCodes = (gIdx) => {
  let offset = 0
  for (let i = 0; i < gIdx; i++) {
    offset += modelGroups.value[i].count || 0
  }
  const codes = []
  for (let j = 0; j < (modelGroups.value[gIdx].count || 0); j++) {
    codes.push(String.fromCharCode(65 + offset + j))
  }
  return codes.join(', ')
}

const updateDistribution = (list, index, newVal) => {
  const othersSum = list.reduce((sum, item, idx) => idx === index ? sum : sum + (item.percentage || 0), 0)
  if (othersSum + newVal > 100) {
    list[index].percentage = Math.max(0, 100 - othersSum)
  } else {
    list[index].percentage = newVal
  }
}

// ═══════════════════════════════════════════════════════════
// Step 1 Master-Detail Sidebar Navigation State & Validation
// ═══════════════════════════════════════════════════════════
const activeStep1Section = ref(1)
const validatedOnce = ref(false)

const isSectionValid = (sectionId) => {
  if (sectionId === 1) {
    const hasBase = !!exam.value.yearId && !!exam.value.examPeriodId
    if (!hasBase) return false

    if (exam.value.institution_type === 'school') {
      return !!exam.value.stageId && !!exam.value.classTrackId && !!exam.value.subjectId
    }
    if (exam.value.institution_type === 'university') {
      return (
        !!exam.value.collegeId &&
        !!exam.value.departmentId &&
        !!exam.value.specializationId &&
        !!exam.value.semesterSubjectId
      )
    }
    if (exam.value.institution_type === 'institute') {
      return (
        !!exam.value.instituteFieldId &&
        !!exam.value.instituteEducationSystemId &&
        !!exam.value.instituteSpecializationId &&
        !!exam.value.instituteCurriculumId &&
        !!exam.value.instituteSubjectId
      )
    }
    return false
  }

  if (sectionId === 2) {
    const hasTitle = !!exam.value.title && String(exam.value.title).trim().length > 0
    const qCount = Number(exam.value.questionsCount)
    return hasTitle && !isNaN(qCount) && qCount >= 5 && qCount <= 100
  }

  if (sectionId === 3) {
    if (modelsMode.value === 'uniform') {
      const mCount = Number(exam.value.modelsCount)
      return !isNaN(mCount) && mCount >= 1 && mCount <= 10
    }
    if (!modelGroups.value || modelGroups.value.length === 0) return false
    return modelGroups.value.every(g => {
      const cnt = Number(g.count)
      const diffValid = !isNaN(cnt) && cnt >= 1 && cnt <= 10 && groupDiffTotal(g) === 100
      const geoValid = (g.scope_level || 'all') === 'all' || (Array.isArray(g.target_ids) && g.target_ids.length > 0)
      return diffValid && geoValid
    })
  }

  return true
}

const invalidSections = computed(() => {
  const list = []
  for (let s = 1; s <= 3; s++) {
    if (!isSectionValid(s)) {
      list.push(s)
    }
  }
  return list
})

const invalidSectionsCount = computed(() => invalidSections.value.length)

const step1NavItems = computed(() => {
  return [
    {
      id: 1,
      title: '1. النطاق والتصنيف الأكاديمي',
      desc: exam.value.institution_type === 'school' ? 'تعليم عام ومدرسي' : exam.value.institution_type === 'university' ? 'تعليم جامعي' : 'تعليم مهني',
      icon: 'mdi-school-outline',
      color: 'primary',
    },
    {
      id: 2,
      title: '2. تفاصيل وسعة ورقة الاختبار',
      desc: `${exam.value.questionsCount} سؤال`,
      icon: 'mdi-card-account-details-outline',
      color: 'info',
    },
    {
      id: 3,
      title: '3. إعدادات النماذج والتوزيع المناطقي',
      desc: modelsMode.value === 'uniform' ? `${exam.value.modelsCount} نماذج موحدة` : `${totalModelsCount.value} نماذج (${modelGroups.value.length} مجموعات)`,
      icon: 'mdi-file-multiple-outline',
      color: 'warning',
    }
  ]
})

const goToStep1Section = (sectionId) => {
  if (sectionId >= 1 && sectionId <= 3) {
    activeStep1Section.value = sectionId
  }
}


const onInstitutionTypeToggle = () => {
  exam.value.stageId = null
  exam.value.classTrackId = null
  exam.value.subjectId = null
  exam.value.collegeId = null
  exam.value.departmentId = null
  exam.value.specializationId = null
  exam.value.semesterSubjectId = null
  exam.value.instituteFieldId = null
  exam.value.instituteEducationSystemId = null
  exam.value.instituteSpecializationId = null
  exam.value.instituteCurriculumId = null
  exam.value.instituteSubjectId = null
  blueprint.value.units = []
  selectedTargetIds.value = []
  selectedGovernorateForFilter.value = null
  selectedDirectorateForFilter.value = null
  allSchoolsList.value = []
  if (exam.value.target_scope_level === 'directorate' && exam.value.institution_type !== 'school') {
    exam.value.target_scope_level = 'all'
  }
  if (modelGroups.value && modelGroups.value.length) {
    modelGroups.value.forEach(g => {
      if (g.scope_level === 'directorate' && exam.value.institution_type !== 'school') {
        g.scope_level = 'all'
      }
      g.target_ids = []
      g.filter_governorate_id = null
      g.filter_directorate_id = null
      g.availableSchools = []
      g.units = []
    })
  }
}

watch(() => exam.value.stageId, (newVal, oldVal) => {
  if (isLoadingForEdit.value) return
  if (newVal !== oldVal) {
    exam.value.classTrackId = null
  }
})

watch(() => exam.value.countryId, (newVal, oldVal) => {
  if (isLoadingForEdit.value) return
  if (newVal !== oldVal) {
    exam.value.governorateId = null
    exam.value.directorateId = null
    exam.value.regionId = null
    selectedTargetIds.value = []
    loadGovernorates(newVal)
  }
})

watch(() => exam.value.governorateId, (newVal, oldVal) => {
  if (isLoadingForEdit.value) return
  if (newVal !== oldVal) {
    exam.value.directorateId = null
    exam.value.regionId = null
  }
})

watch(() => exam.value.directorateId, (newVal, oldVal) => {
  if (isLoadingForEdit.value) return
  if (newVal !== oldVal) {
    exam.value.regionId = null
  }
})

watch(() => exam.value.target_scope_level, () => {
  if (isLoadingForEdit.value) return
  selectedTargetIds.value = []
  selectedGovernorateForFilter.value = null
  selectedDirectorateForFilter.value = null
  allSchoolsList.value = []
})

// Options from Store
const subjects = computed(() => store.getAll('subjects'))
const levels = computed(() => store.getAll('levels'))
const branches = computed(() => store.getAll('branches'))
const organizations = computed(() => store.getAll('organizations'))
const years = computed(() => store.getAll('years'))
const levelSubjectBranches = computed(() => store.getAll('levelSubjectBranches'))
const examPeriods = computed(() => store.getAll('examPeriods'))
const examSchedules = computed(() => store.getAll('examSchedules'))
const stages = computed(() => store.getAll('stages'))

const filteredLevels = computed(() => {
  let res = levels.value
  if (exam.value.stageId) {
    res = res.filter(l => l.stage === exam.value.stageId)
  }
  if (exam.value.branchId) {
    const validLevelIds = levelSubjectBranches.value
      .filter(lsb => (lsb.branchId || lsb.branch) === exam.value.branchId)
      .map(lsb => (lsb.levelId || lsb.level))
    res = res.filter(l => validLevelIds.includes(l.id))
  }
  return res
})

const filteredSubjects = computed(() => {
  let res = subjects.value
  if (!exam.value.branchId && !exam.value.stageId && !exam.value.levelId) return res

  let validSubjectIds = new Set(res.map(s => s.id))

  if (exam.value.branchId) {
    const branchSubIds = levelSubjectBranches.value
      .filter(lsb => (lsb.branchId || lsb.branch) === exam.value.branchId)
      .map(lsb => (lsb.subjectId || lsb.subject))
    validSubjectIds = new Set(branchSubIds)
  }

  if (exam.value.stageId && !exam.value.levelId) {
    const stageLevelIds = levels.value.filter(l => l.stage === exam.value.stageId).map(l => l.id)
    const stageSubIds = levelSubjectBranches.value
      .filter(lsb => stageLevelIds.includes(lsb.levelId || lsb.level))
      .map(lsb => (lsb.subjectId || lsb.subject))

    if (exam.value.branchId) {
      validSubjectIds = new Set([...validSubjectIds].filter(x => stageSubIds.includes(x)))
    } else {
      validSubjectIds = new Set(stageSubIds)
    }
  }

  if (exam.value.levelId) {
    const levelSubIds = levelSubjectBranches.value
      .filter(lsb => (lsb.levelId || lsb.level) === exam.value.levelId)
      .map(lsb => (lsb.subjectId || lsb.subject))

    if (exam.value.branchId || exam.value.stageId) {
      validSubjectIds = new Set([...validSubjectIds].filter(x => levelSubIds.includes(x)))
    } else {
      validSubjectIds = new Set([...levelSubIds])
    }
  }

  return res.filter(s => validSubjectIds.has(s.id))
})



watch(years, (newYears) => {
  if (!exam.value.yearId && newYears && newYears.length > 0) {
    const currentYear = newYears.find(y => y.is_current || y.isCurrent)
    exam.value.yearId = currentYear ? currentYear.id : newYears[0].id
  }
}, { immediate: true })

const loadExamForEditing = async (id) => {
  isLoadingForEdit.value = true
  try {
    const res = await examsService.getExamForEdit(id)
    if (res && res.success && res.data) {
      const d = res.data
      isEditing.value = true
      editingExamId.value = d.id
      editingExamCode.value = d.uniqueCode || `EXAM-#${d.id}`

      exam.value.title = d.title || ''
      exam.value.institution_type = d.institution_type || 'school'
      exam.value.yearId = d.yearId
      exam.value.subjectId = d.subjectId
      exam.value.examScheduleId = d.examScheduleId
      exam.value.examPeriodId = d.examPeriodId
      exam.value.stageId = d.stageId
      exam.value.levelId = d.levelId
      exam.value.classTrackId = d.classTrackId
      exam.value.collegeId = d.collegeId
      exam.value.departmentId = d.departmentId
      exam.value.specializationId = d.specializationId
      exam.value.semesterSubjectId = d.semesterSubjectId
      exam.value.countryId = d.countryId
      exam.value.governorateId = d.governorateId
      exam.value.directorateId = d.directorateId
      exam.value.regionId = d.regionId
      exam.value.questionsCount = d.questionsCount || 20
      exam.value.modelsCount = d.modelsCount || 2
      exam.value.totalMarks = d.totalMarks || 100
      exam.value.target_scope_level = d.target_scope_level || 'all'
      exam.value.exclude_previously_used = d.exclude_previously_used || false

      modelsMode.value = d.modelsMode || 'uniform'
      bloomEnabled.value = d.bloomEnabled || false

      if (Array.isArray(d.selectedTargetIds) && d.selectedTargetIds.length > 0) {
        selectedTargetIds.value = d.selectedTargetIds
      }

      if (Array.isArray(d.model_groups) && d.model_groups.length > 0) {
        modelGroups.value = d.model_groups
      }

      if (d.blueprint) {
        if (Array.isArray(d.blueprint.units) && d.blueprint.units.length > 0) {
          blueprint.value.units = d.blueprint.units
        }
        if (Array.isArray(d.blueprint.difficulty) && d.blueprint.difficulty.length > 0) {
          blueprint.value.difficulty = d.blueprint.difficulty
        }
        if (Array.isArray(d.blueprint.bloom) && d.blueprint.bloom.length > 0) {
          blueprint.value.bloom = d.blueprint.bloom
        }
        if (Array.isArray(d.blueprint.types) && d.blueprint.types.length > 0) {
          blueprint.value.types = d.blueprint.types
        }
      }

      if (Array.isArray(d.models) && d.models.length > 0) {
        stagedModels.value = d.models
        activeStagedModelIndex.value = 0
      }


    } else {
      throw new Error(res?.message || 'فشل في استرجاع بيانات الاختبار للتعديل')
    }
  } catch (err) {
    console.error('Error loading exam for edit:', err)
    const errMsg = err?.response?.data?.message || err?.message || 'تعذر استرجاع بيانات الاختبار للتعديل'
    if (proxy && proxy.$alert) {
      proxy.$alert('errorData', {
        message: errMsg,
        title: 'خطأ في تحميل الاختبار'
      })
    }
  } finally {
    setTimeout(() => {
      isLoadingForEdit.value = false
    }, 500)
  }
}

const exitEditMode = () => {
  isEditing.value = false
  editingExamId.value = null
  editingExamCode.value = ''
  router.replace({ path: '/exams-create' }).catch(() => {
    router.replace({ path: '/ExamGenerator/ExamCreateView' })
  })
  exam.value.title = ''
  exam.value.questionsCount = 20
  exam.value.modelsCount = 2
  stagedModels.value = []
  step.value = 1
}

onMounted(async () => {
  const editId = route.query.edit_exam_id

  // If editing an exam, start loading it IMMEDIATELY without waiting for background store caches
  const editTask = editId ? loadExamForEditing(editId) : Promise.resolve()

  // Background fetch store items in parallel without blocking the UI
  const bgFetches = Promise.allSettled([
    store.getAll('questions').length === 0 ? store.fetchQuestions() : Promise.resolve(),
    store.getAll('lessons').length === 0 ? store.fetchLessons() : Promise.resolve(),
    store.getAll('units').length === 0 ? store.fetchUnits() : Promise.resolve(),
    store.getAll('years').length === 0 ? store.fetchYears() : Promise.resolve(),
    loadGeographicOrgs()
  ])

  if (editId) {
    await editTask
  } else {
    await bgFetches
    if (!exam.value.yearId) {
      const currentYear = years.value.find(y => y.is_current || y.isCurrent)
      if (currentYear) {
        exam.value.yearId = currentYear.id
      } else if (years.value.length > 0) {
        exam.value.yearId = years.value[0].id
      }
    }
  }
})


watch(() => route.query.edit_exam_id, async (newId) => {
  if (newId && Number(newId) !== Number(editingExamId.value)) {
    await loadExamForEditing(newId)
  } else if (!newId && isEditing.value) {
    exitEditMode()
  }
})

// Blueprint
const blueprint = ref({
  units: [],
  difficulty: [
    { name: 'سهل', percentage: 30, color: 'success' },
    { name: 'متوسط', percentage: 50, color: 'warning' },
    { name: 'صعب', percentage: 20, color: 'error' },
  ],
  bloom: [
    { name: 'تذكر', percentage: 20, color: 'info' },
    { name: 'فهم', percentage: 25, color: 'success' },
    { name: 'تطبيق', percentage: 25, color: 'primary' },
    { name: 'تحليل', percentage: 15, color: 'warning' },
    { name: 'تقويم', percentage: 10, color: 'deep-orange' },
    { name: 'إبداع', percentage: 5, color: 'error' },
  ],
  types: [
    {
      id: 'single_choice',
      value: 'single_choice',
      name: 'اختيار من متعدد (إجابة واحدة)',
      shortName: 'MCQ فردي',
      subtitle: 'سؤال اختيار من متعدد بإجابة صحيحة واحدة فقط',
      percentage: 50,
      mark: 2.0,
      color: 'primary',
      icon: 'mdi-radiobox-marked'
    },
    {
      id: 'true_false',
      value: 'true_false',
      name: 'صواب / خطأ',
      shortName: 'صح/خطأ',
      subtitle: 'سؤال تحديد مدى صحة أو خطأ العبارة المعروضة',
      percentage: 50,
      mark: 1.0,
      color: 'success',
      icon: 'mdi-check-circle-outline'
    },
    {
      id: 'multiple_choice',
      value: 'multiple_choice',
      name: 'اختيار متعدد (أكثر من إجابة)',
      shortName: 'اختيار متعدد',
      subtitle: 'سؤال اختيار من متعدد يتضمن أكثر من إجابة صحيحة',
      percentage: 0,
      mark: 2.0,
      color: 'info',
      icon: 'mdi-checkbox-multiple-marked-outline'
    },
    {
      id: 'essay',
      value: 'essay',
      name: 'أسئلة مقالية (إنشائية)',
      shortName: 'مقالي',
      subtitle: 'أسئلة شرح وحلول تفصيلية تتطلب كتابة مقالية',
      percentage: 0,
      mark: 5.0,
      color: 'warning',
      icon: 'mdi-text-box-edit-outline'
    },
    {
      id: 'fill_blanks',
      value: 'fill_blanks',
      name: 'إكمال الفراغات',
      shortName: 'إكمال فراغ',
      subtitle: 'سؤال كتابة أو إدراج الكلمات الناقصة في الجمل',
      percentage: 0,
      mark: 2.0,
      color: 'deep-purple',
      icon: 'mdi-form-textbox'
    },
    {
      id: 'matching',
      value: 'matching',
      name: 'مطابقة وتوصيل (مزاوجة)',
      shortName: 'توصيل ومقابلة',
      subtitle: 'المقابلة والتوصيل بين مفردات القائمتين (أ) و (ب)',
      percentage: 0,
      mark: 2.0,
      color: 'teal',
      icon: 'mdi-swap-horizontal-bold'
    },
    {
      id: 'ordering',
      value: 'ordering',
      name: 'إعادة ترتيب',
      shortName: 'ترتيب تسلسلي',
      subtitle: 'إعادة ترتيب العناصر والخطوات بالترتيب الصحيح',
      percentage: 0,
      mark: 2.0,
      color: 'cyan',
      icon: 'mdi-sort-ascending'
    },
  ]
})

const getCurrentLsbId = () => {
  const lsb = levelSubjectBranches.value.find(l =>
    (l.subjectId || l.subject) === exam.value.subjectId &&
    (l.levelId || l.level) === exam.value.levelId &&
    (exam.value.branchId ? (l.branchId || l.branch) === exam.value.branchId : true)
  )
  return lsb ? lsb.id : null
}

const getUnitsForSubject = () => {
  const lsbId = getCurrentLsbId()
  if (!lsbId) return []
  const units = store.getAll('units')
  return units.filter(u => (u.levelSubjectBranchId || u.level_subject_branch) === lsbId)
}

const getUnitLessonsCount = (unitId) => {
  const bpUnit = blueprint.value.units?.find(u => u.id === unitId)
  if (bpUnit && typeof bpUnit.lessonsCount === 'number') {
    return bpUnit.lessonsCount
  }
  return store.getAll('lessons').filter(l => (l.unitId || l.unit) === unitId || (l.unit && l.unit.id === unitId)).length
}

const getUnitApprovedQuestionsCount = (unitId) => {
  const bpUnit = blueprint.value.units?.find(u => u.id === unitId)
  if (bpUnit && typeof bpUnit.approvedQuestionsCount === 'number') {
    return bpUnit.approvedQuestionsCount
  }
  const unitLessons = store.getAll('lessons').filter(l => (l.unitId || l.unit) === unitId || (l.unit && l.unit.id === unitId))
  const unitLessonIds = unitLessons.map(l => l.id)
  return store.getAll('questions').filter(q => {
    const qLessonId = q.lessonId || (typeof q.lesson === 'object' ? q.lesson?.id : q.lesson)
    const isApproved = q.status === 'معتمد' || q.status === 'approved'
    return unitLessonIds.includes(qLessonId) && isApproved
  }).length
}

const getUnitRequiredQuestions = (unit) => {
  if (!unit || unit.isExcluded) return 0
  const totalExamQuestions = Number(exam.value?.questionsCount) || 0
  const pct = Number(unit.percentage) || 0
  if (exam.value?.use_question_groups && currentUnitGroup?.value) {
    const grpQ = Number(currentUnitGroup.value.questions_count) || 0
    return Math.round(grpQ * (pct / 100))
  }
  return Math.round(totalExamQuestions * (pct / 100))
}

const getUnitRemainingQuestions = (unit) => {
  if (!unit) return 0
  const approved = unit.approvedQuestionsCount ?? getUnitApprovedQuestionsCount(unit.id) ?? 0
  const required = getUnitRequiredQuestions(unit)
  return approved - required
}

const unitDetailsDialog = ref({
  show: false,
  unitId: null,
  unitName: '',
  lessons: []
})

const openUnitDetails = async (unitId, unitName) => {
  let lessons = store.getAll('lessons').filter(l => (l.unitId || l.unit) === unitId || (l.unit && l.unit.id === unitId))

  if (!lessons || lessons.length === 0) {
    try {
      const endpoint = exam.value?.institution_type === 'school' ? 'school-lessons' : 'lessons'
      let res = await api.get(`api/academic/${endpoint}/all/`, { params: { unit: unitId } }).catch(() => null)
      let list = Array.isArray(res?.data) ? res.data : (res?.data?.data || res?.data?.results || [])
      if (!list || list.length === 0) {
        const otherEndpoint = endpoint === 'school-lessons' ? 'lessons' : 'school-lessons'
        res = await api.get(`api/academic/${otherEndpoint}/all/`, { params: { unit: unitId } }).catch(() => null)
        list = Array.isArray(res?.data) ? res.data : (res?.data?.data || res?.data?.results || [])
      }
      if (list && list.length > 0) {
        lessons = list
        const existing = store.getAll('lessons')
        const toAdd = list.filter(item => !existing.some(e => e.id === item.id))
        if (toAdd.length > 0) {
          store.setAll('lessons', [...existing, ...toAdd])
        }
      }
    } catch (e) {
      console.warn("Error fetching lessons for unit dialog:", e)
    }
  }

  // Ensure questions are loaded if empty
  if (store.getAll('questions').length === 0) {
    try {
      await store.fetchQuestions()
    } catch (e) {
      console.warn("Error fetching questions in openUnitDetails:", e)
    }
  }

  const allQuestions = store.getAll('questions')
  const enrichedLessons = (lessons || []).map(l => {
    const questionsCount = allQuestions.filter(q => {
      const qLessonId = q.lessonId || (typeof q.lesson === 'object' ? q.lesson?.id : q.lesson)
      const isApproved = q.status === 'معتمد' || q.status === 'approved'
      return qLessonId === l.id && isApproved
    }).length
    return { id: l.id, name: l.name_ar || l.name || l.name_en || `درس #${l.id}`, questionsCount }
  })

  // Synchronize unit card counts
  const bpUnit = blueprint.value.units?.find(u => u.id === unitId)
  if (bpUnit) {
    bpUnit.lessonsCount = enrichedLessons.length
    bpUnit.approvedQuestionsCount = enrichedLessons.reduce((sum, l) => sum + l.questionsCount, 0)
    bpUnit.lessons = enrichedLessons
  }

  const totalQ = bpUnit ? (bpUnit.approvedQuestionsCount ?? getUnitApprovedQuestionsCount(unitId)) : enrichedLessons.reduce((sum, l) => sum + l.questionsCount, 0)
  const reqQ = bpUnit ? getUnitRequiredQuestions(bpUnit) : 0
  const remQ = Math.max(0, totalQ - reqQ)

  unitDetailsDialog.value = {
    show: true,
    unitId,
    unitName,
    lessons: enrichedLessons,
    totalQuestions: totalQ,
    requiredQuestions: reqQ,
    remainingQuestions: remQ
  }
}

const expandedLessonId = ref(null)
const lessonQuestionsLoading = ref(false)
const lessonQuestionsList = reactive({})

const toggleLessonQuestions = async (lessonId) => {
  if (expandedLessonId.value === lessonId) {
    expandedLessonId.value = null
    return
  }
  expandedLessonId.value = lessonId
  if (!lessonQuestionsList[lessonId]) {
    lessonQuestionsLoading.value = true
    try {
      const res = await api.get('api/bank/questions/', {
        params: { lesson: lessonId, page_size: 100 }
      })
      const items = Array.isArray(res?.data) ? res.data : (res?.data?.results || [])
      // Fetch details in parallel to get options and answers
      const detailed = await Promise.all(
        items.map(async (q) => {
          try {
            const dRes = await api.get(`api/bank/questions/${q.id}/`)
            return dRes?.data?.data || dRes?.data || q
          } catch (e) {
            return q
          }
        })
      )
      lessonQuestionsList[lessonId] = detailed
    } catch (e) {
      console.error("Error fetching lesson questions:", e)
      lessonQuestionsList[lessonId] = []
    } finally {
      lessonQuestionsLoading.value = false
    }
  }
}

const getDifficultyColor = (diff) => {
  if (diff === 1 || diff === 'easy' || diff === 'سهل') return 'success'
  if (diff === 2 || diff === 'medium' || diff === 'متوسط') return 'warning'
  return 'error'
}

const getDifficultyText = (diff) => {
  if (diff === 1 || diff === 'easy' || diff === 'سهل') return 'سهل'
  if (diff === 2 || diff === 'medium' || diff === 'متوسط') return 'متوسط'
  return 'صعب'
}

const getQuestionTypeText = (type) => {
  const map = {
    'mcq': 'اختيار من متعدد',
    'single_choice': 'اختيار من متعدد',
    'multiple_choice': 'اختيارات متعددة',
    'true_false': 'صح / خطأ',
    'essay': 'مقالي',
    'fill_blanks': 'إكمال فراغات',
    'matching': 'مطابقة'
  }
  return map[type] || type || 'سؤال'
}

const goToAddQuestion = (unitId, lessonId) => {
  router.push({
    path: '/question-bank-new',
    query: {
      institution_type: exam.value.institution_type || 'school',
      stageId: exam.value.stageId,
      classTrackId: exam.value.classTrackId,
      subjectId: exam.value.subjectId,
      unitId,
      lessonId
    }
  })
}

const goToEditQuestion = (questionId) => {
  window.open(`/question-bank-new?id=${questionId}`, '_blank')
}

const openInQuestionBank = (unitId) => {
  unitDetailsDialog.value.show = false
  router.push({
    path: '/question-bank',
    query: {
      institution_type: exam.value.institution_type || 'school',
      stage: exam.value.stageId,
      class_track: exam.value.classTrackId,
      subject: exam.value.subjectId,
      unit: unitId
    }
  })
}

const loadBlueprintUnits = async () => {
  if (exam.value.institution_type === 'university' && exam.value.semesterSubjectId) {
    try {
      const res = await academicService.getUnits({ semester_subject_id: exam.value.semesterSubjectId })
      const uList = res.results || res || []
      if (uList.length > 0) {
        const perUnit = Math.floor(100 / uList.length)
        blueprint.value.units = uList.map((u, idx) => ({
          id: u.id,
          name: u.name_ar || u.name_en || u.name || `مفردة #${u.id}`,
          term: u.term || u.semester || 3,
          percentage: idx === uList.length - 1 ? 100 - (perUnit * (uList.length - 1)) : perUnit
        }))
      } else {
        blueprint.value.units = []
      }
    } catch (e) {
      console.error("Error loading university units for blueprint:", e)
      blueprint.value.units = []
    }
  } else if (exam.value.institution_type === 'institute' && exam.value.instituteSubjectId) {
    try {
      const res = await academicService.getUnits({ subject_id: exam.value.instituteSubjectId })
      const uList = res.results || res || []
      if (uList.length > 0) {
        const perUnit = Math.floor(100 / uList.length)
        blueprint.value.units = uList.map((u, idx) => ({
          id: u.id,
          name: u.name_ar || u.name_en || u.name || `الوحدة #${u.id}`,
          term: u.term || u.semester || 3,
          percentage: idx === uList.length - 1 ? 100 - (perUnit * (uList.length - 1)) : perUnit
        }))
      } else {
        blueprint.value.units = []
      }
    } catch (e) {
      console.error("Error loading institute units for blueprint:", e)
      blueprint.value.units = []
    }
  } else if (exam.value.subjectId && (exam.value.classTrackId || exam.value.levelId || exam.value.stageId)) {
    try {
      const params = {
        subject_id: exam.value.subjectId,
        school_subject: exam.value.subjectId,
        subject: exam.value.subjectId,
        institution_type: 'school'
      }
      if (exam.value.classTrackId) {
        params.class_track_id = exam.value.classTrackId
        params.class_track = exam.value.classTrackId
      }
      if (exam.value.levelId) params.level_id = exam.value.levelId
      if (exam.value.stageId) {
        params.stage_id = exam.value.stageId
        params.stage = exam.value.stageId
      }
      const res = await academicService.getSchoolUnits(params)
      let dbUnits = Array.isArray(res) ? res : (res?.results || [])
      if (!dbUnits || dbUnits.length === 0) {
        const fallbackRes = await academicService.getUnits(params)
        dbUnits = Array.isArray(fallbackRes) ? fallbackRes : (fallbackRes?.results || [])
      }
      if (!Array.isArray(dbUnits) || dbUnits.length === 0) {
        dbUnits = getUnitsForSubject()
      }
      if (dbUnits.length > 0) {
        const periodId = exam.value.examPeriodId;
        let targetTerms = [1, 2, 3]
        const selectedPeriod = store.getAll('examPeriods').find(p => p.id === periodId)
        if (selectedPeriod && selectedPeriod.target_terms) {
          try {
            targetTerms = typeof selectedPeriod.target_terms === 'string' 
                          ? JSON.parse(selectedPeriod.target_terms) 
                          : selectedPeriod.target_terms;
          } catch(e) {
            console.error("Invalid target_terms", e)
          }
        } else {
          if (periodId === 1 || periodId === 2) targetTerms = [1]
          else if (periodId === 3) targetTerms = [2]
          else if (periodId === 4) targetTerms = [1, 2]
        }

        let activeUnits = dbUnits.filter(u => targetTerms.includes(u.term || u.semester || 3))
        if (activeUnits.length === 0) activeUnits = dbUnits

        const perUnit = Math.floor(100 / activeUnits.length)

        if (dbUnits.length > 0) {
          try {
            const endpoint = exam.value.institution_type === 'school' ? 'school-lessons' : 'lessons'
            const { data } = await api.get(`api/academic/${endpoint}/all/`, { 
              params: exam.value.institution_type === 'school' ? { school_subject: exam.value.subjectId } : {} 
            })
            const list = Array.isArray(data) ? data : (data?.data || data?.results || [])
            if (list.length > 0) {
              const currentLessons = store.getAll('lessons')
              const map = new Map(currentLessons.map(l => [l.id, l]))
              list.forEach(l => map.set(l.id, l))
              store.setAll('lessons', Array.from(map.values()))
            }
          } catch(e) {
            console.warn("Error prefetching lessons for units:", e)
          }

          try {
            const qParams = { page_size: 1000 }
            if (exam.value.institution_type === 'school' && exam.value.subjectId) {
              qParams.subject = exam.value.subjectId
            }
            const qRes = await api.get('api/bank/questions/', { params: qParams })
            const qList = Array.isArray(qRes?.data) ? qRes.data : (qRes?.data?.results || [])
            if (qList.length > 0) {
              const currentQuestions = store.getAll('questions')
              const qMap = new Map(currentQuestions.map(q => [q.id, q]))
              qList.forEach(q => qMap.set(q.id, q))
              store.setAll('questions', Array.from(qMap.values()))
            }
          } catch(e) {
            console.warn("Error prefetching questions for units:", e)
          }
        }

        const allLessons = store.getAll('lessons')
        const allQuestions = store.getAll('questions')

        blueprint.value.units = dbUnits.map((u) => {
          const isActive = activeUnits.some(active => active.id === u.id)
          let percentage = 0
          if (isActive) {
            const activeIndex = activeUnits.findIndex(active => active.id === u.id)
            percentage = activeIndex === activeUnits.length - 1 ? 100 - (perUnit * (activeUnits.length - 1)) : perUnit
          }
          const uLessons = allLessons.filter(l => (l.unitId || l.unit) === u.id || (l.unit && l.unit.id === u.id))
          const uLessonIds = uLessons.map(l => l.id)
          const approvedCount = allQuestions.filter(q => {
            const qLessonId = q.lessonId || (typeof q.lesson === 'object' ? q.lesson?.id : q.lesson)
            const isApproved = q.status === 'معتمد' || q.status === 'approved'
            return uLessonIds.includes(qLessonId) && isApproved
          }).length

          return {
            id: u.id,
            name: u.name_ar || u.name_en || u.name || `وحدة #${u.id}`,
            term: u.term || u.semester || 3,
            percentage: percentage,
            lessonsCount: uLessons.length,
            approvedQuestionsCount: approvedCount,
            lessons: uLessons
          }
        })
      } else {
        blueprint.value.units = []
      }
    } catch (e) {
      console.error("Error loading school units:", e)
      const fallback = getUnitsForSubject()
      blueprint.value.units = fallback.map((u, idx) => ({
        id: u.id,
        name: u.name_ar || u.name_en || u.name || `وحدة #${u.id}`,
        term: u.term || u.semester || 3,
        percentage: idx === fallback.length - 1 ? 100 - (Math.floor(100 / fallback.length) * (fallback.length - 1)) : Math.floor(100 / fallback.length)
      }))
    }
  }

  // 🛡️ Check active curriculum exclusions for this year and subject
  const resolvedYear = exam.value.yearId || (years.value.find(y => y.is_current || y.isCurrent)?.id)
  const effectiveSubId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId
  if (resolvedYear && effectiveSubId && blueprint.value.units && blueprint.value.units.length > 0) {
    try {
      const exclRes = await examsService.getActiveExclusionIds({
        year_id: resolvedYear,
        institution_type: exam.value.institution_type,
        subject_id: effectiveSubId
      })
      const excludedUnitIds = new Set(exclRes?.excluded_unit_ids || [])
      if (excludedUnitIds.size > 0) {
        const includedUnits = blueprint.value.units.filter(u => !excludedUnitIds.has(u.id))
        const perInc = includedUnits.length > 0 ? Math.floor(100 / includedUnits.length) : 0
        let incIdx = 0
        blueprint.value.units.forEach(u => {
          if (excludedUnitIds.has(u.id)) {
            u.isExcluded = true
            u.percentage = 0
          } else {
            u.isExcluded = false
            u.percentage = incIdx === includedUnits.length - 1 ? 100 - (perInc * (includedUnits.length - 1)) : perInc
            incIdx++
          }
        })
      }
    } catch (exclErr) {
      console.error("Error loading curriculum exclusions for exam blueprint:", exclErr)
    }
  }

  syncModelGroupsUnits()
}

watch([
  () => exam.value.subjectId, 
  () => exam.value.classTrackId,
  () => exam.value.stageId,
  () => exam.value.levelId, 
  () => exam.value.branchId, 
  () => exam.value.examPeriodId, 
  () => exam.value.semesterSubjectId,
  () => exam.value.instituteSubjectId,
  () => exam.value.institution_type
], async () => {
  if (isLoadingForEdit.value) return
  await loadBlueprintUnits()
})

const totalUnitsPercentage = computed(() =>
  blueprint.value.units.reduce((sum, u) => sum + u.percentage, 0)
)
const totalDifficultyPercentage = computed(() =>
  blueprint.value.difficulty.reduce((sum, d) => sum + d.percentage, 0)
)
const totalBloomPercentage = computed(() => {
  if (!bloomEnabled.value) return 100
  return blueprint.value.bloom.reduce((sum, b) => sum + b.percentage, 0)
})
const totalTypesPercentage = computed(() =>
  blueprint.value.types.reduce((sum, t) => sum + t.percentage, 0)
)

// ═══════════════════════════════════════════════════════════
// Advanced Model Groups Units Distribution Helpers
// ═══════════════════════════════════════════════════════════
const activeUnitGroupIndex = ref(0)

const currentUnitGroup = computed(() => {
  if (modelsMode.value !== 'advanced') return null
  if (!modelGroups.value || modelGroups.value.length === 0) return null
  const idx = Math.min(Math.max(0, activeUnitGroupIndex.value), modelGroups.value.length - 1)
  return modelGroups.value[idx]
})

const selectUnitGroup = (gIdx) => {
  activeUnitGroupIndex.value = gIdx
  const grp = modelGroups.value[gIdx]
  if (grp && (!grp.units || grp.units.length === 0) && blueprint.value.units && blueprint.value.units.length > 0) {
    grp.units = JSON.parse(JSON.stringify(blueprint.value.units))
  }
}

const syncModelGroupsUnits = () => {
  const baseUnits = blueprint.value.units
  if (!baseUnits || baseUnits.length === 0) return
  modelGroups.value.forEach(group => {
    const isGrpEmpty = !group.units || group.units.length === 0 || group.units.every(u => (u.percentage || 0) === 0)
    if (isGrpEmpty || group.units.length !== baseUnits.length) {
      group.units = JSON.parse(JSON.stringify(baseUnits))
    } else {
      const existingMap = new Map(group.units.map(u => [u.id, u.percentage]))
      group.units = baseUnits.map(baseU => ({
        ...baseU,
        percentage: existingMap.has(baseU.id) ? existingMap.get(baseU.id) : baseU.percentage,
        isExcluded: baseU.isExcluded
      }))
    }
  })
}

// Pure computed property: NO side-effects, NO mutations
const currentActiveUnitsList = computed(() => {
  if (modelsMode.value === 'advanced') {
    const grp = currentUnitGroup.value
    if (grp && Array.isArray(grp.units) && grp.units.length > 0) {
      return grp.units
    }
  }
  return blueprint.value.units || []
})

const isUnitInTerm = (u, termId) => {
  const t = Number(u.term || u.semester || 3)
  if (termId === 1) return t === 1
  if (termId === 2) return t === 2
  return t !== 1 && t !== 2
}

const hasTermSeparation = computed(() => {
  const list = currentActiveUnitsList.value
  if (!list || list.length === 0) return false
  if (exam.value.institution_type === 'university' || exam.value.institution_type === 'institute') return false
  const hasTerm1 = list.some(u => Number(u.term || u.semester) === 1)
  const hasTerm2 = list.some(u => Number(u.term || u.semester) === 2)
  return hasTerm1 && hasTerm2
})

const updateUnitPercentage = (unitId, val) => {
  let targetList = blueprint.value.units
  if (modelsMode.value === 'advanced') {
    const grp = currentUnitGroup.value
    if (grp) {
      if (!grp.units || grp.units.length === 0) {
        if (blueprint.value.units && blueprint.value.units.length > 0) {
          grp.units = JSON.parse(JSON.stringify(blueprint.value.units))
        }
      }
      targetList = grp.units
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(u => u.id === unitId)
  if (realIndex !== -1) {
    updateDistribution(targetList, realIndex, val)
  }
}

const adjustUnitPercentage = (unitId, delta) => {
  let targetList = blueprint.value.units
  if (modelsMode.value === 'advanced') {
    const grp = currentUnitGroup.value
    if (grp) {
      if (!grp.units || grp.units.length === 0) {
        if (blueprint.value.units && blueprint.value.units.length > 0) {
          grp.units = JSON.parse(JSON.stringify(blueprint.value.units))
        }
      }
      targetList = grp.units
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(u => u.id === unitId)
  if (realIndex !== -1) {
    const currentVal = Number(targetList[realIndex].percentage) || 0
    const newVal = Math.max(0, Math.min(100, currentVal + delta))
    updateDistribution(targetList, realIndex, newVal)
  }
}

const getGroupUnitsTotal = (group) => {
  if (!group || !Array.isArray(group.units) || group.units.length === 0) {
    return totalUnitsPercentage.value
  }
  return group.units.reduce((sum, u) => sum + (Number(u.percentage) || 0), 0)
}

const currentGroupUnitsTotal = computed(() => {
  if (modelsMode.value === 'advanced') {
    return getGroupUnitsTotal(currentUnitGroup.value)
  }
  return totalUnitsPercentage.value
})

const distributeUnitsListEqually = (unitsList) => {
  if (!unitsList || unitsList.length === 0) return
  const activeItems = unitsList.filter(u => !u.isExcluded)
  if (activeItems.length === 0) return
  const perItem = Math.floor(100 / activeItems.length)
  let idx = 0
  unitsList.forEach(item => {
    if (item.isExcluded) {
      item.percentage = 0
    } else {
      item.percentage = idx === activeItems.length - 1 ? 100 - (perItem * (activeItems.length - 1)) : perItem
      idx++
    }
  })
}

const autoDistributeCurrentGroupUnits = async () => {
  if (!blueprint.value.units || blueprint.value.units.length === 0) {
    await loadBlueprintUnits()
  }
  if (modelsMode.value === 'advanced') {
    const grp = currentUnitGroup.value
    if (!grp) return
    if (!grp.units || grp.units.length === 0) {
      if (blueprint.value.units && blueprint.value.units.length > 0) {
        grp.units = JSON.parse(JSON.stringify(blueprint.value.units))
      }
    }
    if (grp.units && grp.units.length > 0) {
      distributeUnitsListEqually(grp.units)
    }
  } else {
    autoDistribute('units')
  }
}

// ═══════════════════════════════════════════════════════════
// Advanced Model Groups Question Types Distribution Helpers
// ═══════════════════════════════════════════════════════════
const activeTypeGroupIndex = ref(0)

const currentTypeGroup = computed(() => {
  if (modelsMode.value !== 'advanced') return null
  if (!modelGroups.value || modelGroups.value.length === 0) return null
  const idx = Math.min(Math.max(0, activeTypeGroupIndex.value), modelGroups.value.length - 1)
  return modelGroups.value[idx]
})

const selectTypeGroup = (gIdx) => {
  activeTypeGroupIndex.value = gIdx
  activeUnitGroupIndex.value = gIdx
  const grp = modelGroups.value[gIdx]
  if (grp && (!grp.types || grp.types.length === 0) && blueprint.value.types && blueprint.value.types.length > 0) {
    grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
  }
}

const syncModelGroupsQuestionTypes = () => {
  const baseTypes = blueprint.value.types
  if (!baseTypes || baseTypes.length === 0) return
  modelGroups.value.forEach(group => {
    const isGrpEmpty = !group.types || group.types.length === 0 || group.types.every(t => (t.percentage || 0) === 0)
    if (isGrpEmpty || group.types.length !== baseTypes.length) {
      group.types = JSON.parse(JSON.stringify(baseTypes))
    } else {
      const existingMap = new Map(group.types.map(t => [t.id || t.value, { pct: t.percentage, mark: t.mark }]))
      group.types = baseTypes.map(baseT => {
        const key = baseT.id || baseT.value
        const existing = existingMap.get(key)
        return {
          ...baseT,
          percentage: existing ? existing.pct : baseT.percentage,
          mark: (existing && existing.mark !== undefined) ? existing.mark : (baseT.mark || 1.0)
        }
      })
    }
  })
}

const currentActiveTypesList = computed(() => {
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp && Array.isArray(grp.types) && grp.types.length > 0) {
      return grp.types
    }
  }
  return blueprint.value.types || []
})

const getGroupTypesTotal = (group) => {
  if (!group || !Array.isArray(group.types) || group.types.length === 0) {
    return totalTypesPercentage.value
  }
  return group.types.reduce((sum, t) => sum + (Number(t.percentage) || 0), 0)
}

const currentGroupTypesTotal = computed(() => {
  if (modelsMode.value === 'advanced') {
    return getGroupTypesTotal(currentTypeGroup.value)
  }
  return totalTypesPercentage.value
})

const getTypeQuestionsCount = (qType) => {
  const pct = Number(qType.percentage) || 0
  const totalQ = Number(exam.value.questionsCount) || 40
  return Math.round(totalQ * pct / 100)
}

const getTypeTotalMarks = (qType) => {
  const count = getTypeQuestionsCount(qType)
  const mark = Number(qType.mark !== undefined ? qType.mark : 1.0)
  return Math.round(count * mark * 100) / 100
}

const currentGroupDistributedMarks = computed(() => {
  const list = currentActiveTypesList.value
  if (!list || list.length === 0) return 0
  const total = list.reduce((sum, t) => sum + getTypeTotalMarks(t), 0)
  return Math.round(total * 100) / 100
})

const updateTypeMark = (typeId, markVal) => {
  let targetList = blueprint.value.types
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp) {
      if (!grp.types || grp.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      targetList = grp.types
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(t => (t.id === typeId || t.value === typeId))
  if (realIndex !== -1) {
    targetList[realIndex].mark = Math.max(0, Math.round(Number(markVal) * 100) / 100)
  }
}

const adjustTypeMark = (typeId, delta) => {
  let targetList = blueprint.value.types
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp) {
      if (!grp.types || grp.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      targetList = grp.types
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(t => (t.id === typeId || t.value === typeId))
  if (realIndex !== -1) {
    const curMark = Number(targetList[realIndex].mark !== undefined ? targetList[realIndex].mark : 1.0)
    const newMark = Math.max(0.25, Math.round((curMark + delta) * 100) / 100)
    targetList[realIndex].mark = newMark
  }
}

const autoBalanceMarks = () => {
  let list = currentActiveTypesList.value
  if (!list || list.length === 0) return
  const activeTypes = list.filter(t => (t.percentage || 0) > 0)
  if (activeTypes.length === 0) return
  const totalTarget = Number(exam.value.totalMarks) || 100

  const hasTf = activeTypes.find(t => (t.id || t.value) === 'true_false' || (t.id || t.value) === 'tf')
  const hasMcq = activeTypes.find(t => (t.id || t.value) === 'single_choice' || (t.id || t.value) === 'mcq')

  if (activeTypes.length === 2 && hasTf && hasMcq) {
    const tfCount = getTypeQuestionsCount(hasTf)
    const mcqCount = getTypeQuestionsCount(hasMcq)
    if (totalTarget === 100 && tfCount === 20 && mcqCount === 40) {
      hasTf.mark = 1.0
      hasMcq.mark = 2.0
      return
    } else if (mcqCount > 0) {
      let tfM = 1.0
      let rem = totalTarget - (tfCount * tfM)
      if (rem > 0) {
        hasTf.mark = tfM
        hasMcq.mark = Math.round((rem / mcqCount) * 100) / 100
        return
      }
    }
  }

  const totalQuestionsInActive = activeTypes.reduce((sum, t) => sum + getTypeQuestionsCount(t), 0)
  if (totalQuestionsInActive > 0) {
    const markPerQ = totalTarget / totalQuestionsInActive
    activeTypes.forEach(t => {
      t.mark = Math.round(markPerQ * 100) / 100
    })
  }
}

const setTotalMarks = (val) => {
  exam.value.totalMarks = val
  autoBalanceMarks()
}

const updateTypePercentage = (typeId, val) => {
  let targetList = blueprint.value.types
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp) {
      if (!grp.types || grp.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      targetList = grp.types
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(t => (t.id === typeId || t.value === typeId))
  if (realIndex !== -1) {
    const newVal = Math.max(0, Math.min(100, Math.round(Number(val) || 0)))
    updateDistribution(targetList, realIndex, newVal)
  }
}

const adjustTypePercentage = (typeId, delta) => {
  let targetList = blueprint.value.types
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (grp) {
      if (!grp.types || grp.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      targetList = grp.types
    }
  }
  if (!targetList || targetList.length === 0) return
  const realIndex = targetList.findIndex(t => (t.id === typeId || t.value === typeId))
  if (realIndex !== -1) {
    const curVal = Number(targetList[realIndex].percentage) || 0
    const newVal = Math.max(0, Math.min(100, curVal + delta))
    updateDistribution(targetList, realIndex, newVal)
  }
}

const autoDistributeTypesList = (typesList) => {
  if (!typesList || typesList.length === 0) return
  let activeTypes = typesList.filter(t => (t.percentage || 0) > 0)
  if (activeTypes.length < 2) {
    activeTypes = typesList.slice(0, 2)
  }
  const perType = Math.floor(100 / activeTypes.length)
  let idx = 0
  typesList.forEach(t => {
    const isAct = activeTypes.some(at => (at.id || at.value) === (t.id || t.value))
    if (!isAct) {
      t.percentage = 0
    } else {
      t.percentage = idx === activeTypes.length - 1 ? 100 - (perType * (activeTypes.length - 1)) : perType
      idx++
    }
  })
}

const autoDistributeCurrentGroupTypes = () => {
  if (modelsMode.value === 'advanced') {
    const grp = currentTypeGroup.value
    if (!grp) return
    if (!grp.types || grp.types.length === 0) {
      if (blueprint.value.types && blueprint.value.types.length > 0) {
        grp.types = JSON.parse(JSON.stringify(blueprint.value.types))
      }
    }
    if (grp.types && grp.types.length > 0) {
      autoDistributeTypesList(grp.types)
    }
  } else {
    autoDistributeTypesList(blueprint.value.types)
  }
}

const autoDistributeAllGroupsTypes = () => {
  if (modelsMode.value === 'advanced' && modelGroups.value.length > 0) {
    modelGroups.value.forEach(group => {
      if (!group.types || group.types.length === 0) {
        if (blueprint.value.types && blueprint.value.types.length > 0) {
          group.types = JSON.parse(JSON.stringify(blueprint.value.types))
        }
      }
      if (group.types && group.types.length > 0) {
        autoDistributeTypesList(group.types)
      }
    })
  } else {
    autoDistributeTypesList(blueprint.value.types)
  }
}

const copyCurrentGroupTypesToAll = () => {
  if (modelsMode.value !== 'advanced') return
  const currentList = currentActiveTypesList.value
  if (!currentList || currentList.length === 0) return
  modelGroups.value.forEach((grp, idx) => {
    if (idx !== activeTypeGroupIndex.value) {
      grp.types = JSON.parse(JSON.stringify(currentList))
    }
  })
  if (proxy && proxy.$alert) {
    proxy.$alert("successData", {
      message: `تم نسخ توزيع أنواع الأسئلة لـ (${currentTypeGroup.value?.name || 'المجموعة الحالية'}) إلى جميع المجموعات بنجاح.`,
      title: "نسخ توزيع أنواع الأسئلة"
    })
  }
}

const autoDistributeAllGroupsUnits = async () => {
  if (!blueprint.value.units || blueprint.value.units.length === 0) {
    await loadBlueprintUnits()
  }
  if (modelsMode.value === 'advanced') {
    modelGroups.value.forEach(g => {
      if (!g.units || g.units.length === 0) {
        if (blueprint.value.units && blueprint.value.units.length > 0) {
          g.units = JSON.parse(JSON.stringify(blueprint.value.units))
        }
      }
      if (g.units && g.units.length > 0) {
        distributeUnitsListEqually(g.units)
      }
    })
  } else {
    autoDistribute('units')
  }
}

const copyCurrentGroupUnitsToAll = () => {
  if (modelsMode.value !== 'advanced') return
  const currentUnits = currentActiveUnitsList.value
  if (!currentUnits || currentUnits.length === 0) return
  modelGroups.value.forEach((g, idx) => {
    if (idx !== activeUnitGroupIndex.value) {
      g.units = JSON.parse(JSON.stringify(currentUnits))
    }
  })
  if (proxy && proxy.$alert) {
    proxy.$alert("success", { message: "تم نسخ توزيع الوحدات بنجاح إلى جميع المجموعات الأخرى", title: "تم النسخ" })
  }
}

watch(step, async (newStep) => {
  if (newStep === 2) {
    if (!blueprint.value.units || blueprint.value.units.length === 0) {
      await loadBlueprintUnits()
    }
    syncModelGroupsUnits()
  }
})

// ═══════════════════════════════════════════════════════════
// Standard Criteria & Auto Distribution
// ═══════════════════════════════════════════════════════════
const applyStandardCriteria = () => {
  blueprint.value.difficulty = [
    { name: 'سهل', percentage: 30, color: 'success' },
    { name: 'متوسط', percentage: 50, color: 'warning' },
    { name: 'صعب', percentage: 20, color: 'error' },
  ]
  blueprint.value.bloom = [
    { name: 'تذكر', percentage: 20, color: 'info' },
    { name: 'فهم', percentage: 25, color: 'success' },
    { name: 'تطبيق', percentage: 25, color: 'primary' },
    { name: 'تحليل', percentage: 15, color: 'warning' },
    { name: 'تقويم', percentage: 10, color: 'deep-orange' },
    { name: 'إبداع', percentage: 5, color: 'error' },
  ]
  autoDistribute('units')
  if (modelsMode.value === 'advanced') {
    autoDistributeAllGroupsUnits()
  }
}

const autoDistribute = (category) => {
  const list = blueprint.value[category]
  if (!list || list.length === 0) return

  if (category === 'units') {
    const activeItems = list.filter(u => !u.isExcluded)
    if (activeItems.length === 0) return
    const perItem = Math.floor(100 / activeItems.length)
    let idx = 0
    list.forEach(item => {
      if (item.isExcluded) {
        item.percentage = 0
      } else {
        item.percentage = idx === activeItems.length - 1 ? 100 - (perItem * (activeItems.length - 1)) : perItem
        idx++
      }
    })
  } else {
    const perItem = Math.floor(100 / list.length)
    list.forEach((item, idx) => {
      item.percentage = idx === list.length - 1 ? 100 - (perItem * (list.length - 1)) : perItem
    })
  }
}

// ═══════════════════════════════════════════════════════════
// Generation Flow
// ═══════════════════════════════════════════════════════════
const performGenerationSequence = async () => {
  generating.value = true

  try {
    await generateAndSaveExam()
    if (proxy && proxy.$alert) {
      proxy.$alert("success", { message: "تم إنشاء وتوليد الاختبار بنجاح وتم تحويله إلى أرشيف الاختبارات", title: "عملية ناجحة" })
    }
    router.push('/ExamGenerator/ExamArchiveView').catch(() => {
      router.push({ name: 'exams-archive' })
    })
  } catch (e) {
    console.error("Exam generation error:", e)
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", { message: e.message || "فشل إنشاء وتوليد الاختبار", title: "خطأ" })
    }
  } finally {
    generating.value = false
  }
}

// ═══════════════════════════════════════════════════════════════
// STEP 4: INTERACTIVE EXAM STAGING & COMPOSER LOGIC
// ═══════════════════════════════════════════════════════════════
const stagedModels = ref([])
const stagingLoading = ref(false)
const activeStagedModelIndex = ref(0)
const showCorrectAnswers = ref(true)

// Question Swap Dialog State
const swapDialog = ref(false)
const swapLoading = ref(false)
const swapCandidates = ref([])
const swapSearchQuery = ref('')
const swapScope = ref('lesson') // 'lesson' | 'unit' | 'all'
const targetSwapQuestion = ref(null)
const targetSwapModelIndex = ref(0)
// Quick Create Dialog State
const quickCreateDialog = ref(false)
const quickCreateLoading = ref(false)
const quickCreateForm = ref({
  content: '',
  unitId: null,
  unitName: '',
  lessonId: null,
  difficulty: 2,
  bloomLevel: 'تطبيق',
  questionType: 'Single Choice',
  defaultMark: 1.0,
  tfAnswer: true,
  options: [
    { text: '', isTrue: true },
    { text: '', isTrue: false },
    { text: '', isTrue: false },
    { text: '', isTrue: false },
  ]
})

const prepareStagingAndProceed = async () => {
  stagingLoading.value = true
  try {
    let resolvedYearId = exam.value.yearId
    if (!resolvedYearId) {
      const currentYear = years.value.find(y => y.is_current || y.isCurrent)
      resolvedYearId = currentYear ? currentYear.id : (years.value[0]?.id || null)
    }

    const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null

    const payload = {
      title: exam.value.title || 'اختبار جديد',
      institution_type: exam.value.institution_type || 'school',
      subjectId: effectiveSubjectId,
      semesterSubjectId: exam.value.semesterSubjectId || null,
      instituteSubjectId: exam.value.instituteSubjectId || null,
      yearId: resolvedYearId,
      stageId: exam.value.stageId || null,
      classTrackId: exam.value.classTrackId || null,
      questionsCount: exam.value.questionsCount,
      modelsCount: exam.value.modelsCount,
      total_marks: Number(exam.value.totalMarks) || 100,
      blueprint: blueprint.value,
      models_mode: modelsMode.value,
      model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
      bloom_enabled: bloomEnabled.value,
      exclude_previously_used: exam.value.exclude_previously_used,
    }

    const res = await examsService.previewStaging(payload)
    const modelsList = res?.models || res?.versions || []
    if (res && res.success && modelsList.length > 0) {
      stagedModels.value = modelsList
      activeStagedModelIndex.value = 0
      step.value = 4
      nextTick(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' })
      })
      if (proxy && proxy.$snack) {
        proxy.$snack("success", {
          message: "تم تجهيز المسودة التفاعلية للنماذج بنجاح",
        })
      }
    } else {
      if (proxy && proxy.$alert) {
        proxy.$alert("errorData", {
          message: res?.message || "تعذر إعداد مسودة النماذج.",
          title: "تنبيه"
        })
      }
    }
  } catch (err) {
    console.error("Preview staging error:", err)
    const errMsg = err?.response?.data?.message || err?.message || "حدث خطأ أثناء إعداد المسودة التفاعلية."
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", {
        message: errMsg,
        title: "خطأ في سحب الأسئلة"
      })
    }
  } finally {
    stagingLoading.value = false
  }
}

// 🔄 Quick Auto-Swap for a Question
const quickAutoSwap = async (question, modelIndex) => {
  const currentModel = stagedModels.value[modelIndex]
  if (!currentModel) return

  const allUsedIds = []
  stagedModels.value.forEach(m => {
    (m.questions || []).forEach(q => {
      if (q.id) allUsedIds.push(q.id)
    })
  })

  try {
    const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null
    const payload = {
      subjectId: effectiveSubjectId,
      semesterSubjectId: exam.value.semesterSubjectId || null,
      instituteSubjectId: exam.value.instituteSubjectId || null,
      institution_type: exam.value.institution_type || 'school',
      unitId: question.unitId,
      difficulty: question.difficulty,
      bloomLevel: question.bloomLevel,
      questionType: question.questionType,
      excludeIds: allUsedIds,
      limit: 1,
    }

    const res = await examsService.findReplacement(payload)
    if (res && res.success && res.questions && res.questions.length > 0) {
      const oldQuestionId = question.id
      const isSameGroupScrambled = currentModel.questions_variation !== 'different_questions'
      const currentGroupIndex = currentModel.model_group_index

      stagedModels.value.forEach((m, mIdx) => {
        if (mIdx === modelIndex || (isSameGroupScrambled && m.model_group_index === currentGroupIndex)) {
          const qIdx = (m.questions || []).findIndex(q => q.id === oldQuestionId)
          if (qIdx !== -1) {
            const replacement = {
              ...res.questions[0],
              orderIndex: m.questions[qIdx].orderIndex,
              assignedMark: m.questions[qIdx].assignedMark,
            }
            m.questions.splice(qIdx, 1, replacement)
          }
        }
      })

      if (proxy && proxy.$alert) {
        proxy.$alert("successData", {
          message: "تم استبدال السؤال بنجاح بسؤال مكافئ من البنك!",
          title: "تم الاستبدال"
        })
      }
    } else {
      if (proxy && proxy.$alert) {
        proxy.$alert("errorData", {
          message: "لم يتم العثور على سؤال بديل مطابق تماماً في البنك. يمكنك اختياره يدوياً أو إنشاء سؤال جديد فوراً.",
          title: "لا يوجد بديل مطابق"
        })
      }
    }
  } catch (err) {
    console.error("Auto swap error:", err)
  }
}

// 🔍 Manual Bank Replacement Dialog
const setSwapScope = async (scope) => {
  swapScope.value = scope
  await searchSwapCandidates()
}

const openSwapDialog = async (question, modelIndex) => {
  targetSwapQuestion.value = question
  targetSwapModelIndex.value = modelIndex
  swapSearchQuery.value = ''
  swapScope.value = question.lessonId ? 'lesson' : 'unit'
  swapDialog.value = true
  await searchSwapCandidates()
}

const searchSwapCandidates = async () => {
  if (!targetSwapQuestion.value) return
  swapLoading.value = true

  const allUsedIds = []
  stagedModels.value.forEach(m => {
    (m.questions || []).forEach(q => {
      if (q.id && q.id !== targetSwapQuestion.value.id) allUsedIds.push(q.id)
    })
  })

  try {
    const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null
    const payload = {
      subjectId: effectiveSubjectId,
      semesterSubjectId: exam.value.semesterSubjectId || null,
      instituteSubjectId: exam.value.instituteSubjectId || null,
      institution_type: exam.value.institution_type || 'school',
      unitId: targetSwapQuestion.value.unitId,
      lessonId: targetSwapQuestion.value.lessonId,
      scope: swapScope.value,
      difficulty: targetSwapQuestion.value.difficulty,
      bloomLevel: targetSwapQuestion.value.bloomLevel,
      questionType: targetSwapQuestion.value.questionType,
      excludeIds: allUsedIds,
      searchQuery: swapSearchQuery.value,
      limit: 20,
    }

    const res = await examsService.findReplacement(payload)
    if (res && res.success && res.questions) {
      swapCandidates.value = res.questions
    } else {
      swapCandidates.value = []
    }
  } catch (err) {
    console.error("Search swap candidates error:", err)
    swapCandidates.value = []
  } finally {
    swapLoading.value = false
  }
}

const applyReplacement = (cand) => {
  const currentModel = stagedModels.value[targetSwapModelIndex.value]
  if (!currentModel || !targetSwapQuestion.value) return

  const oldQuestionId = targetSwapQuestion.value.id
  const isSameGroupScrambled = currentModel.questions_variation !== 'different_questions'
  const currentGroupIndex = currentModel.model_group_index

  stagedModels.value.forEach((m, mIdx) => {
    if (mIdx === targetSwapModelIndex.value || (isSameGroupScrambled && m.model_group_index === currentGroupIndex)) {
      const qIdx = (m.questions || []).findIndex(q => q.id === oldQuestionId)
      if (qIdx !== -1) {
        const replacement = {
          ...cand,
          orderIndex: m.questions[qIdx].orderIndex,
          assignedMark: m.questions[qIdx].assignedMark,
        }
        m.questions.splice(qIdx, 1, replacement)
      }
    }
  })

  swapDialog.value = false
  if (proxy && proxy.$alert) {
    proxy.$alert("successData", {
      message: "تم اعتماد السؤال البديل في النموذج بنجاح!",
      title: "تم الاستبدال"
    })
  }
}

const openQuickCreateFromSwap = () => {
  swapDialog.value = false
  openQuickCreateDialog(targetSwapQuestion.value, targetSwapModelIndex.value)
}

// ➕ Quick On-The-Fly Question Creation
const openQuickCreateDialog = (question, modelIndex) => {
  targetSwapQuestion.value = question
  targetSwapModelIndex.value = modelIndex

  let qType = 'Single Choice'
  if (question.questionType && (question.questionType.includes('True') || question.questionType.includes('tf'))) {
    qType = 'True/False'
  } else if (question.questionType && question.questionType.includes('Essay')) {
    qType = 'Essay'
  }

  quickCreateForm.value = {
    content: '',
    unitId: question.unitId,
    unitName: question.unitName || 'الوحدة الحالية',
    lessonId: question.lessonId,
    difficulty: question.difficulty || 2,
    bloomLevel: question.bloomLevel || 'تطبيق',
    questionType: qType,
    defaultMark: question.assignedMark || 1.0,
    tfAnswer: true,
    options: [
      { text: '', isTrue: true },
      { text: '', isTrue: false },
      { text: '', isTrue: false },
      { text: '', isTrue: false },
    ]
  }

  quickCreateDialog.value = true
}

const addQuickOption = () => {
  quickCreateForm.value.options.push({ text: '', isTrue: false })
}

const removeQuickOption = (idx) => {
  if (quickCreateForm.value.options.length > 2) {
    quickCreateForm.value.options.splice(idx, 1)
    if (!quickCreateForm.value.options.some(o => o.isTrue)) {
      quickCreateForm.value.options[0].isTrue = true
    }
  }
}

const setQuickCorrectOption = (idx) => {
  quickCreateForm.value.options.forEach((opt, i) => {
    opt.isTrue = (i === idx)
  })
}

const submitQuickCreateQuestion = async () => {
  if (!quickCreateForm.value.content || !quickCreateForm.value.content.trim()) {
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", { message: "يرجى كتابة نص السؤال أولاً", title: "حقل مطلوب" })
    }
    return
  }

  quickCreateLoading.value = true
  try {
    let optionsPayload = []
    if (quickCreateForm.value.questionType === 'Single Choice') {
      const validOptions = quickCreateForm.value.options.filter(o => o.text && o.text.trim())
      if (validOptions.length < 2) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", { message: "يرجى إدخال خيارين على الأقل لسؤال الاختيار من متعدد", title: "خيارات ناقصة" })
        }
        quickCreateLoading.value = false
        return
      }
      optionsPayload = validOptions
    } else if (quickCreateForm.value.questionType === 'True/False') {
      optionsPayload = [
        { text: 'صواب', isTrue: quickCreateForm.value.tfAnswer === true },
        { text: 'خطأ', isTrue: quickCreateForm.value.tfAnswer === false },
      ]
    }

    const payload = {
      content: quickCreateForm.value.content,
      questionType: quickCreateForm.value.questionType,
      difficulty: quickCreateForm.value.difficulty,
      bloomLevel: quickCreateForm.value.bloomLevel,
      defaultMark: quickCreateForm.value.defaultMark,
      institution_type: exam.value.institution_type || 'school',
      unitId: quickCreateForm.value.unitId,
      lessonId: quickCreateForm.value.lessonId,
      options: optionsPayload,
    }

    const res = await examsService.quickCreateQuestion(payload)
    if (res && res.success && res.question) {
      const createdQ = res.question
      const currentModel = stagedModels.value[targetSwapModelIndex.value]
      const oldQuestionId = targetSwapQuestion.value ? targetSwapQuestion.value.id : null
      const isSameGroupScrambled = currentModel && currentModel.questions_variation !== 'different_questions'
      const currentGroupIndex = currentModel ? currentModel.model_group_index : 0

      stagedModels.value.forEach((m, mIdx) => {
        if (mIdx === targetSwapModelIndex.value || (isSameGroupScrambled && m.model_group_index === currentGroupIndex)) {
          const qIdx = oldQuestionId ? (m.questions || []).findIndex(q => q.id === oldQuestionId) : -1
          if (qIdx !== -1) {
            const replacement = {
              ...createdQ,
              orderIndex: m.questions[qIdx].orderIndex,
              assignedMark: quickCreateForm.value.defaultMark || m.questions[qIdx].assignedMark,
            }
            m.questions.splice(qIdx, 1, replacement)
          } else if (mIdx === targetSwapModelIndex.value) {
            createdQ.orderIndex = targetSwapQuestion.value ? targetSwapQuestion.value.orderIndex : (m.questions.length + 1)
            createdQ.assignedMark = quickCreateForm.value.defaultMark
            m.questions.push(createdQ)
          }
        }
      })

      quickCreateDialog.value = false
      if (proxy && proxy.$alert) {
        proxy.$alert("successData", {
          message: "تم حفظ السؤال في بنك الأسئلة وإدراجه في النموذج بنجاح!",
          title: "تم الحفظ والإدراج"
        })
      }
    } else {
      if (proxy && proxy.$alert) {
        proxy.$alert("errorData", { message: res?.message || "فشل إنشاء السؤال", title: "خطأ" })
      }
    }
  } catch (err) {
    console.error("Quick create error:", err)
    const msg = err?.response?.data?.message || err?.message || "حدث خطأ أثناء حفظ السؤال"
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", { message: msg, title: "خطأ" })
    }
  } finally {
    quickCreateLoading.value = false
  }
}

// 🏛️ Final Atomic Commit of Staged Models
const commitFinalExam = async () => {
  generating.value = true
  try {
    let resolvedYearId = exam.value.yearId
    if (!resolvedYearId) {
      const currentYear = years.value.find(y => y.is_current || y.isCurrent)
      resolvedYearId = currentYear ? currentYear.id : (years.value[0]?.id || null)
    }

    const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null

    const model_region_assignments = []
    const target_scopes = []
    let overall_target_scope_level = 'all'

    if (modelsMode.value === 'advanced') {
      modelGroups.value.forEach((group, gIdx) => {
        const scopeLvl = group.scope_level || 'all'
        if (scopeLvl !== 'all' && Array.isArray(group.target_ids) && group.target_ids.length > 0) {
          if (overall_target_scope_level === 'all') {
            overall_target_scope_level = scopeLvl
          }
          group.target_ids.forEach(targetId => {
            const assignment = {
              model_group_index: gIdx,
              difficulty_profile: group.difficulty_profile,
              scope_level: scopeLvl,
            }
            if (scopeLvl === 'governorate') assignment.governorate_id = targetId
            else if (scopeLvl === 'directorate') assignment.directorate_id = targetId
            else if (scopeLvl === 'sub_directorate') assignment.sub_directorate_id = targetId
            else if (scopeLvl === 'village') assignment.village_id = targetId
            else if (scopeLvl === 'center') assignment.exam_center_id = targetId
            model_region_assignments.push(assignment)
          })
        }
      })
    }

    const examPayload = {
      title: exam.value.title || 'اختبار نهائي',
      description: exam.value.description,
      exam_type: exam.value.exam_type || 'final',
      institution_type: exam.value.institution_type || 'school',
      subjectId: effectiveSubjectId,
      semesterSubjectId: exam.value.semesterSubjectId || null,
      instituteSubjectId: exam.value.instituteSubjectId || null,
      levelId: exam.value.levelId,
      branchId: exam.value.branchId,
      stageId: exam.value.stageId,
      classTrackId: exam.value.classTrackId,
      termId: exam.value.termId,
      academicRoundId: exam.value.academicRoundId,
      yearId: resolvedYearId,
      exam_period: exam.value.exam_period || 'morning',
      target_scope_level: overall_target_scope_level,
      target_scope_id: exam.value.target_scope_id,
      questionsCount: exam.value.questionsCount,
      modelsCount: exam.value.modelsCount,
      durationMinutes: exam.value.durationMinutes,
      totalMarks: Number(exam.value.totalMarks) || 100,
      passingMarks: exam.value.passingMarks || Math.round((Number(exam.value.totalMarks) || 100) * 0.5),
      blueprint: blueprint.value,
      models_mode: modelsMode.value,
      model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
      model_region_assignments: model_region_assignments,
      target_scopes: target_scopes,
      bloom_enabled: bloomEnabled.value,
      exclude_previously_used: exam.value.exclude_previously_used,
      final_versions: stagedModels.value,
    }

    if (isEditing.value && editingExamId.value) {
      examPayload.exam_id = editingExamId.value
    }

    const res = await examsService.generateExam(examPayload)
    if (res && res.success) {
      if (proxy && proxy.$alert) {
        proxy.$alert("successData", {
          message: isEditing.value ? "تم تحديث الاختبار ونماذجه بنجاح!" : "تم إنشاء الاختبار ونماذجه بنجاح كمسودة بانتظار الاعتماد!",
          title: isEditing.value ? "تم تحديث الاختبار بنجاح" : "مبروك! تم حفظ الاختبار"
        })
      }
      setTimeout(() => {
        router.push('/exams-archive').catch(() => {
          router.push({ path: '/ExamGenerator/ExamArchiveView' }).catch(() => {
            router.push({ name: 'exams-archive' })
          })
        })
      }, 1200)
    } else {
      if (proxy && proxy.$alert) {
        proxy.$alert("errorData", {
          message: res?.message || "فشل توليد الاختبار",
          title: "خطأ في الاعتماد"
        })
      }
    }
  } catch (err) {
    console.error("Commit final exam error:", err)
    const msg = err?.response?.data?.message || err?.message || "حدث خطأ أثناء اعتماد الاختبار"
    if (proxy && proxy.$alert) {
      proxy.$alert("errorData", { message: msg, title: "خطأ" })
    }
  } finally {
    generating.value = false
  }
}

const nextStep = async () => {
  if (step.value === 1) {
    validatedOnce.value = true

    let formValid = true
    if (step1Form.value) {
      const result = step1ComponentRef.value ? await step1ComponentRef.value.validate() : await step1Form.value.validate()
      formValid = result.valid
    }

    if (!formValid || invalidSections.value.length > 0) {
      const firstInvalid = invalidSections.value[0] || 1
      activeStep1Section.value = firstInvalid
      return
    }

    if (!blueprint.value.units || blueprint.value.units.length === 0) {
      await loadBlueprintUnits()
    }
    syncModelGroupsUnits()
    syncModelGroupsQuestionTypes()
    step.value = 2
    return
  }

  if (step.value === 2) {
    validatedStep2Once.value = true
    if (modelsMode.value === 'advanced') {
      const invalidGrp = modelGroups.value.find(g => getGroupUnitsTotal(g) !== 100)
      if (invalidGrp) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", {
            message: `مجموع نسب توزيع الوحدات في (${invalidGrp.name || 'إحدى المجموعات'}) هو ${getGroupUnitsTotal(invalidGrp)}% ويجب أن يعادل 100% تماماً قبل المتابعة.`,
            title: "تنبيه توزيع الوحدات"
          })
        }
        return
      }
      const invalidTypeGrp = modelGroups.value.find(g => getGroupTypesTotal(g) !== 100)
      if (invalidTypeGrp) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", {
            message: `مجموع نسب توزيع أنواع الأسئلة في (${invalidTypeGrp.name || 'إحدى المجموعات'}) هو ${getGroupTypesTotal(invalidTypeGrp)}% ويجب أن يعادل 100% تماماً قبل المتابعة.`,
            title: "تنبيه أنواع الأسئلة"
          })
        }
        return
      }
    } else {
      if (totalUnitsPercentage.value !== 100) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", {
            message: `مجموع نسب توزيع الوحدات الحالي هو ${totalUnitsPercentage.value}% ويجب أن يعادل 100% تماماً قبل المتابعة.`,
            title: "تنبيه توزيع الوحدات"
          })
        }
        return
      }
      if (totalTypesPercentage.value !== 100) {
        if (proxy && proxy.$alert) {
          proxy.$alert("errorData", {
            message: `مجموع نسب توزيع أنواع الأسئلة الحالي هو ${totalTypesPercentage.value}% ويجب أن يعادل 100% تماماً قبل المتابعة.`,
            title: "تنبيه أنواع الأسئلة"
          })
        }
        return
      }
    }
    step.value = 3
    return
  }

  if (step.value === 3) {
    try {
      const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null
      const payload = {
        subjectId: effectiveSubjectId,
        semesterSubjectId: exam.value.semesterSubjectId || null,
        instituteSubjectId: exam.value.instituteSubjectId || null,
        institution_type: exam.value.institution_type || 'school',
        stageId: exam.value.stageId || null,
        classTrackId: exam.value.classTrackId || null,
        questionsCount: exam.value.questionsCount,
        blueprint: blueprint.value,
        models_mode: modelsMode.value,
        model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
        bloom_enabled: bloomEnabled.value,
        exclude_previously_used: exam.value.exclude_previously_used,
      }
      const res = await examsService.checkShortage(payload)
      if (res && res.report) {
        shortageReport.value = res.report
        if (res.hasShortage) {
          shortageDialog.value = true
          return
        }
      }
      await prepareStagingAndProceed()
    } catch (e) {
      console.error("Shortage check error:", e)
      await prepareStagingAndProceed()
    }
    return
  }

  if (step.value === 4) {
    await commitFinalExam()
  }
}

const generateAndSaveExam = async () => {
  let resolvedYearId = exam.value.yearId
  if (!resolvedYearId) {
    const currentYear = years.value.find(y => y.is_current || y.isCurrent)
    resolvedYearId = currentYear ? currentYear.id : (years.value[0]?.id || null)
  }

  const effectiveSubjectId = exam.value.subjectId || exam.value.semesterSubjectId || exam.value.instituteSubjectId || null

  // Build model-region assignments and target scopes from per-group configuration
  const model_region_assignments = []
  const target_scopes = []
  let overall_target_scope_level = 'all'

  if (modelsMode.value === 'advanced') {
    modelGroups.value.forEach((group, gIdx) => {
      const scopeLvl = group.scope_level || 'all'
      if (scopeLvl !== 'all' && Array.isArray(group.target_ids) && group.target_ids.length > 0) {
        if (overall_target_scope_level === 'all') {
          overall_target_scope_level = scopeLvl
        }
        group.target_ids.forEach(targetId => {
          const assignment = {
            model_group_index: gIdx,
            difficulty_profile: group.difficulty_profile,
            scope_level: scopeLvl,
          }
          const scope = { scope_level: scopeLvl }

          if (scopeLvl === 'governorate') {
            assignment.governorate_id = targetId
            scope.governorate_id = targetId
          } else if (scopeLvl === 'directorate') {
            assignment.directorate_id = targetId
            scope.directorate_id = targetId
          } else if (scopeLvl === 'school') {
            assignment.organization_id = targetId
            scope.organization_id = targetId
          }

          model_region_assignments.push(assignment)
          target_scopes.push(scope)
        })
      }
    })
  }

  const payload = {
    title: exam.value.title,
    institution_type: exam.value.institution_type || 'school',
    subjectId: effectiveSubjectId,
    levelId: exam.value.levelId || null,
    stageId: exam.value.stageId || null,
    classTrackId: exam.value.classTrackId || null,
    branchId: exam.value.branchId || null,
    collegeId: exam.value.collegeId || null,
    departmentId: exam.value.departmentId || null,
    specializationId: exam.value.specializationId || null,
    semesterSubjectId: exam.value.semesterSubjectId || null,
    instituteFieldId: exam.value.instituteFieldId || null,
    instituteEducationSystemId: exam.value.instituteEducationSystemId || null,
    instituteSpecializationId: exam.value.instituteSpecializationId || null,
    instituteCurriculumId: exam.value.instituteCurriculumId || null,
    instituteSubjectId: exam.value.instituteSubjectId || null,
    yearId: resolvedYearId,
    countryId: exam.value.countryId || null,
    governorateId: exam.value.governorateId || null,
    directorateId: exam.value.directorateId || null,
    regionId: exam.value.regionId || null,
    questionsCount: exam.value.questionsCount,
    modelsCount: modelsMode.value === 'uniform' ? exam.value.modelsCount : totalModelsCount.value,
    total_marks: exam.value.totalMarks || 100,
    totalMarks: exam.value.totalMarks || 100,
    blueprint: {
      ...blueprint.value,
      total_marks: exam.value.totalMarks || 100
    },
    // Advanced Options
    bloom_enabled: bloomEnabled.value,
    models_mode: modelsMode.value,
    model_groups: modelsMode.value === 'advanced' ? modelGroups.value : [],
    target_scope_level: overall_target_scope_level,
    target_scopes: target_scopes,
    model_region_assignments: model_region_assignments,
    exclude_previously_used: exam.value.exclude_previously_used,
  }

  if (isEditing.value && editingExamId.value) {
    payload.exam_id = editingExamId.value
  }

  const res = await examsService.generateExam(payload)
  if (res && (res.success || res.id || res.examId)) {
    if (res.data) {
      store.add('exams', res.data)
    }
    return res
  } else {
    throw new Error(res?.message || "فشل توليد الاختبار")
  }
}
</script>

<style lang="scss" src="./styles/exam_create.scss">
</style>
