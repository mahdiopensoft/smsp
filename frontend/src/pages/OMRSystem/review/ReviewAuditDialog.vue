<template>
  <v-dialog
    :model-value="modelValue"
    max-width="1680px"
    persistent
    scrollable
    transition="dialog-bottom-transition"
    :fullscreen="isFullScreen"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <v-card class="rounded-2xl overflow-hidden main-card d-flex flex-column" style="height: 94vh; max-height: 96vh;" v-if="activeReviewSheet">
      <!-- ── رأس نافذة المراجعة والتدقيق ── -->
      <v-card-title class="d-flex align-center justify-space-between bg-surface px-5 py-3 border-b flex-wrap gap-2">
        <!-- بيانات الطالب والورقة المحدثة -->
        <div class="d-flex align-center gap-3 flex-wrap">
          <v-avatar
            color="primary"
            variant="tonal"
            size="46"
            rounded="lg"
            class="border"
          >
            <v-icon size="26" color="primary">
              {{ isStudentIdentified ? 'mdi-account-check-outline' : 'mdi-barcode-scan' }}
            </v-icon>
          </v-avatar>

          <div>
            <div class="d-flex align-center gap-2 flex-wrap">
              <span class="font-weight-black text-h6 text-high-emphasis">
                {{ activeReviewSheet.student_name || 'طالب غير محدد (تعذر قراءة الباركود)' }}
              </span>

              <!-- جلوس الطالب بتصميم الشارة الموحدة المستطيلة الزرقاء -->
              <div class="center-count-badge unified-badge-primary px-2.5 py-0.5 text-caption font-weight-bold d-inline-flex align-center gap-1">
                <v-icon size="14">mdi-numeric</v-icon>
                <span>جلوس:</span>
                <span class="font-mono">{{ activeReviewSheet.seat_number || 'غير مسجل' }}</span>
              </div>

              <!-- نموذج الاختبار بتصميم الشارة الموحدة المستطيلة الزرقاء -->
              <div class="center-count-badge unified-badge-primary px-2.5 py-0.5 text-caption font-weight-bold d-inline-flex align-center gap-1">
                <v-icon size="14">mdi-layers-outline</v-icon>
                <span>نموذج</span>
                <span class="font-mono">{{ activeReviewSheet.version_code || 'A' }}</span>
              </div>
            </div>

            <!-- السطر الفرعي للبيانات الأكاديمية بالأيقونات المؤسسية -->
            <div class="text-caption text-medium-emphasis d-flex align-center gap-2 mt-1 flex-wrap">
              <div class="d-flex align-center gap-1">
                <v-icon size="14" color="primary">mdi-book-education-outline</v-icon>
                <span class="font-weight-medium text-high-emphasis">{{ activeReviewSheet.exam_title || 'الاختبار الأكاديمي الموحد' }}</span>
              </div>
              <span v-if="activeReviewSheet.school_name" class="d-flex align-center gap-1">
                <span class="opacity-50">•</span>
                <v-icon size="14" color="medium-emphasis">mdi-school-outline</v-icon>
                <span>{{ activeReviewSheet.school_name }}</span>
              </span>
              <span class="d-flex align-center gap-1">
                <span class="opacity-50">•</span>
                <v-icon size="14" color="medium-emphasis">mdi-barcode-scan</v-icon>
                <span>معرف التسليم: <strong class="font-mono text-high-emphasis">#{{ activeReviewSheet.submission || activeReviewSheet.id }}</strong></span>
              </span>
            </div>
          </div>
        </div>

        <!-- أزرار التنقل والحفظ والتحكم بالشاشة -->
        <div class="d-flex align-center gap-2">
          <!-- بطاقة الدرجة المحتسبة بنمط مؤشرات KPI الموحد الأنيق -->
          <div class="px-3 py-1.5 rounded-lg border bg-surface-variant-subtle d-flex align-center gap-3 me-2">
            <div>
              <div class="text-caption text-medium-emphasis font-weight-medium" style="font-size: 11px !important;">الدرجة المحتسبة</div>
              <div class="d-flex align-baseline gap-1">
                <span class="font-weight-black text-h6 text-primary font-mono leading-none">
                  {{ currentScore.toFixed(2) }}
                </span>
                <span class="text-caption text-medium-emphasis font-mono">
                  / {{ Number(activeReviewSheet.mcq_max_score ?? activeReviewSheet.total_questions ?? 0).toFixed(2) }}
                </span>
              </div>
            </div>
            <div
              class="center-count-badge unified-badge-primary px-2 py-0.5 text-caption font-mono font-weight-bold"
              style="font-size: 11px !important;"
            >
              {{ Math.round((currentScore / (activeReviewSheet.mcq_max_score || activeReviewSheet.total_questions || 1)) * 100) }}%
            </div>
          </div>

          <!-- التنقل بين الأوراق السابقة والتالية -->
          <v-btn-group density="comfortable" rounded="lg" variant="outlined" class="me-2">
            <v-btn
              icon="mdi-chevron-right"
              :disabled="!hasPrevSheet"
              title="الورقة السابقة (K)"
              @click="$emit('prev-sheet')"
            />
            <v-btn
              icon="mdi-chevron-left"
              :disabled="!hasNextSheet"
              title="الورقة التالية (J)"
              @click="$emit('next-sheet')"
            />
          </v-btn-group>

          <!-- زر ملء الشاشة -->
          <v-btn
            :icon="isFullScreen ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'"
            variant="tonal"
            density="comfortable"
            title="تبديل وضع ملء الشاشة"
            @click="isFullScreen = !isFullScreen"
          />

          <!-- زر الاعتماد السريع -->
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            prepend-icon="mdi-check-decagram"
            :loading="approvingLoading"
            class="font-weight-bold"
            @click="$emit('approve-sheet', activeReviewSheet)"
          >
            اعتماد النتيجة
          </v-btn>

          <!-- زر إغلاق النافذة -->
          <v-btn
            icon="mdi-close"
            variant="text"
            density="comfortable"
            @click="$emit('update:modelValue', false)"
          />
        </div>
      </v-card-title>

      <!-- ── مساحة العرض المزدوج (Split-Screen) ── -->
      <v-card-text class="pa-3 bg-surface flex-grow-1 overflow-hidden">
        <div class="review-split-layout d-flex flex-column flex-md-row gap-3 h-100">
          <!-- العمود الأيمن / الأول: فاحص الورقة (صورة الماسح أو SVG التفاعلي) -->
          <div class="viewer-column flex-grow-1" style="flex-basis: 52%; min-width: 0;">
            <ReviewSheetViewer
              :active-review-sheet="activeReviewSheet"
              :selected-question="selectedQuestion"
            />
          </div>

          <!-- العمود الأيسر / الثاني: جدول الأسئلة والإجابات والتحكم -->
          <div class="table-column flex-grow-1" style="flex-basis: 48%; min-width: 0;">
            <ReviewQuestionsTable
              :questions="enrichedQuestions"
              :selected-question="selectedQuestion"
              :overriding-loading="overridingLoading"
              @select-question="onSelectQuestion"
              @override-choice="onOverrideChoice"
            />
          </div>
        </div>
      </v-card-text>

      <!-- ── ذيل النافذة (Footer Actions) ── -->
      <v-card-actions class="px-5 py-2.5 bg-surface border-t d-flex align-center justify-space-between flex-wrap gap-2">
        <div class="d-flex align-center gap-2 text-caption text-medium-emphasis">
          <v-icon size="16" color="primary">mdi-shield-check-outline</v-icon>
          <span>التدقيق الجنائي والرقابي موثق بنظام OMR Audit Log</span>
          <span v-if="activeReviewSheet.ambiguous_count > 0" class="text-primary font-weight-bold">
            • توجد {{ activeReviewSheet.ambiguous_count }} إجابات بحاجة لمراجعة
          </span>
        </div>

        <div class="d-flex align-center gap-2">
          <v-btn
            variant="text"
            color="secondary"
            rounded="lg"
            class="font-weight-bold"
            @click="$emit('update:modelValue', false)"
          >
            إغلاق
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            prepend-icon="mdi-check-all"
            :loading="approvingLoading"
            class="font-weight-bold px-5"
            @click="$emit('approve-sheet', activeReviewSheet)"
          >
            اعتماد ومصادقة
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import ReviewSheetViewer from './ReviewSheetViewer.vue'
import ReviewQuestionsTable from './ReviewQuestionsTable.vue'
import { enrichQuestion } from './reviewUtils'

const props = defineProps<{
  modelValue: boolean
  activeReviewSheet: any
  hasPrevSheet?: boolean
  hasNextSheet?: boolean
  approvingLoading?: boolean
  overridingLoading?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'prev-sheet'): void
  (e: 'next-sheet'): void
  (e: 'approve-sheet', sheet: any): void
  (e: 'override-question', payload: { question: any; choice: string }): void
}>()

const isFullScreen = ref(false)
const selectedQuestion = ref<any>(null)

const isStudentIdentified = computed(() => {
  const name = props.activeReviewSheet?.student_name || ''
  return Boolean(name && !name.includes('غير محدد') && !name.includes('تعذر'))
})

const hasValidSeat = computed(() => {
  const seat = props.activeReviewSheet?.seat_number
  return Boolean(seat && seat !== 'غير مسجل' && seat !== '—')
})

const enrichedQuestions = computed(() => {
  const rawQs = props.activeReviewSheet?.questions || []
  const total = props.activeReviewSheet?.total_questions || rawQs.length || 50
  return rawQs.map((q: any) => enrichQuestion({ ...q }, total))
})

const currentScore = computed(() => {
  if (enrichedQuestions.value && enrichedQuestions.value.length > 0) {
    const hasAnyCorrect = enrichedQuestions.value.some((q: any) => q.is_correct === true)
    if (hasAnyCorrect) {
      return enrichedQuestions.value.reduce((acc: number, q: any) => acc + (q.is_correct ? Number(q.marks_awarded || q.assigned_weight || 1.0) : 0), 0)
    }
  }
  return Number(props.activeReviewSheet?.mcq_score ?? 0)
})

watch(
  () => props.activeReviewSheet,
  (newSheet) => {
    if (newSheet && Array.isArray(newSheet.questions) && newSheet.questions.length > 0) {
      const qs = enrichedQuestions.value
      const ambiguous = qs.find((q: any) => q.bubble_state === 'ambiguous' || (q.final_confidence && q.final_confidence < 0.7))
      selectedQuestion.value = ambiguous || qs[0] || null
    } else {
      selectedQuestion.value = null
    }
  },
  { immediate: true }
)

function onSelectQuestion(q: any) {
  selectedQuestion.value = q
}

function onOverrideChoice(payload: { question: any; choice: string }) {
  emit('override-question', payload)
}
</script>

<style scoped>
.review-split-layout {
  height: calc(100% - 2px);
}
@media (max-width: 959px) {
  .review-split-layout {
    overflow-y: auto;
  }
}

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

.unified-badge-error {
  background: rgba(239, 68, 68, 0.12) !important;
  color: #dc2626 !important;
  border: 1px solid rgba(239, 68, 68, 0.25) !important;
}

.unified-badge-secondary {
  background: rgba(var(--v-theme-secondary), 0.12) !important;
  color: rgb(var(--v-theme-secondary)) !important;
  border: 1px solid rgba(var(--v-theme-secondary), 0.25) !important;
}
</style>
