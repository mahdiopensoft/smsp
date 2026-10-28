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
        <!-- بيانات الطالب والورقة -->
        <div class="d-flex align-center gap-3 flex-wrap">
          <v-avatar color="primary" variant="tonal" size="44" rounded="xl">
            <v-icon size="26" color="primary">mdi-account-check-outline</v-icon>
          </v-avatar>

          <div>
            <div class="d-flex align-center gap-2">
              <span class="font-weight-black text-h6 text-primary">
                {{ activeReviewSheet.student_name || 'طالب اختبار' }}
              </span>
              <v-chip size="small" variant="tonal" color="indigo" class="font-weight-bold">
                جلوس: {{ activeReviewSheet.seat_number || 'غير مسجل' }}
              </v-chip>
              <v-chip size="small" variant="flat" color="primary" class="font-weight-bold">
                نموذج {{ activeReviewSheet.version_code || 'A' }}
              </v-chip>
            </div>
            <div class="text-caption text-medium-emphasis d-flex align-center gap-2 mt-0.5">
              <span>{{ activeReviewSheet.exam_title || 'الاختبار الأكاديمي الموحد' }}</span>
              <span v-if="activeReviewSheet.school_name">• {{ activeReviewSheet.school_name }}</span>
              <span>• معرف التسليم: #{{ activeReviewSheet.submission || activeReviewSheet.id }}</span>
            </div>
          </div>
        </div>

        <!-- أزرار التنقل والحفظ والتحكم بالشاشة -->
        <div class="d-flex align-center gap-2">
          <!-- الدرجة الحالية والمراجعة -->
          <div class="text-end me-3 d-none d-md-block">
            <div class="text-caption text-medium-emphasis">الدرجة المحتسبة</div>
            <div class="font-weight-black text-body-1 text-success">
              {{ activeReviewSheet.mcq_score ?? 0 }} / {{ activeReviewSheet.mcq_max_score ?? activeReviewSheet.total_questions ?? 0 }}
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
            color="success"
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
          <span v-if="activeReviewSheet.ambiguous_count > 0" class="text-warning font-weight-bold">
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
            color="success"
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

const enrichedQuestions = computed(() => {
  const rawQs = props.activeReviewSheet?.questions || []
  const total = props.activeReviewSheet?.total_questions || rawQs.length || 50
  return rawQs.map((q: any) => enrichQuestion({ ...q }, total))
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
</style>
