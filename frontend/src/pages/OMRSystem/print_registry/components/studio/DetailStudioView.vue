<template>
  <div class="detail-studio-container">
    <!-- 1. شريط الفلاتر الهيكلية واختيار الاختبار المعتمد (مرتب وهرمي) -->
    <StudioHierarchyBar
      :selected-school-name="selectedSchoolName"
      :exam-details="examDetails"
      :selected-exam="selectedExam"
      :show-hierarchy-filters="showHierarchyFilters"
      @update:show-hierarchy-filters="$emit('update:showHierarchyFilters', $event)"
      :loading-exams="loadingExams"
      :institution-type="institutionType"
      @update:institution-type="$emit('update:institutionType', $event)"
      :sector-options-objects="sectorOptionsObjects"
      :selected-office-id="selectedOfficeId"
      @update:selected-office-id="$emit('update:selectedOfficeId', $event)"
      :offices-objects="officesObjects"
      :selected-directorate-id="selectedDirectorateId"
      @update:selected-directorate-id="$emit('update:selectedDirectorateId', $event)"
      :directorates-objects-formatted="directoratesObjectsFormatted"
      :selected-school-id="selectedSchoolId"
      @update:selected-school-id="$emit('update:selectedSchoolId', $event)"
      :schools-objects-formatted="schoolsObjectsFormatted"
      :selected-exam-id="selectedExamId"
      @update:selected-exam-id="$emit('update:selectedExamId', $event)"
      :exams-objects-formatted="examsObjectsFormatted"
      @clear-school-filter="$emit('clear-school-filter')"
      @return-to-master="$emit('return-to-master')"
      @reset-filters="$emit('reset-hierarchy-filters')"
      @refresh="$emit('fetch-exams')"
      @sector-change="$emit('sector-change', $event)"
      @office-change="$emit('office-change', $event)"
      @directorate-change="$emit('directorate-change', $event)"
      @school-change="$emit('school-change', $event)"
      @exam-selected="$emit('exam-selected', $event)"
    />

    <!-- 2. بطاقة معلومات الاختبار المحدد -->
    <StudioExamHeader
      v-if="selectedExam"
      :selected-exam="selectedExam"
      :selected-school-name="selectedSchoolName"
      :versions-chip-label="versionsChipLabel"
      :exam-details="examDetails"
    />

    <!-- 3. شريط التنقل بين التبويبات -->
    <StudioTabsBar
      :active-tab="activeTab"
      :batches-count="(batches && batches.length) || 0"
      @switch-tab="$emit('switch-tab', $event)"
    />

    <!-- 4. محتوى الاستوديو -->
    <div v-show="activeTab !== 'history'">
      <!-- حالة التحميل -->
      <div v-if="loadingExamDetails" class="text-center py-12">
        <v-progress-circular indeterminate color="primary" size="48" class="mb-3" />
        <p class="text-body-2 font-weight-bold">جاري تحميل بيانات الاختبار والطلاب ونماذج الأسئلة...</p>
      </div>

      <!-- لم يتم اختيار اختبار -->
      <div v-else-if="!selectedExamId" class="text-center py-16 main-card rounded-2xl border">
        <v-avatar size="64" color="primary" variant="tonal" class="mb-4">
          <v-icon size="36">mdi-file-document-multiple-outline</v-icon>
        </v-avatar>
        <h3 class="text-h6 font-weight-black mb-1">يرجى اختيار الاختبار لعرض وتوليد أوراق الأسئلة والتظليل</h3>
        <p class="text-caption text-medium-emphasis mb-4">
          حدد الاختبار من القائمة المنسدلة أعلاه لعرض ورقة الأسئلة المعتمدة أو أوراق التظليل للطلاب المسجلين
        </p>
      </div>

      <!-- الاستوديو نشط -->
      <div v-else-if="examDetails">
        <!-- تنبيه الإشعارات -->
        <v-alert
          v-if="batchPrintNotification?.show"
          :type="batchPrintNotification?.color"
          variant="tonal"
          closable
          class="mb-4 rounded-xl font-weight-bold"
          @click:close="batchPrintNotification.show = false"
        >
          {{ batchPrintNotification?.message }}
        </v-alert>

        <!-- تبويب 1: أوراق التظليل وكشف الطلاب -->
        <div v-if="isTabVisited('sheets')" v-show="activeTab === 'sheets'">
          <StudioSheetsTab
            :exam-details="examDetails"
            :target-batch-students="targetBatchStudents || []"
            :selected-student-ids="selectedStudentIds || []"
            :filtered-roster-students="filteredRosterStudents || []"
            :printing-batch="printingBatch || false"
            :selected-sheet-layout="selectedSheetLayout || 'compact_a5'"
            @update:selected-sheet-layout="$emit('update:selectedSheetLayout', $event)"
            :show-adjustments-panel="showAdjustmentsPanel || false"
            @update:show-adjustments-panel="$emit('update:showAdjustmentsPanel', $event)"
            :custom-center-name="customCenterName"
            @update:custom-center-name="$emit('update:customCenterName', $event)"
            :custom-directorate="customDirectorate"
            @update:custom-directorate="$emit('update:customDirectorate', $event)"
            :custom-governorate="customGovernorate"
            @update:custom-governorate="$emit('update:customGovernorate', $event)"
            :custom-stage-title="customStageTitle"
            @update:custom-stage-title="$emit('update:customStageTitle', $event)"
            :custom-exam-year="customExamYear"
            @update:custom-exam-year="$emit('update:customExamYear', $event)"
            :selected-exam="selectedExam"
            :roster-model-filter="rosterModelFilter || 'all'"
            @update:roster-model-filter="$emit('update:rosterModelFilter', $event)"
            :model-filter-objects="modelFilterObjects || []"
            :roster-print-filter="rosterPrintFilter || 'all'"
            @update:roster-print-filter="$emit('update:rosterPrintFilter', $event)"
            :print-status-filter-objects="printStatusFilterObjects || []"
            :roster-search="rosterSearch"
            :roster-table-items="rosterTableItems"
            :get-roster-data="getRosterData"
            :roster-headers="rosterHeaders || []"
            :loading-exam-details="loadingExamDetails"
            :get-model-chip-color="getModelChipColor"
            @print-batch="$emit('print-batch')"
            @print-audit="$emit('print-audit')"
            @print-blank="$emit('print-blank', $event)"
            @select-all="$emit('select-all-roster')"
            @mark-printed="$emit('mark-printed')"
            @reset-overrides="$emit('reset-overrides')"
            @reset-filters="$emit('reset-roster-filters')"
            @toggle-select="$emit('toggle-student-select', $event)"
            @toggle-printed="$emit('toggle-student-printed', $event)"
            @preview-sheet="$emit('preview-sheet', $event)"
            @print-single="$emit('print-single-student', $event)"
          />
        </div>

        <!-- تبويب 2: نماذج الأسئلة الرسمية -->
        <div v-if="isTabVisited('questions')" v-show="activeTab === 'questions'">
          <StudioQuestionsTab
            :question-models-list="questionModelsList || []"
            :selected-question-paper-layout="selectedQuestionPaperLayout || 'a4'"
            @update:selected-question-paper-layout="$emit('update:selectedQuestionPaperLayout', $event)"
            :question-models-table-items="questionModelsTableItems"
            :get-question-models-data="getQuestionModelsData"
            :question-models-headers="questionModelsHeaders || []"
            :loading-exam-details="loadingExamDetails"
            :selected-exam="selectedExam"
            :custom-stage-title="customStageTitle"
            :custom-exam-year="customExamYear"
            :custom-governorate="customGovernorate"
            :custom-directorate="customDirectorate"
            :custom-center-name="customCenterName"
            :active-sheet-student="activeSheetStudent"
            :sheet-generation-mode="sheetGenerationMode"
            :exam-versions="examDetails?.versions"
            :get-model-chip-color="getModelChipColor"
            @print-all="$emit('print-all-questions')"
            @print-model="$emit('print-question-model', $event)"
            @print-current="$emit('print-current-questions', $event)"
          />
        </div>

        <!-- تبويب 3: حزم الاختبار المتكاملة للطلاب -->
        <div v-if="isTabVisited('package')" v-show="activeTab === 'package'">
          <StudioPackagesTab
            :printing-packages="printingPackages || false"
            :filtered-package-students="filteredPackageStudents || []"
            :selected-package-student-ids="selectedPackageStudentIds || []"
            :package-model-filter="packageModelFilter || 'all'"
            @update:package-model-filter="$emit('update:packageModelFilter', $event)"
            :model-filter-objects="modelFilterObjects || []"
            :package-table-items="packageTableItems"
            :get-package-data="getPackageData"
            :package-headers="packageHeaders || []"
            :loading-exam-details="loadingExamDetails"
            :selected-exam="selectedExam"
            :exam-details="examDetails"
            :custom-stage-title="customStageTitle"
            :custom-exam-year="customExamYear"
            :custom-governorate="customGovernorate"
            :custom-directorate="customDirectorate"
            :custom-center-name="customCenterName"
            :sheet-artboard-style="sheetArtboardStyle"
            :exam-field-layout="examFieldLayout"
            :institution-type="institutionType"
            :get-model-chip-color="getModelChipColor"
            @batch-print-packages="$emit('batch-print-packages')"
            @select-all-packages="$emit('select-all-packages')"
            @toggle-package-select="$emit('toggle-package-select', $event)"
            @toggle-printed="$emit('toggle-student-printed', $event)"
            @print-single-package="$emit('print-single-package', $event)"
          />
        </div>
      </div>

      <!-- حالة تعذر تحميل البيانات أو حدوث خطأ من الخادم -->
      <div v-else class="text-center py-16 main-card rounded-2xl border bg-surface">
        <v-avatar size="64" color="error" variant="tonal" class="mb-4">
          <v-icon size="36">mdi-cloud-alert</v-icon>
        </v-avatar>
        <h3 class="text-h6 font-weight-black mb-1 text-error">تعذر تحميل بيانات الاختبار من الخادم</h3>
        <p class="text-caption text-medium-emphasis mb-4">
          {{ examDetailsError?.message || 'حدث خطأ أثناء محاولة جلب تفاصيل الاختبار وقائمة الطلاب ونماذج الأسئلة، أو انقطع الاتصال بالخادم.' }}
        </p>
        <v-btn
          color="primary"
          variant="elevated"
          prepend-icon="mdi-refresh"
          :loading="loadingExamDetails"
          class="font-weight-bold px-4"
          @click="$emit('exam-selected', selectedExamId)"
        >
          إعادة المحاولة
        </v-btn>
      </div>
    </div>

    <!-- تبويب 4: سجل الدفعات المطبوعة -->
    <div v-if="isTabVisited('history')" v-show="activeTab === 'history'">
      <StudioHistoryTab
        :batches-table-items="batchesTableItems"
        :get-batches-data="getBatchesData"
        :headers="batchesHeaders || []"
        :loading-batches="loadingBatches || false"
        @view-batch="$emit('view-batch', $event)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import StudioHierarchyBar from './StudioHierarchyBar.vue'
import StudioExamHeader from './StudioExamHeader.vue'
import StudioTabsBar from './StudioTabsBar.vue'
import StudioSheetsTab from './StudioSheetsTab.vue'
import StudioQuestionsTab from './StudioQuestionsTab.vue'
import StudioPackagesTab from './StudioPackagesTab.vue'
import StudioHistoryTab from './StudioHistoryTab.vue'

defineProps<{
  // Selection & Hierarchy
  selectedSchoolName?: string
  examDetails?: any
  selectedExam?: any
  showHierarchyFilters: boolean
  loadingExams?: boolean
  institutionType: string
  sectorOptionsObjects?: any[]
  selectedOfficeId?: any
  officesObjects?: any[]
  selectedDirectorateId?: any
  directoratesObjectsFormatted?: any[]
  selectedSchoolId?: any
  schoolsObjectsFormatted?: any[]
  selectedExamId?: any
  examsObjectsFormatted?: any[]
  versionsChipLabel?: string

  // Navigation & Tabs
  activeTab: string
  batches?: any[]
  isTabVisited: (tab: string) => boolean
  loadingExamDetails: boolean
  examDetailsError?: any
  batchPrintNotification?: any

  // Tab 1: Sheets
  targetBatchStudents?: any[]
  selectedStudentIds?: any[]
  filteredRosterStudents?: any[]
  printingBatch?: boolean
  selectedSheetLayout?: string
  showAdjustmentsPanel?: boolean
  customCenterName?: string
  customDirectorate?: string
  customGovernorate?: string
  customStageTitle?: string
  customExamYear?: string
  rosterModelFilter?: string
  modelFilterObjects?: any[]
  rosterPrintFilter?: string
  printStatusFilterObjects?: any[]
  rosterSearch?: string
  rosterTableItems?: any
  getRosterData?: any
  rosterHeaders?: any[]
  getModelChipColor: (code?: string) => string

  // Tab 2: Questions
  questionModelsList?: any[]
  selectedQuestionPaperLayout?: string
  questionModelsTableItems?: any
  getQuestionModelsData?: any
  questionModelsHeaders?: any[]
  activeSheetStudent?: any
  sheetGenerationMode?: string

  // Tab 3: Packages
  printingPackages?: boolean
  filteredPackageStudents?: any[]
  selectedPackageStudentIds?: any[]
  packageModelFilter?: string
  packageTableItems?: any
  getPackageData?: any
  packageHeaders?: any[]
  sheetArtboardStyle?: any
  examFieldLayout?: any

  // Tab 4: History
  batchesTableItems?: any
  getBatchesData?: any
  batchesHeaders?: any[]
  loadingBatches?: boolean
}>()

defineEmits<{
  (e: 'update:showHierarchyFilters', val: boolean): void
  (e: 'update:institutionType', val: string): void
  (e: 'update:selectedOfficeId', val: any): void
  (e: 'update:selectedDirectorateId', val: any): void
  (e: 'update:selectedSchoolId', val: any): void
  (e: 'update:selectedExamId', val: any): void
  (e: 'clear-school-filter'): void
  (e: 'return-to-master'): void
  (e: 'reset-hierarchy-filters'): void
  (e: 'fetch-exams'): void
  (e: 'sector-change', val: string): void
  (e: 'office-change', val: any): void
  (e: 'directorate-change', val: any): void
  (e: 'school-change', val: any): void
  (e: 'exam-selected', val: any): void
  (e: 'switch-tab', tab: string): void

  // Sheets Tab Emits
  (e: 'update:selectedSheetLayout', val: string): void
  (e: 'update:showAdjustmentsPanel', val: boolean): void
  (e: 'update:customCenterName', val: string): void
  (e: 'update:customDirectorate', val: string): void
  (e: 'update:customGovernorate', val: string): void
  (e: 'update:customStageTitle', val: string): void
  (e: 'update:customExamYear', val: string): void
  (e: 'update:rosterModelFilter', val: string): void
  (e: 'update:rosterPrintFilter', val: string): void
  (e: 'print-batch'): void
  (e: 'print-audit'): void
  (e: 'print-blank', ver: string): void
  (e: 'select-all-roster'): void
  (e: 'mark-printed'): void
  (e: 'reset-overrides'): void
  (e: 'reset-roster-filters'): void
  (e: 'toggle-student-select', id: any): void
  (e: 'toggle-student-printed', item: any): void
  (e: 'preview-sheet', item: any): void
  (e: 'print-single-student', item: any): void

  // Questions Tab Emits
  (e: 'update:selectedQuestionPaperLayout', val: string): void
  (e: 'print-all-questions'): void
  (e: 'print-question-model', versionCode: string): void
  (e: 'print-current-questions', versionCode: string): void

  // Packages Tab Emits
  (e: 'update:packageModelFilter', val: string): void
  (e: 'batch-print-packages'): void
  (e: 'select-all-packages'): void
  (e: 'toggle-package-select', id: any): void
  (e: 'print-single-package', item: any): void

  // History Tab Emits
  (e: 'view-batch', item: any): void
}>()
</script>

<style scoped>
.detail-studio-container {
  width: 100%;
}
</style>
