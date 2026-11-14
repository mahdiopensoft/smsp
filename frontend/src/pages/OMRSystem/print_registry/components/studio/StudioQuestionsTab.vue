<template>
  <div class="questions-paper-viewport mb-6">
    <!-- شريط الإجراءات والمقاس الوزاري المعتمد -->
    <div class="main-card pa-3 px-4 rounded-2xl mb-4 bg-surface border elevation-1">
      <div class="d-flex align-center justify-space-between flex-wrap gap-2">
        <div class="d-flex align-center gap-2 flex-wrap">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-printer"
            @click="$emit('print-all')"
            :disabled="!questionModelsList.some(m => m.hasQuestions)"
          >
            طباعة كافة نماذج الأسئلة ({{ questionModelsList.map(m => m.versionCode).join(', ') }})
          </v-btn>

          <v-btn-toggle
            :model-value="selectedQuestionPaperLayout"
            @update:model-value="$emit('update:selectedQuestionPaperLayout', $event)"
            mandatory
            density="compact"
            color="secondary"
            variant="outlined"
            rounded="lg"
          >
            <v-btn value="a4" class="font-weight-bold px-3" prepend-icon="mdi-file-outline">
              A4 الوزاري القياسي
            </v-btn>
            <v-btn value="a3" class="font-weight-bold px-3" prepend-icon="mdi-file-document-outline">
              A3 عريض (عمودين)
            </v-btn>
          </v-btn-toggle>
        </div>

        <div class="d-flex align-center gap-2">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
            <v-icon start size="16">mdi-book-open-page-variant-outline</v-icon>
            كراسات الأسئلة المعتمدة (4 نماذج)
          </v-chip>
        </div>
      </div>
    </div>

    <!-- الجدول الموحد لكراسات النماذج الأربعة (custom-data-table) -->
    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <custom-data-table
        :items="questionModelsTableItems"
        :getData="getQuestionModelsData"
        :headers="questionModelsHeaders"
        :customLoading="loadingExamDetails"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :numbering="true"
        :showSelect="false"
        :actions="false"
        :search="false"
        class="bg-transparent"
      >
        <template v-slot:item-slot="{ item, key, index }">
          <template v-if="key === 'numbering'">
            <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
          </template>

          <!-- Model Code -->
          <template v-else-if="key === 'model_code'">
            <v-chip
              size="small"
              :color="getModelChipColor(item.versionCode)"
              variant="tonal"
              class="font-weight-black rounded-lg border px-3 font-mono"
            >
              نموذج {{ item.versionCode }}
            </v-chip>
          </template>

          <!-- Paper Title -->
          <template v-else-if="key === 'paper_title'">
            <div class="py-1">
              <div class="font-weight-bold text-body-2 text-on-surface">
                كراسة أسئلة مادة {{ selectedExam?.subject_name || 'الاختبار' }} - النموذج ({{ item.versionCode }})
              </div>
              <div class="text-caption text-medium-emphasis mt-0.5">
                {{ selectedExam?.title || 'اختبار معتمد' }} • {{ customExamYear || selectedExam?.year_name || 'العام الحالي' }}
              </div>
            </div>
          </template>

          <!-- Questions Count -->
          <template v-else-if="key === 'questions_count'">
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
              {{ item.questionsCount }} سؤال
            </v-chip>
          </template>

          <!-- Approved Layout -->
          <template v-else-if="key === 'layout_type'">
            <span class="text-caption font-weight-bold text-medium-emphasis">
              {{ selectedQuestionPaperLayout === 'a3' ? 'A3 عريض (عمودين)' : 'A4 الوزاري القياسي' }}
            </span>
          </template>

          <!-- Paper Status -->
          <template v-else-if="key === 'status'">
            <v-chip
              size="small"
              :color="item.hasQuestions ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold"
              :prepend-icon="item.hasQuestions ? 'mdi-check-decagram-outline' : 'mdi-alert-circle-outline'"
            >
              {{ item.hasQuestions ? 'معتمد وجاهز' : 'فارغ (لا توجد أسئلة)' }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-2">
              <v-btn
                size="small"
                color="secondary"
                variant="tonal"
                rounded="lg"
                class="font-weight-bold"
                prepend-icon="mdi-eye-outline"
                @click="openPreview(item.versionCode)"
              >
                معاينة
              </v-btn>
              <v-btn
                size="small"
                color="primary"
                variant="flat"
                rounded="lg"
                class="font-weight-bold"
                prepend-icon="mdi-printer"
                @click="$emit('print-model', item.versionCode)"
              >
                طباعة
              </v-btn>
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- نافذة حوار معاينة كراسة الأسئلة الرسمية المنبثقة -->
    <v-dialog v-model="previewDialog" max-width="960" scrollable>
      <v-card rounded="2xl" class="overflow-hidden">
        <v-toolbar color="surface" density="comfortable" class="border-b px-4">
          <div class="d-flex align-center gap-2">
            <v-avatar color="primary" variant="tonal" size="32" rounded="lg">
              <v-icon size="18">mdi-file-document-outline</v-icon>
            </v-avatar>
            <span class="text-subtitle-1 font-weight-black">
              معاينة كراسة الأسئلة الرسمية - نموذج {{ selectedModelCode }}
            </span>
            <v-chip size="small" :color="getModelChipColor(selectedModelCode)" variant="tonal" class="font-weight-bold ms-2">
              نموذج {{ selectedModelCode }}
            </v-chip>
          </div>
          <v-spacer />
          <v-btn
            color="primary"
            variant="flat"
            size="small"
            rounded="lg"
            class="font-weight-bold me-2"
            prepend-icon="mdi-printer"
            @click="$emit('print-current', selectedModelCode)"
          >
            طباعة الكراسة الآن
          </v-btn>
          <v-btn icon size="small" variant="text" @click="previewDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text class="pa-4 bg-grey-lighten-4 d-flex justify-center" style="max-height: 80vh;">
          <div ref="questionPaperRef" class="w-100 d-flex justify-center">
            <YemeniOfficialQuestionPaper
              :exam-title="customStageTitle || selectedExam?.title || ''"
              :exam-subject="selectedExam?.subject_name || ''"
              :stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || ''))"
              :exam-year="customExamYear || selectedExam?.year_name || ''"
              :governorate="customGovernorate || selectedExam?.governorate || ''"
              :directorate="customDirectorate || selectedExam?.directorate || ''"
              :center-name="customCenterName || activeSheetStudent?.school_name || selectedExam?.school_name || selectedExam?.center_name || 'المركز الامتحاني الرئيسي'"
              :center-code="activeSheetStudent?.school_id || selectedExam?.center_code || selectedExam?.id || '11'"
              :exam-time="selectedExam?.time_allowed || selectedExam?.exam_time || ''"
              :day-name="selectedExam?.day_name || ''"
              :exam-date="selectedExam?.exam_date || ''"
              :envelope-no="selectedExam?.envelope_no || '1'"
              :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.student_name || ''))"
              :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.seat_number || ''))"
              :secret-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.secret_number || ''))"
              :student-photo="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_photo || activeSheetStudent?.photo || '') : ''"
              :is-blank-mode="sheetGenerationMode === 'blank'"
              :model-code="selectedModelCode"
              :questions="selectedVersionQuestions"
              :default-layout="selectedQuestionPaperLayout"
            />
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'

const props = defineProps<{
  questionModelsList: any[]
  selectedQuestionPaperLayout: string
  questionModelsTableItems: any
  getQuestionModelsData: any
  questionModelsHeaders: any[]
  loadingExamDetails: boolean
  selectedExam: any
  customStageTitle?: string
  customExamYear?: string
  customGovernorate?: string
  customDirectorate?: string
  customCenterName?: string
  activeSheetStudent?: any
  sheetGenerationMode?: string
  examVersions?: any[]
  getModelChipColor: (code?: string) => string
}>()

const emit = defineEmits<{
  (e: 'update:selectedQuestionPaperLayout', val: string): void
  (e: 'print-all'): void
  (e: 'print-model', versionCode: string): void
  (e: 'print-current', versionCode: string): void
}>()

const previewDialog = ref(false)
const selectedModelCode = ref('A')
const questionPaperRef = ref<HTMLElement | null>(null)

const selectedVersionQuestions = computed(() => {
  if (!props.examVersions || props.examVersions.length === 0) return []
  const code = (selectedModelCode.value || 'A').trim().toUpperCase()
  const ver = props.examVersions.find(v => {
    const vCode = String(v.versionCode || v.model_code || v.version_code || v.code || '').trim().toUpperCase()
    return vCode === code
  }) || props.examVersions.find(v => {
    const vCode = String(v.versionCode || v.model_code || v.version_code || v.code || '').trim().toUpperCase()
    return vCode === 'A'
  }) || props.examVersions[0]
  return ver?.questions || []
})

const openPreview = (code: string) => {
  selectedModelCode.value = code
  previewDialog.value = true
}

defineExpose({
  questionPaperRef,
  openPreview
})
</script>
