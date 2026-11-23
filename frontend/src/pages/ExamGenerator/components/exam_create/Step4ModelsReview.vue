<template>
  <div>
    <!-- Staging Loading Pulse -->
    <div v-if="stagingLoading" class="py-16 text-center">
      <v-progress-circular indeterminate color="primary" size="64" width="4" />
      <h3 class="text-h6 font-weight-black mt-4 text-high-emphasis">جاري تحضير المسودة التفاعلية لنماذج الاختبار...</h3>
      <p class="text-caption text-medium-emphasis mt-1">يتم سحب وتوزيع الأسئلة وفق محددات مصفوفة المعايير والمجموعات</p>
    </div>

    <div v-else-if="!stagedModels || stagedModels.length === 0" class="py-16 text-center">
      <v-icon size="64" color="warning" class="mb-3">mdi-alert-circle-outline</v-icon>
      <h3 class="text-h6 font-weight-bold">لم يتم تجهيز مسودة النماذج بعد</h3>
      <p class="text-caption text-medium-emphasis mb-4">يرجى الرجوع للخطوة السابقة وتأكيد الانتقال للمسودة التفاعلية</p>
      <v-btn color="primary" variant="tonal" class="font-weight-bold rounded-xl" @click="$emit('goToStep', 3)">
        العودة للمعاينة والتأكيد
      </v-btn>
    </div>

    <div v-else>
      <!-- Unified Command Hub -->
      <div class="staged-command-hub pa-4 rounded-2xl border mb-4 bg-surface">
        <!-- Top Row: Title, Badges & Master Action Buttons -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" size="42" rounded="xl">
              <v-icon size="22">mdi-file-document-edit-outline</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2 flex-wrap">
                <h2 class="text-subtitle-1 font-weight-black mb-0 text-high-emphasis">
                  استعراض وضبط أسئلة نماذج الاختبار
                </h2>
                <v-chip size="x-small" color="primary" variant="tonal" rounded="sm" class="staged-tag font-weight-bold">
                  مسودة تفاعلية ذكية
                </v-chip>
                <v-chip size="x-small" color="warning" variant="tonal" rounded="sm" class="staged-tag font-weight-bold">
                  لم يتم الحفظ في القاعدة بعد
                </v-chip>
              </div>
              <div class="text-caption text-medium-emphasis mt-0.5">
                يمكنك مراجعة وتدقيق الأسئلة، واستبدال أي سؤال فورياً أو من البنك، قبل الاعتماد والتوليد النهائي.
              </div>
            </div>
          </div>

          <!-- Master Action Buttons -->
          <div class="d-flex align-center gap-2 flex-wrap">
            <v-btn
              variant="tonal"
              color="secondary"
              size="small"
              rounded="lg"
              class="font-weight-bold px-3 text-caption"
              prepend-icon="mdi-refresh"
              :loading="stagingLoading"
              @click="$emit('prepareStagingAndProceed')"
            >
              إعادة توليد عشوائي
            </v-btn>
            <v-btn
              color="success"
              variant="flat"
              size="small"
              rounded="lg"
              class="font-weight-black px-4 text-caption shadow-success"
              prepend-icon="mdi-check-decagram"
              :loading="generating"
              @click="$emit('commitFinalExam')"
            >
              اعتماد وتوليد الاختبار النهائي
            </v-btn>
          </div>
        </div>

        <!-- Bottom Row: Model Selector Pills & Stats -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-3 pt-3">
          <!-- Model Switcher Tabs -->
          <div class="d-flex align-center gap-2 flex-wrap">
            <span class="text-caption font-weight-bold text-medium-emphasis me-1">النموذج:</span>
            <div
              v-for="(model, mIdx) in stagedModels"
              :key="mIdx"
              class="staged-model-tab"
              :class="{ 'is-active': activeStagedModelIndex === mIdx }"
              @click="$emit('update:activeStagedModelIndex', mIdx)"
            >
              <span class="staged-tab-badge">{{ model.versionCode }}</span>
              <span class="staged-tab-name">النموذج ({{ model.versionCode }})</span>
              <span class="staged-tab-count">{{ model.questions?.length || 0 }} سؤال</span>
            </div>
          </div>

          <!-- Right: Model Stats & Show Answers Switch -->
          <div class="d-flex align-center gap-3 flex-wrap">
            <div v-if="currentStagedModel" class="d-flex align-center gap-2 text-caption text-medium-emphasis">
              <span>الدرجات: <strong class="text-primary">{{ calculateStagedTotalMarks(currentStagedModel) }} / {{ totalMarks || 100 }}</strong></span>
              <span>&bull;</span>
              <span>الصعوبة: <strong class="text-on-surface">{{ difficultyLabel(currentStagedModel.difficulty_profile) }}</strong></span>
              <span>&bull;</span>
              <span>{{ currentStagedModel.questions_variation === 'different_questions' ? 'أسئلة مستقلة' : 'خلط وترتيب' }}</span>
            </div>

            <v-switch
              :model-value="showCorrectAnswers"
              color="success"
              hide-details
              density="compact"
              label="إظهار الإجابات الصحيحة"
              class="ma-0 pa-0 font-weight-bold text-caption"
              @update:model-value="$emit('update:showCorrectAnswers', $event)"
            />
          </div>
        </div>
      </div>

      <!-- Questions List for Current Staged Model -->
      <div v-if="currentStagedModel && currentStagedModel.questions" class="d-flex flex-column gap-3 mb-6">
        <div
          v-for="(q, qIdx) in currentStagedModel.questions"
          :key="q.id || qIdx"
          class="staged-question-card pa-4 rounded-xl border bg-surface"
        >
          <!-- Card Header Bar -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-2 pb-2 border-b">
            <!-- Number Badge, Type, Difficulty & Academic Context -->
            <div class="d-flex align-center gap-2 flex-wrap">
              <span class="q-number-badge">
                #{{ q.orderIndex || (qIdx + 1) }}
              </span>
              <v-chip size="x-small" color="primary" variant="tonal" rounded="sm" class="staged-tag font-weight-bold px-2">
                <v-icon start size="12">{{ questionTypeIcon(q.questionType) }}</v-icon>
                {{ questionTypeLabel(q.questionType) }}
              </v-chip>
              <v-chip size="x-small" :color="difficultyColor(q.difficulty)" variant="tonal" rounded="sm" class="staged-tag font-weight-bold px-2">
                {{ difficultyLabel(q.difficulty) }}
              </v-chip>
              <span v-if="q.unitName" class="text-caption text-medium-emphasis d-none d-sm-inline">
                &bull; {{ q.unitName }} {{ q.lessonName ? `• ${q.lessonName}` : '' }}
              </span>
            </div>

            <!-- Mark & Action Buttons -->
            <div class="d-flex align-center gap-1.5 flex-wrap">
              <span class="staged-mark-badge font-weight-black">
                {{ q.assignedMark }} {{ Number(q.assignedMark) === 1 ? 'درجة' : 'درجات' }}
              </span>

              <div class="d-flex align-center gap-1">
                <v-btn
                  size="x-small"
                  variant="tonal"
                  color="primary"
                  rounded="sm"
                  class="staged-action-btn font-weight-bold"
                  prepend-icon="mdi-swap-horizontal"
                  @click="$emit('quickAutoSwap', { question: q, modelIndex: activeStagedModelIndex })"
                >
                  استبدال فوري
                </v-btn>
                <v-btn
                  size="x-small"
                  variant="tonal"
                  color="secondary"
                  rounded="sm"
                  class="staged-action-btn font-weight-bold"
                  prepend-icon="mdi-database-search"
                  @click="$emit('openSwapDialog', { question: q, modelIndex: activeStagedModelIndex })"
                >
                  اختيار من البنك
                </v-btn>
                <v-btn
                  size="x-small"
                  variant="outlined"
                  color="medium-emphasis"
                  rounded="sm"
                  class="staged-action-btn font-weight-bold"
                  prepend-icon="mdi-plus"
                  @click="$emit('openQuickCreateDialog', { question: q, modelIndex: activeStagedModelIndex })"
                >
                  بديل جديد
                </v-btn>
              </div>
            </div>
          </div>

          <!-- Question Text Content -->
          <div class="text-body-1 font-weight-medium my-2 text-high-emphasis leading-relaxed" v-html="$sanitizeHtml(q.content)"></div>

          <!-- Optional Question Image -->
          <div v-if="q.image" class="my-2">
            <img :src="q.image" alt="Question Image" style="max-height: 180px; border-radius: 8px; border: 1px solid rgba(var(--v-theme-primary), 0.15);" />
          </div>

          <!-- Options Rendering -->
          <!-- 1. True / False Mode -->
          <div v-if="isTF(q.questionType)" class="d-flex align-center gap-2 mt-2 flex-wrap">
            <div
              class="tf-option-pill"
              :class="{
                'is-correct': showCorrectAnswers && isOptionTrue(q, 0),
                'is-neutral': !showCorrectAnswers || !isOptionTrue(q, 0)
              }"
            >
              <v-icon size="15" class="me-1.5" :color="showCorrectAnswers && isOptionTrue(q, 0) ? 'success' : 'medium-emphasis'">
                {{ showCorrectAnswers && isOptionTrue(q, 0) ? 'mdi-check-circle' : 'mdi-radiobox-blank' }}
              </v-icon>
              <span>صح / صواب</span>
              <span v-if="showCorrectAnswers && isOptionTrue(q, 0)" class="ms-1.5 text-caption font-weight-bold text-success">(صحيحة)</span>
            </div>

            <div
              class="tf-option-pill"
              :class="{
                'is-correct': showCorrectAnswers && isOptionTrue(q, 1),
                'is-neutral': !showCorrectAnswers || !isOptionTrue(q, 1)
              }"
            >
              <v-icon size="15" class="me-1.5" :color="showCorrectAnswers && isOptionTrue(q, 1) ? 'success' : 'medium-emphasis'">
                {{ showCorrectAnswers && isOptionTrue(q, 1) ? 'mdi-check-circle' : 'mdi-radiobox-blank' }}
              </v-icon>
              <span>خطأ</span>
              <span v-if="showCorrectAnswers && isOptionTrue(q, 1)" class="ms-1.5 text-caption font-weight-bold text-success">(صحيحة)</span>
            </div>
          </div>

          <!-- 2. Multiple Choice (MCQ) Mode -->
          <div v-else-if="q.options && q.options.length > 0" class="options-grid mt-2">
            <div
              v-for="(opt, optIdx) in q.options"
              :key="opt.id || optIdx"
              class="mcq-option-card"
              :class="{ 'is-correct': showCorrectAnswers && opt.isTrue, 'is-neutral': !showCorrectAnswers || !opt.isTrue }"
            >
              <div class="d-flex align-center gap-2 overflow-hidden">
                <span class="opt-letter-avatar" :class="{ 'is-correct': showCorrectAnswers && opt.isTrue }">
                  {{ arabicOptionLetter(optIdx) }}
                </span>
                <span class="text-body-2 font-weight-medium text-truncate" :title="opt.text">{{ opt.text }}</span>
              </div>
              <div v-if="showCorrectAnswers && opt.isTrue" class="d-flex align-center gap-1 text-success text-caption font-weight-bold flex-shrink-0">
                <v-icon size="14">mdi-check</v-icon>
                <span>صحيحة</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  difficultyColor,
  difficultyLabel,
  questionTypeLabel,
  questionTypeIcon,
  arabicOptionLetter,
  isTF,
  isOptionTrue,
  calculateStagedTotalMarks
} from '../../composables/examHelpers'

const props = defineProps({
  stagingLoading: {
    type: Boolean,
    default: false
  },
  generating: {
    type: Boolean,
    default: false
  },
  stagedModels: {
    type: Array,
    default: () => []
  },
  activeStagedModelIndex: {
    type: Number,
    default: 0
  },
  totalMarks: {
    type: [Number, String],
    default: 100
  },
  showCorrectAnswers: {
    type: Boolean,
    default: false
  }
})

defineEmits([
  'update:activeStagedModelIndex',
  'update:showCorrectAnswers',
  'prepareStagingAndProceed',
  'commitFinalExam',
  'goToStep',
  'quickAutoSwap',
  'openSwapDialog',
  'openQuickCreateDialog'
])

const currentStagedModel = computed(() => {
  if (!props.stagedModels || props.stagedModels.length === 0) return null
  return props.stagedModels[props.activeStagedModelIndex] || props.stagedModels[0]
})
</script>
