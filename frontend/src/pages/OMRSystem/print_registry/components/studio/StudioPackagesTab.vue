<template>
  <div class="exam-package-viewport mb-6">
    <!-- شريط الإجراءات والبحث وفلاتر حزم الطلاب (منظم وموحد) -->
    <div class="main-card pa-3 px-4 rounded-2xl mb-4 bg-surface border elevation-1">
      <div class="d-flex align-center justify-space-between flex-wrap gap-2">
        <div class="d-flex align-center gap-2 flex-wrap">
          <v-btn
            color="success"
            variant="flat"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-printer"
            :loading="printingPackages"
            :disabled="!filteredPackageStudents.length"
            @click="$emit('batch-print-packages')"
          >
            طباعة حزم الاختبار {{ selectedPackageStudentIds.length > 0 ? `المحددة (${selectedPackageStudentIds.length})` : `للكل (${filteredPackageStudents.length})` }}
          </v-btn>

          <v-btn
            v-if="filteredPackageStudents.length > 0"
            size="small"
            variant="tonal"
            color="primary"
            class="font-weight-bold"
            prepend-icon="mdi-checkbox-multiple-marked-outline"
            @click="$emit('select-all-packages')"
          >
            {{ selectedPackageStudentIds.length === filteredPackageStudents.length ? 'إلغاء تحديد الكل' : 'تحديد كل المعروضين' }}
          </v-btn>
        </div>

        <!-- حقول التصفية والبحث عبر المكونات الموحدة -->
        <div class="d-flex align-center gap-2 flex-wrap">
          <div style="min-width: 190px; max-width: 230px;">
            <auto-list
              :model-value="packageModelFilter"
              @update:model-value="$emit('update:packageModelFilter', $event)"
              :objects="modelFilterObjects"
              name="ScreenTypeChoices"
              label="النموذج"
              placeholder="النموذج"
              cols="12"
              :add="false"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- الجدول الموحد لحزم الاختبار المتكاملة للطلاب (custom-data-table) -->
    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <custom-data-table
        :items="packageTableItems"
        :getData="getPackageData"
        :headers="packageHeaders"
        :customLoading="loadingExamDetails"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :numbering="true"
        :showSelect="false"
        :search="true"
        class="bg-transparent"
      
        :actionList="(item) => ([ { label: 'معاينة الحزمة المتكاملة', icon: 'eye-outline', color: 'primary', onClick: () => openPreview(item) }, { label: 'طباعة حزمة هذا الطالب', icon: 'printer', color: 'success', onClick: () => $emit('print-single-package', item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
        <template v-slot:item-slot="{ item, key, index }">
          <template v-if="key === 'numbering'">
            <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
          </template>

          <!-- Select Box -->
          <template v-else-if="key === 'select_box'">
            <div class="d-flex justify-center">
              <v-checkbox-btn
                :model-value="selectedPackageStudentIds.includes(item.id)"
                color="primary"
                density="compact"
                hide-details
                @update:model-value="$emit('toggle-package-select', item.id)"
              />
            </div>
          </template>

          <!-- Seat Number -->
          <template v-else-if="key === 'seat_number'">
            <span class="font-mono font-weight-black text-primary px-2 py-1 bg-blue-lighten-5 rounded-lg border">
              {{ item.seat_number }}
            </span>
          </template>

          <!-- Student Info -->
          <template v-else-if="key === 'student_name'">
            <div class="py-1">
              <div class="font-weight-bold text-body-2 text-on-surface">
                {{ item.student_name || 'طالب بدون اسم' }}
              </div>
              <div class="text-caption text-medium-emphasis mt-0.5">
                {{ item.school_name || selectedExam?.directorate || 'المركز الرئيسي' }}
              </div>
            </div>
          </template>

          <!-- School / Center -->
          <template v-else-if="key === 'school_name'">
            <div class="py-1">
              <div class="font-weight-medium text-body-2">{{ item.school_name || selectedExam?.directorate || 'المركز الرئيسي' }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.directorate || selectedExam?.directorate || '-' }}</div>
            </div>
          </template>

          <!-- Model Code -->
          <template v-else-if="key === 'model_code'">
            <span class="font-mono font-weight-bold text-body-2">نموذج {{ item.model_code || 'A' }}</span>
          </template>

          <!-- Package Contents -->
          <template v-else-if="key === 'package_contents'">
            <span class="text-caption font-weight-medium">
              كراسة أسئلة ({{ item.model_code || 'A' }}) + ورقة تظليل OMR
            </span>
          </template>

          <!-- Print Status -->
          <template v-else-if="key === 'is_printed'">
            <v-chip
              size="small"
              :color="item.is_printed ? 'success' : 'grey'"
              variant="tonal"
              class="font-weight-bold cursor-pointer"
              :title="item._updating ? 'جاري توثيق التحديث في السجل...' : 'انقر لتبديل حالة الطباعة'"
              :disabled="item._updating"
              @click="$emit('toggle-printed', item)"
            >
              <v-progress-circular v-if="item._updating" indeterminate size="12" width="2" class="me-1" />
              {{ item._updating ? 'جاري التحديث...' : (item.is_printed ? 'تمت الطباعة' : 'جاهز للطباعة') }}
            </v-chip>
          </template>

          <!-- Actions -->
          
        </template>
      </custom-data-table>
    </div>

    <!-- نافذة حوار معاينة حزمة الاختبار المتكاملة للطلاب المنبثقة -->
    <custom-dialog
      v-model="previewPackageDialog"
      :title="`معاينة حزمة الاختبار للطالب: ${previewPackageStudent?.student_name || ''}`"
      width="960"
      height="88vh"
    >
      <div v-if="previewPackageStudent">
        <div class="d-flex align-center justify-space-between pb-3 mb-4 border-b flex-wrap gap-2">
          <v-chip size="small" :color="getModelChipColor(previewPackageStudent.model_code)" variant="tonal" class="font-weight-bold">
            نموذج {{ previewPackageStudent.model_code || 'A' }}
          </v-chip>
          <v-btn
            color="success"
            variant="flat"
            size="small"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-printer"
            @click="$emit('print-single-package', previewPackageStudent)"
          >
            طباعة حزمة الطالب
          </v-btn>
        </div>

        <div class="pa-4 bg-grey-lighten-4 rounded-xl">
          <div class="d-flex flex-column align-center gap-6">
            <div class="text-caption font-weight-black text-primary border-b pb-1 w-100 text-center d-flex align-center justify-center gap-1">
              <v-icon size="16" color="primary">mdi-file-document-outline</v-icon>
              <span>الجزء 1: كراسة ورقة الأسئلة الرسمية المعتمدة (نموذج {{ previewPackageStudent.model_code || 'A' }})</span>
            </div>
            <YemeniOfficialQuestionPaper
              :exam-title="customStageTitle || selectedExam?.title || ''"
              :exam-subject="selectedExam?.subject_name || ''"
              :stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || ''))"
              :exam-year="customExamYear || selectedExam?.year_name || ''"
              :governorate="customGovernorate || selectedExam?.governorate || ''"
              :directorate="customDirectorate || selectedExam?.directorate || ''"
              :center-name="customCenterName || previewPackageStudent.school_name || selectedExam?.school_name || selectedExam?.center_name || 'المركز الامتحاني الرئيسي'"
              :center-code="previewPackageStudent.school_id || selectedExam?.center_code || selectedExam?.id || '11'"
              :exam-time="selectedExam?.time_allowed || selectedExam?.exam_time || ''"
              :day-name="selectedExam?.day_name || ''"
              :exam-date="selectedExam?.exam_date || ''"
              :envelope-no="selectedExam?.envelope_no || '1'"
              :student-name="previewPackageStudent.student_name"
              :seat-number="previewPackageStudent.seat_number"
              :secret-number="previewPackageStudent.secret_number || '60'"
              :model-code="previewPackageStudent.model_code || 'A'"
              :questions="examDetails?.versions?.find((v: any) => v.versionCode === (previewPackageStudent.model_code || 'A'))?.questions || []"
              :default-layout="'a4'"
            />

            <div class="text-caption font-weight-black text-teal border-b pb-1 w-100 text-center mt-4 d-flex align-center justify-center gap-1">
              <v-icon size="16" color="teal">mdi-checkbox-marked-circle-outline</v-icon>
              <span>الجزء 2: ورقة التظليل الإلكترونية OMR المخصصة للطالب</span>
            </div>
            <div class="sheet-page-card elevation-4 bg-white rounded-lg position-relative d-inline-block text-start" :style="sheetArtboardStyle">
              <YemeniMinistrySheet
                layout-mode="compact_a5"
                :student-name="previewPackageStudent.student_name"
                :seat-number="previewPackageStudent.seat_number"
                :serial-number="previewPackageStudent.secret_number || previewPackageStudent.model_code"
                :model-code="previewPackageStudent.model_code || 'A'"
                :exam-subject="selectedExam?.subject_name || ''"
                :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار'))"
                :exam-year="customExamYear || selectedExam?.year_name || ''"
                :center-name="customCenterName || previewPackageStudent.school_name || selectedExam?.center_name || selectedExam?.school_name || selectedExam?.directorate || ''"
                :governorate="customGovernorate || selectedExam?.governorate || ''"
                :directorate="customDirectorate || previewPackageStudent.directorate || selectedExam?.directorate || ''"
                :barcode-value="`EXAM_${selectedExam?.id}_VER_${previewPackageStudent.model_code || 'A'}_SEAT_${previewPackageStudent.seat_number}`"
                :qr-value="`${selectedExam?.uniqueCode}|${previewPackageStudent.model_code || 'A'}|${previewPackageStudent.seat_number}`"
                :field-layout="examFieldLayout"
                :institution-type="previewPackageStudent.institution_type || selectedExam?.institution_type || institutionType || 'school'"
                :college-name="previewPackageStudent.college_name || selectedExam?.college_name || ''"
                :major-name="previewPackageStudent.major_name || selectedExam?.major_name || ''"
                :academic-year="previewPackageStudent.academic_year || selectedExam?.academic_year || ''"
                :semester-name="previewPackageStudent.semester_name || selectedExam?.semester_name || ''"
                :course-name="previewPackageStudent.course_name || selectedExam?.subject_name || ''"
                :course-code="previewPackageStudent.course_code || selectedExam?.subject_code || ''"
                :student-level="previewPackageStudent.student_level || selectedExam?.stage_name || ''"
                :group-section="previewPackageStudent.group_section || ''"
                :term-name="previewPackageStudent.term_name || ''"
                :student-id="previewPackageStudent.seat_number"
                :is-preview="true"
              />
            </div>
          </div>
        </div>
      </div>
    </custom-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'

defineProps<{
  printingPackages: boolean
  filteredPackageStudents: any[]
  selectedPackageStudentIds: any[]
  packageModelFilter: string
  modelFilterObjects: any[]
  packageTableItems: any
  getPackageData: any
  packageHeaders: any[]
  loadingExamDetails: boolean
  selectedExam: any
  examDetails: any
  customStageTitle?: string
  customExamYear?: string
  customGovernorate?: string
  customDirectorate?: string
  customCenterName?: string
  sheetArtboardStyle?: any
  examFieldLayout?: any
  institutionType?: string
  getModelChipColor: (code?: string) => string
}>()

defineEmits<{
  (e: 'update:packageModelFilter', val: string): void
  (e: 'batch-print-packages'): void
  (e: 'select-all-packages'): void
  (e: 'toggle-package-select', id: any): void
  (e: 'toggle-printed', item: any): void
  (e: 'print-single-package', item: any): void
}>()

const previewPackageDialog = ref(false)
const previewPackageStudent = ref<any>(null)

const openPreview = (item: any) => {
  previewPackageStudent.value = item
  previewPackageDialog.value = true
}

defineExpose({
  openPreview
})
</script>
