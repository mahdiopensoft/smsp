<template>
  <div class="qb-omr-print-registry pa-4 pa-md-6">

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. MASTER VIEW: الهيكل الإداري وسجل الطباعة المركزي             -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <MasterView
      v-if="currentView === 'master'"
      :filters="filters"
      :loading-master="loadingMaster"
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
      :batches="batches"
      :is-tab-visited="isTabVisited"
      :loading-exam-details="loadingExamDetails"
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
          :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
          :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة العامة'))"
          :exam-year="customExamYear || selectedExam?.year_name || '2026'"
          :center-name="customCenterName || st.school_name || selectedExam?.directorate || 'المركز الاختباري الرئيسي'"
          :center-code="st.school_id || selectedExam?.id || '101'"
          :governorate="customGovernorate || st.governorate || selectedExam?.governorate || 'أمانة العاصمة'"
          :directorate="customDirectorate || st.directorate || selectedExam?.directorate || 'السبعين'"
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
          :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
          :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة العامة'))"
          :exam-year="customExamYear || selectedExam?.year_name || '2026'"
          :center-name="customCenterName || st.school_name || selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
          :governorate="customGovernorate || selectedExam?.governorate || 'أمانة العاصمة'"
          :directorate="customDirectorate || st.directorate || selectedExam?.directorate || 'السبعين'"
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
import { printOmrElement, printOmrBatch, printOfficialQuestionPaper, printExamPackage } from './utils/omrPrint'
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
const loadingBatches = ref(false)

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
    return (directoratesList.value || []).filter(d => officeIds.includes(Number(d.office_id)))
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
    const dObjs = (directoratesList.value || []).filter(d => dirIds.includes(Number(d.id)))
    const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
    list = list.filter(s => 
      dirIds.includes(Number(s.directorate_id)) ||
      dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
    )
  } else if (officeIds.length > 0) {
    const oObjs = (officesList.value || []).filter(o => officeIds.includes(Number(o.id)))
    const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
    list = list.filter(s => 
      officeIds.includes(Number(s.office_id)) ||
      oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
    )
  }
  const schoolIds = normalizeIds(selectedSchoolId.value)
  if (schoolIds.length > 0) {
    list = list.filter(s => schoolIds.includes(Number(s.id)))
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
    list = list.filter(o => effGov.includes(Number(o.id)) || effGov.includes(Number(o.governorate_id)))
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
    list = list.filter(d => effGov.includes(Number(d.office_id)) || effGov.includes(Number(d.governorate_id)))
  }
  const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
  if (effDir.length > 0) {
    list = list.filter(d => effDir.includes(Number(d.id)))
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
    const dObjs = (directoratesList.value || []).filter(d => effDir.includes(Number(d.id)))
    const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
    list = list.filter(s => 
      effDir.includes(Number(s.directorate_id)) ||
      dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
    )
  } else if (effGov.length > 0) {
    const oObjs = (officesList.value || []).filter(o => effGov.includes(Number(o.id)))
    const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
    list = list.filter(s => 
      effGov.includes(Number(s.office_id)) ||
      effGov.includes(Number(s.governorate_id)) ||
      oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
    )
  }
  const effOrg = filterOrganization.value ? [Number(filterOrganization.value)] : normalizeIds(selectedSchoolId.value)
  if (effOrg.length > 0) {
    list = list.filter(s => effOrg.includes(Number(s.id)))
  }
  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    const sObj = subjectsList.value.find(s => s.id === effSubj)
    const sName = sObj?.name?.trim()
    list = list.filter(s => {
      if (s.subjects && Array.isArray(s.subjects)) {
        return s.subjects.some(sub => sub === sName || (sName && sub.includes(sName)))
      }
      return s.subject_name === sName || (sName && s.subject_name && s.subject_name.includes(sName))
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
    list = list.filter(e => effOrg.includes(Number(e.school_id)) || effOrg.includes(Number(e.school)) || effOrg.includes(Number(e.organization_id)))
  } else if (effDir.length > 0) {
    list = list.filter(e => effDir.includes(Number(e.directorate_id)) || effDir.includes(Number(e.directorate)))
  } else if (effGov.length > 0) {
    list = list.filter(e => effGov.includes(Number(e.governorate_id)) || effGov.includes(Number(e.office_id)) || effGov.includes(Number(e.governorate)))
  }

  if (filterStage.value) {
    list = list.filter(e => Number(e.stage_id) === Number(filterStage.value) || Number(e.stage) === Number(filterStage.value))
  }
  if (filterClassTrack.value) {
    list = list.filter(e => Number(e.class_track_id) === Number(filterClassTrack.value) || Number(e.class_track) === Number(filterClassTrack.value))
  }

  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    list = list.filter(e => Number(e.subject_id) === Number(effSubj) || Number(e.subject) === Number(effSubj))
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
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(b => 
      (b.batch_id && b.batch_id.toLowerCase().includes(q)) ||
      (b.exam_title && b.exam_title.toLowerCase().includes(q)) ||
      (b.exam_code && b.exam_code.toLowerCase().includes(q))
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

// ── Sub-tabs for "الاختبارات المعتمدة للطباعة" (الطلبات / المجدولة / المستحقة / المكتملة / الملغية / السجل الشامل) ──
const examSubTab = ref('orders')
const savedPrintOrders = ref([])
const manifestDialog = ref(false)
const selectedManifestOrder = ref(null)

const loadSavedPrintOrders = async () => {
  try {
    const res = await api.get('/api/omr/print-orders/')
    if (res.data && res.data.success) {
      savedPrintOrders.value = res.data.results || []
    }
  } catch (err) {
    console.error('Failed to load real print orders from backend:', err)
  }
}

const previewOrderManifest = (exam) => {
  const order = (savedPrintOrders.value || []).find(o => 
    String(o.exam_id) === String(exam.id) || 
    (o.exam_code && o.exam_code === exam.uniqueCode) ||
    (o.order_number && exam.uniqueCode && o.order_number.includes(exam.uniqueCode))
  )
  if (order) {
    selectedManifestOrder.value = {
      ...order,
      exam_title: exam.title || order.exam_title,
      subject_name: exam.subject_name || order.subject_name || 'عام',
      grand_total: exam.total_registered || exam.total_students || order.grand_total || 0,
      actual_exam_date: exam.exam_date || order.actual_exam_date,
    }
    manifestDialog.value = true
  } else {
    selectedManifestOrder.value = {
      order_number: exam.order_number || `PRN-REQ-${exam.uniqueCode || exam.id}`,
      exam_id: exam.id,
      exam_title: exam.title,
      exam_code: exam.uniqueCode,
      subject_name: exam.subject_name || 'عام',
      press_name: exam.press_name || 'المطبعة السرية المركزية (ديوان الوزارة)',
      scheduled_print_date: exam.scheduled_print_date || getTodayIso(),
      actual_exam_date: exam.exam_date || exam.actual_exam_date || getTodayIso(),
      status: exam.order_status || 'approved',
      grand_total: exam.total_registered || exam.total_students || 0,
    }
    manifestDialog.value = true
  }
}

const getTodayIso = () => {
  const d = new Date()
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const enrichedMasterExamsList = computed(() => {
  try {
    const baseList = filteredMasterExamsTable.value || []
    const today = getTodayIso()

    return baseList.filter(Boolean).map(exam => {
      try {
        const order = (savedPrintOrders.value || []).find(o => 
          o && (
            String(o.exam_id) === String(exam.id) || 
            (o.exam_code && exam.uniqueCode && String(o.exam_code) === String(exam.uniqueCode)) ||
            (o.order_number && exam.uniqueCode && String(o.order_number).includes(String(exam.uniqueCode)))
          )
        )

        const rawStatus = order?.status || (exam.order_status || 'pending')
        const scheduledDate = order?.scheduled_print_date || exam.scheduled_print_date || null
        const examDate = order?.actual_exam_date || exam.exam_date || null
        const orderNumber = order?.order_number || exam.order_number || null
        const pressName = order?.press_name || exam.press_name || null
        const grandTotal = order?.grand_total || (exam.total_registered || exam.total_students || 0)
        const returnReason = order?.return_reason || exam.return_reason || ''
        const returnNotes = order?.return_notes || exam.return_notes || ''

        const isFullyPrinted = (Number(exam.printed_rate) >= 100) || (exam.print_status === 'full') || (exam.print_status === 'printed') || rawStatus === 'completed'
        const isFailed = rawStatus === 'failed' || rawStatus === 'returned'
        const isCancelled = rawStatus === 'cancelled'

        // 1. Completed: 100% printed or status completed
        const isCompleted = isFullyPrinted

        // 2. Returned / Failed
        const isReturned = !isCompleted && isFailed

        // 3. Pending: incoming request not yet approved by committee
        const isPending = !isCompleted && !isReturned && !isCancelled && (rawStatus === 'pending')

        // 4. Scheduled: approved with future print date (> today)
        const isScheduled = !isCompleted && !isReturned && !isCancelled && !isPending && (rawStatus === 'scheduled' || (scheduledDate && scheduledDate > today))

        // 5. Due: approved with print date today or earlier (<= today), or in active printing
        const isDue = !isCompleted && !isReturned && !isCancelled && !isPending && !isScheduled && (rawStatus === 'ready' || rawStatus === 'printing' || (scheduledDate && scheduledDate <= today) || rawStatus === 'approved')

        const effectiveStatus = isCompleted ? 'completed' :
                               (isReturned ? 'failed' :
                               (isScheduled ? 'scheduled' :
                               (isDue ? (rawStatus === 'printing' ? 'printing' : 'ready') :
                               (isCancelled ? 'cancelled' : 'pending'))))

        return {
          ...exam,
          has_order: !!order || !!exam.order_number,
          order_status: effectiveStatus,
          raw_order_status: rawStatus,
          return_reason: returnReason,
          return_notes: returnNotes,
          order_number: orderNumber,
          scheduled_print_date: scheduledDate,
          actual_exam_date: examDate,
          press_name: pressName,
          total_to_print: grandTotal,
          is_pending: isPending,
          is_returned: isReturned,
          is_approved: !isPending && !isReturned && !isCancelled,
          is_scheduled: isScheduled,
          is_due: isDue,
          is_completed: isCompleted,
        }
      } catch (itemErr) {
        console.error('Error enriching exam item:', exam, itemErr)
        return exam
      }
    })
  } catch (err) {
    console.error('Error in enrichedMasterExamsList:', err)
    return filteredMasterExamsTable.value || []
  }
})

// ── Dialog States & Handlers for Print Orders Workflow ──
const approveOrderDialog = ref(false)
const targetExamForApproval = ref(null)
const actionLoading = ref(false)

const getCurrentUserOfficerName = () => {
  try {
    const raw = localStorage.getItem('auth_user') || localStorage.getItem('profile')
    if (raw) {
      const u = JSON.parse(raw)
      return u.full_name || u.name || u.username || 'مدير إدارة الامتحانات والكنترول'
    }
  } catch (e) {}
  return 'مدير إدارة الامتحانات والكنترول'
}

const openApproveDialog = (exam) => {
  targetExamForApproval.value = exam
  approveOrderDialog.value = true
}

const onOrderApproved = async (payload) => {
  await loadSavedPrintOrders()
  await loadMasterData()

  const today = getTodayIso()
  const isFuture = payload.scheduledDate > today
  if (isFuture) {
    examSubTab.value = 'scheduled'
    batchPrintNotification.value = {
      show: true,
      color: 'info',
      message: `تم اعتماد وتوثيق أمر الطباعة بنجاح للاختبار "${payload.exam.title}"! تم نقله إلى تبويب [المجدولة] بموعد طباعة (${payload.scheduledDate}).`,
    }
  } else {
    examSubTab.value = 'due'
    batchPrintNotification.value = {
      show: true,
      color: 'success',
      message: `تم اعتماد وتوثيق أمر الطباعة بنجاح للاختبار "${payload.exam.title}"! تم نقله إلى تبويب [المستحقة] وهو جاهز للتنفيذ الفوري الآن.`,
    }
  }

  if (payload.openManifest) {
    previewOrderManifest(payload.exam)
  }
}

const returnOrderDialog = ref(false)
const targetExamForReturn = ref(null)
const returnReasonSelected = ref('كمية الاحتياط تتجاوز النسبة المعتمدة دون وثيقة تفويض')
const returnNotesText = ref('')
const predefinedReturnReasons = [
  'كمية الاحتياط تتجاوز النسبة المعتمدة دون وثيقة تفويض',
  'نقص أو عدم تطابق في كشوفات الطلاب لبعض المراكز الامتحانية',
  'نماذج الأسئلة بحاجة لإعادة تدقيق ومراجعة فنية',
  'تعارض موعد الطباعة مع جدول تشغيل المطبعة المركزية',
  'أخرى (توضيح في الملاحظات أدناه)',
]

const returnReasonsObjects = computed(() => {
  return predefinedReturnReasons.map(r => ({
    id: r,
    value: r,
    name: r,
    title: r,
  }))
})

const advanceScheduleDialog = ref(false)
const targetExamForAdvance = ref(null)
const advanceReasonSelected = ref('شحن وترحيل مبكر لمحافظات بعيدة أو نائية (سقطرى، المهرة، إلخ)')
const advanceAuthDoc = ref('')
const advanceReasonsList = [
  'شحن وترحيل مبكر لمحافظات بعيدة أو نائية (سقطرى، المهرة، إلخ)',
  'توزيع أحمال ماكينات المطبعة المركزية وتفادي ضغط الأيام الأخيرة',
  'توجيه وزاري استثنائي لتقديم موعد الاختبار',
  'إجازة رسمية أو طارئ مناخي/أمني يستوجب الترحيل المبكر',
  'أخرى (مبرر إداري استثنائي)',
]

const openReturnDialog = (exam) => {
  targetExamForReturn.value = exam
  returnReasonSelected.value = predefinedReturnReasons[0]
  returnNotesText.value = ''
  returnOrderDialog.value = true
}

const confirmOrderReturn = async () => {
  if (!targetExamForReturn.value) return
  actionLoading.value = true
  try {
    const exam = targetExamForReturn.value

    await api.post('/api/omr/print-orders/return-order/', {
      exam_id: exam.id,
      return_reason: returnReasonSelected.value,
      return_notes: returnNotesText.value,
    })

    await loadSavedPrintOrders()
    await loadMasterData()
    returnOrderDialog.value = false

    batchPrintNotification.value = {
      show: true,
      color: 'warning',
      message: `تم إرجاع طلب طباعة الاختبار "${exam.title}" للتعديل بنجاح: (${returnReasonSelected.value}). سيظهر كمرتجع في السجل وشاشة إدارة الاختبارات.`,
    }
  } catch (e) {
    console.error('Failed to return order:', e)
  } finally {
    actionLoading.value = false
  }
}

const openAdvanceScheduleDialog = (exam) => {
  targetExamForAdvance.value = exam
  advanceReasonSelected.value = advanceReasonsList[0]
  advanceAuthDoc.value = ''
  advanceScheduleDialog.value = true
}

const onConfirmAdvanceSchedule = async ({ exam, reason, authDoc }) => {
  const target = exam || targetExamForAdvance.value
  if (!target) return
  actionLoading.value = true
  try {
    await api.post('/api/omr/print-orders/advance/', {
      exam_id: target.id,
      advance_reason: reason || advanceReasonSelected.value,
      advance_auth_doc: authDoc || advanceAuthDoc.value,
    })

    await loadSavedPrintOrders()
    await loadMasterData()
    advanceScheduleDialog.value = false
    examSubTab.value = 'due'

    batchPrintNotification.value = {
      show: true,
      color: 'success',
      message: `تم تقديم موعد طباعة "${target.title}" لليوم وتوثيق التفويض رسمياً! تم نقله إلى تبويب [المستحقة] وهو جاهز للتنفيذ الفوري الآن.`,
    }
  } catch (e) {
    console.error('Failed to advance schedule:', e)
  } finally {
    actionLoading.value = false
  }
}

// ── Cancel Print Order Handlers ──
const cancelOrderDialog = ref(false)
const targetExamForCancel = ref(null)

const openCancelOrderDialog = (exam) => {
  targetExamForCancel.value = exam
  cancelOrderDialog.value = true
}

const onConfirmCancelOrder = async ({ exam, reason, notes }) => {
  const target = exam || targetExamForCancel.value
  if (!target) return
  actionLoading.value = true
  try {
    const fullReason = (reason || 'تم إلغاء الاختبار بقرار من إدارة الامتحانات والكنترول') + (notes ? ` (${notes})` : '')

    await api.post('/api/omr/print-orders/cancel-order/', {
      exam_id: target.id,
      cancel_reason: fullReason,
    })

    target.order_status = 'cancelled'
    target.raw_order_status = 'cancelled'
    target.is_cancelled = true
    target.is_due = false
    target.is_scheduled = false
    target.return_reason = fullReason

    await Promise.all([
      loadSavedPrintOrders(),
      loadMasterData(),
    ])

    cancelOrderDialog.value = false
    examSubTab.value = 'cancelled'

    batchPrintNotification.value = {
      show: true,
      color: 'info',
      message: `تم إلغاء أمر طباعة "${target.title}" بنجاح وتوثيق القرار رسمياً! تم نقله إلى تبويب [الملغية].`,
    }
  } catch (err) {
    console.error('Failed to cancel order:', err)
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: 'تعذر إلغاء أمر الطباعة، يرجى المحاولة لاحقاً.',
    }
  } finally {
    actionLoading.value = false
  }
}

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

  const orderNum = exam.order_number || `PRN-REQ-${exam.uniqueCode || exam.id}`
  const examTitle = exam.title || 'الاختبار العام'
  const examCode = exam.uniqueCode || 'EXAM-CODE'
  const subjectName = exam.subject_name || 'الرياضيات'
  const pressName = exam.press_name || 'المطبعة السرية المركزية (ديوان الوزارة)'
  const officerName = exam.responsible_officer || 'مدير إدارة الامتحانات والكنترول'
  const schedDate = exam.scheduled_print_date || getTodayIso()
  const totalCount = exam.total_registered || exam.total_students || 0
  const schoolsCount = exam.schools_count || 1

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
          <div class="order-code">رقم أمر الطباعة: ${orderNum}</div>
        </div>

        <table class="info-table">
          <tr>
            <td class="lbl">اسم الاختبار:</td>
            <td class="val"><strong>${examTitle}</strong></td>
            <td class="lbl">المادة:</td>
            <td class="val">${subjectName}</td>
          </tr>
          <tr>
            <td class="lbl">كود الاختبار:</td>
            <td class="val font-mono">${examCode}</td>
            <td class="lbl">تاريخ التنفيذ المعتمد:</td>
            <td class="val font-mono">${schedDate}</td>
          </tr>
          <tr>
            <td class="lbl">المطبعة المنفذة:</td>
            <td class="val">${pressName}</td>
            <td class="lbl">المسؤول المعتمد:</td>
            <td class="val">${officerName}</td>
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
            <div>التاريخ: ${schedDate}</div>
          </div>
          <div class="sig-box">
            <div>المشرف المسؤول بالمطبعة</div>
            <div class="sig-line">التوقيع: ...........................</div>
            <div>الختم الرسمي: ....................</div>
          </div>
          <div class="sig-box">
            <div>مدير عام الامتحانات والكنترول</div>
            <div class="sig-line">المصادقة: ...........................</div>
            <div>التاريخ: ${schedDate}</div>
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
            <div class="order-code">الاختبار: ${examTitle} (${examCode}) — المادة: ${subjectName}</div>
          </div>
          <div style="border: 2px dashed #b71c1c; background: #fff8f8; color: #b71c1c; padding: 30px 20px; text-align: center; border-radius: 8px; margin: 40px auto; max-width: 650px;">
            <div style="font-size: 17px; font-weight: bold; margin-bottom: 8px;">تنبيه الرقابة والكنترول: لا تتوفر سجلات طلاب مقيدين</div>
            <p style="font-size: 13px; margin: 0; color: #374151; line-height: 1.6;">
              لا توجد بيانات طلاب مقيدين في قاعدة البيانات لهذا الاختبار (${examCode}).
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
            <td style="text-align: center; font-family: monospace; font-weight: bold;">${st.seat_number || ''}</td>
            <td style="text-align: center; font-family: monospace;">${st.secret_number || ''}</td>
            <td style="font-weight: bold;">${st.student_name || ''}</td>
            <td>${st.school_name || 'المركز الرئيسي'}</td>
            <td style="text-align: center; font-weight: bold;">نموذج ${st.model_code || 'A'}</td>
            <td style="min-width: 100px;"></td>
          </tr>
        `
      })

      sectionsHtml += `
        <div class="print-page">
          <div class="header">
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كشف تسليم واستلام وثائق الاختبار للمركز الامتحاني</h3>
            <div class="order-code">الاختبار: ${examTitle} (${examCode}) — المادة: ${subjectName}</div>
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
      sectionsHtml += `
        <div class="print-page question-booklet-page">
          <div class="header">
            <div class="header-badge">سري للغاية — وثيقة امتحانية رسمية</div>
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كراسة الأسئلة الامتحانية المقننة — نموذج (${m.model_code || 'A'})</h3>
            <div class="order-code">المادة: ${subjectName} | كود الاختبار: ${examCode}</div>
          </div>
          <div style="border: 2px dashed #000; padding: 25px; text-align: center; margin: 40px 0; border-radius: 8px;">
            <h2 style="margin: 0 0 10px 0;">كراسة الأسئلة — نموذج (${m.model_code || 'A'})</h2>
            <p style="font-size: 14px; color: #444;">
              عدد الفقرات: <strong>${m.questions_count || 50} فقرة اختيار من متعدد</strong> | الزمن المحدد: <strong>ساعتان ونصف</strong>
            </p>
            <p style="font-size: 12px; color: #777; margin-top: 20px;">
              تعليمات: تأكد من تطابق نموذج كراسة الأسئلة (${m.model_code || 'A'}) مع النموذج المطبوع على ورقة إجابتك المخصصة.
            </p>
          </div>
        </div>
      `
    })
  }

  // 4. أوراق إجابة OMR الرسمية الحقيقية للنظام (SVGs الأصلية المعتمدة)
  if (options?.sheets && realOmrElements && realOmrElements.length > 0) {
    realOmrElements.forEach(el => {
      const cloned = el.cloneNode(true)
      if (cloned instanceof HTMLElement) {
        cloned.querySelectorAll('.d-print-none, button, .v-btn').forEach(b => b.remove())
      }
      sectionsHtml += `
        <div class="print-page omr-real-sheet-page">
          <div class="real-sheet-container">
            ${cloned.outerHTML}
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
          <h1>${examTitle} (${examCode})</h1>
        </div>
        <p style="text-align: center; font-size: 16px; margin-top: 30px;">
          المادة: ${subjectName} | إجمالي المقيدين: ${totalCount} طالب | المطبعة: ${pressName}
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
      <title>أمر سحب وثائق الاختبار - ${examTitle} (${examCode})</title>
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

  // إنشاء إطار طباعة مخفي في الصفحة (لا يحظره أي متصفح كالنوافذ المنبثقة)
  const iframe = document.createElement('iframe')
  iframe.id = 'omr-hardware-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
  iframe.setAttribute('aria-hidden', 'true')
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document || iframe.contentDocument
  if (doc) {
    doc.open()
    doc.write(fullHtml)
    doc.close()

    // استدعاء نافذة الطباعة الحقيقية للنظام والمتصفح فوراً بعد إعداد المستند
    setTimeout(() => {
      try {
        iframe.contentWindow?.focus()
        iframe.contentWindow?.print()
      } catch (err) {
        console.warn('Iframe print error, falling back to window.print():', err)
        window.print()
      }
    }, 250)
  } else {
    window.print()
  }
}

const onDirectPrintStart = async ({ exam, options }) => {
  if (!exam) return

  directPrintLoading.value = true
  try {
    // 1. التأكد من تحديد الاختبار وتحميل بياناته
    selectedExam.value = exam
    selectedExamId.value = exam.id
    if (!examDetails.value || examDetails.value.id !== exam.id) {
      await loadExamDetails(exam.id)
    }

    rosterModelFilter.value = 'all'
    selectedStudentIds.value = []

    // 2. إذا تم اختيار أوراق إجابة OMR، نقوم باستخراج الأوراق الحقيقية الأصلية من المكون المعتمد
    let realOmrElements = []
    if (options?.sheets) {
      printingBatch.value = true
      await nextTick()
      const stagingEl = document.getElementById('omr-registry-batch-staging')
      if (stagingEl) {
        stagingEl.classList.remove('d-none')
        await nextTick()
        // منح وقت كافٍ للمكون لرسم SVG وشفرات الباركود وQR الرسمية
        await new Promise(resolve => setTimeout(resolve, 450))

        const isAudit = selectedSheetLayout.value === 'full_a4'
        if (isAudit) {
          realOmrElements = Array.from(stagingEl.querySelectorAll('.yemeni-audit-report-sheet'))
        } else {
          realOmrElements = Array.from(stagingEl.querySelectorAll('svg.yemeni-ministry-sheet-svg'))
          if (!realOmrElements.length) {
            realOmrElements = Array.from(stagingEl.querySelectorAll('svg'))
          }
        }
        stagingEl.classList.add('d-none')
      }
    }

    // 3. التحقق من الحالات المحددة بدقة كاملة وفق ما يحدده المستخدم فقط:
    // أ) إذا اختار المستخدم أوراق إجابة OMR فقط:
    if (options?.sheets && !options?.manifest && !options?.roster && !options?.booklets) {
      if (realOmrElements.length > 0) {
        await printOmrBatch(realOmrElements, {
          title: `أوراق_تظليل_${exam.uniqueCode || 'OMR'}_${selectedSheetLayout.value}`,
          isA5: selectedSheetLayout.value === 'compact_a5',
        })
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
  } finally {
    directPrintLoading.value = false
    printingBatch.value = false
  }
}

const executeDirectPrint = async (payload) => {
  const exam = payload?.exam || targetExamForDirectPrint.value
  const actualCount = Number(payload?.actualPrintedCount ?? (exam?.total_registered || exam?.total_students || 0))
  const totalCount = exam?.total_registered || exam?.total_students || 0
  const chosenOptions = payload?.options || directPrintOptions.value
  const notes = payload?.notes || ''

  if (!exam) return
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
    const batchId = `BATCH_DIRECT_${Date.now()}`

    // 1. Call mark-printed on real backend database with the verified count
    await api.post(`/api/omr/exam-linking/${exam.id}/mark-printed/`, {
      batch_id: batchId,
      student_ids: actualCount >= totalCount ? 'all' : undefined,
      notes: notes,
    })

    // 2. Update state reflecting whether it's fully or partially printed
    exam.printed_count = actualCount
    exam.printed_rate = Math.round((actualCount / (totalCount || 1)) * 100)
    if (actualCount >= totalCount) {
      exam.print_status = 'full'
      exam.is_completed = true
      exam.is_due = false
      examSubTab.value = 'completed'
    } else {
      exam.print_status = 'partial'
      exam.is_completed = false
      exam.is_due = true
    }

    // 3. Reload persistent state from backend
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
      message: actualCount >= totalCount 
        ? `تمت مصادقة إتمام الطباعة بنجاح للاختبار "${exam.title}"! تم توثيق الدفعة برقم (${batchId}) لعدد ${actualCount} ورقة بنسبة 100%.`
        : `تم توثيق السحب الجزئي بنجاح للاختبار "${exam.title}"! تم قيد ${actualCount} ورقة وتبقى ${totalCount - actualCount} ورقة في قائمة المستحقة.`,
    }
  } catch (err) {
    console.error('Direct print error:', err)
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

const allExamsList = computed(() => enrichedMasterExamsList.value || [])
const pendingAndActiveOrdersList = computed(() => (enrichedMasterExamsList.value || []).filter(e => !e.is_completed && !e.is_cancelled && e.order_status !== 'cancelled'))
const scheduledExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_scheduled))
const dueExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_due))
const completedExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_completed))
const cancelledExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.order_status === 'cancelled' || e.raw_order_status === 'cancelled' || e.is_cancelled))

const allExamsCount = computed(() => allExamsList.value.length)
const pendingAndActiveOrdersCount = computed(() => pendingAndActiveOrdersList.value.length)
const scheduledExamsCount = computed(() => scheduledExamsList.value.length)
const dueExamsCount = computed(() => dueExamsList.value.length)
const completedExamsCount = computed(() => completedExamsList.value.length)
const cancelledExamsCount = computed(() => cancelledExamsList.value.length)

const currentExamSubTabList = computed(() => {
  if (examSubTab.value === 'orders') return pendingAndActiveOrdersList.value
  if (examSubTab.value === 'scheduled') return scheduledExamsList.value
  if (examSubTab.value === 'due') return dueExamsList.value
  if (examSubTab.value === 'completed') return completedExamsList.value
  if (examSubTab.value === 'cancelled') return cancelledExamsList.value
  return allExamsList.value
})

const examMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const examMasterSearchTerm = ref('')

const getExamMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  if (p.search !== undefined) {
    examMasterSearchTerm.value = (p.search || '').trim().toLowerCase()
  }
  const page = p.page || 1
  const pageSize = p.page_size || 20
  let all = currentExamSubTabList.value || []

  if (examMasterSearchTerm.value) {
    const q = examMasterSearchTerm.value
    all = all.filter(e => 
      (e.title && e.title.toLowerCase().includes(q)) ||
      (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
      (e.subject_name && e.subject_name.toLowerCase().includes(q)) ||
      (e.order_number && e.order_number.toLowerCase().includes(q)) ||
      (e.institution_name && e.institution_name.toLowerCase().includes(q)) ||
      (e.directorate_name && e.directorate_name.toLowerCase().includes(q)) ||
      (e.governorate_name && e.governorate_name.toLowerCase().includes(q))
    )
  }

  const start = (page - 1) * pageSize
  examMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return examMasterTableItems.value
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

watch([currentExamSubTabList, examSubTab], () => {
  getExamMasterData()
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

// Master Methods
const loadSubjects = async () => {
  try {
    const res = await gradebookAPI.getSubjects()
    subjectsList.value = res.data?.results || []
  } catch (err) {
    console.error('Failed to load subjects:', err)
  }
}

const loadMasterData = async () => {
  loadingMaster.value = true
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
        ? gradebookAPI.getByOffice(baseParams).catch(() => ({ data: { results: [] } }))
        : Promise.resolve({ data: { results: allOfficesList.value } }),
      gradebookAPI.getByOffice(officeParams).catch(() => ({ data: { results: [] } })),
      gradebookAPI.getByDirectorate(dirParams).catch(() => ({ data: { results: [] } })),
      gradebookAPI.getBySchool(schoolParams).catch(() => ({ data: { results: [] } })),
      gradebookAPI.list(schoolParams).catch(() => ({ data: { results: [] } }))
    ])
    if (!allOfficesList.value || !allOfficesList.value.length) {
      allOfficesList.value = allOfficesRes.data?.results || []
    }
    officesList.value = officesRes.data?.results || []
    directoratesList.value = directoratesRes.data?.results || []
    schoolsList.value = schoolsRes.data?.results || []
    masterExamsList.value = examsRes.data?.results || []
    await loadSavedPrintOrders()
    getOfficeMasterData()
    getDirectorateMasterData()
    getSchoolMasterData()
    getExamMasterData()
    getBatchMasterData()
  } catch (err) {
    console.error('Failed to load master data:', err)
  } finally {
    loadingMaster.value = false
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
  filterInstitutionType.value = val
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
  selectedSchoolName.value = school.name
  if (school.directorate_name) selectedDirectorateName.value = school.directorate_name
  if (school.governorate_name) selectedOfficeName.value = school.governorate_name
  currentView.value = 'detail'
  await fetchExamsList({ school_id: school.id })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { school_id: school.id })
  }
}

const openDirectorateStudio = async (dir) => {
  selectedDirectorateId.value = dir.id
  selectedDirectorateName.value = dir.name
  if (dir.office_name) selectedOfficeName.value = dir.office_name
  currentView.value = 'detail'
  await fetchExamsList({ directorate_id: dir.id })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { directorate_id: dir.id })
  }
}

const openOfficeStudio = async (office) => {
  selectedOfficeId.value = office.id
  selectedOfficeName.value = office.office_name
  currentView.value = 'detail'
  await fetchExamsList({ office_id: office.id })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { office_id: office.id })
  }
}

const openExamStudio = async (exam) => {
  selectedExamId.value = exam.id
  currentView.value = 'detail'
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
  const base = examsList.value.find(e => e.id === selectedExamId.value) || {}
  const detailed = examDetails.value?.exam || {}
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
const batchPrintNotification = ref({ show: false, message: '', color: 'success' })

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

const toggleStudentPrintedStatus = (st) => {
  st.is_printed = !st.is_printed
  if (st.is_printed) {
    st.printed_at = new Date().toLocaleTimeString('ar-YE')
  }
  if (selectedExamId.value) {
    api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
      student_ids: [st.id],
      is_printed: st.is_printed
    }).catch(e => console.error("Toggle print status error:", e))
  }
}

const markSelectedAsPrinted = () => {
  if (!selectedStudentIds.value.length) return
  const idSet = new Set(selectedStudentIds.value)
  const targetIds = []
  ;(examDetails.value?.registered_students || []).forEach(st => {
    if (idSet.has(st.id)) {
      st.is_printed = true
      st.printed_at = new Date().toLocaleTimeString('ar-YE')
      targetIds.push(st.id)
    }
  })
  if (selectedExamId.value && targetIds.length) {
    api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
      student_ids: targetIds,
      is_printed: true
    }).catch(e => console.error("Mark printed error:", e))
  }
  batchPrintNotification.value = {
    show: true,
    color: 'success',
    message: `تم تحديد ${targetIds.length} طالب كمطبوع وتحديث السجل بنجاح.`
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
      st.is_printed = true
      st.printed_at = new Date().toLocaleTimeString('ar-YE')
      if (selectedExamId.value && st.id && !String(st.id).startsWith('blank_')) {
        api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
          student_ids: [st.id],
          is_printed: true
        }).catch(e => console.error(e))
      }
    }
  } else {
    window.print()
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
    school_name: customCenterName.value || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
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
  const center = customCenterName.value || exam.directorate || 'المركز الاختباري الرئيسي'
  const directorate = customDirectorate.value || exam.directorate || 'السبعين'
  const governorate = customGovernorate.value || exam.governorate || 'أمانة العاصمة'
  const examTitle = customStageTitle.value || exam.title || 'اختبار الشهادة الثانوية العامة'
  const yearName = customExamYear.value || exam.year_name || '1445هـ - 2024م'
  const subjectName = exam.subject_name || 'الرياضيات'

  let rowsHtml = ''
  students.forEach((st, idx) => {
    rowsHtml += `
      <tr>
        <td style="text-align: center; font-weight: bold;">${idx + 1}</td>
        <td style="text-align: center; font-family: monospace; font-weight: bold; font-size: 14px;">${st.seat_number || ''}</td>
        <td style="text-align: center; font-family: monospace;">${st.secret_number || ''}</td>
        <td style="font-weight: bold; padding-right: 8px;">${st.student_name || ''}</td>
        <td>${st.school_name || ''}</td>
        <td style="text-align: center; font-weight: bold;">النموذج ${st.model_code || 'A'}</td>
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
      <title>كشف تسليم واستلام الكنترول - ${exam.uniqueCode || ''}</title>
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
        <div>العام الدراسي: ${yearName} | إجمالي الطلاب: ${students.length}</div>
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
        <div>تاريخ التسليم: ${new Date().toLocaleDateString('ar-YE')}</div>
      </div>
    </body>
    </html>
  `

  const existingFrame = document.getElementById('roster-print-frame')
  if (existingFrame) existingFrame.remove()

  const iframe = document.createElement('iframe')
  iframe.id = 'roster-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
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
        window.print()
      }
    }, 250)
  } else {
    window.print()
  }
}

const printSelectedOrAllRoster = async () => {
  if (!targetBatchStudents.value.length) {
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
    let elements = []

    await nextTick()
    const stagingEl = document.getElementById('omr-registry-batch-staging')
    if (stagingEl) {
      stagingEl.classList.remove('d-none')
      await nextTick()
      if (isAudit) {
        elements = Array.from(stagingEl.querySelectorAll('.yemeni-audit-report-sheet'))
      } else {
        elements = Array.from(stagingEl.querySelectorAll('svg.yemeni-ministry-sheet-svg'))
        if (!elements.length) {
          elements = Array.from(stagingEl.querySelectorAll('svg'))
        }
      }
      stagingEl.classList.add('d-none')
    }

    if (elements.length > 0) {
      const batchId = `BATCH_${Date.now()}`
      await printOmrBatch(elements, {
        title: `كشف_أوراق_تظليل_${selectedExam.value?.uniqueCode || 'الاختبار'}_${selectedSheetLayout.value}`,
        isA5: selectedSheetLayout.value === 'compact_a5'
      })

      const targetStudentIds = targetBatchStudents.value.map(s => s.id)
      if (selectedExamId.value && targetStudentIds.length > 0) {
        targetStudentIds.forEach(id => {
          const st = examDetails.value?.registered_students?.find(s => s.id === id)
          if (st) {
            st.is_printed = true
            st.printed_at = new Date().toLocaleTimeString('ar-YE')
            st.print_batch = batchId
          }
        })

        api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
          student_ids: targetStudentIds,
          batch_id: batchId
        }).catch(e => console.error("Mark printed error:", e))

        fetchBatches()
      }

      batchPrintNotification.value = {
        show: true,
        color: 'success',
        message: `تم إرسال ${elements.length} ورقة تظليل إلى أمر الطباعة وتحديث سجل الدفعات بنجاح.`
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

  let all = batches.value || []
  if (searchQuery.value) {
    const q = searchQuery.value
    all = all.filter(b =>
      String(b.batch_id || '').toLowerCase().includes(q) ||
      String(b.exam_title || '').toLowerCase().includes(q) ||
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

watch(batches, () => {
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
const fetchExamsList = async (customParams = {}) => {
  loadingExams.value = true
  try {
    const params = {
      school_id: selectedSchoolId.value || undefined,
      directorate_id: selectedDirectorateId.value || undefined,
      office_id: selectedOfficeId.value || undefined,
      ...customParams,
    }
    const effType = getEffectiveInstitutionType()
    if (effType) {
      params.institution_type = effType
    }
    if (filterInstitutionType.value === 'school') {
      if (filterStage.value) params.stage = filterStage.value
      if (filterClassTrack.value) params.class_track = filterClassTrack.value
      if (filterSubject.value) params.subject = filterSubject.value
    } else if (filterInstitutionType.value === 'university') {
      if (filterCollege.value) params.college = filterCollege.value
      if (filterDepartment.value) params.department = filterDepartment.value
      if (filterSpecialization.value) params.specialization = filterSpecialization.value
      if (filterSemesterSubject.value) params.semester_subject = filterSemesterSubject.value
    } else if (filterInstitutionType.value === 'institute') {
      if (filterInstituteField.value) params.institute_field = filterInstituteField.value
      if (filterInstituteEducationSystem.value) params.institute_education_system = filterInstituteEducationSystem.value
      if (filterInstituteSpecialization.value) params.institute_specialization = filterInstituteSpecialization.value
      if (filterInstituteSubject.value) params.institute_subject = filterInstituteSubject.value
    } else {
      if (filterSubject.value) params.subject = filterSubject.value
    }

    const resp = await api.get('/api/omr/exam-linking/', { params })
    if (resp.data && resp.data.results) {
      examsList.value = resp.data.results
      if (selectedExamId.value && !examsList.value.some(e => e.id === selectedExamId.value)) {
        selectedExamId.value = null
        examDetails.value = null
      }
    }
  } catch (err) {
    console.error('Failed to load exams list:', err)
  } finally {
    loadingExams.value = false
  }
}

const loadExamDetails = async (examId, customParams = {}) => {
  if (!examId) return
  loadingExamDetails.value = true
  try {
    const params = {
      school_id: selectedSchoolId.value || undefined,
      directorate_id: selectedDirectorateId.value || undefined,
      office_id: selectedOfficeId.value || undefined,
      ...customParams,
    }
    const resp = await api.get(`/api/omr/exam-linking/${examId}/`, { params })
    examDetails.value = resp.data
    showHierarchyFilters.value = false
    if (resp.data.registered_students && resp.data.registered_students.length > 0) {
      selectedStudentId.value = resp.data.registered_students[0].id
      sheetGenerationMode.value = 'all_students'
    } else {
      sheetGenerationMode.value = 'blank'
    }
    await getRosterData()
    await getQuestionModelsData()
    await getPackageData()
  } catch (err) {
    console.error('Failed to load exam details:', err)
  } finally {
    loadingExamDetails.value = false
  }
}

const onExamSelected = (newId) => {
  if (newId) {
    loadExamDetails(newId)
  } else {
    examDetails.value = null
  }
}

const fetchBatches = async () => {
  loadingBatches.value = true
  try {
    const resp = await api.get('/api/omr/print-registry/', {
      params: { search: searchQuery.value }
    })
    if (resp.data && resp.data.success) {
      batches.value = resp.data.results
    }
  } catch (e) {
    console.error("Failed to load print batches", e)
  } finally {
    loadingBatches.value = false
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  fetchBatches()
}

const viewBatchDetails = async (batch) => {
  activeBatch.value = batch
  detailsDialog.value = true
  loadingDetails.value = true
  batchStudents.value = []
  try {
    const resp = await api.get(`/api/omr/print-registry/${batch.batch_id}/`)
    if (resp.data && resp.data.success) {
      batchStudents.value = resp.data.students
    }
  } catch (e) {
    console.error("Failed to load batch students", e)
  } finally {
    loadingDetails.value = false
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
    console.error('Failed to seed students:', err)
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

const printCurrentQuestionPaper = async () => {
  if (questionPaperRef.value) {
    const paperEl = questionPaperRef.value.querySelector('.yemeni-official-question-paper') || questionPaperRef.value
    await printOfficialQuestionPaper(paperEl, {
      title: `ورقة_أسئلة_${selectedExam.value?.subject_name || 'الاختبار'}_النموذج_${selectedQuestionsModelCode.value}`,
      isA3: selectedQuestionPaperLayout.value === 'a3'
    })
  } else {
    const verObj = selectedQuestionsVersionObj.value
    await printExamPackage({
      examTitle: customStageTitle.value || selectedExam.value?.title || 'اختبار الشهادة الثانوية العامة',
      subjectName: selectedExam.value?.subject_name || 'الرياضيات',
      stageName: selectedExam.value?.stage_name || '',
      yearName: customExamYear.value || selectedExam.value?.year_name || '1445هـ - 2024-2023م',
      governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
      directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
      centerName: customCenterName.value || activeSheetStudent.value?.school_name || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
      centerCode: activeSheetStudent.value?.school_id || selectedExam.value?.id || '3026',
      versionCode: selectedQuestionsModelCode.value,
      studentName: sheetGenerationMode.value === 'student' ? activeSheetStudent.value?.student_name : '',
      seatNumber: sheetGenerationMode.value === 'student' ? activeSheetStudent.value?.seat_number : '',
      secretNumber: sheetGenerationMode.value === 'student' ? activeSheetStudent.value?.secret_number : '60',
      isA3: selectedQuestionPaperLayout.value === 'a3',
      questions: verObj?.questions || [],
      mode: 'questions_only'
    })
  }
}

const printCurrentExamPackage = async () => {
  const st = activeSheetStudent.value
  const vCode = st?.model_code || selectedBlankVersionCode.value || selectedQuestionsModelCode.value || 'A'
  const verObj = examDetails.value?.versions?.find(ver => ver.versionCode === vCode) || examDetails.value?.versions?.[0]

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

  await printExamPackage({
    examTitle: customStageTitle.value || selectedExam.value?.title || 'اختبار الشهادة الثانوية العامة',
    subjectName: selectedExam.value?.subject_name || 'الرياضيات',
    stageName: selectedExam.value?.stage_name || '',
    yearName: customExamYear.value || selectedExam.value?.year_name || '1445هـ - 2024-2023م',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
    centerName: customCenterName.value || st?.school_name || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
    centerCode: st?.school_id || selectedExam.value?.id || '3026',
    versionCode: vCode,
    studentName: st?.student_name || '',
    seatNumber: st?.seat_number || '',
    secretNumber: st?.secret_number || '60',
    isA3: false,
    questions: verObj?.questions || [],
    omrElement: omrEl,
    mode: 'package',
    isA5: selectedSheetLayout.value === 'compact_a5'
  })
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
  const verObj = examDetails.value?.versions?.find(ver => ver.versionCode === modelCode) || examDetails.value?.versions?.[0]
  await printExamPackage({
    examTitle: customStageTitle.value || selectedExam.value?.title || 'اختبار الشهادة العامة',
    subjectName: selectedExam.value?.subject_name || 'الرياضيات',
    stageName: selectedExam.value?.stage_name || '',
    yearName: customExamYear.value || selectedExam.value?.year_name || '1446هـ - 2024-2025م',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
    centerName: customCenterName.value || selectedExam.value?.school_name || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
    centerCode: selectedExam.value?.id || '3026',
    versionCode: modelCode,
    studentName: '',
    seatNumber: '',
    secretNumber: '',
    isA3: selectedQuestionPaperLayout.value === 'a3',
    questions: verObj?.questions || [],
    mode: 'questions_only'
  })
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
  const vCode = student?.model_code || 'A'
  const verObj = examDetails.value?.versions?.find(ver => ver.versionCode === vCode) || examDetails.value?.versions?.[0]
  await printExamPackage({
    examTitle: customStageTitle.value || selectedExam.value?.title || 'اختبار الشهادة العامة',
    subjectName: selectedExam.value?.subject_name || 'الرياضيات',
    stageName: selectedExam.value?.stage_name || '',
    yearName: customExamYear.value || selectedExam.value?.year_name || '1446هـ - 2024-2025م',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
    centerName: customCenterName.value || student?.school_name || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
    centerCode: student?.school_id || selectedExam.value?.id || '3026',
    versionCode: vCode,
    studentName: student?.student_name || '',
    seatNumber: student?.seat_number || '',
    secretNumber: student?.secret_number || '60',
    isA3: false,
    questions: verObj?.questions || [],
    omrElement: null,
    mode: 'package',
    isA5: selectedSheetLayout.value === 'compact_a5'
  })
}

const batchPrintSelectedPackages = async () => {
  printingPackages.value = true
  try {
    const targets = selectedPackageStudentIds.value.length > 0
      ? filteredPackageStudents.value.filter(s => selectedPackageStudentIds.value.includes(s.id))
      : filteredPackageStudents.value
    for (const st of targets) {
      await printSingleStudentPackage(st)
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
    window.print()
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
