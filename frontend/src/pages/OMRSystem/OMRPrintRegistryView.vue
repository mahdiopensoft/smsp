<template>
  <div class="qb-omr-print-registry pa-4 pa-md-6">

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. MASTER VIEW: الهيكل الإداري وسجل الطباعة المركزي             -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <MasterView
      v-if="currentView === 'master'"
      :filters="filters"
      :loading-master="loadingMaster"
      :master-error="masterDataError"
      @clear-error="masterDataError = null"
      v-model:master-tab="masterTab"
      :institution-type="institutionType"
      :filtered-offices-table="filteredOfficesTable"
      :filtered-directorates-table="filteredDirectoratesTable"
      :filtered-schools-table="filteredSchoolsTable"
      :filtered-master-exams-table="filteredMasterExamsTable"
      :filtered-batches-table="filteredBatchesTable"
      :office-master-table-items="officeMasterTableItems"
      :get-office-master-data="getOfficeMasterData"
      :office-master-headers="officeMasterHeaders"
      v-model:selected-office-master-rows="selectedOfficeMasterRows"
      :directorate-master-table-items="directorateMasterTableItems"
      :get-directorate-master-data="getDirectorateMasterData"
      :directorate-master-headers="directorateMasterHeaders"
      v-model:selected-directorate-master-rows="selectedDirectorateMasterRows"
      :school-master-table-items="schoolMasterTableItems"
      :get-school-master-data="getSchoolMasterData"
      :school-master-headers="schoolMasterHeaders"
      v-model:selected-school-master-rows="selectedSchoolMasterRows"
      v-model:exam-sub-tab="examSubTab"
      v-model:selected-exam-master-rows="selectedExamMasterRows"
      :exam-master-table-items="examMasterTableItems"
      :get-exam-master-data="getExamMasterData"
      :exam-master-headers="examMasterHeaders"
      :pending-and-active-orders-count="pendingAndActiveOrdersCount"
      :scheduled-exams-count="scheduledExamsCount"
      :due-exams-count="dueExamsCount"
      :completed-exams-count="completedExamsCount"
      :cancelled-exams-count="cancelledExamsCount"
      :all-exams-count="allExamsCount"
      v-model:selected-batch-master-rows="selectedBatchMasterRows"
      :batch-master-table-items="batchMasterTableItems"
      :get-batch-master-data="getBatchMasterData"
      :registry-master-headers="registryMasterHeaders"
      :loading-batches="loadingBatches"
      :selected-office-id="selectedOfficeId"
      :selected-directorate-id="selectedDirectorateId"
      :selected-school-id="selectedSchoolId"
      :normalize-ids="normalizeIds"
      @load-master-data="loadMasterData"
      @drill-down-office="drillDownToOffice"
      @open-office-studio="openOfficeStudio"
      @drill-down-directorate="drillDownToDirectorate"
      @open-directorate-studio="openDirectorateStudio"
      @open-school-exams-dialog="openSchoolExamsDialog"
      @open-school-studio="openSchoolStudio"
      @direct-print="openDirectPrintDialog"
      @open-exam-studio="openExamStudio"
      @preview-manifest="previewOrderManifest"
      @approve-order="openApproveDialog"
      @return-order="openReturnDialog"
      @advance-schedule="openAdvanceScheduleDialog"
      @cancel-order="openCancelOrderDialog"
      @view-history="openExamBatchesHistory"
      @view-batch="viewBatchDetails"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 2. DETAIL VIEW: استوديو المعاينة وطباعة الوثائق وحزم الاختبار  -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <DetailStudioView
      v-else
      :selected-school-name="selectedSchoolName"
      :exam-details="examDetails"
      :selected-exam="selectedExam"
      v-model:show-hierarchy-filters="showHierarchyFilters"
      :loading-exams="loadingExams"
      :exam-details-error="examDetailsError"
      v-model:institution-type="institutionType"
      :sector-options-objects="sectorOptionsObjects"
      v-model:selected-office-id="selectedOfficeId"
      :offices-objects="officesObjects"
      v-model:selected-directorate-id="selectedDirectorateId"
      :directorates-objects-formatted="directoratesObjectsFormatted"
      v-model:selected-school-id="selectedSchoolId"
      :schools-objects-formatted="schoolsObjectsFormatted"
      v-model:selected-exam-id="selectedExamId"
      :exams-objects-formatted="examsObjectsFormatted"
      :versions-chip-label="versionsChipLabel"
      :active-tab="activeTab"
      :batches="currentExamBatches"
      :is-tab-visited="isTabVisited"
      :loading-exam-details="loadingExamDetails"
      :marking-printed-loading="markingSelectedLoading"
      :batch-print-notification="batchPrintNotification"
      :target-batch-students="targetBatchStudents"
      :selected-student-ids="selectedStudentIds"
      :filtered-roster-students="filteredRosterStudents"
      :printing-batch="printingBatch"
      v-model:selected-sheet-layout="selectedSheetLayout"
      v-model:show-adjustments-panel="showAdjustmentsPanel"
      v-model:custom-center-name="customCenterName"
      v-model:custom-directorate="customDirectorate"
      v-model:custom-governorate="customGovernorate"
      v-model:custom-stage-title="customStageTitle"
      v-model:custom-exam-year="customExamYear"
      v-model:roster-model-filter="rosterModelFilter"
      :model-filter-objects="modelFilterObjects"
      v-model:roster-print-filter="rosterPrintFilter"
      :print-status-filter-objects="printStatusFilterObjects"
      :roster-search="rosterSearch"
      :roster-table-items="rosterTableItems"
      :get-roster-data="getRosterData"
      :roster-headers="rosterHeaders"
      :get-model-chip-color="getModelChipColor"
      :question-models-list="questionModelsList"
      v-model:selected-question-paper-layout="selectedQuestionPaperLayout"
      :question-models-table-items="questionModelsTableItems"
      :get-question-models-data="getQuestionModelsData"
      :question-models-headers="questionModelsHeaders"
      :active-sheet-student="activeSheetStudent"
      :sheet-generation-mode="sheetGenerationMode"
      :printing-packages="printingPackages"
      :filtered-package-students="filteredPackageStudents"
      :selected-package-student-ids="selectedPackageStudentIds"
      v-model:package-model-filter="packageModelFilter"
      :package-table-items="packageTableItems"
      :get-package-data="getPackageData"
      :package-headers="packageHeaders"
      :sheet-artboard-style="sheetArtboardStyle"
      :exam-field-layout="examFieldLayout"
      :batches-table-items="batchesTableItems"
      :get-batches-data="getBatchesData"
      :batches-headers="headers"
      :loading-batches="loadingBatches"
      @clear-school-filter="clearSchoolFilter"
      @return-to-master="returnToMaster"
      @reset-hierarchy-filters="resetHierarchyStudioFilters"
      @fetch-exams="fetchExamsList"
      @sector-change="onSectorChange"
      @office-change="onStudioOfficeChange"
      @directorate-change="onStudioDirectorateChange"
      @school-change="onStudioSchoolChange"
      @exam-selected="onExamSelected"
      @switch-tab="switchDetailTab"
      @print-batch="printSelectedOrAllRoster"
      @print-audit="printAuditRoster"
      @print-blank="printBlankSheetVersion"
      @select-all-roster="selectAllRosterStudents"
      @mark-printed="markSelectedAsPrinted"
      @reset-overrides="resetHeaderOverrides"
      @reset-roster-filters="resetRosterFilters"
      @toggle-student-select="toggleStudentSelection"
      @toggle-student-printed="toggleStudentPrintedStatus"
      @preview-sheet="openSingleSheetPreview"
      @print-single-student="printSingleStudentDirect"
      @print-all-questions="printAllQuestionPapers"
      @print-question-model="printQuestionPaperForModel"
      @print-current-questions="printCurrentQuestionPaper"
      @batch-print-packages="batchPrintSelectedPackages"
      @select-all-packages="selectAllPackageStudents"
      @toggle-package-select="togglePackageStudentSelection"
      @print-single-package="printSingleStudentPackage"
      @view-batch="viewBatchDetails"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- DIALOG: Batch Details (تفاصيل الدفعة المطبوعة وقائمة الطلاب)    -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <BatchDetailsDialog
      v-model="detailsDialog"
      :active-batch="activeBatch"
      :loading="loadingDetails"
      :table-items="batchStudentsTableItems"
      :get-data="getBatchStudentsData"
      :headers="studentsHeaders"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- DIALOG: Single Sheet Preview (معاينة ورقة التظليل الفردية)     -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <SingleSheetPreviewDialog
      ref="singlePreviewRef"
      v-model="singleSheetDialog"
      :student="previewStudent"
      :exam="selectedExam"
      :layout="selectedSheetLayout"
      :custom-stage-title="customStageTitle"
      :custom-exam-year="customExamYear"
      :custom-center-name="customCenterName"
      :custom-governorate="customGovernorate"
      :custom-directorate="customDirectorate"
      :questions-count="getQuestionsCountForVersion(previewStudent?.model_code)"
      :sections="getSectionsForVersion(previewStudent?.model_code)"
      :get-model-chip-color="getModelChipColor"
      @print="printPreviewStudentSheet"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 3. نافذة تفاصيل اختبارات ومواد المدرسة / المركز الامتحاني      -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <SchoolExamsDialog
      v-model="schoolExamsDialog"
      :school="selectedSchoolDialogItem"
      :table-items="schoolExamsTableItems"
      :get-data="getSchoolExamsData"
      :headers="schoolExamsHeaders"
      @select-exam="selectExamFromSchoolDialog"
      @open-studio="openSchoolStudio"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 4. نافذة معاينة إذن الصرف وأمر الطباعة الرسمي A4                -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <PrintOrderManifestDialog
      v-model="manifestDialog"
      :order-data="selectedManifestOrder"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 5. نافذة تأكيد اعتماد وجدولة طلب الطباعة (مكون منفصل ومستقل)     -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <PrintOrderApproveDialog
      v-model="approveOrderDialog"
      :exam="targetExamForApproval"
      @approved="onOrderApproved"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 6. نافذة إرجاع طلب الطباعة للتعديل مع الملاحظات                  -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <ReturnOrderDialog
      v-model="returnOrderDialog"
      :exam="targetExamForReturn"
      v-model:reason="returnReasonSelected"
      :reason-objects="returnReasonsObjects"
      v-model:notes="returnNotesText"
      :loading="actionLoading"
      @confirm="confirmOrderReturn"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 7. نافذة تقديم موعد الطباعة استثنائياً (مكون موحد)               -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <AdvanceScheduleDialog
      v-model="advanceScheduleDialog"
      :exam="targetExamForAdvance"
      :loading="actionLoading"
      @confirm="onConfirmAdvanceSchedule"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 8. نافذة إلغاء أمر الطباعة رسمياً وتوثيق القرار (مكون موحد)      -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <CancelPrintOrderDialog
      v-model="cancelOrderDialog"
      :exam="targetExamForCancel"
      :loading="actionLoading"
      @confirm="onConfirmCancelOrder"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 8. نافذة تنفيذ أمر الطباعة المباشر الفوري (مكون منفصل ومستقل)     -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <DirectPrintOrderDialog
      v-model="directPrintDialog"
      :exam="targetExamForDirectPrint"
      :loading="directPrintLoading"
      @start-print="onDirectPrintStart"
      @confirm-execution="executeDirectPrint"
      @open-studio="openExamStudioFromDirect"
      @preview-omr="previewFirstOmrSheet"
      @preview-question-paper="previewFirstQuestionPaper"
      @preview-manifest="previewOrderManifest"
    />

    <!-- Hidden Staging Container for Print Batches (Available at Root Template Level for Zero DOM Overhead in Both Master & Studio Views) -->
    <div v-if="printingBatch" id="omr-registry-batch-staging" class="d-none">
      <div
        v-for="st in targetBatchStudents"
        :key="`staging-reg-${st.id}-${selectedSheetLayout}`"
        class="batch-sheet-slot"
      >
        <YemeniAuditReportSheet
          v-if="selectedSheetLayout === 'full_a4'"
          :hide-action-bar="true"
          :student-name="st.student_name"
          :seat-number="st.seat_number"
          :serial-number="st.secret_number || st.model_code"
          :model-code="st.model_code || 'A'"
          :form-number="st.model_code || 'A'"
          :exam-subject="selectedExam?.subject_name || ''"
          :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار'))"
          :exam-year="customExamYear || selectedExam?.year_name || ''"
          :center-name="customCenterName || st.school_name || selectedExam?.center_name || selectedExam?.school_name || ''"
          :center-code="st.school_id || selectedExam?.id || ''"
          :governorate="customGovernorate || st.governorate || selectedExam?.governorate || ''"
          :directorate="customDirectorate || st.directorate || selectedExam?.directorate || ''"
          :barcode-value="st.barcode_value || `EXAM_${selectedExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
          :qr-value="st.qr_value || `${selectedExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
          :total-questions="getQuestionsCountForVersion(st.model_code)"
          :sections="getSectionsForVersion(st.model_code)"
        />

        <YemeniMinistrySheet
          v-else
          layout-mode="compact_a5"
          :student-name="st.student_name"
          :seat-number="st.seat_number"
          :serial-number="st.secret_number || st.model_code"
          :model-code="st.model_code || 'A'"
          :exam-subject="selectedExam?.subject_name || ''"
          :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار'))"
          :exam-year="customExamYear || selectedExam?.year_name || ''"
          :center-name="customCenterName || st.school_name || selectedExam?.center_name || selectedExam?.school_name || ''"
          :governorate="customGovernorate || st.governorate || selectedExam?.governorate || ''"
          :directorate="customDirectorate || st.directorate || selectedExam?.directorate || ''"
          :barcode-value="st.barcode_value || `EXAM_${selectedExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
          :qr-value="st.qr_value || `${selectedExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
          :total-questions="getQuestionsCountForVersion(st.model_code)"
          :sections="getSectionsForVersion(st.model_code)"
          :interactive="false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/omr/client.js'
import { gradebookAPI } from '@/services/omr/endpoints'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'
import YemeniAuditReportSheet from '@/components/omr_templates/YemeniAuditReportSheet.vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'
import { printOmrElement, printOmrBatch, printOfficialQuestionPaper, printExamPackage, printExamPackagesBatch, escapeHtml, sanitizePrintNode } from './utils/omrPrint'
import PrintOrderManifestDialog from './components/PrintOrderManifestDialog.vue'
import PrintOrderApproveDialog from './components/PrintOrderApproveDialog.vue'
import DirectPrintOrderDialog from './components/DirectPrintOrderDialog.vue'
import AdvanceScheduleDialog from './components/AdvanceScheduleDialog.vue'
import CancelPrintOrderDialog from './components/CancelPrintOrderDialog.vue'
import MasterView from './print_registry/components/master/MasterView.vue'
import SchoolExamsDialog from './print_registry/components/dialogs/SchoolExamsDialog.vue'
import ReturnOrderDialog from './print_registry/components/dialogs/ReturnOrderDialog.vue'
import DetailStudioView from './print_registry/components/studio/DetailStudioView.vue'
import BatchDetailsDialog from './print_registry/components/dialogs/BatchDetailsDialog.vue'
import SingleSheetPreviewDialog from './print_registry/components/dialogs/SingleSheetPreviewDialog.vue'
import { usePrintRegistryFilters } from './print_registry/composables/usePrintRegistryFilters'
import { usePrintOrdersWorkflow } from './print_registry/composables/usePrintOrdersWorkflow'


const route = useRoute()
const router = useRouter()

// ── Master View & Administrative Hierarchy State ──
const currentView = ref(route.query.exam ? 'detail' : 'master')
const masterTab = ref('schools')
const sectorOptions = [
  { title: 'التعليم العام (المدرسي)', value: 'school', icon: 'mdi-school' },
  { title: 'التعليم الجامعي (كليات وجامعات)', value: 'university', icon: 'mdi-domain' },
  { title: 'التعليم الفني والمهني (معاهد)', value: 'institute', icon: 'mdi-tools' },
]
const loadingMaster = ref(false)

// ── Unified Tripartite Filters State via Composable ──
const filters = usePrintRegistryFilters({ onFilterChange: () => loadMasterData() })
const {
  filterInstitutionType,
  institutionType,
  filterGovernorate,
  filterDirectorate,
  filterOrganization,
  filterStage,
  filterClassTrack,
  filterSubject,
  filterCollege,
  filterDepartment,
  filterSpecialization,
  filterSemesterSubject,
  filterInstituteField,
  filterInstituteEducationSystem,
  filterInstituteSpecialization,
  filterInstituteSubject,
  masterSearchQuery,
  getEffectiveInstitutionType,
  isSchoolFilter,
  isOrgDisabled,
  orgFieldLabel,
  orgPlaceholder,
  orgParam,
  subjectFilterParam,
  instituteSpecParam,
  instituteSubjectParam,
  onInstitutionTypeChange,
  onGovernorateChange,
  onDirectorateChange,
  onOrganizationChange,
  onStageChange,
  onClassTrackChange,
  onCollegeChange,
  onDepartmentChange,
  onSpecializationChange,
  onInstituteFieldChange,
  onInstituteEducationSystemChange,
  resetUnifiedFilters,
} = filters

const allOfficesList = ref([])
const selectedOfficeId = ref([])
const selectedOfficeName = ref('')
const selectedDirectorateId = ref([])
const selectedDirectorateName = ref('')
const selectedSchoolId = ref([])
const selectedSchoolName = ref('')
const selectedSubjectId = ref(null)
const selectedSubjectName = ref('')
const subjectsList = ref([])

// Dialog for School Exams List
const schoolExamsDialog = ref(false)
const selectedSchoolDialogItem = ref(null)

const officesList = ref([])
const directoratesList = ref([])
const schoolsList = ref([])
const masterExamsList = ref([])
const batches = ref([])
const currentExamBatches = computed(() => {
  if (!selectedExamId.value) return []
  return (batches.value || []).filter(b => Number(b.exam_id) === Number(selectedExamId.value))
})
const loadingBatches = ref(false)

// ── Unified Notification & Error Handling System ──
const batchPrintNotification = ref({ show: false, message: '', color: 'success' })

const handleOmrError = (operationName, err, customFallbackMsg = 'حدث خطأ أثناء تنفيذ العملية') => {
  const statusCode = err?.response?.status
  const serverMessage = err?.response?.data?.message || err?.response?.data?.detail || err?.response?.data?.error
  const errorDetails = {
    operation: operationName,
    statusCode,
    serverMessage,
    clientMessage: err?.message,
    url: err?.config?.url,
    timestamp: new Date().toISOString()
  }
  console.error(`[OMR Registry Error: ${operationName}]`, errorDetails)

  const displayMsg = serverMessage || (statusCode ? `خطأ في الخادم (رمز: ${statusCode})` : err?.message || customFallbackMsg)
  batchPrintNotification.value = {
    show: true,
    color: 'error',
    message: `${customFallbackMsg}: ${displayMsg}`
  }
  return errorDetails
}

// Master Table Headers
const officeMasterHeaders = [
  { title: "مكتب التربية والتعليم (المحافظة)", key: "office_name", sortable: true, align: "start", width: "340px", minWidth: "320px" },
  { title: "المديريات", key: "directorates_count", sortable: true, align: "center", width: "95px" },
  { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "125px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "95px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الإنجاز", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
]

const directorateMasterHeaders = [
  { title: "إدارة التربية والتعليم (المديرية)", key: "name", sortable: true, align: "start", width: "340px", minWidth: "320px" },
  { title: "المكتب التابع له", key: "office_name", sortable: true, align: "center", width: "180px" },
  { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "125px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "95px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الإنجاز", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
]

const schoolMasterHeaders = [
  { title: "المدرسة / المركز الامتحاني", key: "name", sortable: true, align: "start", width: "320px", minWidth: "280px" },
  { title: "نوع المؤسسة", key: "institution_type", sortable: true, align: "center", width: "105px" },
  { title: "المحافظة والمديرية", key: "directorate_name", sortable: true, align: "center", width: "170px" },
  { title: "المادة الدراسية", key: "subject_name", sortable: true, align: "center", width: "160px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "105px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "115px" },
  { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "120px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "115px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "190px" },
]

const schoolExamsHeaders = [
  { title: "رمز الاختبار", key: "code", sortable: true, align: "center", width: "135px" },
  { title: "عنوان الاختبار والمواصفات", key: "title", sortable: true, align: "start" },
  { title: "المادة الدراسية", key: "subject", sortable: true, align: "center", width: "120px" },
  { title: "طلاب المركز", key: "students_count", sortable: true, align: "center", width: "105px" },
  { title: "النماذج المخصصة للطلاب وتوزيعها", key: "versions", sortable: false, align: "center", width: "230px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "110px" },
]

const examMasterHeaders = [
  { title: "رمز الاختبار", key: "uniqueCode", sortable: true, align: "center", width: "125px" },
  { title: "عنوان الاختبار والمادة", key: "title", sortable: true, align: "start", width: "290px", minWidth: "240px" },
  { title: "المدارس المشاركة", key: "schools_count", sortable: true, align: "center", width: "115px" },
  { title: "المقيدون", key: "total_registered", sortable: true, align: "center", width: "95px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "105px" },
  { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "115px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "140px" },
]

const registryMasterHeaders = [
  { title: "رقم الدفعة", key: "batch_id", sortable: true, align: "center", width: "170px" },
  { title: "عنوان الاختبار", key: "exam_title", sortable: true, align: "start", width: "300px", minWidth: "260px" },
  { title: "عدد الأوراق", key: "total_sheets", sortable: true, align: "center", width: "110px" },
  { title: "تاريخ الطباعة", key: "printed_at", sortable: true, align: "center", width: "160px" },
  { title: "المسؤول", key: "printed_by_name", sortable: true, align: "center", width: "140px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "120px" },
]

// Master KPI Computeds
const kpiTotalPrinted = computed(() => {
  return masterExamsList.value.reduce((acc, e) => acc + (Number(e.printed_count) || 0), 0)
})

const kpiTotalRegistered = computed(() => {
  return masterExamsList.value.reduce((acc, e) => acc + (Number(e.total_registered || e.total_students) || 0), 0)
})

const kpiPrintRate = computed(() => {
  if (!kpiTotalRegistered.value) return 0
  return Math.round((kpiTotalPrinted.value / kpiTotalRegistered.value) * 1000) / 10
})

const kpiSchoolsCount = computed(() => {
  return schoolsList.value.length
})

const kpiExamsCount = computed(() => {
  return masterExamsList.value.length
})

const normalizeIds = (val) => {
  if (!val) return []
  if (Array.isArray(val)) {
    return val.map(x => {
      if (typeof x === 'object' && x !== null) {
        return Number(x.id ?? x.value ?? x.raw?.id)
      }
      return Number(x)
    }).filter(n => !isNaN(n) && n > 0)
  }
  if (typeof val === 'object' && val !== null) {
    const id = Number(val.id ?? val.value ?? val.raw?.id)
    return (!isNaN(id) && id > 0) ? [id] : []
  }
  if (typeof val === 'string' && val.includes(',')) {
    return val.split(',').map(s => Number(s.trim())).filter(n => !isNaN(n) && n > 0)
  }
  const num = Number(val)
  return (!isNaN(num) && num > 0) ? [num] : []
}

// Autocomplete Options
const directoratesOptions = computed(() => {
  const officeIds = normalizeIds(selectedOfficeId.value)
  if (officeIds.length > 0) {
    const oObjs = (officesList.value || []).filter(o => 
      officeIds.includes(Number(o.id)) ||
      officeIds.includes(Number(o.core_org_id)) ||
      officeIds.includes(Number(o.office_id)) ||
      officeIds.includes(Number(o.governorate_id)) ||
      officeIds.includes(Number(o.fk_governorate_id))
    )
    const allOffIds = [...officeIds, ...oObjs.map(o => Number(o.id)), ...oObjs.map(o => Number(o.office_id)), ...oObjs.map(o => Number(o.governorate_id)), ...oObjs.map(o => Number(o.fk_governorate_id))].filter(Boolean)
    return (directoratesList.value || []).filter(d => 
      allOffIds.includes(Number(d.office_id)) ||
      allOffIds.includes(Number(d.governorate_id)) ||
      allOffIds.includes(Number(d.fk_governorate_id))
    )
  }
  return directoratesList.value || []
})

const schoolsOptions = computed(() => {
  let list = schoolsList.value || []
  const effType = getEffectiveInstitutionType()
  if (effType) {
    list = list.filter(s => !s.institution_type || s.institution_type === effType)
  }
  const dirIds = normalizeIds(selectedDirectorateId.value)
  const officeIds = normalizeIds(selectedOfficeId.value)

  if (dirIds.length > 0) {
    const dObjs = (directoratesList.value || []).filter(d => 
      dirIds.includes(Number(d.id)) ||
      dirIds.includes(Number(d.directorate_id)) ||
      dirIds.includes(Number(d.fk_directorate_id))
    )
    const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
    const allDirIds = [...dirIds, ...dObjs.map(d => Number(d.id)), ...dObjs.map(d => Number(d.directorate_id)), ...dObjs.map(d => Number(d.fk_directorate_id))].filter(Boolean)
    list = list.filter(s => 
      allDirIds.includes(Number(s.directorate_id)) ||
      allDirIds.includes(Number(s.fk_directorate_id)) ||
      dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
    )
  } else if (officeIds.length > 0) {
    const oObjs = (officesList.value || []).filter(o => 
      officeIds.includes(Number(o.id)) ||
      officeIds.includes(Number(o.core_org_id)) ||
      officeIds.includes(Number(o.office_id)) ||
      officeIds.includes(Number(o.governorate_id)) ||
      officeIds.includes(Number(o.fk_governorate_id))
    )
    const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
    const allOffIds = [...officeIds, ...oObjs.map(o => Number(o.id)), ...oObjs.map(o => Number(o.office_id)), ...oObjs.map(o => Number(o.governorate_id)), ...oObjs.map(o => Number(o.fk_governorate_id))].filter(Boolean)
    list = list.filter(s => 
      allOffIds.includes(Number(s.office_id)) ||
      allOffIds.includes(Number(s.governorate_id)) ||
      allOffIds.includes(Number(s.fk_governorate_id)) ||
      oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
    )
  }
  return list
})

// Unified Objects for <auto-list> integration
const sectorOptionsObjects = computed(() => {
  return (sectorOptions || []).map(opt => ({
    id: opt.value,
    value: opt.value,
    name: opt.title,
    title: opt.title,
  }))
})

const officesObjects = computed(() => {
  return (officesList.value || []).map(o => ({
    id: o.id,
    value: o.id,
    name: o.office_name || o.name_ar || o.name,
    title: o.office_name || o.name_ar || o.name,
  }))
})

const directoratesObjectsFormatted = computed(() => {
  return (directoratesOptions.value || []).map(d => ({
    id: d.id,
    value: d.id,
    name: d.name || d.name_ar,
    title: d.name || d.name_ar,
  }))
})

const schoolsObjectsFormatted = computed(() => {
  return (schoolsOptions.value || []).map(s => ({
    id: s.id,
    value: s.id,
    name: s.name || s.school_name || s.name_ar,
    title: s.name || s.school_name || s.name_ar,
  }))
})

const examsObjectsFormatted = computed(() => {
  return (examsList.value || []).map(e => ({
    id: e.id,
    value: e.id,
    name: `${e.title || e.name || 'اختبار'} (${e.subject_name || 'عام'} - ${e.uniqueCode || ''})`,
    title: `${e.title || e.name || 'اختبار'} (${e.subject_name || 'عام'} - ${e.uniqueCode || ''})`,
  }))
})

// Filtered Master Tables Computeds
const filteredOfficesTable = computed(() => {
  let list = officesList.value || []
  const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)
  if (effGov.length > 0) {
    list = list.filter(o => 
      effGov.includes(Number(o.id)) || 
      effGov.includes(Number(o.governorate_id)) || 
      effGov.includes(Number(o.fk_governorate_id))
    )
  }
  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    list = list.filter(o => (o.exams_count || 0) > 0)
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(o => 
      (o.office_name && o.office_name.toLowerCase().includes(q)) ||
      (o.governorate_name && o.governorate_name.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredDirectoratesTable = computed(() => {
  let list = directoratesList.value || []
  const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)
  if (effGov.length > 0) {
    list = list.filter(d => 
      effGov.includes(Number(d.office_id)) || 
      effGov.includes(Number(d.governorate_id)) ||
      effGov.includes(Number(d.fk_governorate_id))
    )
  }
  const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
  if (effDir.length > 0) {
    list = list.filter(d => 
      effDir.includes(Number(d.id)) || 
      effDir.includes(Number(d.directorate_id)) || 
      effDir.includes(Number(d.fk_directorate_id))
    )
  }
  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    list = list.filter(d => (d.exams_count || 0) > 0)
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(d => 
      (d.name && d.name.toLowerCase().includes(q)) ||
      (d.office_name && d.office_name.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredSchoolsTable = computed(() => {
  let list = schoolsList.value || []
  const effType = getEffectiveInstitutionType()
  if (effType) {
    list = list.filter(s => !s.institution_type || s.institution_type === effType)
  }
  const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
  const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)

  if (effDir.length > 0) {
    const dObjs = (directoratesList.value || []).filter(d => 
      effDir.includes(Number(d.id)) || 
      effDir.includes(Number(d.directorate_id)) || 
      effDir.includes(Number(d.fk_directorate_id))
    )
    const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
    list = list.filter(s => 
      effDir.includes(Number(s.directorate_id)) ||
      effDir.includes(Number(s.fk_directorate_id)) ||
      dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
    )
  } else if (effGov.length > 0) {
    const oObjs = (officesList.value || []).filter(o => 
      effGov.includes(Number(o.id)) || 
      effGov.includes(Number(o.governorate_id)) || 
      effGov.includes(Number(o.fk_governorate_id))
    )
    const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
    list = list.filter(s => 
      effGov.includes(Number(s.office_id)) ||
      effGov.includes(Number(s.governorate_id)) ||
      effGov.includes(Number(s.fk_governorate_id)) ||
      oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
    )
  }
  const effOrg = filterOrganization.value ? [Number(filterOrganization.value)] : normalizeIds(selectedSchoolId.value)
  if (effOrg.length > 0) {
    list = list.filter(s => effOrg.includes(Number(s.id)) || effOrg.includes(Number(s.organization_id)))
  }
  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    const sObj = subjectsList.value.find(s => Number(s.id) === Number(effSubj))
    const sName = sObj?.name?.trim() || sObj?.name_ar?.trim()
    list = list.filter(s => {
      if (!sName) return true
      if (s.subjects && Array.isArray(s.subjects)) {
        return s.subjects.some(sub => sub === sName || sub.includes(sName))
      }
      return s.subject_name === sName || (s.subject_name && s.subject_name.includes(sName))
    })
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(s => 
      (s.name && s.name.toLowerCase().includes(q)) ||
      (s.directorate_name && s.directorate_name.toLowerCase().includes(q)) ||
      (s.governorate_name && s.governorate_name.toLowerCase().includes(q)) ||
      (s.subject_name && s.subject_name.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredMasterExamsTable = computed(() => {
  let list = masterExamsList.value || []
  const effType = getEffectiveInstitutionType()
  if (effType) {
    list = list.filter(e => !e.institution_type || e.institution_type === effType)
  }
  const effOrg = filterOrganization.value ? [Number(filterOrganization.value)] : normalizeIds(selectedSchoolId.value)
  const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
  const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)

  if (effOrg.length > 0) {
    list = list.filter(e => 
      effOrg.includes(Number(e.school_id)) || 
      effOrg.includes(Number(e.school)) || 
      effOrg.includes(Number(e.organization_id)) ||
      (e.schools && Array.isArray(e.schools) && e.schools.some(sId => effOrg.includes(Number(sId)))) ||
      !e.school_id // Directorate/Ministry-level exams whose registered students or target scope match the school
    )
  } else if (effDir.length > 0) {
    list = list.filter(e => effDir.includes(Number(e.directorate_id)) || effDir.includes(Number(e.directorate)))
  } else if (effGov.length > 0) {
    list = list.filter(e => effGov.includes(Number(e.governorate_id)) || effGov.includes(Number(e.office_id)) || effGov.includes(Number(e.governorate)))
  }

  if (filterStage.value) {
    list = list.filter(e => Number(e.stage_id) === Number(filterStage.value) || Number(e.stage) === Number(filterStage.value) || !e.stage_id)
  }
  if (filterClassTrack.value) {
    list = list.filter(e => Number(e.class_track_id) === Number(filterClassTrack.value) || Number(e.class_track) === Number(filterClassTrack.value))
  }

  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    const sObj = subjectsList.value.find(s => Number(s.id) === Number(effSubj))
    const sName = sObj?.name?.trim() || sObj?.name_ar?.trim()
    list = list.filter(e => 
      Number(e.subject_id) === Number(effSubj) || 
      Number(e.subject) === Number(effSubj) ||
      (sName && e.subject_name && (e.subject_name === sName || e.subject_name.includes(sName)))
    )
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(e => 
      (e.title && e.title.toLowerCase().includes(q)) ||
      (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
      (e.subject_name && e.subject_name.toLowerCase().includes(q)) ||
      (e.order_number && e.order_number.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredBatchesTable = computed(() => {
  let list = batches.value || []
  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    const sObj = subjectsList.value.find(s => Number(s.id) === Number(effSubj))
    const sName = sObj?.name?.trim() || sObj?.name_ar?.trim()
    list = list.filter(b => 
      Number(b.subject_id) === Number(effSubj) ||
      (sName && b.subject_name && (b.subject_name === sName || b.subject_name.includes(sName)))
    )
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(b => 
      (b.batch_id && b.batch_id.toLowerCase().includes(q)) ||
      (b.exam_title && b.exam_title.toLowerCase().includes(q)) ||
      (b.exam_code && b.exam_code.toLowerCase().includes(q)) ||
      (b.subject_name && b.subject_name.toLowerCase().includes(q))
    )
  }
  return list
})

// ── Master Tables Selection State ──
const selectedOfficeMasterRows = ref([])
const selectedDirectorateMasterRows = ref([])
const selectedSchoolMasterRows = ref([])
const selectedExamMasterRows = ref([])
const selectedBatchMasterRows = ref([])

// ── Master Tables Reactive State for custom-data-table ──
const officeMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getOfficeMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredOfficesTable.value || []
  const start = (page - 1) * pageSize
  officeMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return officeMasterTableItems.value
}

const directorateMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getDirectorateMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredDirectoratesTable.value || []
  const start = (page - 1) * pageSize
  directorateMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return directorateMasterTableItems.value
}

const schoolMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getSchoolMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredSchoolsTable.value || []
  const start = (page - 1) * pageSize
  schoolMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return schoolMasterTableItems.value
}

const schoolExamsPage = ref(1)
const schoolExamsPageSize = ref(10)
const schoolExamsTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getSchoolExamsData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = Number(p.page) || schoolExamsPage.value || 1
  const pageSize = Number(p.page_size) || schoolExamsPageSize.value || 10
  schoolExamsPage.value = page
  schoolExamsPageSize.value = pageSize

  const all = selectedSchoolDialogItem.value?.exams || []
  const total = all.length
  const numPages = Math.ceil(total / pageSize) || 1
  const validPage = Math.min(Math.max(1, page), numPages)
  const start = (validPage - 1) * pageSize

  schoolExamsTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: total,
    pagination: {
      count: total,
      total: total,
      num_pages: numPages,
      current_page: validPage,
    },
  }
  return schoolExamsTableItems.value
}

// ── Print Orders Workflow via Composable ──
const {
  examSubTab,
  savedPrintOrders,
  manifestDialog,
  selectedManifestOrder,
  loadSavedPrintOrders,
  savedPrintOrdersMap,
  getPrintOrderForExam,
  parseCalendarDate,
  getTodayIso,
  previewOrderManifest,
  enrichedMasterExamsList,
  approveOrderDialog,
  targetExamForApproval,
  actionLoading,
  getCurrentUserOfficerName,
  openApproveDialog,
  onOrderApproved,
  returnOrderDialog,
  targetExamForReturn,
  returnReasonSelected,
  returnNotesText,
  returnReasonsObjects,
  advanceScheduleDialog,
  targetExamForAdvance,
  advanceReasonSelected,
  advanceAuthDoc,
  advanceReasonsList,
  openReturnDialog,
  confirmOrderReturn,
  openAdvanceScheduleDialog,
  onConfirmAdvanceSchedule,
  cancelOrderDialog,
  targetExamForCancel,
  openCancelOrderDialog,
  onConfirmCancelOrder,
  allExamsList,
  pendingAndActiveOrdersList,
  scheduledExamsList,
  dueExamsList,
  completedExamsList,
  cancelledExamsList,
  allExamsCount,
  pendingAndActiveOrdersCount,
  scheduledExamsCount,
  dueExamsCount,
  completedExamsCount,
  cancelledExamsCount,
  currentExamSubTabList,
  examMasterTableItems,
  examMasterSearchTerm,
  getExamMasterData,
} = usePrintOrdersWorkflow({
  filteredMasterExamsTable,
  batchPrintNotification,
  loadMasterData: () => loadMasterData(),
})

// ── Direct Print Workflow Handlers ──
const directPrintDialog = ref(false)
const targetExamForDirectPrint = ref(null)
const directPrintLoading = ref(false)
const directPrintOptions = ref({
  sheets: true,
  booklets: true,
  roster: true,
  manifest: true,
})

const openDirectPrintDialog = async (exam) => {
  targetExamForDirectPrint.value = exam
  directPrintOptions.value = {
    sheets: true,
    booklets: true,
    roster: true,
    manifest: true,
  }
  rosterModelFilter.value = 'all'
  selectedStudentIds.value = []
  directPrintDialog.value = true
  if (selectedExamId.value !== exam.id || !examDetails.value) {
    selectedExamId.value = exam.id
    loadExamDetails(exam.id)
  }
}

const previewFirstOmrSheet = async () => {
  if (!examDetails.value || !examDetails.value.registered_students?.length) {
    if (targetExamForDirectPrint.value?.id) {
      await loadExamDetails(targetExamForDirectPrint.value.id)
    }
  }
  const st = examDetails.value?.registered_students?.[0]
  if (st) {
    openSingleSheetPreview(st)
  } else {
    openDemoSheetPreview('A')
  }
}

const openDemoSheetPreview = (verCode = 'A') => {
  previewStudent.value = {
    id: `demo_preview_${verCode}`,
    is_demo: true,
    student_name: 'بيانات تجريبية للمعاينة (TEST DEMO)',
    seat_number: '—',
    secret_number: 'TEST',
    model_code: verCode,
    school_name: customCenterName.value || selectedExam.value?.directorate || 'مركز اختباري (معاينة تجريبية)',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'معاينة تجريبية',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'معاينة تجريبية',
    barcode_value: `DEMO_PREVIEW_OMR_VER_${verCode}`,
    qr_value: `DEMO|${verCode}|PREVIEW_ONLY`
  }
  singleSheetDialog.value = true
}

const previewFirstQuestionPaper = async () => {
  if (!examDetails.value?.question_models?.length) {
    if (targetExamForDirectPrint.value?.id) {
      await loadExamDetails(targetExamForDirectPrint.value.id)
    }
  }
  const model = examDetails.value?.question_models?.[0] || {
    id: 1,
    model_code: 'A',
    paper_title: targetExamForDirectPrint.value?.title || 'كراسة الأسئلة الامتحانية',
    questions_count: 50,
  }
  selectedQuestionPaperForPreview.value = model
  previewQuestionPaperDialog.value = true
}

const openExamStudioFromDirect = (exam) => {
  directPrintDialog.value = false
  openExamStudio(exam)
}

const dispatchRealDirectPrint = (exam, options, realOmrElements = []) => {
  if (!exam) return

  const safeOrderNum = escapeHtml(String(exam.order_number || `PRN-REQ-${exam.uniqueCode || exam.id || ''}`))
  const safeExamTitle = escapeHtml(String(exam.title || 'الاختبار العام'))
  const safeExamCode = escapeHtml(String(exam.uniqueCode || 'EXAM-CODE'))
  const safeSubjectName = escapeHtml(String(exam.subject_name || ''))
  const safePressName = escapeHtml(String(exam.press_name || 'المطبعة المركزية'))
  const safeOfficerName = escapeHtml(String(exam.responsible_officer || 'مسؤول الكنترول والامتحانات'))
  const safeSchedDate = escapeHtml(String(exam.scheduled_print_date || getTodayIso()))
  const totalCount = Number(exam.total_registered || exam.total_students || 0) || 0
  const schoolsCount = Number(exam.schools_count || 1) || 1

  const students = examDetails.value?.registered_students || []

  let sectionsHtml = ''

  // 1. إذا تم تحديد إذن الصرف وأمر الطباعة A4
  if (options?.manifest) {
    sectionsHtml += `
      <div class="print-page manifest-page">
        <div class="header">
          <div class="header-badge">وثيقة رسمية معتمدة</div>
          <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
          <h3>اللجنة العليا للاختبارات — الإدارة العامة للاختبارات والكنترول</h3>
          <h1 class="manifest-title">إذن صرف وأمر طباعة رسمي للاختبارات</h1>
          <div class="order-code">رقم أمر الطباعة: ${safeOrderNum}</div>
        </div>

        <table class="info-table">
          <tr>
            <td class="lbl">اسم الاختبار:</td>
            <td class="val"><strong>${safeExamTitle}</strong></td>
            <td class="lbl">المادة:</td>
            <td class="val">${safeSubjectName}</td>
          </tr>
          <tr>
            <td class="lbl">كود الاختبار:</td>
            <td class="val font-mono">${safeExamCode}</td>
            <td class="lbl">تاريخ التنفيذ المعتمد:</td>
            <td class="val font-mono">${safeSchedDate}</td>
          </tr>
          <tr>
            <td class="lbl">المطبعة المنفذة:</td>
            <td class="val">${safePressName}</td>
            <td class="lbl">المسؤول المعتمد:</td>
            <td class="val">${safeOfficerName}</td>
          </tr>
          <tr>
            <td class="lbl">إجمالي الطلاب المشمولين:</td>
            <td class="val"><strong>${totalCount} طالب</strong></td>
            <td class="lbl">عدد المراكز الامتحانية:</td>
            <td class="val">${schoolsCount} مركز</td>
          </tr>
        </table>

        <div class="section-title">بيان وتفويض صرف وثائق الاختبار للمطبعة</div>
        <table class="items-table">
          <thead>
            <tr>
              <th>م</th>
              <th>البيان والمستند</th>
              <th>المواصفة والمقاس</th>
              <th>الكمية المصرح بها</th>
              <th>حالة التجهيز</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>أوراق إجابة التصحيح الآلي (OMR) مشفرة ومؤمنة بالباركود</td>
              <td>A5 / A4 ورق أبيض 80 جرام مقاوم للحرارة</td>
              <td><strong>${totalCount} ورقة</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
            <tr>
              <td>2</td>
              <td>كراسات الأسئلة الامتحانية (النماذج المعتمدة)</td>
              <td>A4 / A3 مغلفة طباعة سرية عالية الدقة</td>
              <td><strong>${totalCount} كراسة</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
            <tr>
              <td>3</td>
              <td>كشوف المناداة ومحاضر فتح المظاريف للمراكز</td>
              <td>A4 كشوف جرد وتسليم رسمية</td>
              <td><strong>${schoolsCount} كشوف</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
          </tbody>
        </table>

        <div class="signatures-grid">
          <div class="sig-box">
            <div>عضو لجنة التحقق والاعتماد</div>
            <div class="sig-line">التوقيع: ...........................</div>
            <div>التاريخ: ${safeSchedDate}</div>
          </div>
          <div class="sig-box">
            <div>المشرف المسؤول بالمطبعة</div>
            <div class="sig-line">التوقيع: ...........................</div>
            <div>الختم الرسمي: ....................</div>
          </div>
          <div class="sig-box">
            <div>مدير عام الامتحانات والكنترول</div>
            <div class="sig-line">المصادقة: ...........................</div>
            <div>التاريخ: ${safeSchedDate}</div>
          </div>
        </div>
      </div>
    `
  }

  // 2. إذا تم تحديد كشوف المناداة ومحاضر المراكز
  if (options?.roster) {
    if (!students || students.length === 0) {
      sectionsHtml += `
        <div class="print-page">
          <div class="header">
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كشف تسليم واستلام وثائق الاختبار للمركز الامتحاني</h3>
            <div class="order-code">الاختبار: ${safeExamTitle} (${safeExamCode}) — المادة: ${safeSubjectName}</div>
          </div>
          <div style="border: 2px dashed #b71c1c; background: #fff8f8; color: #b71c1c; padding: 30px 20px; text-align: center; border-radius: 8px; margin: 40px auto; max-width: 650px;">
            <div style="font-size: 17px; font-weight: bold; margin-bottom: 8px;">تنبيه الرقابة والكنترول: لا تتوفر سجلات طلاب مقيدين</div>
            <p style="font-size: 13px; margin: 0; color: #374151; line-height: 1.6;">
              لا توجد بيانات طلاب مقيدين في قاعدة البيانات لهذا الاختبار (${safeExamCode}).
              <br>
              <strong>يمنع النظام بصورة قاطعة إصدار كشف مناداة رسمي أو توليد أرقام جلوس وسرية افتراضية</strong> لضمان سلامة الوثائق الامتحانية ومطابقتها للكنترول.
            </p>
          </div>
        </div>
      `
    } else {
      let studentRows = ''
      students.forEach((st, idx) => {
        studentRows += `
          <tr>
            <td style="text-align: center;">${idx + 1}</td>
            <td style="text-align: center; font-family: monospace; font-weight: bold;">${escapeHtml(String(st.seat_number ?? ''))}</td>
            <td style="text-align: center; font-family: monospace;">${escapeHtml(String(st.secret_number ?? ''))}</td>
            <td style="font-weight: bold;">${escapeHtml(String(st.student_name ?? ''))}</td>
            <td>${escapeHtml(String(st.school_name || 'المركز الرئيسي'))}</td>
            <td style="text-align: center; font-weight: bold;">نموذج ${escapeHtml(String(st.model_code || 'A'))}</td>
            <td style="min-width: 100px;"></td>
          </tr>
        `
      })

      sectionsHtml += `
        <div class="print-page">
          <div class="header">
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كشف تسليم واستلام وثائق الاختبار للمركز الامتحاني</h3>
            <div class="order-code">الاختبار: ${safeExamTitle} (${safeExamCode}) — المادة: ${safeSubjectName}</div>
          </div>
          <table class="items-table" style="font-size: 12px;">
            <thead>
              <tr>
                <th style="width: 30px;">م</th>
                <th style="width: 90px;">رقم الجلوس</th>
                <th style="width: 80px;">الرقم السري</th>
                <th>اسم الطالب</th>
                <th>المدرسة</th>
                <th style="width: 80px;">النموذج</th>
                <th style="width: 120px;">توقيع الاستلام</th>
              </tr>
            </thead>
            <tbody>
              ${studentRows}
            </tbody>
          </table>
        </div>
      `
    }
  }

  // 3. كراسات الأسئلة الامتحانية (إذا تم تحديدها)
  if (options?.booklets) {
    const models = examDetails.value?.question_models || [
      { model_code: 'A', questions_count: 50 },
      { model_code: 'B', questions_count: 50 },
      { model_code: 'C', questions_count: 50 },
      { model_code: 'D', questions_count: 50 },
    ]
    models.forEach((m) => {
      const safeModelCode = escapeHtml(String(m.model_code || 'A'))
      const safeQuestionsCount = Number(m.questions_count) || 50
      sectionsHtml += `
        <div class="print-page question-booklet-page">
          <div class="header">
            <div class="header-badge">سري للغاية — وثيقة امتحانية رسمية</div>
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كراسة الأسئلة الامتحانية المقننة — نموذج (${safeModelCode})</h3>
            <div class="order-code">المادة: ${safeSubjectName} | كود الاختبار: ${safeExamCode}</div>
          </div>
          <div style="border: 2px dashed #000; padding: 25px; text-align: center; margin: 40px 0; border-radius: 8px;">
            <h2 style="margin: 0 0 10px 0;">كراسة الأسئلة — نموذج (${safeModelCode})</h2>
            <p style="font-size: 14px; color: #444;">
              عدد الفقرات: <strong>${safeQuestionsCount} فقرة اختيار من متعدد</strong> | الزمن المحدد: <strong>ساعتان ونصف</strong>
            </p>
            <p style="font-size: 12px; color: #777; margin-top: 20px;">
              تعليمات: تأكد من تطابق نموذج كراسة الأسئلة (${safeModelCode}) مع النموذج المطبوع على ورقة إجابتك المخصصة.
            </p>
          </div>
        </div>
      `
    })
  }

  // 4. أوراق إجابة OMR الرسمية الحقيقية للنظام (SVGs الأصلية المعتمدة)
  if (options?.sheets && realOmrElements && realOmrElements.length > 0) {
    realOmrElements.forEach(el => {
      if (!el) return
      const cloned = el.cloneNode(true)
      if (cloned instanceof HTMLElement) {
        cloned.querySelectorAll('.d-print-none, button, .v-btn').forEach(b => b.remove())
        sanitizePrintNode(cloned)
      }
      sectionsHtml += `
        <div class="print-page omr-real-sheet-page">
          <div class="real-sheet-container">
            ${cloned instanceof HTMLElement ? cloned.outerHTML : ''}
          </div>
        </div>
      `
    })
  }

  // إذا لم يختر أي خيار محدد، نطبع حزمة الاختبار الأساسية
  if (!sectionsHtml) {
    sectionsHtml = `
      <div class="print-page">
        <div class="header">
          <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
          <h3>أمر سحب وثائق الاختبار</h3>
          <h1>${safeExamTitle} (${safeExamCode})</h1>
        </div>
        <p style="text-align: center; font-size: 16px; margin-top: 30px;">
          المادة: ${safeSubjectName} | إجمالي المقيدين: ${totalCount} طالب | المطبعة: ${safePressName}
        </p>
      </div>
    `
  }

  const onlySheetsSelected = !!(options?.sheets && !options?.manifest && !options?.booklets && !options?.roster)
  const omrPageSize = selectedSheetLayout.value === 'full_a4' ? 'A4 portrait' : 'A5 landscape'

  const fullHtml = `
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
      <meta charset="utf-8">
      <meta http-equiv="Content-Security-Policy" content="script-src 'none'; connect-src 'none'; style-src 'unsafe-inline'; img-src data: blob: 'self'; font-src data: 'self';">
      <title>أمر سحب وثائق الاختبار - ${safeExamTitle} (${safeExamCode})</title>
      <style>
        @page {
          size: ${onlySheetsSelected ? omrPageSize : 'A4 portrait'};
          margin: ${onlySheetsSelected ? '0' : '6mm 8mm'};
        }
        @page omr-page {
          size: ${omrPageSize};
          margin: 0;
        }
        *, *::before, *::after {
          box-sizing: border-box;
          -webkit-print-color-adjust: exact !important;
          print-color-adjust: exact !important;
        }
        body {
          font-family: 'Amiri', 'Traditional Arabic', 'Cairo', Tahoma, Arial, sans-serif;
          margin: 0;
          padding: 0;
          color: #000;
          background: #fff;
        }
        .print-page {
          page-break-after: always;
          break-after: page;
          padding: 6px;
          min-height: 270mm;
          box-sizing: border-box;
        }
        .print-page:last-child {
          page-break-after: auto;
          break-after: auto;
        }
        .header {
          text-align: center;
          border-bottom: 2px solid #000;
          padding-bottom: 8px;
          margin-bottom: 12px;
        }
        .header h2 { margin: 0 0 3px 0; font-size: 17px; font-weight: bold; }
        .header h3 { margin: 0 0 3px 0; font-size: 14px; font-weight: normal; color: #333; }
        .header-badge {
          display: inline-block;
          font-size: 11px;
          font-weight: bold;
          border: 1px solid #000;
          padding: 2px 8px;
          border-radius: 4px;
          margin-bottom: 4px;
        }
        .manifest-title {
          font-size: 19px;
          font-weight: 900;
          margin: 4px 0;
          text-decoration: underline;
        }
        .order-code {
          font-family: monospace;
          font-weight: bold;
          font-size: 13px;
          margin-top: 3px;
        }
        .info-table, .items-table {
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 12px;
          font-size: 12px;
        }
        .info-table td {
          border: 1px solid #666;
          padding: 5px 8px;
        }
        .info-table .lbl {
          background: #f4f4f4;
          width: 18%;
          font-weight: bold;
        }
        .info-table .val {
          width: 32%;
        }
        .items-table th, .items-table td {
          border: 1px solid #000;
          padding: 5px 6px;
          text-align: center;
        }
        .items-table th {
          background: #f0f0f0;
          font-weight: bold;
        }
        .section-title {
          font-weight: bold;
          font-size: 13px;
          margin: 10px 0 5px 0;
        }
        .signatures-grid {
          display: flex;
          justify-content: space-between;
          margin-top: 30px;
          font-size: 11px;
          font-weight: bold;
          text-align: center;
        }
        .sig-box {
          width: 30%;
          border: 1px solid #aaa;
          padding: 8px;
          border-radius: 6px;
        }
        .sig-line {
          margin: 20px 0 6px 0;
        }
        .font-mono {
          font-family: monospace, monospace;
        }

        /* ── تنسيق ورقة OMR الحقيقية الأصلية ── */
        .omr-real-sheet-page {
          page: omr-page;
          display: flex;
          justify-content: center;
          align-items: center;
          padding: 0;
          min-height: ${onlySheetsSelected ? '100vh' : 'auto'};
        }
        .real-sheet-container {
          width: 100%;
          max-width: 210mm;
          margin: auto;
        }
        .real-sheet-container svg {
          width: 100% !important;
          max-width: 210mm !important;
          height: auto !important;
          max-height: ${selectedSheetLayout.value === 'full_a4' ? '297mm' : '148.5mm'} !important;
          display: block !important;
          margin: auto !important;
        }
        .yemeni-audit-report-sheet {
          width: 100% !important;
          max-width: 100% !important;
          margin: 0 auto !important;
        }
      </style>
    </head>
    <body>
      ${sectionsHtml}
    </body>
    </html>
  `

  // إزالة أي إطار طباعة سابق لضمان عدم التراكم
  const existingFrame = document.getElementById('omr-hardware-print-frame')
  if (existingFrame) {
    existingFrame.remove()
  }

  // إنشاء إطار طباعة معزول بأبعاد حقيقية خارج نطاق الرؤية لمنع طباعة نافذة التطبيق بالخطأ
  const iframe = document.createElement('iframe')
  iframe.id = 'omr-hardware-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.left = '-10000px'
  iframe.style.top = '-10000px'
  iframe.style.width = '1024px'
  iframe.style.height = '768px'
  iframe.style.border = '0'
  iframe.style.opacity = '0.01'
  iframe.style.pointerEvents = 'none'
  iframe.style.zIndex = '-9999'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document || iframe.contentDocument
  if (!doc) {
    console.error('Failed to access print iframe document')
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: 'تعذر إنشاء بيئة الطباعة المعزولة للمستند.'
    }
    return
  }

  doc.open()
  doc.write(fullHtml)
  doc.close()

  let triggered = false
  const cleanup = () => {
    setTimeout(() => {
      if (document.body.contains(iframe)) {
        iframe.remove()
      }
    }, 1500)
  }

  const triggerIframePrint = () => {
    if (triggered) return
    triggered = true
    try {
      iframe.contentWindow?.addEventListener('afterprint', cleanup)
      iframe.contentWindow?.focus()
      iframe.contentWindow?.print()
    } catch (err) {
      console.error('Iframe print failed:', err)
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: 'حدث خطأ أثناء استدعاء نافذة الطباعة للمستند المعزول.'
      }
      cleanup()
    }
  }

  iframe.onload = () => {
    setTimeout(triggerIframePrint, 250)
  }
  setTimeout(triggerIframePrint, 700)
}

/**
 * دالة التحقق الحقيقي من اكتمال رسم أوراق OMR والباركود في الحاوية قبل الطباعة
 */
const waitForBatchStagingReady = async (expectedCount, isAudit, maxWaitMs = 5000) => {
  if (expectedCount <= 0) return []

  const startTime = performance.now()
  const selector = isAudit ? '.yemeni-audit-report-sheet' : 'svg.yemeni-ministry-sheet-svg'
  const fallbackSelector = isAudit ? '.yemeni-audit-report-sheet' : 'svg'

  while (performance.now() - startTime < maxWaitMs) {
    await nextTick()
    await new Promise(resolve => requestAnimationFrame(resolve))

    const stagingEl = document.getElementById('omr-registry-batch-staging')
    if (stagingEl) {
      let elements = Array.from(stagingEl.querySelectorAll(selector))
      if (!elements.length && !isAudit) {
        elements = Array.from(stagingEl.querySelectorAll(fallbackSelector))
      }

      if (elements.length >= expectedCount) {
        // التحقق من اكتمال عناصر DOM الداخلية للرسم والباركود
        const allReady = elements.every(el => {
          if (isAudit) {
            return el.children && el.children.length > 0
          }
          return el.childNodes && el.childNodes.length > 5
        })

        if (allReady) {
          await new Promise(resolve => setTimeout(resolve, 60))
          return elements
        }
      }
    }

    await new Promise(resolve => setTimeout(resolve, 50))
  }

  const stagingEl = document.getElementById('omr-registry-batch-staging')
  if (stagingEl) {
    let elements = Array.from(stagingEl.querySelectorAll(selector))
    if (!elements.length && !isAudit) {
      elements = Array.from(stagingEl.querySelectorAll(fallbackSelector))
    }
    return elements
  }
  return []
}

const onDirectPrintStart = async ({ exam, options }) => {
  if (!exam) return

  directPrintLoading.value = true
  try {
    // 1. تحديد الاختبار وتحميل بياناته مع التحقق الصارم من نجاح الخادم
    targetExamForDirectPrint.value = exam
    selectedExamId.value = Number(exam.id)

    if (!examDetails.value || Number(examDetails.value.id) !== Number(exam.id)) {
      const loadSuccess = await loadExamDetails(exam.id)
      if (!loadSuccess || !examDetails.value) {
        batchPrintNotification.value = {
          show: true,
          color: 'error',
          message: 'تعذر تحميل بيانات وتفاصيل الاختبار من الخادم. تم إيقاف عملية الطباعة لحماية سلامة الوثائق.'
        }
        return
      }
    }

    const registeredCount = examDetails.value?.registered_students?.length || 0

    // التحقق من المتطلبات الأساسية حسب الوثائق المختارة
    if ((options?.sheets || options?.roster) && registeredCount === 0) {
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: 'لا يمكن متابعة الطباعة لعدم وجود بيانات طلاب مقيدين أو أرقام جلوس مسجلة لهذا الاختبار.'
      }
      return
    }

    if (options?.booklets && (!examDetails.value?.versions || examDetails.value.versions.length === 0)) {
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: 'لا يمكن طباعة كراسات الأسئلة لعدم توفر نماذج أسئلة معتمدة في تفاصيل الاختبار.'
      }
      return
    }

    rosterModelFilter.value = 'all'
    selectedStudentIds.value = []

    // 2. إذا تم اختيار أوراق إجابة OMR، نقوم باستخراج الأوراق وضمان اكتمال رسم SVG والباركود
    let realOmrElements = []
    if (options?.sheets) {
      const expectedCount = targetBatchStudents.value?.length || registeredCount
      if (expectedCount === 0) {
        batchPrintNotification.value = {
          show: true,
          color: 'error',
          message: 'لا توجد بيانات طلاب لاستخراج أوراق التظليل. تم إيقاف العملية.'
        }
        return
      }

      printingBatch.value = true
      await nextTick()

      const stagingEl = document.getElementById('omr-registry-batch-staging')
      if (stagingEl) {
        stagingEl.classList.remove('d-none')
      }

      const isAudit = selectedSheetLayout.value === 'full_a4'
      realOmrElements = await waitForBatchStagingReady(expectedCount, isAudit)

      if (stagingEl) {
        stagingEl.classList.add('d-none')
      }

      // إيقاف العملية وإظهار خطأ إذا لم يتم تجهيز أوراق OMR المطلوبة بدلاً من المتابعة بصمت
      if (!realOmrElements || realOmrElements.length === 0) {
        batchPrintNotification.value = {
          show: true,
          color: 'error',
          message: 'تعذر رسم وتجهيز أوراق التظليل المعتمدة (0 ورقة). تم إيقاف العملية لمنع طباعة مستندات ناقصة.'
        }
        return
      }
    }

    // 3. مسارات الطباعة المتخصصة:
    // أ) إذا اختار المستخدم أوراق إجابة OMR فقط:
    if (options?.sheets && !options?.manifest && !options?.roster && !options?.booklets) {
      if (realOmrElements.length > 0) {
        await printOmrBatch(realOmrElements, {
          title: `أوراق_تظليل_${exam.uniqueCode || 'OMR'}_${selectedSheetLayout.value}`,
          isA5: selectedSheetLayout.value === 'compact_a5',
        })
        return
      } else {
        batchPrintNotification.value = {
          show: true,
          color: 'error',
          message: 'تعذر العثور على أوراق التظليل للطباعة.'
        }
        return
      }
    }

    // ب) إذا اختار المستخدم كشوف المناداة ومحاضر المراكز فقط:
    if (options?.roster && !options?.sheets && !options?.manifest && !options?.booklets) {
      printAuditRoster()
      return
    }

    // ج) إذا اختار كراسات الأسئلة الرسمية فقط:
    if (options?.booklets && !options?.sheets && !options?.manifest && !options?.roster) {
      await printCurrentQuestionPaper()
      return
    }

    // د) في حال اختيار أكثر من مستند أو توليفة كاملة:
    dispatchRealDirectPrint(exam, options, realOmrElements)
  } catch (err) {
    console.error('Error during direct print execution:', err)
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: `حدث خطأ أثناء تنفيذ الطباعة: ${err?.message || err}`
    }
  } finally {
    directPrintLoading.value = false
    printingBatch.value = false
  }
}

const executeDirectPrint = async (payload) => {
  const exam = payload?.exam || targetExamForDirectPrint.value
  if (!exam) return

  const totalCount = Number(exam?.total_registered || exam?.total_students || 0)
  const alreadyPrinted = Number(exam?.printed_count || 0)
  const remainingTarget = Math.max(0, totalCount - alreadyPrinted)

  const actualCount = Number(payload?.actualPrintedCount ?? (remainingTarget > 0 ? remainingTarget : totalCount))
  const chosenOptions = payload?.options || directPrintOptions.value
  const notes = payload?.notes || ''

  if (actualCount <= 0) {
    directPrintDialog.value = false
    batchPrintNotification.value = {
      show: true,
      color: 'warning',
      message: `تم إلغاء عملية السحب لعدم اكتمال الطباعة على الماكينة (0 ورقة). الطلب لا زال محفوظاً في قائمة المستحقة للتنفيذ.`,
    }
    return
  }

  directPrintLoading.value = true
  try {
    const uniqueBatchId = payload?.batchId || `PRN-BAT-${exam.uniqueCode || exam.id}-${Date.now()}-${Math.floor(Math.random() * 1000)}`

    // 1. استدعاء الخادم لتوثيق الدفعة وربطها بالطلاب وحساب الأعداد التراكمية بشكل موثوق
    const resp = await api.post(`/api/omr/exam-linking/${exam.id}/mark-printed/`, {
      batch_id: uniqueBatchId,
      count: actualCount,
      student_ids: actualCount >= remainingTarget ? 'all' : undefined,
      notes: notes,
    })

    const resData = resp.data || {}

    // 2. اعتماد الحالة مباشرة من الخادم (Server Authoritative)
    if (resData.success) {
      exam.printed_count = resData.total_printed_count ?? (alreadyPrinted + actualCount)
      exam.printed_rate = resData.printed_rate ?? Math.round((exam.printed_count / (totalCount || 1)) * 100)
      exam.print_status = resData.print_status ?? (exam.printed_count >= totalCount ? 'full' : 'partial')
      exam.is_completed = !!resData.is_completed
      exam.is_due = !resData.is_completed

      if (exam.is_completed) {
        examSubTab.value = 'completed'
      }
    }

    // 3. إعادة تحميل السجلات والمصادقة الميدانية
    await Promise.all([
      loadSavedPrintOrders(),
      loadMasterData(),
      fetchExamsList(),
      fetchBatches(),
    ])

    directPrintDialog.value = false

    batchPrintNotification.value = {
      show: true,
      color: 'info',
      message: resData.message || (exam.is_completed 
        ? `تمت مصادقة إتمام الطباعة بنجاح للاختبار "${exam.title}"! تم توثيق الدفعة برقم (${uniqueBatchId}) لعدد ${actualCount} ورقة بنسبة 100%.`
        : `تم توثيق السحب الجزئي بنجاح للاختبار "${exam.title}"! تم قيد ${actualCount} ورقة إضافية ليصبح الإجمالي ${exam.printed_count} ورقة، وتبقى ${totalCount - exam.printed_count} ورقة في قائمة المستحقة.`),
    }
  } catch (err) {
    console.error('Direct print error:', err)
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: `فشل توثيق عملية الطباعة في السجلات: ${err?.response?.data?.message || err?.message || err}`,
    }
  } finally {
    directPrintLoading.value = false
  }
}

const openExamBatchesHistory = (exam) => {
  const b = (batches.value || []).find(x => 
    String(x.exam_id) === String(exam.id) || 
    (x.exam_code && x.exam_code === exam.uniqueCode) || 
    (x.exam_title && exam.title && (x.exam_title.includes(exam.title) || exam.title.includes(x.exam_title)))
  )
  if (b) {
    viewBatchDetails(b)
  } else {
    masterTab.value = 'registry'
    masterSearchQuery.value = exam.title || exam.uniqueCode || ''
    getBatchMasterData()
  }
}

const batchMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getBatchMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredBatchesTable.value || []
  const start = (page - 1) * pageSize
  batchMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return batchMasterTableItems.value
}

watch(filteredOfficesTable, () => {
  getOfficeMasterData()
}, { immediate: true })

watch(filteredDirectoratesTable, () => {
  getDirectorateMasterData()
}, { immediate: true })

watch(filteredSchoolsTable, () => {
  getSchoolMasterData()
}, { immediate: true })

watch(filteredBatchesTable, () => {
  getBatchMasterData()
}, { immediate: true })

watch(masterTab, (tab) => {
  if (tab === 'offices') getOfficeMasterData()
  else if (tab === 'directorates') getDirectorateMasterData()
  else if (tab === 'schools') getSchoolMasterData()
  else if (tab === 'exams') getExamMasterData()
  else if (tab === 'registry') getBatchMasterData()
})

// ── Error & Three-State Diagnostic Tracking ──
const masterDataError = ref(null)
const examsListError = ref(null)
const examDetailsError = ref(null)
const batchesError = ref(null)

const masterDataStatus = ref('idle') // 'idle' | 'loading' | 'success' | 'empty' | 'error'
const examsListStatus = ref('idle')
const examDetailsStatus = ref('idle')

// ── Concurrency & Race-Condition Guards ──
const isRequestCanceled = (err) => {
  return err?.name === 'CanceledError' || err?.code === 'ERR_CANCELED' || err?.message === 'canceled'
}

/**
 * Executes an API fetch function safely with:
 * 1. Distinction between 3 states: Data exists, Data genuinely empty, and Data load error.
 * 2. Structured diagnostic logging (Operation, params, HTTP status, server message, timestamp).
 * 3. Graceful handling of AbortController cancellations without false error alerts.
 */
const safeApiFetch = async (operationName, fetchFn, params = {}) => {
  try {
    const res = await fetchFn()
    const rawData = res?.data
    let results = []
    if (rawData && Array.isArray(rawData.results)) {
      results = rawData.results
    } else if (Array.isArray(rawData)) {
      results = rawData
    } else if (rawData && typeof rawData === 'object' && rawData.data && Array.isArray(rawData.data)) {
      results = rawData.data
    }

    return {
      status: 'success',
      data: results,
      raw: rawData,
      count: results.length,
      isEmpty: results.length === 0,
      error: null
    }
  } catch (err) {
    if (isRequestCanceled(err)) {
      return {
        status: 'canceled',
        data: [],
        raw: null,
        count: 0,
        isEmpty: false,
        error: null
      }
    }

    const errDetails = {
      operation: operationName,
      params,
      statusCode: err?.response?.status || null,
      statusText: err?.response?.statusText || null,
      serverMessage: err?.response?.data?.message || err?.response?.data?.detail || err?.response?.data?.error || null,
      errorMessage: err?.message || 'تعذر الاتصال بالخادم',
      timestamp: new Date().toISOString()
    }

    console.error(`[OMR Registry API Error] فشل في عملية: ${operationName}`, errDetails)

    return {
      status: 'error',
      data: [],
      raw: null,
      count: 0,
      isEmpty: false,
      error: errDetails
    }
  }
}

// Master Methods
const loadSubjects = async () => {
  try {
    const res = await safeApiFetch('loadSubjects:gradebook', () => gradebookAPI.getSubjects())
    if (res.status === 'success' && res.data.length > 0) {
      subjectsList.value = res.data
      return
    }
    const acRes = await safeApiFetch('loadSubjects:academic', () => api.get('/api/academic/subjects/', { skipInterceptor: true }))
    if (acRes.status === 'success' && acRes.data.length > 0) {
      subjectsList.value = acRes.data
    } else if (res.status === 'error' && acRes.status === 'error') {
      console.warn('[OMR Registry] تعذر تحميل قائمة المواد من كلا المصدرين (gradebook & academic).')
    }
  } catch (err) {
    console.error('[OMR Registry API Error] فشل في loadSubjects:', err)
  }
}

let masterDataRequestId = 0
let masterDataAbortController = null

const loadMasterData = async () => {
  // Cancel previous pending master data request to prevent out-of-order race conditions
  if (masterDataAbortController) {
    masterDataAbortController.abort()
  }
  masterDataAbortController = new AbortController()
  const signal = masterDataAbortController.signal
  const currentRequestId = ++masterDataRequestId

  loadingMaster.value = true
  masterDataStatus.value = 'loading'
  masterDataError.value = null

  try {
    const effGov = filterGovernorate.value || (normalizeIds(selectedOfficeId.value)[0] || undefined)
    const effDir = filterDirectorate.value || (normalizeIds(selectedDirectorateId.value)[0] || undefined)
    const effOrg = filterOrganization.value || (normalizeIds(selectedSchoolId.value)[0] || undefined)
    const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value || undefined
    const effType = getEffectiveInstitutionType()

    const baseParams = {
      institution_type: effType,
      subject: effSubj,
      governorate: effGov,
    }
    const officeParams = { ...baseParams }
    if (effGov) {
      officeParams.office_id = effGov
      officeParams.governorate_id = effGov
    }

    const dirParams = { ...officeParams }
    if (effDir) {
      dirParams.directorate_id = effDir
    }

    const schoolParams = { ...dirParams }
    if (effOrg) {
      schoolParams.school_id = effOrg
      schoolParams.organization_id = effOrg
    }
    if (filterStage.value) schoolParams.stage = filterStage.value
    if (filterClassTrack.value) schoolParams.class_track = filterClassTrack.value
    if (filterCollege.value) schoolParams.college = filterCollege.value
    if (filterDepartment.value) schoolParams.department = filterDepartment.value
    if (filterSpecialization.value) schoolParams.specialization = filterSpecialization.value

    const [allOfficesRes, officesRes, directoratesRes, schoolsRes, examsRes] = await Promise.all([
      (!allOfficesList.value || !allOfficesList.value.length)
        ? safeApiFetch('loadMasterData:allOffices', () => gradebookAPI.getByOffice(baseParams, { signal }), baseParams)
        : Promise.resolve({ status: 'success', data: allOfficesList.value, count: allOfficesList.value.length, isEmpty: allOfficesList.value.length === 0, error: null }),
      safeApiFetch('loadMasterData:offices', () => gradebookAPI.getByOffice(officeParams, { signal }), officeParams),
      safeApiFetch('loadMasterData:directorates', () => gradebookAPI.getByDirectorate(dirParams, { signal }), dirParams),
      safeApiFetch('loadMasterData:schools', () => gradebookAPI.getBySchool(schoolParams, { signal }), schoolParams),
      safeApiFetch('loadMasterData:exams', () => gradebookAPI.list(schoolParams, { signal }), schoolParams)
    ])

    // Strict Sequence Guard: Discard stale response if a newer request was dispatched
    if (currentRequestId !== masterDataRequestId) {
      return
    }

    // Check if any request was canceled
    if (
      allOfficesRes.status === 'canceled' ||
      officesRes.status === 'canceled' ||
      directoratesRes.status === 'canceled' ||
      schoolsRes.status === 'canceled' ||
      examsRes.status === 'canceled'
    ) {
      return
    }

    // Inspect failed operations
    const failures = [
      { name: 'مكاتب المحافظات', res: officesRes },
      { name: 'إدارات المديريات', res: directoratesRes },
      { name: 'المراكز الامتحانية والمدارس', res: schoolsRes },
      { name: 'الاختبارات المعتمدة', res: examsRes },
    ].filter(item => item.res.status === 'error')

    if (failures.length > 0) {
      masterDataStatus.value = 'error'
      const failedNames = failures.map(f => f.name).join('، ')
      masterDataError.value = {
        message: `تعذر جلب بيانات: ${failedNames}`,
        failedServices: failures.map(f => f.name),
        errors: failures.map(f => f.res.error)
      }
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: `تعذر تحميل بعض بيانات الهيكل الإداري (${failedNames}). يرجى مراجعة الاتصال أو إعادة المحاولة.`
      }
    } else {
      masterDataError.value = null
    }

    // Safe Atomic Commit: Only adopt successful results
    if (allOfficesRes.status === 'success' && (!allOfficesList.value || !allOfficesList.value.length)) {
      allOfficesList.value = allOfficesRes.data || []
    }
    if (officesRes.status === 'success') {
      officesList.value = officesRes.data || []
    }
    if (directoratesRes.status === 'success') {
      directoratesList.value = directoratesRes.data || []
    }
    if (schoolsRes.status === 'success') {
      schoolsList.value = schoolsRes.data || []
    }
    if (examsRes.status === 'success') {
      masterExamsList.value = examsRes.data || []
    }

    const totalCount = (officesList.value?.length || 0) + (schoolsList.value?.length || 0) + (masterExamsList.value?.length || 0)
    if (failures.length === 0) {
      masterDataStatus.value = totalCount === 0 ? 'empty' : 'success'
    }

    await loadSavedPrintOrders(true)

    if (currentRequestId === masterDataRequestId) {
      getOfficeMasterData()
      getDirectorateMasterData()
      getSchoolMasterData()
      getExamMasterData()
      getBatchMasterData()
    }
  } catch (err) {
    if (!isRequestCanceled(err)) {
      masterDataStatus.value = 'error'
      masterDataError.value = {
        message: 'حدث خطأ غير متوقع أثناء جلب بيانات الهيكل الإداري',
        errorMessage: err.message
      }
      console.error('[OMR Registry API Error] Failed to load master data:', err)
    }
  } finally {
    if (currentRequestId === masterDataRequestId) {
      loadingMaster.value = false
    }
  }
}

const resetHierarchyFilters = async () => {
  institutionType.value = 'school'
  selectedOfficeId.value = []
  selectedOfficeName.value = ''
  selectedDirectorateId.value = []
  selectedDirectorateName.value = ''
  selectedSchoolId.value = []
  selectedSchoolName.value = ''
  selectedSubjectId.value = null
  selectedSubjectName.value = ''
  masterSearchQuery.value = ''
  await loadMasterData()
}

const onSectorChange = (val) => {
  institutionType.value = val
  selectedOfficeId.value = []
  selectedOfficeName.value = ''
  selectedDirectorateId.value = []
  selectedDirectorateName.value = ''
  selectedSchoolId.value = []
  selectedSchoolName.value = ''
  selectedSubjectId.value = null
  selectedSubjectName.value = ''
  if (currentView.value === 'master') {
    loadMasterData()
  } else {
    fetchExamsList()
  }
}

const onSubjectFilterChange = async (subjId) => {
  selectedSubjectId.value = subjId
  if (subjId) {
    const s = subjectsList.value.find(item => item.id === subjId)
    selectedSubjectName.value = s?.name || ''
  } else {
    selectedSubjectName.value = ''
  }
  await loadMasterData()
}

const openSchoolExamsDialog = (schoolItem) => {
  selectedSchoolDialogItem.value = schoolItem
  schoolExamsPage.value = 1
  getSchoolExamsData({ page: 1, page_size: schoolExamsPageSize.value })
  schoolExamsDialog.value = true
}

watch(selectedSchoolDialogItem, () => {
  if (schoolExamsDialog.value) {
    getSchoolExamsData({ page: 1, page_size: schoolExamsPageSize.value })
  }
})

const selectExamFromSchoolDialog = async (exam, school) => {
  schoolExamsDialog.value = false
  selectedExamId.value = exam.id
  if (school) {
    selectedSchoolId.value = school.id
    selectedSchoolName.value = school.name
    if (school.directorate_name) selectedDirectorateName.value = school.directorate_name
    if (school.governorate_name) selectedOfficeName.value = school.governorate_name
  }
  currentView.value = 'detail'
  await loadExamDetails(exam.id, {
    school_id: school?.id || undefined,
  })
}

const onOfficeFilterChange = (officeId) => {
  selectedOfficeId.value = officeId || []
  const officeIds = normalizeIds(selectedOfficeId.value)
  if (officeIds.length > 0) {
    const validDirIds = (directoratesList.value || []).filter(d => officeIds.includes(Number(d.office_id))).map(d => d.id)
    selectedDirectorateId.value = (selectedDirectorateId.value || []).filter(id => validDirIds.includes(id))
  } else {
    selectedDirectorateId.value = []
  }
  selectedSchoolId.value = []
  loadMasterData()
}

const onDirectorateFilterChange = (dirId) => {
  selectedDirectorateId.value = dirId || []
  selectedSchoolId.value = []
  const dirIds = normalizeIds(selectedDirectorateId.value)
  const currentOfficeIds = normalizeIds(selectedOfficeId.value)
  if (dirIds.length > 0 && currentOfficeIds.length === 0) {
    const relatedOffices = (directoratesList.value || [])
      .filter(d => dirIds.includes(Number(d.id)) && d.office_id)
      .map(d => Number(d.office_id))
    if (relatedOffices.length > 0) {
      selectedOfficeId.value = Array.from(new Set(relatedOffices))
    }
  }
  loadMasterData()
}

const onSchoolFilterChange = (schoolId) => {
  selectedSchoolId.value = schoolId || []
  loadMasterData()
}

const drillDownToOffice = (office) => {
  selectedOfficeId.value = office.id
  selectedOfficeName.value = office.office_name
  masterTab.value = 'directorates'
}

const drillDownToDirectorate = (dir) => {
  selectedDirectorateId.value = dir.id
  selectedDirectorateName.value = dir.name
  if (dir.office_id && !selectedOfficeId.value) {
    selectedOfficeId.value = dir.office_id
    selectedOfficeName.value = dir.office_name
  }
  masterTab.value = 'schools'
}

const openSchoolStudio = async (school) => {
  selectedSchoolId.value = school.id
  selectedSchoolName.value = school.name || school.school_name || ''
  if (school.directorate_id && (!selectedDirectorateId.value || !selectedDirectorateId.value.length)) {
    const matchedDir = (directoratesList.value || []).find(d => 
      Number(d.id) === Number(school.directorate_id) || 
      Number(d.fk_directorate_id) === Number(school.fk_directorate_id || school.directorate_id) ||
      Number(d.directorate_id) === Number(school.directorate_id)
    )
    selectedDirectorateId.value = matchedDir ? matchedDir.id : school.directorate_id
    if (school.directorate_name && !selectedDirectorateName.value) {
      selectedDirectorateName.value = school.directorate_name
    }
  } else if (filterDirectorate.value && (!selectedDirectorateId.value || !selectedDirectorateId.value.length)) {
    const matchedDir = (directoratesList.value || []).find(d => 
      Number(d.id) === Number(filterDirectorate.value) || 
      Number(d.fk_directorate_id) === Number(filterDirectorate.value) ||
      Number(d.directorate_id) === Number(filterDirectorate.value)
    )
    selectedDirectorateId.value = matchedDir ? matchedDir.id : filterDirectorate.value
    if (matchedDir) selectedDirectorateName.value = matchedDir.name || ''
  }
  if ((school.office_id || school.governorate_id) && (!selectedOfficeId.value || !selectedOfficeId.value.length)) {
    selectedOfficeId.value = school.office_id || school.governorate_id
    if (school.governorate_name && !selectedOfficeName.value) {
      selectedOfficeName.value = school.governorate_name
    }
  } else if (filterGovernorate.value && (!selectedOfficeId.value || !selectedOfficeId.value.length)) {
    selectedOfficeId.value = filterGovernorate.value
  }
  currentView.value = 'detail'
  await fetchExamsList({ 
    school_id: school.id,
    directorate_id: selectedDirectorateId.value || undefined,
    office_id: selectedOfficeId.value || undefined,
  })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { 
      school_id: school.id,
      directorate_id: selectedDirectorateId.value || undefined,
      office_id: selectedOfficeId.value || undefined,
    })
  }
}

const openDirectorateStudio = async (dir) => {
  selectedDirectorateId.value = dir.id
  selectedDirectorateName.value = dir.name || dir.name_ar || ''
  const offId = dir.office_id || dir.fk_parent_organization_id || dir.governorate_id || dir.fk_governorate_id
  if (offId && (!selectedOfficeId.value || !selectedOfficeId.value.length)) {
    selectedOfficeId.value = offId
    if (dir.office_name) selectedOfficeName.value = dir.office_name
  } else if (filterGovernorate.value && (!selectedOfficeId.value || !selectedOfficeId.value.length)) {
    selectedOfficeId.value = filterGovernorate.value
  }
  if (filterOrganization.value && (!selectedSchoolId.value || !selectedSchoolId.value.length)) {
    const matchedSchool = (schoolsList.value || []).find(s => 
      Number(s.id) === Number(filterOrganization.value) ||
      Number(s.school_id) === Number(filterOrganization.value)
    )
    selectedSchoolId.value = matchedSchool ? matchedSchool.id : filterOrganization.value
    if (matchedSchool) selectedSchoolName.value = matchedSchool.name || ''
  }
  currentView.value = 'detail'
  await fetchExamsList({ 
    directorate_id: dir.id,
    office_id: selectedOfficeId.value || undefined,
    school_id: selectedSchoolId.value || undefined,
  })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { 
      directorate_id: dir.id,
      office_id: selectedOfficeId.value || undefined,
      school_id: selectedSchoolId.value || undefined,
    })
  }
}

const openOfficeStudio = async (office) => {
  selectedOfficeId.value = office.id || office.core_org_id || office.office_id
  selectedOfficeName.value = office.office_name || office.governorate_name || ''
  if (filterDirectorate.value && (!selectedDirectorateId.value || !selectedDirectorateId.value.length)) {
    const matchedDir = (directoratesList.value || []).find(d => 
      Number(d.id) === Number(filterDirectorate.value) || 
      Number(d.fk_directorate_id) === Number(filterDirectorate.value) ||
      Number(d.directorate_id) === Number(filterDirectorate.value)
    )
    selectedDirectorateId.value = matchedDir ? matchedDir.id : filterDirectorate.value
    if (matchedDir) selectedDirectorateName.value = matchedDir.name || ''
  }
  if (filterOrganization.value && (!selectedSchoolId.value || !selectedSchoolId.value.length)) {
    const matchedSchool = (schoolsList.value || []).find(s => 
      Number(s.id) === Number(filterOrganization.value) ||
      Number(s.school_id) === Number(filterOrganization.value)
    )
    selectedSchoolId.value = matchedSchool ? matchedSchool.id : filterOrganization.value
    if (matchedSchool) selectedSchoolName.value = matchedSchool.name || ''
  }
  currentView.value = 'detail'
  await fetchExamsList({ 
    office_id: selectedOfficeId.value || undefined,
    directorate_id: selectedDirectorateId.value || undefined,
    school_id: selectedSchoolId.value || undefined,
  })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { 
      office_id: selectedOfficeId.value || undefined,
      directorate_id: selectedDirectorateId.value || undefined,
      school_id: selectedSchoolId.value || undefined,
    })
  }
}

const openExamStudio = async (exam) => {
  selectedExamId.value = exam.id
  if (exam.office_id && (!selectedOfficeId.value || !selectedOfficeId.value.length)) {
    selectedOfficeId.value = exam.office_id
    selectedOfficeName.value = exam.governorate_name || ''
  }
  if (exam.directorate_id && (!selectedDirectorateId.value || !selectedDirectorateId.value.length)) {
    selectedDirectorateId.value = exam.directorate_id
    selectedDirectorateName.value = exam.directorate_name || ''
  }
  if (exam.school_id && (!selectedSchoolId.value || !selectedSchoolId.value.length)) {
    selectedSchoolId.value = exam.school_id
    selectedSchoolName.value = exam.school_name || ''
  } else if (filterOrganization.value && (!selectedSchoolId.value || !selectedSchoolId.value.length)) {
    selectedSchoolId.value = filterOrganization.value
  }
  currentView.value = 'detail'
  await fetchExamsList()
  await loadExamDetails(exam.id, {
    school_id: selectedSchoolId.value || undefined,
    directorate_id: selectedDirectorateId.value || undefined,
    office_id: selectedOfficeId.value || undefined,
  })
}

const returnToMaster = async () => {
  currentView.value = 'master'
  showHierarchyFilters.value = false
  await loadMasterData()
}

const clearSchoolFilter = async () => {
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  if (selectedExamId.value) {
    await loadExamDetails(selectedExamId.value)
  }
}

// Studio Hierarchical Filter Handlers
const onStudioOfficeChange = async (officeId) => {
  onOfficeFilterChange(officeId)
  await fetchExamsList()
  if (examsList.value && examsList.value.length > 0) {
    if (!examsList.value.some(e => e.id === selectedExamId.value)) {
      selectedExamId.value = examsList.value[0].id
      await loadExamDetails(selectedExamId.value)
    }
  } else {
    selectedExamId.value = null
    examDetails.value = null
  }
}

const onStudioDirectorateChange = async (dirId) => {
  onDirectorateFilterChange(dirId)
  await fetchExamsList()
  if (examsList.value && examsList.value.length > 0) {
    if (!examsList.value.some(e => e.id === selectedExamId.value)) {
      selectedExamId.value = examsList.value[0].id
      await loadExamDetails(selectedExamId.value)
    }
  } else {
    selectedExamId.value = null
    examDetails.value = null
  }
}

const onStudioSchoolChange = async (schoolId) => {
  onSchoolFilterChange(schoolId)
  await fetchExamsList()
  if (examsList.value && examsList.value.length > 0) {
    if (!examsList.value.some(e => e.id === selectedExamId.value)) {
      selectedExamId.value = examsList.value[0].id
      await loadExamDetails(selectedExamId.value)
    }
  } else {
    selectedExamId.value = null
    examDetails.value = null
  }
}

const resetHierarchyStudioFilters = async () => {
  selectedOfficeId.value = null
  selectedOfficeName.value = ''
  selectedDirectorateId.value = null
  selectedDirectorateName.value = ''
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  await fetchExamsList()
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value)
  }
}

// Active Tab: 'sheets' | 'questions' | 'package' | 'history'
const activeTab = ref(
  route.query.tab === 'history' ? 'history' :
  route.query.tab === 'questions' ? 'questions' :
  route.query.tab === 'package' ? 'package' : 'sheets'
)

// Track visited tabs for instant lazy-mounting & zero-lag tab switching
const visitedTabs = ref(new Set([activeTab.value]))
const isTabVisited = (tab) => {
  return visitedTabs.value ? visitedTabs.value.has(tab) : true
}
const switchDetailTab = (tab) => {
  activeTab.value = tab
  if (visitedTabs.value) {
    visitedTabs.value.add(tab)
  }
  if (tab === 'history' && (!batches.value || batches.value.length === 0)) {
    fetchBatches()
  }
}

// Document Category: أوراق التظليل vs ورقة الأسئلة الرسمية vs حزمة الاختبار الكاملة
const selectedDocType = ref(
  ['sheets', 'questions', 'package'].includes(activeTab.value) ? activeTab.value : 'sheets'
)
const selectedQuestionsModelCode = ref('A')
const selectedQuestionPaperLayout = ref('a4') // 'a4' | 'a3'
const questionPaperRef = ref(null)

// ── Smart Print Job Manifest Computeds ──
const activeTabTitle = computed(() => {
  if (activeTab.value === 'sheets') return 'أوراق التظليل المخصصة للطلاب (OMR Sheets)'
  if (activeTab.value === 'questions') return 'كراسة الأسئلة الرسمية المعتمدة (Exam Booklet)'
  if (activeTab.value === 'package') return 'حزمة الاختبار المتكاملة للمظروف (أسئلة + تظليل)'
  return 'سجل الدفعات المطبوعة'
})

watch(activeTab, (newTab) => {
  visitedTabs.value.add(newTab)
  if (['sheets', 'questions', 'package'].includes(newTab)) {
    selectedDocType.value = newTab
  }
  if (newTab === 'unified') {
    getRosterData()
  } else if (newTab === 'questions') {
    getQuestionModelsData()
  } else if (newTab === 'package') {
    getPackageData()
  }
})

watch(selectedDocType, (newDoc) => {
  if (['sheets', 'questions', 'package'].includes(newDoc) && activeTab.value !== newDoc && activeTab.value !== 'history') {
    activeTab.value = newDoc
    visitedTabs.value.add(newDoc)
  }
})

// Exams List & Selection
const loadingExams = ref(false)
const examsList = ref([])
const selectedExamId = ref(null)

const institutionTypeOptions = [
  { text: 'الكل (مدارس وجامعات ومعاهد)', value: 'all', icon: 'mdi-domain' },
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]

const resetInstitutionFilters = () => {
  resetUnifiedFilters()
  selectedExamId.value = null
  examDetails.value = null
  fetchExamsList()
}

const selectedExam = computed(() => {
  if (!selectedExamId.value) return null
  const targetId = Number(selectedExamId.value)
  const base = (examsList.value || []).find(e => Number(e.id) === targetId) ||
               (masterExamsList.value || []).find(e => Number(e.id) === targetId) ||
               (Number(targetExamForDirectPrint.value?.id) === targetId ? targetExamForDirectPrint.value : {}) || {}
  const detailed = examDetails.value?.exam || (Number(examDetails.value?.id) === targetId ? examDetails.value : {})
  return (base.id || detailed.id) ? { ...base, ...detailed } : null
})

// Exam Details State
const showHierarchyFilters = ref(false)
const loadingExamDetails = ref(false)
const examDetails = ref(null)
const seedingStudents = ref(false)

// Sheet Generation Settings
const sheetGenerationMode = ref('all_students') // 'all_students' | 'student' | 'blank'
const selectedSheetLayout = ref('compact_a5') // 'compact_a5' | 'full_a4'
const selectedStudentId = ref(null)
const selectedBlankVersionCode = ref('A')
const sheetZoomLevel = ref(1.0)
const printingBatch = ref(false)

// Designer Stream & Batch Adjustments
const filterStreamModelCode = ref('all')
const customCenterName = ref('')
const customDirectorate = ref('')
const customGovernorate = ref('')
const customExamYear = ref('')
const customStageTitle = ref('')
const showAdjustmentsPanel = ref(false)

// DOM Refs
const sheetArtboardRef = ref(null)
const batchStreamRef = ref(null)

// Batches Registry State
const searchQuery = ref('')
const detailsDialog = ref(false)
const activeBatch = ref(null)
const loadingDetails = ref(false)
const batchStudents = ref([])

// Version Code Options
const versionCodeOptions = computed(() => {
  if (examDetails.value?.versions && examDetails.value.versions.length > 0) {
    return examDetails.value.versions.map(v => v.versionCode)
  }
  return ['A', 'B', 'C', 'D']
})

const modelFilterSelectOptions = computed(() => {
  const students = examDetails.value?.registered_students || []
  const total = students.length
  const list = [
    { title: `كافة النماذج (${total})`, value: 'all' }
  ]
  const versions = examDetails.value?.versions || []
  if (versions.length > 0) {
    versions.forEach(v => {
      const count = students.filter(s => (s.model_code || 'A') === v.versionCode).length
      list.push({ title: `نموذج ${v.versionCode} (${count})`, value: v.versionCode })
    })
  } else {
    ['A', 'B', 'C', 'D'].forEach(code => {
      const count = students.filter(s => (s.model_code || 'A') === code).length
      list.push({ title: `نموذج ${code} (${count})`, value: code })
    })
  }
  return list
})

const printStatusFilterOptions = computed(() => {
  const students = examDetails.value?.registered_students || []
  return [
    { title: `كافة الحالات (${students.length})`, value: 'all' },
    { title: `جاهز للطباعة (${unprintedCount.value})`, value: 'unprinted' },
    { title: `المطبوعة (${printedCount.value})`, value: 'printed' },
  ]
})

const modelFilterObjects = computed(() => {
  return (modelFilterSelectOptions.value || []).map(o => ({
    id: o.value,
    value: o.value,
    name: o.title,
    title: o.title,
  }))
})

const printStatusFilterObjects = computed(() => {
  return (printStatusFilterOptions.value || []).map(o => ({
    id: o.value,
    value: o.value,
    name: o.title,
    title: o.title,
  }))
})

const rosterTableRef = ref(null)
const resetRosterFilters = () => {
  rosterModelFilter.value = 'all'
  rosterPrintFilter.value = 'all'
  rosterSearch.value = ''
  if (rosterTableRef.value?.params) {
    rosterTableRef.value.params.search = ''
  }
  getRosterData()
}

const questionsModelSelectOptions = computed(() => {
  if (!examDetails.value?.versions?.length) return []
  return examDetails.value.versions.map(v => ({
    title: `النموذج ${v.versionCode} (${v.questions?.length || v.questionsCount || 0} سؤال)`,
    value: v.versionCode
  }))
})

const versionsChipLabel = computed(() => {
  const versions = examDetails.value?.versions || []
  if (versions.length > 0) {
    const codes = versions.map(v => v.versionCode).filter(Boolean).join(', ')
    const count = versions.length
    return count === 1 ? `نموذج واحد (${codes || 'A'})` : `${count} نماذج (${codes})`
  }
  const count = selectedExam.value?.versions_count || 1
  return count === 1 ? 'نموذج واحد (A)' : `${count} نماذج`
})

// ── Unified Roster Table & Batch Print State (الجدول الموحد لأوراق التظليل والطلاب) ──
const rosterSearch = ref('')
const rosterModelFilter = ref('all')
const rosterPrintFilter = ref('all')
const selectedStudentIds = ref([])
const singleSheetDialog = ref(false)
const previewStudent = ref(null)
const singlePreviewRef = ref(null)

const rosterHeaders = computed(() => [
  { title: "تحديد", key: "select_box", sortable: false, align: "center", width: "65px" },
  { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "110px" },
  { title: "الرقم السري", key: "secret_number", sortable: true, align: "center", width: "100px" },
  { title: "اسم الطالب الرباعي", key: "student_name", sortable: true, align: "start" },
  { title: "المدرسة والمركز", key: "school_name", sortable: true, align: "start" },
  { title: "النموذج", key: "model_code", sortable: true, align: "center", width: "115px" },
  { title: "حالة الطباعة", key: "is_printed", sortable: true, align: "center", width: "135px" },
  { title: "إجراءات الطباعة والمعاينة", key: "actions", sortable: false, align: "center", width: "130px" },
])

const toggleStudentSelection = (studentId) => {
  const idx = selectedStudentIds.value.indexOf(studentId)
  if (idx > -1) {
    selectedStudentIds.value.splice(idx, 1)
  } else {
    selectedStudentIds.value.push(studentId)
  }
}

const unprintedCount = computed(() => {
  return (examDetails.value?.registered_students || []).filter(s => !s.is_printed).length
})

const printedCount = computed(() => {
  return (examDetails.value?.registered_students || []).filter(s => s.is_printed).length
})

const modelCounts = computed(() => {
  const students = examDetails.value?.registered_students || []
  return {
    all: students.length,
    A: students.filter(s => (s.model_code || 'A') === 'A').length,
    B: students.filter(s => s.model_code === 'B').length,
    C: students.filter(s => s.model_code === 'C').length,
    D: students.filter(s => s.model_code === 'D').length,
  }
})

const getModelChipColor = (code) => {
  switch (code) {
    case 'A': return 'primary'
    case 'B': return 'deep-purple'
    case 'C': return 'amber-darken-3'
    case 'D': return 'teal'
    default: return 'primary'
  }
}

const filteredRosterStudents = computed(() => {
  if (!examDetails.value?.registered_students) return []
  let list = examDetails.value.registered_students

  if (rosterModelFilter.value && rosterModelFilter.value !== 'all') {
    list = list.filter(s => (s.model_code || 'A') === rosterModelFilter.value)
  }

  if (rosterPrintFilter.value === 'printed') {
    list = list.filter(s => s.is_printed)
  } else if (rosterPrintFilter.value === 'unprinted') {
    list = list.filter(s => !s.is_printed)
  }

  if (rosterSearch.value && rosterSearch.value.trim()) {
    const q = rosterSearch.value.trim().toLowerCase()
    list = list.filter(s =>
      String(s.seat_number || '').toLowerCase().includes(q) ||
      String(s.secret_number || '').toLowerCase().includes(q) ||
      String(s.student_name || '').toLowerCase().includes(q) ||
      String(s.school_name || '').toLowerCase().includes(q) ||
      String(s.directorate || '').toLowerCase().includes(q)
    )
  }

  return list
})

const rosterTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getRosterData = async (params = {}) => {
  const p = params?.params || params || {}
  if (p.search !== undefined) {
    rosterSearch.value = (p.search || '').trim().toLowerCase()
  }
  const page = p.page || 1
  const pageSize = p.page_size || 50
  const all = filteredRosterStudents.value || []
  const start = (page - 1) * pageSize
  rosterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return rosterTableItems.value
}

watch(filteredRosterStudents, () => {
  getRosterData()
}, { immediate: true })

const targetBatchStudents = computed(() => {
  if (selectedStudentIds.value && selectedStudentIds.value.length > 0) {
    const idSet = new Set(selectedStudentIds.value)
    return (examDetails.value?.registered_students || []).filter(s => idSet.has(s.id))
  }
  if (filteredRosterStudents.value && filteredRosterStudents.value.length > 0) {
    return filteredRosterStudents.value
  }
  if (examDetails.value?.registered_students && examDetails.value.registered_students.length > 0) {
    return examDetails.value.registered_students
  }
  return []
})

const filteredStreamStudents = computed(() => filteredRosterStudents.value)

const selectAllRosterStudents = () => {
  if (selectedStudentIds.value.length === filteredRosterStudents.value.length) {
    selectedStudentIds.value = []
  } else {
    selectedStudentIds.value = filteredRosterStudents.value.map(s => s.id)
  }
}

const markingSelectedLoading = ref(false)

const toggleStudentPrintedStatus = async (st) => {
  if (!st || st._updating || !selectedExamId.value) return

  const targetState = !st.is_printed
  st._updating = true

  const payload = {
    student_ids: [st.id],
    is_printed: targetState
  }

  try {
    const resp = await api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, payload)

    if (resp.data && resp.data.success) {
      // 1. تثبيت الحالة في السجل فقط بعد مصادقة ونجاح الخادم
      st.is_printed = targetState
      st.printed_at = targetState ? (resp.data.printed_at || new Date().toLocaleTimeString('ar-YE')) : null

      // 2. تحديث الإحصائيات التراكمية المعتمدة من الخادم مباشرة
      if (selectedExam.value && resp.data.total_printed_count !== undefined) {
        selectedExam.value.printed_count = resp.data.total_printed_count
        selectedExam.value.is_completed = !!resp.data.is_completed
        selectedExam.value.print_status = resp.data.print_status || (resp.data.is_completed ? 'full' : 'partial')
      }

      batchPrintNotification.value = {
        show: true,
        color: targetState ? 'success' : 'info',
        message: targetState
          ? `تم توثيق طباعة الطالب (${st.student_name || st.id}) رسمياً في السجل التشغيلي.`
          : `تم إلغاء تأشير طباعة الطالب (${st.student_name || st.id}) في السجل.`
      }

      fetchBatches()
    } else {
      throw new Error(resp.data?.message || 'تعذر اعتماد حالة الطباعة بالخادم')
    }
  } catch (err) {
    const errDetails = {
      operation: 'toggleStudentPrintedStatus',
      studentId: st.id,
      examId: selectedExamId.value,
      payload,
      statusCode: err?.response?.status,
      serverMessage: err?.response?.data?.message || err?.response?.data?.detail,
      errorMessage: err.message
    }
    console.error('[OMR Registry API Error] فشل في تحديث حالة طباعة الطالب:', errDetails)

    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: `تعذر تحديث حالة طباعة الطالب (${st.student_name || st.id}) على الخادم: ${errDetails.serverMessage || errDetails.errorMessage || 'خطأ في الاتصال'}. لم يتم تغيير السجل.`
    }
  } finally {
    st._updating = false
  }
}

const markSelectedAsPrinted = async () => {
  if (!selectedStudentIds.value.length || markingSelectedLoading.value || !selectedExamId.value) return

  markingSelectedLoading.value = true
  const targetIds = [...selectedStudentIds.value]
  const idSet = new Set(targetIds)

  const payload = {
    student_ids: targetIds,
    is_printed: true
  }

  try {
    const resp = await api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, payload)

    if (resp.data && resp.data.success) {
      // 1. تثبيت تعديل الطلاب في الواجهة فقط بعد تأكيد الخادم الرسمي
      const printTime = new Date().toLocaleTimeString('ar-YE')
      ;(examDetails.value?.registered_students || []).forEach(st => {
        if (idSet.has(st.id)) {
          st.is_printed = true
          st.printed_at = printTime
        }
      })

      // 2. تحديث الإحصائيات التراكمية من الخادم مباشرة
      if (selectedExam.value && resp.data.total_printed_count !== undefined) {
        selectedExam.value.printed_count = resp.data.total_printed_count
        selectedExam.value.is_completed = !!resp.data.is_completed
        selectedExam.value.print_status = resp.data.print_status || (resp.data.is_completed ? 'full' : 'partial')
      }

      // 3. إلغاء التحديد فقط بعد نجاح وتوثيق العملية
      selectedStudentIds.value = []

      batchPrintNotification.value = {
        show: true,
        color: 'success',
        message: resp.data.message || `تم توثيق طباعة ${targetIds.length} طالب بنجاح في السجل التشغيلي.`
      }

      fetchBatches()
    } else {
      throw new Error(resp.data?.message || 'تعذر اعتماد طباعة الطلاب على الخادم')
    }
  } catch (err) {
    const errDetails = {
      operation: 'markSelectedAsPrinted',
      studentCount: targetIds.length,
      examId: selectedExamId.value,
      payload,
      statusCode: err?.response?.status,
      serverMessage: err?.response?.data?.message || err?.response?.data?.detail,
      errorMessage: err.message
    }
    console.error('[OMR Registry API Error] فشل في تحديث حالة طباعة الطلاب المحددين:', errDetails)

    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: `تعذر توثيق طباعة الطلاب على الخادم: ${errDetails.serverMessage || errDetails.errorMessage || 'حدث خطأ في الاتصال'}. لم يتم تغيير أي سجل في الواجهة.`
    }
  } finally {
    markingSelectedLoading.value = false
  }
}

const openSingleSheetPreview = (st) => {
  previewStudent.value = st
  singleSheetDialog.value = true
}

const printPreviewStudentSheet = async () => {
  await nextTick()
  let printableEl = null
  if (singlePreviewRef.value) {
    printableEl = singlePreviewRef.value.querySelector('.yemeni-audit-report-sheet') ||
                  singlePreviewRef.value.querySelector('svg.yemeni-ministry-sheet-svg') ||
                  singlePreviewRef.value.querySelector('svg')
  }
  if (printableEl && previewStudent.value) {
    const st = previewStudent.value
    await printOmrElement(printableEl, {
      title: `${selectedExam.value?.uniqueCode || 'OMR'}_${st?.seat_number || st?.model_code || 'SHEET'}`,
      isA5: selectedSheetLayout.value === 'compact_a5'
    })
    if (!st.is_demo) {
      if (selectedExamId.value && st.id && !String(st.id).startsWith('blank_')) {
        try {
          const resp = await api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
            student_ids: [st.id],
            is_printed: true
          })
          if (resp.data && resp.data.success) {
            // تثبيت حالة الطباعة فقط بعد تأكيد الخادم
            st.is_printed = true
            st.printed_at = resp.data.printed_at || new Date().toLocaleTimeString('ar-YE')
            if (selectedExam.value && resp.data.total_printed_count !== undefined) {
              selectedExam.value.printed_count = resp.data.total_printed_count
              selectedExam.value.is_completed = !!resp.data.is_completed
              selectedExam.value.print_status = resp.data.print_status || (resp.data.is_completed ? 'full' : 'partial')
            }
          }
        } catch (err) {
          console.error('[OMR Registry API Error] فشل في توثيق حالة طباعة الورقة الفردية:', {
            operation: 'printPreviewStudentSheet',
            studentId: st.id,
            error: err?.message || err
          })
          batchPrintNotification.value = {
            show: true,
            color: 'warning',
            message: 'تم إرسال الورقة للطباعة ولكن تعذر توثيق حالة الطباعة على الخادم.'
          }
        }
      }
    }
  } else {
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: 'تعذر العثور على عنصر ورقة التظليل القابل للطباعة في نافذة المعاينة.'
    }
  }
}

const printSingleStudentDirect = async (st) => {
  previewStudent.value = st
  singleSheetDialog.value = true
  await nextTick()
  await printPreviewStudentSheet()
}

const printBlankSheetVersion = async (verCode) => {
  previewStudent.value = {
    id: `blank_${verCode}`,
    student_name: '............................................',
    seat_number: '.....',
    secret_number: verCode,
    model_code: verCode,
    school_name: customCenterName.value || selectedExam.value?.school_name || selectedExam.value?.center_name || selectedExam.value?.directorate || '',
    directorate: customDirectorate.value || selectedExam.value?.directorate || '',
    governorate: customGovernorate.value || selectedExam.value?.governorate || '',
    barcode_value: `EXAM_${selectedExam.value?.id}_VER_${verCode}_BLANK`,
    qr_value: `${selectedExam.value?.uniqueCode}|${verCode}|BLANK`
  }
  singleSheetDialog.value = true
  await nextTick()
  await printPreviewStudentSheet()
}

const printAuditRoster = () => {
  const students = (filteredRosterStudents.value && filteredRosterStudents.value.length > 0)
    ? filteredRosterStudents.value
    : (examDetails.value?.registered_students || [])
  if (!students.length) {
    batchPrintNotification.value = {
      show: true,
      color: 'warning',
      message: 'تعذر طباعة كشف تسليم الكنترول: لا توجد سجلات طلاب مقيدين في قاعدة البيانات لهذا الاختبار. يمنع النظام توليد كشوف رسمية ببيانات افتراضية.'
    }
    return
  }

  const exam = selectedExam.value || {}
  const center = escapeHtml(String(customCenterName.value || exam.school_name || exam.center_name || exam.directorate || ''))
  const directorate = escapeHtml(String(customDirectorate.value || exam.directorate || ''))
  const governorate = escapeHtml(String(customGovernorate.value || exam.governorate || ''))
  const examTitle = escapeHtml(String(customStageTitle.value || exam.title || ''))
  const yearName = escapeHtml(String(customExamYear.value || exam.year_name || ''))
  const subjectName = escapeHtml(String(exam.subject_name || ''))
  const examCode = escapeHtml(String(exam.uniqueCode || ''))
  const totalStudents = Number(students.length) || 0

  let rowsHtml = ''
  students.forEach((st, idx) => {
    rowsHtml += `
      <tr>
        <td style="text-align: center; font-weight: bold;">${idx + 1}</td>
        <td style="text-align: center; font-family: monospace; font-weight: bold; font-size: 14px;">${escapeHtml(String(st.seat_number ?? ''))}</td>
        <td style="text-align: center; font-family: monospace;">${escapeHtml(String(st.secret_number ?? ''))}</td>
        <td style="font-weight: bold; padding-right: 8px;">${escapeHtml(String(st.student_name ?? ''))}</td>
        <td>${escapeHtml(String(st.school_name || ''))}</td>
        <td style="text-align: center; font-weight: bold;">النموذج ${escapeHtml(String(st.model_code || 'A'))}</td>
        <td style="text-align: center;">${st.is_printed ? 'نعم' : 'لا'}</td>
        <td style="min-width: 120px;"></td>
      </tr>
    `
  })

  const html = `
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
      <meta charset="utf-8">
      <meta http-equiv="Content-Security-Policy" content="script-src 'none'; connect-src 'none'; style-src 'unsafe-inline'; img-src data: blob: 'self'; font-src data: 'self';">
      <title>كشف تسليم واستلام الكنترول - ${examCode}</title>
      <style>
        @page { size: A4 landscape; margin: 10mm; }
        *, *::before, *::after { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        body { font-family: 'Amiri', 'Traditional Arabic', Tahoma, sans-serif; margin: 0; padding: 10px; color: #000; background: #fff; }
        .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 16px; }
        .header h2 { margin: 0 0 6px 0; font-size: 20px; }
        .header h3 { margin: 0 0 6px 0; font-size: 16px; font-weight: normal; }
        .meta-grid { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 13px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
        th, td { border: 1px solid #000; padding: 6px 4px; }
        th { background-color: #f0f0f0; }
        .footer { margin-top: 25px; display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; }
      </style>
    </head>
    <body>
      <div class="header">
        <h2>الجمهورية اليمنية - وزارة التربية والتعليم</h2>
        <h3>قطاع المناهج والتوجيه - الإدارة العامة للاختبارات</h3>
        <h2>كشف تسليم واستلام أوراق إجابة التظليل (OMR)</h2>
      </div>
      <div class="meta-grid">
        <div>المحافظة: ${governorate} | المديرية: ${directorate}</div>
        <div>المركز / المدرسة: ${center}</div>
      </div>
      <div class="meta-grid">
        <div>المادة: ${subjectName} | المرحلة: ${examTitle}</div>
        <div>العام الدراسي: ${yearName} | إجمالي الطلاب: ${totalStudents}</div>
      </div>
      <table>
        <thead>
          <tr>
            <th style="width: 35px;">م</th>
            <th style="width: 85px;">رقم الجلوس</th>
            <th style="width: 75px;">الرقم السري</th>
            <th>اسم الطالب الرباعي</th>
            <th>المدرسة</th>
            <th style="width: 75px;">النموذج</th>
            <th style="width: 65px;">مطبوع</th>
            <th style="width: 140px;">توقيع المستلم / الملاحظات</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>
      <div class="footer">
        <div>مسؤول الكنترول: .......................................</div>
        <div>رئيس المركز الامتحاني: .......................................</div>
        <div>تاريخ التسليم: ${escapeHtml(new Date().toLocaleDateString('ar-YE'))}</div>
      </div>
    </body>
    </html>
  `

  const existingFrame = document.getElementById('roster-print-frame')
  if (existingFrame) existingFrame.remove()

  const iframe = document.createElement('iframe')
  iframe.id = 'roster-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.left = '-10000px'
  iframe.style.top = '-10000px'
  iframe.style.width = '1024px'
  iframe.style.height = '768px'
  iframe.style.border = '0'
  iframe.style.opacity = '0.01'
  iframe.style.pointerEvents = 'none'
  iframe.style.zIndex = '-9999'
  iframe.setAttribute('aria-hidden', 'true')
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document || iframe.contentDocument
  if (doc) {
    doc.open()
    doc.write(html)
    doc.close()

    setTimeout(() => {
      try {
        iframe.contentWindow?.focus()
        iframe.contentWindow?.print()
      } catch (err) {
        console.error('[OMR Registry] خطأ في طباعة كشف التسليم:', err)
        batchPrintNotification.value = {
          show: true,
          color: 'error',
          message: 'تعذر تشغيل أمر الطباعة لكشف التسليم من الإطار المخصص.'
        }
      } finally {
        setTimeout(() => {
          if (iframe.parentNode) iframe.parentNode.removeChild(iframe)
        }, 1500)
      }
    }, 250)
  } else {
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: 'تعذر تجهيز إطار الطباعة لكشف تسليم الكنترول.'
    }
  }
}

const printSelectedOrAllRoster = async () => {
  const expectedCount = targetBatchStudents.value?.length || 0
  if (!expectedCount) {
    batchPrintNotification.value = {
      show: true,
      color: 'warning',
      message: 'لا توجد بيانات طلاب مسجلين لهذا الاختبار للطباعة. يرجى قيد وتسكين الطلاب وأرقام جلوسهم أولاً.'
    }
    return
  }
  printingBatch.value = true
  try {
    const isAudit = selectedSheetLayout.value === 'full_a4'

    const stagingEl = document.getElementById('omr-registry-batch-staging')
    if (stagingEl) {
      stagingEl.classList.remove('d-none')
    }

    // انتظار حقيقي لديناميكية رسم SVG والباركود
    const elements = await waitForBatchStagingReady(expectedCount, isAudit, 5000)

    if (stagingEl) {
      stagingEl.classList.add('d-none')
    }

    // إيقاف العملية وإظهار خطأ إذا لم يتم العثور على أوراق OMR المطلوبة
    if (!elements || elements.length === 0) {
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: 'تعذر تجهيز أوراق الإجابة للطباعة: لم يتم العثور على أوراق التظليل المطلوبة أو تعذر رسم عناصر SVG. تم إيقاف العملية.'
      }
      return
    }

    if (elements.length < expectedCount) {
      batchPrintNotification.value = {
        show: true,
        color: 'warning',
        message: `تم تجهيز ${elements.length} من أصل ${expectedCount} ورقة تظليل فقط. تم إيقاف الطباعة لتفادي نقص في الدفعة.`
      }
      return
    }

    const batchId = `BATCH_${Date.now()}`
    await printOmrBatch(elements, {
      title: `كشف_أوراق_تظليل_${selectedExam.value?.uniqueCode || 'الاختبار'}_${selectedSheetLayout.value}`,
      isA5: selectedSheetLayout.value === 'compact_a5'
    })

      const targetStudentIds = targetBatchStudents.value.map(s => s.id)
      if (selectedExamId.value && targetStudentIds.length > 0) {
        try {
          const resp = await api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
            student_ids: targetStudentIds,
            batch_id: batchId
          })

          if (resp.data && resp.data.success) {
            // تثبيت حالة الطلاب فقط بعد مصادقة الخادم
            const printTime = new Date().toLocaleTimeString('ar-YE')
            targetStudentIds.forEach(id => {
              const st = examDetails.value?.registered_students?.find(s => s.id === id)
              if (st) {
                st.is_printed = true
                st.printed_at = printTime
                st.print_batch = batchId
              }
            })

            // تحديث الإحصائيات التراكمية المعتمدة من الخادم
            if (selectedExam.value && resp.data.total_printed_count !== undefined) {
              selectedExam.value.printed_count = resp.data.total_printed_count
              selectedExam.value.is_completed = !!resp.data.is_completed
              selectedExam.value.print_status = resp.data.print_status || (resp.data.is_completed ? 'full' : 'partial')
            }

            fetchBatches()
            batchPrintNotification.value = {
              show: true,
              color: 'success',
              message: `تم إرسال ${elements.length} ورقة تظليل إلى أمر الطباعة وتحديث سجل الدفعات بنجاح.`
            }
          } else {
            throw new Error(resp.data?.message || 'تعذر توثيق الدفعة بالخادم')
          }
        } catch (postErr) {
          console.error('[OMR Registry API Error] فشل في تسجيل الدفعة على الخادم:', {
            operation: 'printTargetBatch',
            batchId,
            studentCount: targetStudentIds.length,
            error: postErr?.message || postErr
          })
          batchPrintNotification.value = {
            show: true,
            color: 'warning',
            message: `تم إرسال المستندات للطباعة ولكن تعذر توثيق الدفعة #${batchId} على الخادم: ${postErr?.message || postErr}. لم يتم تحديث سجل الطلاب كـ "مطبوع".`
          }
        }
      } else {
        batchPrintNotification.value = {
          show: true,
          color: 'success',
          message: `تم إرسال ${elements.length} ورقة تظليل إلى أمر الطباعة بنجاح.`
        }
      }
  } catch (err) {
    console.error("Batch print error:", err)
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: `تعذر إتمام عملية الطباعة: ${err?.message || err}`
    }
  } finally {
    printingBatch.value = false
  }
}

const batchPrintAllStudents = printSelectedOrAllRoster

const activeSheetStudent = computed(() => {
  if (previewStudent.value) return previewStudent.value
  if (!examDetails.value?.registered_students) return null
  return examDetails.value.registered_students[0] || null
})

const activeSheetModelCode = computed(() => {
  return activeSheetStudent.value?.model_code || 'A'
})

const resetHeaderOverrides = () => {
  customCenterName.value = ''
  customDirectorate.value = ''
  customGovernorate.value = ''
  customExamYear.value = ''
  customStageTitle.value = ''
}

const sheetArtboardStyle = computed(() => {
  return {
    width: '218mm',
    maxWidth: '100%',
    zoom: sheetZoomLevel.value,
    transition: 'zoom 0.15s ease'
  }
})

const getQuestionsCountForVersion = (versionCode) => {
  const v = examDetails.value?.versions?.find(ver => ver.versionCode === versionCode) ||
            examDetails.value?.versions?.[0]
  if (v?.questions?.length !== undefined) return v.questions.length
  if (v?.questionsCount !== undefined) return v.questionsCount
  return 0
}

const getSectionsForVersion = (versionCode) => {
  const v = examDetails.value?.versions?.find(ver => ver.versionCode === versionCode) ||
            examDetails.value?.versions?.[0]
  const qList = v?.questions || []
  const total = qList.length || (v?.questionsCount || 0)
  let tfCount = 0
  let mcqCount = 0

  qList.forEach(q => {
    const typeStr = String(q.questionType || '').toLowerCase()
    if (typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ')) {
      tfCount++
    } else {
      mcqCount++
    }
  })

  // If no detailed question records found, use standard ministerial distribution
  if (tfCount === 0 && mcqCount === 0) {
    if (total <= 20) {
      tfCount = Math.min(10, Math.floor(total / 2))
      mcqCount = total - tfCount
    } else {
      tfCount = 20
      mcqCount = total - 20
    }
  }

  if (tfCount > 0 && mcqCount > 0) {
    return [
      { id: 'sec1', title: 'القسم الأول: أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: tfCount, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'القسم الثاني: أسئلة الاختيار من متعدد', type: 'mcq', from_q: tfCount + 1, to_q: total, choices: ['1', '2', '3', '4'], mark: 2 }
    ]
  } else if (tfCount > 0) {
    return [
      { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: total, choices: ['صح', 'خطأ'], mark: 1 }
    ]
  } else {
    return [
      { id: 'sec1', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 1, to_q: total, choices: ['1', '2', '3', '4'], mark: 2 }
    ]
  }
}

const activeModelQuestionsCount = computed(() => {
  return getQuestionsCountForVersion(activeSheetModelCode.value)
})

const activeExamSections = computed(() => {
  return getSectionsForVersion(activeSheetModelCode.value)
})

const selectedQuestionsVersionObj = computed(() => {
  return examDetails.value?.versions?.find(ver => ver.versionCode === selectedQuestionsModelCode.value) ||
         examDetails.value?.versions?.[0] || null
})

// Tables Headers
const headers = computed(() => [
  { title: "معرف الدفعة (Batch)", key: "batch_info", sortable: true },
  { title: "الاختبار", key: "exam_info", sortable: true },
  { title: "الأوراق المطبوعة", key: "papers_count", sortable: true, align: "center", width: "160px" },
  { title: "الحالة", key: "status", sortable: true, align: "center", width: "120px" },
  { title: "استعراض الأوراق", key: "actions", sortable: false, align: "center", width: "140px" },
])

const batchesPage = ref(1)
const batchesPageSize = ref(10)
const batchesTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getBatchesData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = Number(p.page) || batchesPage.value || 1
  const pageSize = Number(p.page_size) || batchesPageSize.value || 10
  batchesPage.value = page
  batchesPageSize.value = pageSize

  if (p.search !== undefined) {
    searchQuery.value = (p.search || '').trim().toLowerCase()
  }

  let all = (currentView.value === 'detail' && selectedExamId.value)
    ? (currentExamBatches.value || [])
    : (filteredBatchesTable.value || [])

  if (searchQuery.value) {
    const q = searchQuery.value
    all = all.filter(b =>
      String(b.batch_id || '').toLowerCase().includes(q) ||
      String(b.exam_title || '').toLowerCase().includes(q) ||
      String(b.exam_code || '').toLowerCase().includes(q) ||
      String(b.subject_name || '').toLowerCase().includes(q) ||
      String(b.print_date || '').toLowerCase().includes(q) ||
      String(b.status || '').toLowerCase().includes(q)
    )
  }

  const total = all.length
  const numPages = Math.ceil(total / pageSize) || 1
  const validPage = Math.min(Math.max(1, page), numPages)
  const start = (validPage - 1) * pageSize

  batchesTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: total,
    pagination: {
      count: total,
      total: total,
      num_pages: numPages,
      current_page: validPage,
    },
  }
  return batchesTableItems.value
}

watch([batches, currentExamBatches, currentView, selectedExamId], () => {
  batchesPage.value = 1
  getBatchesData({ page: 1, page_size: batchesPageSize.value })
}, { immediate: true })

const tableItems = computed(() => batchesTableItems.value)

const studentsHeaders = computed(() => [
  { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center" },
  { title: "اسم الطالب", key: "student_name", sortable: true },
  { title: "النموذج", key: "model_code", sortable: true, align: "center" },
  { title: "وقت الطباعة الفعلي", key: "printed_at", sortable: true, align: "center" },
])

const batchStudentsPage = ref(1)
const batchStudentsPageSize = ref(10)
const batchStudentsTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getBatchStudentsData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = Number(p.page) || batchStudentsPage.value || 1
  const pageSize = Number(p.page_size) || batchStudentsPageSize.value || 10
  batchStudentsPage.value = page
  batchStudentsPageSize.value = pageSize

  const all = batchStudents.value || []
  const total = all.length
  const numPages = Math.ceil(total / pageSize) || 1
  const validPage = Math.min(Math.max(1, page), numPages)
  const start = (validPage - 1) * pageSize

  batchStudentsTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: total,
    pagination: {
      count: total,
      total: total,
      num_pages: numPages,
      current_page: validPage,
    },
  }
  return batchStudentsTableItems.value
}

watch(batchStudents, () => {
  batchStudentsPage.value = 1
  getBatchStudentsData({ page: 1, page_size: batchStudentsPageSize.value })
}, { immediate: true })

const studentsTableItems = computed(() => batchStudentsTableItems.value)

// Methods
let examsListRequestId = 0
let examsListAbortController = null

const fetchExamsList = async (customParams = {}) => {
  // Cancel previous in-flight exam list query to eliminate race conditions
  if (examsListAbortController) {
    examsListAbortController.abort()
  }
  examsListAbortController = new AbortController()
  const signal = examsListAbortController.signal
  const currentRequestId = ++examsListRequestId

  loadingExams.value = true
  examsListError.value = null
  examsListStatus.value = 'loading'

  try {
    const offParam = customParams.office_id || (normalizeIds(selectedOfficeId.value)[0] || (filterGovernorate.value ? Number(filterGovernorate.value) : undefined))
    const dirParam = customParams.directorate_id || (normalizeIds(selectedDirectorateId.value)[0] || (filterDirectorate.value ? Number(filterDirectorate.value) : undefined))
    const schParam = customParams.school_id || (normalizeIds(selectedSchoolId.value)[0] || (filterOrganization.value ? Number(filterOrganization.value) : undefined))

    const params = {
      school_id: schParam,
      directorate_id: dirParam,
      office_id: offParam,
      ...customParams,
    }
    const effType = getEffectiveInstitutionType()
    if (effType) {
      params.institution_type = effType
    }
    if (institutionType.value === 'school') {
      if (filterStage.value) params.stage = filterStage.value
      if (filterClassTrack.value) params.class_track = filterClassTrack.value
      if (filterSubject.value) params.subject = filterSubject.value
    } else if (institutionType.value === 'university') {
      if (filterCollege.value) params.college = filterCollege.value
      if (filterDepartment.value) params.department = filterDepartment.value
      if (filterSpecialization.value) params.specialization = filterSpecialization.value
      if (filterSemesterSubject.value) params.semester_subject = filterSemesterSubject.value
    } else if (institutionType.value === 'institute') {
      if (filterInstituteField.value) params.institute_field = filterInstituteField.value
      if (filterInstituteEducationSystem.value) params.institute_education_system = filterInstituteEducationSystem.value
      if (filterInstituteSpecialization.value) params.institute_specialization = filterInstituteSpecialization.value
      if (filterInstituteSubject.value) params.institute_subject = filterInstituteSubject.value
    } else {
      if (filterSubject.value) params.subject = filterSubject.value
    }

    const res = await safeApiFetch(
      'fetchExamsList',
      () => api.get('/api/omr/exam-linking/', { params, signal, skipInterceptor: true }),
      params
    )

    // Strict Sequence Guard: Discard stale response
    if (currentRequestId !== examsListRequestId || res.status === 'canceled') {
      return
    }

    if (res.status === 'error') {
      examsListStatus.value = 'error'
      examsListError.value = res.error
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: `تعذر جلب قائمة الاختبارات من الخادم: ${res.error?.serverMessage || res.error?.errorMessage || 'خطأ في الاتصال'}`
      }
      return
    }

    // Success State
    examsList.value = res.data
    examsListStatus.value = res.count === 0 ? 'empty' : 'success'
    examsListError.value = null

    if (selectedExamId.value && !examsList.value.some(e => e.id === selectedExamId.value)) {
      selectedExamId.value = null
      examDetails.value = null
    }
    if (!selectedExamId.value && examsList.value.length > 0) {
      selectedExamId.value = examsList.value[0].id
      await loadExamDetails(selectedExamId.value, {
        school_id: schParam,
        directorate_id: dirParam,
        office_id: offParam,
      })
    }
  } catch (err) {
    if (!isRequestCanceled(err)) {
      examsListStatus.value = 'error'
      examsListError.value = { errorMessage: err.message }
      console.error('[OMR Registry API Error] Failed to load exams list:', err)
    }
  } finally {
    if (currentRequestId === examsListRequestId) {
      loadingExams.value = false
    }
  }
}

let examDetailsRequestId = 0
let examDetailsAbortController = null

const loadExamDetails = async (examId, customParams = {}) => {
  if (!examId) return false

  // Cancel prior pending exam details request
  if (examDetailsAbortController) {
    examDetailsAbortController.abort()
  }
  examDetailsAbortController = new AbortController()
  const signal = examDetailsAbortController.signal
  const currentRequestId = ++examDetailsRequestId
  const targetId = Number(examId)

  loadingExamDetails.value = true
  examDetailsError.value = null
  examDetailsStatus.value = 'loading'

  try {
    const offParam = customParams.office_id || (normalizeIds(selectedOfficeId.value)[0] || (filterGovernorate.value ? Number(filterGovernorate.value) : undefined))
    const dirParam = customParams.directorate_id || (normalizeIds(selectedDirectorateId.value)[0] || (filterDirectorate.value ? Number(filterDirectorate.value) : undefined))
    const schParam = customParams.school_id || (normalizeIds(selectedSchoolId.value)[0] || (filterOrganization.value ? Number(filterOrganization.value) : undefined))

    const params = {
      school_id: schParam,
      directorate_id: dirParam,
      office_id: offParam,
      ...customParams,
    }

    const res = await safeApiFetch(
      `loadExamDetails:${examId}`,
      () => api.get(`/api/omr/exam-linking/${examId}/`, { params, signal, skipInterceptor: true }),
      params
    )

    // Strict Sequence Guard: Discard stale response if newer request was dispatched or exam changed
    if (currentRequestId !== examDetailsRequestId || Number(selectedExamId.value) !== targetId || res.status === 'canceled') {
      return false
    }

    if (res.status === 'error') {
      examDetailsStatus.value = 'error'
      examDetailsError.value = {
        examId,
        message: res.error?.serverMessage || res.error?.errorMessage || 'تعذر تحميل تفاصيل الاختبار وقائمة الطلاب من الخادم',
        details: res.error
      }
      examDetails.value = null
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: `تعذر تحميل تفاصيل الاختبار #${examId}: ${res.error?.serverMessage || res.error?.errorMessage || 'خطأ في الاتصال'}`
      }
      return false
    }

    // Atomic State Commit on Success
    examDetails.value = res.raw
    examDetailsStatus.value = res.raw ? 'success' : 'empty'
    examDetailsError.value = null
    showHierarchyFilters.value = false

    if (res.raw?.registered_students && res.raw.registered_students.length > 0) {
      selectedStudentId.value = res.raw.registered_students[0].id
      sheetGenerationMode.value = 'all_students'
    } else {
      sheetGenerationMode.value = 'blank'
    }
    await getRosterData()
    await getQuestionModelsData()
    await getPackageData()

    return true
  } catch (err) {
    if (!isRequestCanceled(err)) {
      examDetailsStatus.value = 'error'
      examDetailsError.value = {
        examId,
        message: 'حدث خطأ غير متوقع أثناء تحميل تفاصيل الاختبار',
        errorMessage: err.message
      }
      examDetails.value = null
      console.error('[OMR Registry API Error] Failed to load exam details:', err)
    }
    return false
  } finally {
    if (currentRequestId === examDetailsRequestId) {
      loadingExamDetails.value = false
    }
  }
}

const onExamSelected = (newId) => {
  if (newId) {
    selectedExamId.value = Number(newId)
    loadExamDetails(newId)
  } else {
    selectedExamId.value = null
    examDetails.value = null
  }
}

let batchesRequestId = 0
let batchesAbortController = null

const fetchBatches = async (customParams = {}) => {
  if (batchesAbortController) {
    batchesAbortController.abort()
  }
  batchesAbortController = new AbortController()
  const signal = batchesAbortController.signal
  const currentRequestId = ++batchesRequestId

  loadingBatches.value = true
  batchesError.value = null

  try {
    const params = {
      search: searchQuery.value,
      ...customParams,
    }
    const res = await safeApiFetch(
      'fetchBatches',
      () => api.get('/api/omr/print-registry/', { params, signal, skipInterceptor: true }),
      params
    )

    if (currentRequestId !== batchesRequestId || res.status === 'canceled') {
      return
    }

    if (res.status === 'error') {
      batchesError.value = res.error
      console.error('[OMR Registry API Error] Failed to load print batches:', res.error)
      return
    }

    if (res.raw && res.raw.success) {
      batches.value = res.raw.results || []
    }
  } catch (e) {
    if (!isRequestCanceled(e)) {
      batchesError.value = { errorMessage: e.message }
      console.error('[OMR Registry API Error] Failed to load print batches', e)
    }
  } finally {
    if (currentRequestId === batchesRequestId) {
      loadingBatches.value = false
    }
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  fetchBatches()
}

let batchDetailsRequestId = 0
let batchDetailsAbortController = null

const viewBatchDetails = async (batch) => {
  activeBatch.value = batch
  detailsDialog.value = true
  loadingDetails.value = true
  batchStudents.value = []

  if (batchDetailsAbortController) {
    batchDetailsAbortController.abort()
  }
  batchDetailsAbortController = new AbortController()
  const signal = batchDetailsAbortController.signal
  const currentRequestId = ++batchDetailsRequestId
  const targetBatchId = batch.batch_id

  try {
    const res = await safeApiFetch(
      `viewBatchDetails:${batch.batch_id}`,
      () => api.get(`/api/omr/print-registry/${batch.batch_id}/`, { signal, skipInterceptor: true })
    )

    if (currentRequestId !== batchDetailsRequestId || activeBatch.value?.batch_id !== targetBatchId || res.status === 'canceled') {
      return
    }

    if (res.status === 'error') {
      console.error('[OMR Registry API Error] Failed to load batch students:', res.error)
      batchPrintNotification.value = {
        show: true,
        color: 'error',
        message: `تعذر جلب تفاصيل الطلاب للدفعة #${batch.batch_id}: ${res.error?.serverMessage || res.error?.errorMessage || 'خطأ في الاتصال'}`
      }
      return
    }

    if (res.raw && res.raw.success) {
      batchStudents.value = res.raw.students || []
    }
  } catch (e) {
    if (!isRequestCanceled(e)) {
      console.error('[OMR Registry API Error] Failed to load batch students', e)
    }
  } finally {
    if (currentRequestId === batchDetailsRequestId) {
      loadingDetails.value = false
    }
  }
}

const seedSampleStudents = async () => {
  if (!selectedExamId.value) return
  seedingStudents.value = true
  try {
    await api.post(`/api/omr/exam-linking/${selectedExamId.value}/seed-students/`)
    await loadExamDetails(selectedExamId.value)
    fetchExamsList()
  } catch (err) {
    const errDetails = {
      operation: 'seedSampleStudents',
      examId: selectedExamId.value,
      statusCode: err?.response?.status,
      serverMessage: err?.response?.data?.message || err?.response?.data?.detail,
      errorMessage: err.message
    }
    console.error('[OMR Registry API Error] Failed to seed students:', errDetails)
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: `تعذر توليد بيانات الطلاب التجريبية: ${errDetails.serverMessage || errDetails.errorMessage || 'خطأ في الاتصال'}`
    }
  } finally {
    seedingStudents.value = false
  }
}

const printSingleStudentCard = async (globalIndex) => {
  const isAudit = selectedSheetLayout.value === 'full_a4'
  let printableEl = null

  // 1. Check if the element is currently visible in the paginated stream
  if (batchStreamRef.value) {
    const localIndex = globalIndex % streamPageSize.value
    const pageOfIndex = Math.floor(globalIndex / streamPageSize.value) + 1
    if (pageOfIndex === streamCurrentPage.value) {
      const cards = batchStreamRef.value.querySelectorAll('.sheet-page-card')
      if (cards && cards[localIndex]) {
        printableEl = isAudit
          ? cards[localIndex].querySelector('.yemeni-audit-report-sheet')
          : (cards[localIndex].querySelector('svg.yemeni-ministry-sheet-svg') || cards[localIndex].querySelector('svg'))
      }
    }
  }

  // 2. Fallback to hidden staging container
  if (!printableEl) {
    const stagingEl = document.getElementById('omr-registry-batch-staging')
    if (stagingEl) {
      const slots = stagingEl.querySelectorAll('.batch-sheet-slot')
      if (slots && slots[globalIndex]) {
        printableEl = isAudit
          ? slots[globalIndex].querySelector('.yemeni-audit-report-sheet')
          : (slots[globalIndex].querySelector('svg.yemeni-ministry-sheet-svg') || slots[globalIndex].querySelector('svg'))
      }
    }
  }

  if (printableEl) {
    const st = filteredStreamStudents.value[globalIndex]
    await printOmrElement(printableEl, {
      title: `${selectedExam.value?.uniqueCode || 'OMR'}_${st?.seat_number || st?.model_code || globalIndex + 1}`,
      isA5: selectedSheetLayout.value === 'compact_a5'
    })
  }
}

// ── Centralized Print Package Configuration Builder ──
const resolveExamPackageConfig = (student = null, overrides = {}) => {
  const exam = selectedExam.value || targetExamForDirectPrint.value || {}
  const vCode = student?.model_code || overrides.versionCode || selectedQuestionsModelCode.value || 'A'
  const verObj = examDetails.value?.versions?.find(ver => ver.versionCode === vCode) || examDetails.value?.versions?.[0]

  return {
    examTitle: customStageTitle.value || exam.title || '',
    subjectName: exam.subject_name || '',
    stageName: exam.stage_name || '',
    yearName: customExamYear.value || exam.year_name || '',
    governorate: customGovernorate.value || student?.governorate || exam.governorate || '',
    directorate: customDirectorate.value || student?.directorate || exam.directorate || '',
    centerName: customCenterName.value || student?.school_name || exam.center_name || exam.school_name || exam.directorate || '',
    centerCode: student?.school_id || exam.center_code || exam.id || '',
    versionCode: vCode,
    studentName: student?.student_name || '',
    seatNumber: student?.seat_number || '',
    secretNumber: student?.secret_number || '',
    isA3: false,
    questions: verObj?.questions || [],
    omrElement: null,
    mode: 'package',
    isA5: selectedSheetLayout.value === 'compact_a5',
    ...overrides
  }
}

const printCurrentQuestionPaper = async () => {
  if (questionPaperRef.value) {
    const paperEl = questionPaperRef.value.querySelector('.yemeni-official-question-paper') || questionPaperRef.value
    await printOfficialQuestionPaper(paperEl, {
      title: `ورقة_أسئلة_${selectedExam.value?.subject_name || 'الاختبار'}_النموذج_${selectedQuestionsModelCode.value}`,
      isA3: selectedQuestionPaperLayout.value === 'a3'
    })
  } else {
    const config = resolveExamPackageConfig(
      sheetGenerationMode.value === 'student' ? activeSheetStudent.value : null,
      {
        versionCode: selectedQuestionsModelCode.value,
        isA3: selectedQuestionPaperLayout.value === 'a3',
        mode: 'questions_only'
      }
    )
    await printExamPackage(config)
  }
}

const printCurrentExamPackage = async () => {
  const st = activeSheetStudent.value
  let omrEl = null
  if (sheetArtboardRef.value) {
    omrEl = sheetArtboardRef.value.querySelector('.yemeni-audit-report-sheet') ||
            sheetArtboardRef.value.querySelector('svg.yemeni-ministry-sheet-svg') ||
            sheetArtboardRef.value.querySelector('svg')
  } else if (batchStreamRef.value) {
    omrEl = batchStreamRef.value.querySelector('.sheet-page-card:first-child .yemeni-audit-report-sheet') ||
            batchStreamRef.value.querySelector('.sheet-page-card:first-child svg.yemeni-ministry-sheet-svg') ||
            batchStreamRef.value.querySelector('svg')
  }

  const config = resolveExamPackageConfig(st, {
    versionCode: st?.model_code || selectedBlankVersionCode.value || selectedQuestionsModelCode.value || 'A',
    omrElement: omrEl,
    mode: 'package'
  })
  await printExamPackage(config)
}

// State & Methods for Tab 2: Question Booklets
const previewQuestionPaperDialog = ref(false)
const questionModelsList = computed(() => {
  const vers = examDetails.value?.versions || []
  if (vers.length > 0) {
    return vers.map(v => {
      const qCount = v.questions?.length || 0
      return {
        versionCode: v.versionCode,
        title: `كراسة ورقة الأسئلة - نموذج ${v.versionCode}`,
        questionsCount: qCount,
        hasQuestions: qCount > 0,
      }
    })
  }
  return []
})

const questionModelsHeaders = computed(() => [
  { title: "النموذج", key: "model_code", sortable: false, align: "center", width: "120px" },
  { title: "عنوان كراسة الأسئلة", key: "paper_title", sortable: false, align: "start" },
  { title: "عدد الأسئلة", key: "questions_count", sortable: false, align: "center", width: "130px" },
  { title: "المقاس المعتمد", key: "layout_type", sortable: false, align: "center", width: "170px" },
  { title: "حالة الكراسة", key: "status", sortable: false, align: "center", width: "150px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "230px" },
])

const questionModelsTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getQuestionModelsData = async (params = {}) => {
  const all = questionModelsList.value || []
  questionModelsTableItems.value = {
    results: all,
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: 1,
      current_page: 1,
    },
  }
  return questionModelsTableItems.value
}

watch(questionModelsList, () => {
  getQuestionModelsData()
}, { immediate: true })

const openPreviewQuestionPaper = (modelCode) => {
  selectedQuestionsModelCode.value = modelCode
  previewQuestionPaperDialog.value = true
}

const printQuestionPaperForModel = async (modelCode) => {
  selectedQuestionsModelCode.value = modelCode
  await nextTick()
  const config = resolveExamPackageConfig(null, {
    versionCode: modelCode,
    isA3: selectedQuestionPaperLayout.value === 'a3',
    mode: 'questions_only'
  })
  await printExamPackage(config)
}

const printAllQuestionPapers = async () => {
  const versions = questionModelsList.value.filter(m => m.hasQuestions).map(m => m.versionCode)
  for (const ver of versions) {
    await printQuestionPaperForModel(ver)
  }
}

// State & Methods for Tab 3: Combined Student Packages
const packageSearch = ref('')
const packageTableRef = ref(null)
const packageModelFilter = ref('all')
const selectedPackageStudentIds = ref([])
const previewPackageStudent = ref(null)
const previewPackageDialog = ref(false)
const printingPackages = ref(false)

const packageHeaders = computed(() => [
  { title: "تحديد", key: "select_box", sortable: false, align: "center", width: "65px" },
  { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "115px" },
  { title: "اسم الطالب الرباعي", key: "student_name", sortable: true, align: "start" },
  { title: "المدرسة / المركز الامتحاني", key: "school_name", sortable: true, align: "start" },
  { title: "النموذج", key: "model_code", sortable: true, align: "center", width: "110px" },
  { title: "محتوى الحزمة", key: "package_contents", sortable: false, align: "center", width: "220px" },
  { title: "حالة الطباعة", key: "is_printed", sortable: true, align: "center", width: "130px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "180px" },
])

const packageTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const filteredPackageStudents = computed(() => {
  if (!examDetails.value?.registered_students) return []
  let list = examDetails.value.registered_students
  if (packageModelFilter.value && packageModelFilter.value !== 'all') {
    list = list.filter(s => (s.model_code || 'A') === packageModelFilter.value)
  }
  if (packageSearch.value && packageSearch.value.trim()) {
    const q = packageSearch.value.trim().toLowerCase()
    list = list.filter(s =>
      String(s.seat_number || '').toLowerCase().includes(q) ||
      String(s.student_name || '').toLowerCase().includes(q) ||
      String(s.school_name || '').toLowerCase().includes(q)
    )
  }
  return list
})

const getPackageData = async (params = {}) => {
  const p = params?.params || params || {}
  if (p.search !== undefined) {
    packageSearch.value = (p.search || '').trim().toLowerCase()
  }
  const page = p.page || 1
  const pageSize = p.page_size || 50
  const all = filteredPackageStudents.value || []
  const start = (page - 1) * pageSize
  packageTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return packageTableItems.value
}

watch(filteredPackageStudents, () => {
  getPackageData()
}, { immediate: true })

const togglePackageStudentSelection = (studentId) => {
  const idx = selectedPackageStudentIds.value.indexOf(studentId)
  if (idx > -1) {
    selectedPackageStudentIds.value.splice(idx, 1)
  } else {
    selectedPackageStudentIds.value.push(studentId)
  }
}

const openPreviewPackage = (student) => {
  previewPackageStudent.value = student
  previewPackageDialog.value = true
}

const printSingleStudentPackage = async (student) => {
  const config = resolveExamPackageConfig(student, { mode: 'package' })
  await printExamPackage(config)
}

const batchPrintSelectedPackages = async () => {
  const rawTargets = selectedPackageStudentIds.value.length > 0
    ? filteredPackageStudents.value.filter(s => selectedPackageStudentIds.value.includes(s.id))
    : filteredPackageStudents.value

  if (!rawTargets || rawTargets.length === 0) {
    batchPrintNotification.value = {
      show: true,
      color: 'warning',
      message: 'لا يوجد طلاب مسجلون محددون لطباعة حزم الاختبار.'
    }
    return
  }

  // 1. المحافظة الصارمة على ترتيب الطلاب حسب رقم الجلوس أو الترتيب المعتمد
  const sortedTargets = [...rawTargets].sort((a, b) => {
    const numA = Number(a.seat_number)
    const numB = Number(b.seat_number)
    if (!isNaN(numA) && !isNaN(numB)) return numA - numB
    return String(a.seat_number || '').localeCompare(String(b.seat_number || ''))
  })

  // 2. إمكانية الاستئناف دون إعادة طباعة ما سبق
  const alreadyPrinted = sortedTargets.filter(s => s.is_printed)
  let targetsToProcess = sortedTargets
  if (alreadyPrinted.length > 0 && alreadyPrinted.length < sortedTargets.length) {
    targetsToProcess = sortedTargets.filter(s => !s.is_printed)
    batchPrintNotification.value = {
      show: true,
      color: 'info',
      message: `استئناف الطباعة الجماعية: سيتم استكمال ${targetsToProcess.length} طالباً متبقياً (تم استبعاد ${alreadyPrinted.length} طالباً سبق توثيق طباعتهم لمنع التكرار).`
    }
  }

  if (targetsToProcess.length === 0) {
    batchPrintNotification.value = {
      show: true,
      color: 'info',
      message: 'جميع الطلاب المحددين تمت طباعة حزمهم مسبقاً وموثقون في السجل التشغيلي.'
    }
    return
  }

  // 3. تقسيم المعالجة إلى مجموعات محددة الحجم (Chunking) لمنع تجمد المتصفح
  const CHUNK_SIZE = 25
  const chunks = []
  for (let i = 0; i < targetsToProcess.length; i += CHUNK_SIZE) {
    chunks.push(targetsToProcess.slice(i, i + CHUNK_SIZE))
  }

  printingPackages.value = true
  let successfulChunks = 0
  const failedChunks = []

  try {
    for (let chunkIdx = 0; chunkIdx < chunks.length; chunkIdx++) {
      const chunk = chunks[chunkIdx]

      // 4. التحقق من اكتمال كل مجموعة قبل إرسالها للطباعة
      const invalidStudents = []
      for (const st of chunk) {
        const vCode = st?.model_code || 'A'
        const verObj = examDetails.value?.versions?.find(ver => ver.versionCode === vCode) || examDetails.value?.versions?.[0]
        if (!verObj || !verObj.questions || verObj.questions.length === 0) {
          invalidStudents.push(`${st.student_name || 'بدون اسم'} (${st.seat_number || ''})`)
        }
      }

      if (invalidStudents.length > 0) {
        failedChunks.push({
          chunkIndex: chunkIdx + 1,
          error: `نقص أسئلة النموذج للطلاب: ${invalidStudents.slice(0, 3).join(', ')}${invalidStudents.length > 3 ? '...' : ''}`
        })
        break
      }

      // 5. إنشاء حزمة واحدة موحدة للمجموعة ترسل إلى أمر طباعة واحد فقط
      const packagesOptionsList = chunk.map(st => resolveExamPackageConfig(st, { mode: 'package' }))

      const chunkTitle = `حزم_اختبار_${selectedExam.value?.uniqueCode || 'OMR'}_المجموعة_${chunkIdx + 1}_من_${chunks.length}`
      await printExamPackagesBatch(packagesOptionsList, { title: chunkTitle })

      // 6. تسجيل نجاح وفشل كل جزء على الخادم وحفظ أرقام الدفعات
      const chunkBatchId = `PKG-CHUNK-${selectedExam.value?.uniqueCode || selectedExamId.value}-${Date.now()}-${chunkIdx + 1}`
      const chunkStudentIds = chunk.map(s => s.id)

      if (selectedExamId.value && chunkStudentIds.length > 0) {
        try {
          const resp = await api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
            student_ids: chunkStudentIds,
            batch_id: chunkBatchId,
            notes: `طباعة حزم مجمعة - المجموعة ${chunkIdx + 1} من ${chunks.length} (${chunk.length} طالب)`
          })

          if (resp.data && resp.data.success) {
            const printTime = new Date().toLocaleTimeString('ar-YE')
            chunk.forEach(st => {
              st.is_printed = true
              st.printed_at = printTime
              st.print_batch = chunkBatchId
            })

            if (selectedExam.value && resp.data.total_printed_count !== undefined) {
              selectedExam.value.printed_count = resp.data.total_printed_count
              selectedExam.value.is_completed = !!resp.data.is_completed
              selectedExam.value.print_status = resp.data.print_status || (resp.data.is_completed ? 'full' : 'partial')
            }
            successfulChunks++
          } else {
            failedChunks.push({
              chunkIndex: chunkIdx + 1,
              error: resp.data?.message || 'تعذر توثيق المجموعة بالخادم'
            })
            break
          }
        } catch (postErr) {
          console.error(`[OMR Registry] خطأ في توثيق المجموعة ${chunkIdx + 1} بالخادم:`, postErr)
          failedChunks.push({
            chunkIndex: chunkIdx + 1,
            error: postErr?.message || postErr
          })
          break
        }
      } else {
        successfulChunks++
      }
    }

    // 7. إظهار تقرير الإنجاز النهائي وتحديث السجل
    if (failedChunks.length === 0) {
      batchPrintNotification.value = {
        show: true,
        color: 'success',
        message: `اكتملت طباعة وتوثيق جميع حزم الطلاب بنجاح! تم إرسال ${chunks.length} مجموعات بإجمالي ${targetsToProcess.length} طالب.`
      }
      selectedPackageStudentIds.value = []
      fetchBatches()
    } else {
      batchPrintNotification.value = {
        show: true,
        color: 'warning',
        message: `تمت طباعة ${successfulChunks} من أصل ${chunks.length} مجموعات بنجاح. توقفت العملية عند المجموعة ${failedChunks[0]?.chunkIndex}: ${failedChunks[0]?.error}. يمكنك الاستئناف مباشرة للطلاب المتبقين.`
      }
      fetchBatches()
    }
  } catch (err) {
    console.error('Batch package print error:', err)
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: `حدث خطأ أثناء طباعة حزم الطلاب: ${err?.message || err}`
    }
  } finally {
    printingPackages.value = false
  }
}

const selectAllPackageStudents = () => {
  if (selectedPackageStudentIds.value.length === filteredPackageStudents.value.length) {
    selectedPackageStudentIds.value = []
  } else {
    selectedPackageStudentIds.value = filteredPackageStudents.value.map(s => s.id)
  }
}

const printSingleSheet = async () => {
  await nextTick()
  let printableEl = null
  if (sheetArtboardRef.value) {
    printableEl = sheetArtboardRef.value.querySelector('.yemeni-audit-report-sheet') ||
                  sheetArtboardRef.value.querySelector('svg.yemeni-ministry-sheet-svg') ||
                  sheetArtboardRef.value.querySelector('svg')
  } else if (batchStreamRef.value) {
    printableEl = batchStreamRef.value.querySelector('.sheet-page-card:first-child .yemeni-audit-report-sheet') ||
                  batchStreamRef.value.querySelector('.sheet-page-card:first-child svg.yemeni-ministry-sheet-svg') ||
                  batchStreamRef.value.querySelector('svg')
  }

  if (printableEl) {
    await printOmrElement(printableEl, {
      title: `${selectedExam.value?.uniqueCode || 'OMR'}_${activeSheetStudent.value?.seat_number || activeSheetModelCode.value}`,
      isA5: selectedSheetLayout.value === 'compact_a5'
    })
  } else {
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: 'تعذر العثور على عنصر ورقة التظليل القابل للطباعة في نافذة المعاينة.'
    }
  }
}

const refreshData = async () => {
  if (currentView.value === 'master') {
    await loadMasterData()
    await fetchBatches()
  } else {
    await fetchExamsList()
    if (selectedExamId.value) {
      await loadExamDetails(selectedExamId.value)
    }
    await fetchBatches()
  }
}

onMounted(async () => {
  await Promise.all([
    loadSavedPrintOrders(),
    loadSubjects(),
    loadMasterData(),
    fetchBatches(),
  ])

  const qExam = route.query.exam || route.query.exam_id
  const qView = route.query.view
  const qTab = route.query.tab

  if (qView === 'orders' || qTab === 'exams') {
    currentView.value = 'master'
    masterTab.value = 'exams'
    if (route.query.subtab) {
      examSubTab.value = route.query.subtab
    }
  } else if (qExam) {
    currentView.value = 'detail'
    selectedExamId.value = Number(qExam)
    await loadExamDetails(selectedExamId.value)
    if (route.query.tab && ['sheets', 'questions', 'package', 'history'].includes(route.query.tab)) {
      activeTab.value = route.query.tab
    } else {
      activeTab.value = 'sheets'
    }
    const title = selectedExam.value?.title || examDetails.value?.exam?.title || 'الاختبار'
    batchPrintNotification.value = {
      show: true,
      color: 'success',
      message: `تم نقل واستلام "${title}" بنجاح! كافة وثائق الاختبار وأوراق التظليل جاهزة للمعاينة والطباعة الفورية.`
    }
  } else {
    await fetchExamsList()
  }
})

// Watch route.query to maintain URL and tab/subtab synchronization reactively
watch(() => route.query, (q) => {
  if (!q) return
  const qExam = q.exam || q.exam_id
  const qView = q.view
  const qTab = q.tab

  if (qView === 'orders' || qTab === 'exams') {
    currentView.value = 'master'
    masterTab.value = 'exams'
    if (q.subtab && ['orders', 'all', 'scheduled', 'due', 'completed', 'cancelled'].includes(q.subtab)) {
      examSubTab.value = q.subtab
    }
  } else if (qExam) {
    const eid = Number(qExam)
    if (eid && selectedExamId.value !== eid) {
      currentView.value = 'detail'
      selectedExamId.value = eid
      loadExamDetails(eid)
    }
  }
}, { deep: true })

// Keep route.query updated when user switches subtabs
watch(examSubTab, (sub) => {
  examMasterSearchTerm.value = ''
  getExamMasterData()
  if (masterTab.value === 'exams' && currentView.value === 'master') {
    if (route.query.subtab !== sub) {
      router.replace({ query: { ...route.query, subtab: sub } }).catch(() => {})
    }
  }
})
</script>

<style scoped>
/* ── Custom Data Table Cell Width & Centering Fixes ── */
:deep(.custom-data-table td),
:deep(.custom-data-table .v-data-table__td) {
  max-width: none !important;
  white-space: normal !important;
  word-break: normal !important;
  overflow: visible !important;
  text-overflow: clip !important;
}

/* ── Compact & Refined Table Action Buttons and Chips ── */
:deep(.table-actions-cell) {
  min-height: 30px;
}

:deep(.table-action-btn),
.table-action-btn {
  height: 28px !important;
  min-height: 28px !important;
  font-size: 0.74rem !important;
  letter-spacing: 0 !important;
  padding: 0 8px !important;
  border-radius: 6px !important;
  box-shadow: none !important;
  text-transform: none !important;
  transition: all 0.15s ease-in-out !important;
}

:deep(.table-action-btn:hover),
.table-action-btn:hover {
  transform: translateY(-1px);
}

:deep(.table-action-btn .v-icon),
.table-action-btn .v-icon {
  font-size: 14px !important;
  width: 14px !important;
  height: 14px !important;
  margin-inline-end: 4px !important;
}

:deep(.table-action-chip),
.table-action-chip {
  height: 24px !important;
  min-height: 24px !important;
  font-size: 0.72rem !important;
  padding: 0 8px !important;
  border-radius: 6px !important;
}

:deep(.table-action-icon-btn),
.table-action-icon-btn {
  height: 28px !important;
  width: 28px !important;
  min-width: 28px !important;
  max-width: 28px !important;
  padding: 0 !important;
  border-radius: 6px !important;
}

:deep(.table-action-icon-btn .v-icon),
.table-action-icon-btn .v-icon {
  font-size: 15px !important;
  width: 15px !important;
  height: 15px !important;
  margin: 0 !important;
}

:deep(.table-action-chip .v-icon),
.table-action-chip .v-icon {
  font-size: 13px !important;
  width: 13px !important;
  height: 13px !important;
  margin-inline-end: 4px !important;
}

:deep(.custom-data-table th),
:deep(.custom-data-table .v-data-table__th) {
  white-space: nowrap !important;
}

:deep(.custom-data-table .class-numbering-child-2 th:nth-child(2)),
:deep(.custom-data-table .class-numbering-child-2 td:nth-child(2)),
:deep(.class-numbering-child-2 th:nth-child(2)),
:deep(.class-numbering-child-2 td:nth-child(2)) {
  width: 44px !important;
  min-width: 44px !important;
  max-width: 50px !important;
  text-align: center !important;
}

.font-mono {
  font-family: monospace, monospace;
}
.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
.omr-preview-viewport {
  background-color: #f1f5f9;
  min-height: 500px;
}
.all-sheets-stream {
  width: 100%;
}
.sheet-page-card {
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  border-radius: 16px !important;
}

.sheet-paper-wrapper {
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: visible;
}

/* ── Lightweight Navigation Bar ── */
/* Active Exam Banner Styling */
.active-exam-banner {
  border-color: rgba(var(--v-border-color), var(--v-border-opacity, 0.12)) !important;
  background-color: rgb(var(--v-theme-surface)) !important;
  transition: all 0.2s ease;
}

.exam-icon-badge {
  background-color: rgba(var(--v-theme-primary), 0.1) !important;
  border-color: rgba(var(--v-theme-primary), 0.2) !important;
}

.exam-code-tag {
  letter-spacing: 0.5px;
  font-size: 0.72rem !important;
  border-color: rgba(var(--v-border-color), var(--v-border-opacity, 0.12)) !important;
  background-color: rgba(var(--v-theme-surface), 0.8) !important;
  color: rgb(var(--v-theme-primary)) !important;
}

.exam-stat-chip {
  border-color: rgba(var(--v-border-color), var(--v-border-opacity, 0.12)) !important;
  background-color: rgba(var(--v-theme-surface), 0.8) !important;
  min-width: 110px;
}

.registry-nav-bar {
  direction: rtl;
}

.registry-nav-container {
  display: flex;
  align-items: center;
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity, 0.12));
  border-radius: 12px;
  padding: 6px;
  gap: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.registry-nav-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 9px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.84rem;
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.7);
  background: transparent;
  transition: all 0.2s ease;
  user-select: none;
  white-space: nowrap;
}

.registry-nav-item:hover {
  background: rgba(var(--v-theme-on-surface), 0.06);
  color: rgb(var(--v-theme-on-surface));
}

.registry-nav-item.is-active {
  background: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
  font-weight: 800;
  border: 1px solid rgba(var(--v-theme-primary), 0.25);
}

.registry-nav-item.is-active .nav-icon {
  color: rgb(var(--v-theme-primary));
}

@media (max-width: 1024px) {
  .registry-nav-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .registry-nav-container {
    grid-template-columns: 1fr;
  }
}

/* ── Unified Rectangular Status Badges ── */
.center-count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-surface-variant), 0.35);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 6px !important;
  font-size: 0.74rem;
  line-height: 1.2;
}

.unified-badge-primary {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  color: rgb(var(--v-theme-primary)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.25) !important;
}

.unified-badge-warning {
  background: rgba(245, 158, 11, 0.12) !important;
  color: #b45309 !important;
  border: 1px solid rgba(245, 158, 11, 0.25) !important;
}

.unified-badge-info {
  background: rgba(2, 132, 199, 0.12) !important;
  color: #0284c7 !important;
  border: 1px solid rgba(2, 132, 199, 0.25) !important;
}

.unified-badge-error {
  background: rgba(239, 68, 68, 0.12) !important;
  color: #dc2626 !important;
  border: 1px solid rgba(239, 68, 68, 0.25) !important;
}

.unified-badge-grey {
  background: rgba(148, 163, 184, 0.14) !important;
  color: #64748b !important;
  border: 1px solid rgba(148, 163, 184, 0.28) !important;
}
</style>
