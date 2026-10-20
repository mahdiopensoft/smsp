<template>
  <div class="exam-booklet-tab">
    <!-- Header Control Bar for Booklet -->
    <div class="main-card rounded-2xl pa-4 mb-4 border d-flex align-center justify-space-between flex-wrap gap-3 bg-white">
      <div class="d-flex align-center gap-3 flex-wrap">
        <div class="text-caption font-weight-black text-primary d-flex align-center gap-1">
          <v-icon size="18">mdi-format-list-bulleted-type</v-icon>
          اختيار النموذج:
        </div>
        <v-btn-toggle
          :model-value="activeVersionTab"
          mandatory
          density="compact"
          color="primary"
          variant="outlined"
          rounded="lg"
          @update:model-value="(val) => $emit('update:activeVersionTab', val)"
        >
          <v-btn
            v-for="(v, idx) in (examDetails?.versions || [])"
            :key="`tab-qp-${v.id || idx}`"
            :value="idx"
            class="font-weight-bold px-3"
          >
            النموذج {{ v.versionCode }} ({{ v.questions?.length || v.questionsCount || 0 }} سؤال)
          </v-btn>
        </v-btn-toggle>

        <v-btn-toggle
          v-model="selectedQuestionPaperLayout"
          mandatory
          density="compact"
          color="secondary"
          variant="outlined"
          rounded="lg"
        >
          <v-btn value="a4" class="font-weight-bold px-3" prepend-icon="mdi-file-outline">
            مقاس A4 (النمط الوزاري المعتمد)
          </v-btn>
          <v-btn value="a3" class="font-weight-bold px-3" prepend-icon="mdi-file-document-outline">
            مقاس كبير A3 (ورقة واحدة عمودين)
          </v-btn>
        </v-btn-toggle>
      </div>

      <div class="d-flex align-center gap-2">
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-black px-5"
          prepend-icon="mdi-printer"
          @click="() => printQuestionsAndSheets('questions_only')"
        >
          طباعة ورقة الأسئلة الرسمية
        </v-btn>
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold px-4"
          prepend-icon="mdi-package-variant-closed"
          @click="() => printQuestionsAndSheets('package')"
        >
          طباعة الحزمة المتكاملة (أسئلة + تظليل)
        </v-btn>
      </div>
    </div>

    <!-- Official Question Paper Component Frame -->
    <div class="overflow-auto bg-grey-lighten-4 pa-4 rounded-2xl border d-flex justify-center mb-6">
      <YemeniOfficialQuestionPaper
        :exam-title="customStageTitle || activeExam?.title || ''"
        :exam-subject="activeExam?.subject_name || ''"
        :stage-title="customStageTitle || (activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || ''))"
        :exam-year="customExamYear || activeExam?.year_name || ''"
        :governorate="customGovernorate || activeExam?.governorate || ''"
        :directorate="customDirectorate || activeExam?.directorate || ''"
        :center-name="customCenterName || activeSheetStudent?.school_name || ''"
        :center-code="activeSheetStudent?.school_id || activeExam?.id || ''"
        :exam-time="activeExam?.time_allowed || activeExam?.exam_time || ''"
        :day-name="activeExam?.day_name || ''"
        :exam-date="activeExam?.exam_date || ''"
        :envelope-no="activeExam?.envelope_no || ''"
        :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.student_name || ''))"
        :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.seat_number || ''))"
        :secret-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.secret_number || ''))"
        :student-photo="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_photo || activeSheetStudent?.photo || '') : ''"
        :is-blank-mode="sheetGenerationMode === 'blank'"
        :model-code="currentVersionObj?.versionCode || 'A'"
        :questions="currentVersionObj?.questions || []"
        :default-layout="selectedQuestionPaperLayout"
      />
    </div>

    <!-- ── Official Question Paper (A3 Large Sheet) Preview Modal ── -->
    <v-dialog v-model="showQuestionPaperDialog" max-width="1340" scrollable>
      <v-card class="pa-4 rounded-2xl">
        <div class="d-flex align-center justify-space-between pb-3 border-b mb-3">
          <div class="d-flex align-center gap-2">
            <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-newspaper-variant-outline</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-subtitle-1 font-weight-black mb-0">معاينة ورقة الأسئلة الرسمية المعتمدة (النمط الوزاري الموحد A4)</h3>
              <span class="text-caption text-medium-emphasis">مطابقة تماماً للنسخة الرسمية الوزارية الصادرة عن لجنة المطبعة السرية المركزية</span>
            </div>
          </div>
          <v-btn icon size="small" variant="text" @click="showQuestionPaperDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <div class="overflow-auto bg-grey-lighten-4 pa-4 rounded-xl d-flex justify-center" style="max-height: 80vh;">
          <YemeniOfficialQuestionPaper
            :exam-title="activeExam?.title || ''"
            :exam-subject="activeExam?.subject_name || ''"
            :stage-title="activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || '')"
            :exam-year="activeExam?.year_name || ''"
            :governorate="activeExam?.governorate || ''"
            :directorate="activeExam?.directorate || ''"
            :center-name="activeSheetStudent?.school_name || ''"
            :center-code="activeSheetStudent?.school_id || activeExam?.id || ''"
            :exam-time="activeExam?.time_allowed || activeExam?.exam_time || ''"
            :day-name="activeExam?.day_name || ''"
            :exam-date="activeExam?.exam_date || ''"
            :envelope-no="activeExam?.envelope_no || ''"
            :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.student_name || ''))"
            :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.seat_number || ''))"
            :secret-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.secret_number || ''))"
            :student-photo="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_photo || activeSheetStudent?.photo || '') : ''"
            :is-blank-mode="sheetGenerationMode === 'blank'"
            :model-code="currentVersionObj?.versionCode || '1'"
            :questions="currentVersionObj?.questions || []"
            :default-layout="'a4'"
          />
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'
import { printExamPackage } from '../utils/omrPrint'

const props = defineProps({
  activeExam: { type: Object, default: () => ({}) },
  examDetails: { type: Object, default: () => ({}) },
  activeVersionTab: { type: Number, default: 0 },
  sheetGenerationMode: { type: String, default: 'all_students' },
  activeSheetStudent: { type: Object, default: null },
  customStageTitle: { type: String, default: '' },
  customExamYear: { type: String, default: '' },
  customCenterName: { type: String, default: '' },
  customGovernorate: { type: String, default: '' },
  customDirectorate: { type: String, default: '' },
  selectedSheetLayout: { type: String, default: 'compact_a5' },
  getOmrElement: { type: Function, default: null },
})

const emit = defineEmits(['update:activeVersionTab'])

const selectedQuestionPaperLayout = ref('a4')
const showQuestionPaperDialog = ref(false)

const currentVersionObj = computed(() => {
  if (!props.examDetails?.versions?.length) return null
  return props.examDetails.versions[props.activeVersionTab] || props.examDetails.versions[0]
})

const printQuestionsAndSheets = async (mode = 'package') => {
  await nextTick()
  const targetVersion = currentVersionObj.value || props.examDetails?.versions?.[0]

  if (!targetVersion || !targetVersion.questions || !targetVersion.questions.length) {
    console.warn('No questions found to print.')
    return
  }

  const activeVCode = targetVersion.versionCode || 'A'

  await printExamPackage({
    title: mode === 'package'
      ? `حزمة_اختبار_${props.activeExam?.subject_name || 'الاختبار'}_النموذج_${activeVCode}`
      : `كراسة_أسئلة_${props.activeExam?.subject_name || 'الاختبار'}_النموذج_${activeVCode}`,
    examTitle: props.activeExam?.title || '',
    subjectName: props.activeExam?.subject_name || '',
    stageName: props.activeExam?.stage_name ? `اختبار ${props.activeExam.stage_name}` : '',
    yearName: (props.activeExam?.year_name && String(props.activeExam.year_name).length > 2 && props.activeExam.year_name !== '1') ? props.activeExam.year_name : '',
    governorate: props.activeExam?.governorate || '',
    directorate: props.activeExam?.directorate || '',
    centerName: props.activeSheetStudent?.school_name || props.activeExam?.directorate || '',
    centerCode: props.activeSheetStudent?.school_id || props.activeExam?.id || '',
    dayName: props.activeExam?.day_name || '',
    examDate: props.activeExam?.exam_date || '',
    envelopeNo: props.activeExam?.envelope_no || '1',
    timeAllowed: props.activeExam?.time_allowed || '',
    versionCode: activeVCode,
    studentName: props.sheetGenerationMode === 'student' ? props.activeSheetStudent?.student_name : '',
    seatNumber: props.sheetGenerationMode === 'student' ? props.activeSheetStudent?.seat_number : '',
    secretNumber: props.sheetGenerationMode === 'student' ? (props.activeSheetStudent?.secret_number || '') : '',
    studentPhoto: props.sheetGenerationMode === 'student' ? (props.activeSheetStudent?.student_photo || '') : '',
    schoolName: props.activeSheetStudent?.school_name || props.activeExam?.directorate || '',
    institutionType: props.activeExam?.institution_type || 'school',
    questions: targetVersion.questions,
    omrElement: props.getOmrElement ? props.getOmrElement() : null,
    mode: mode,
    isA3: selectedQuestionPaperLayout.value === 'a3',
    isA5: props.selectedSheetLayout === 'compact_a5'
  })
}

defineExpose({
  openQuestionPaperModal: () => { showQuestionPaperDialog.value = true },
  printQuestionsAndSheets,
})
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
</style>
