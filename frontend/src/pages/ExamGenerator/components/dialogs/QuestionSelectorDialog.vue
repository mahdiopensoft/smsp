<template>
  <CustomDialog
    :model-value="modelValue"
    width="920"
    title="اختيار سؤال بديل من بنك الأسئلة"
    subTitle="استعراض الأسئلة المعتمدة المتاحة كبدائل متوافقة مع معايير الاختبار"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div v-if="targetSwapQuestion" class="pa-2">
      <!-- Target Question Summary Card -->
      <div class="swap-target-box mb-4">
        <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-2 border-b">
          <div class="d-flex align-center gap-2 flex-wrap">
            <span class="q-number-badge">
              #{{ targetSwapQuestion.orderIndex }}
            </span>
            <v-chip size="x-small" color="primary" variant="tonal" rounded="sm" class="staged-tag font-weight-bold px-2.5">
              <v-icon start size="12">{{ questionTypeIcon(targetSwapQuestion.questionType) }}</v-icon>
              {{ questionTypeLabel(targetSwapQuestion.questionType) }}
            </v-chip>
            <v-chip size="x-small" :color="difficultyColor(targetSwapQuestion.difficulty)" variant="tonal" rounded="sm" class="staged-tag font-weight-bold px-2.5">
              {{ difficultyLabel(targetSwapQuestion.difficulty) }}
            </v-chip>
            <span class="staged-mark-badge font-weight-black">
              {{ targetSwapQuestion.assignedMark }} {{ Number(targetSwapQuestion.assignedMark) === 1 ? 'درجة' : 'درجات' }}
            </span>
          </div>

          <div v-if="!swapLoading" class="text-caption font-weight-bold text-success d-flex align-center gap-1">
            <v-icon size="14" color="success">mdi-check-decagram</v-icon>
            <span>{{ swapCandidates.length }} سؤال بديل متاح</span>
          </div>
        </div>

        <div class="text-caption text-medium-emphasis mt-2 d-flex align-center gap-2 flex-wrap">
          <div class="d-flex align-center gap-1">
            <v-icon size="14" color="medium-emphasis">mdi-folder-outline</v-icon>
            <span>الوحدة: <strong class="text-high-emphasis">{{ targetSwapQuestion.unitName }}</strong></span>
          </div>
          <span v-if="targetSwapQuestion.lessonName" class="opacity-40">•</span>
          <div v-if="targetSwapQuestion.lessonName" class="d-flex align-center gap-1">
            <v-icon size="14" color="medium-emphasis">mdi-book-open-page-variant</v-icon>
            <span>الدرس: <strong class="text-high-emphasis">{{ targetSwapQuestion.lessonName }}</strong></span>
          </div>
        </div>
      </div>

      <!-- Scope & Action Controls Bar -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-3">
        <div class="d-flex align-center gap-1.5 flex-wrap">
          <span class="text-caption font-weight-bold text-medium-emphasis me-1">نطاق البحث:</span>
          <v-btn
            size="small"
            :variant="swapScope === 'lesson' ? 'flat' : 'outlined'"
            :color="swapScope === 'lesson' ? 'primary' : 'medium-emphasis'"
            rounded="sm"
            class="swap-scope-pill"
            :disabled="!targetSwapQuestion.lessonId"
            prepend-icon="mdi-book-open-page-variant"
            @click="$emit('setScope', 'lesson')"
          >
            نفس الدرس
          </v-btn>
          <v-btn
            size="small"
            :variant="swapScope === 'unit' ? 'flat' : 'outlined'"
            :color="swapScope === 'unit' ? 'primary' : 'medium-emphasis'"
            rounded="sm"
            class="swap-scope-pill"
            prepend-icon="mdi-folder-outline"
            @click="$emit('setScope', 'unit')"
          >
            نفس الوحدة
          </v-btn>
          <v-btn
            size="small"
            :variant="swapScope === 'all' ? 'flat' : 'outlined'"
            :color="swapScope === 'all' ? 'primary' : 'medium-emphasis'"
            rounded="sm"
            class="swap-scope-pill"
            prepend-icon="mdi-database-outline"
            @click="$emit('setScope', 'all')"
          >
            كامل المادة
          </v-btn>
        </div>

        <v-btn
          size="small"
          color="primary"
          variant="tonal"
          rounded="sm"
          class="staged-action-btn font-weight-bold px-3"
          prepend-icon="mdi-plus"
          @click="$emit('openQuickCreate')"
        >
          إنشاء سؤال بديل جديد
        </v-btn>
      </div>

      <!-- Search Bar -->
      <div class="d-flex align-center gap-2 mb-4">
        <v-text-field
          :model-value="swapSearchQuery"
          density="compact"
          variant="outlined"
          placeholder="البحث بنص السؤال في بنك الأسئلة..."
          hide-details
          clearable
          prepend-inner-icon="mdi-magnify"
          class="flex-grow-1"
          rounded="sm"
          @update:model-value="$emit('update:swapSearchQuery', $event)"
          @keyup.enter="$emit('search')"
        />
        <v-btn
          color="primary"
          variant="flat"
          size="small"
          rounded="sm"
          class="staged-action-btn font-weight-bold px-4"
          :loading="swapLoading"
          @click="$emit('search')"
        >
          بحث
        </v-btn>
      </div>

      <!-- Candidate Questions List -->
      <div v-if="swapLoading" class="py-12 text-center">
        <v-progress-circular indeterminate color="primary" size="36" />
        <p class="text-caption text-medium-emphasis mt-3">جاري البحث عن الأسئلة البديلة المطابقة للمعايير...</p>
      </div>

      <div v-else-if="swapCandidates.length === 0" class="py-10 text-center">
        <v-icon size="44" color="warning" class="mb-2">mdi-alert-circle-outline</v-icon>
        <div class="text-subtitle-2 font-weight-bold">لم يتم العثور على أسئلة بديلة مطابقة في هذا النطاق</div>
        <p class="text-caption text-medium-emphasis mt-1 mb-4">
          يمكنك توسيع النطاق إلى "نفس الوحدة" أو "كامل المادة"، أو إنشاء سؤال بديل جديد فوراً.
        </p>
        <div class="d-flex justify-center gap-2">
          <v-btn
            v-if="swapScope === 'lesson'"
            color="primary"
            variant="tonal"
            rounded="sm"
            class="staged-action-btn font-weight-bold px-3"
            @click="$emit('setScope', 'unit')"
          >
            توسيع لنفس الوحدة
          </v-btn>
          <v-btn
            color="success"
            variant="flat"
            rounded="sm"
            class="staged-action-btn font-weight-bold px-4"
            @click="$emit('openQuickCreate')"
          >
            <v-icon start size="14">mdi-plus</v-icon>
            إنشاء بديل جديد فوراً
          </v-btn>
        </div>
      </div>

      <div v-else class="d-flex flex-column gap-3" style="max-height: 480px; overflow-y: auto; padding-left: 4px; padding-right: 4px;">
        <div
          v-for="cand in swapCandidates"
          :key="cand.id"
          class="swap-candidate-card"
        >
          <!-- Candidate Card Header -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-2 pb-2 border-b mb-2">
            <div class="d-flex align-center gap-2 flex-wrap">
              <v-chip size="x-small" color="primary" variant="tonal" rounded="sm" class="staged-tag font-weight-bold px-2">
                <v-icon start size="12">{{ questionTypeIcon(cand.questionType) }}</v-icon>
                {{ questionTypeLabel(cand.questionType) }}
              </v-chip>
              <v-chip size="x-small" :color="difficultyColor(cand.difficulty)" variant="tonal" rounded="sm" class="staged-tag font-weight-bold px-2">
                {{ difficultyLabel(cand.difficulty) }}
              </v-chip>
              <v-chip v-if="cand.lessonId === targetSwapQuestion.lessonId" size="x-small" color="success" variant="tonal" rounded="sm" class="staged-tag font-weight-bold px-2">
                نفس الدرس
              </v-chip>
              <span class="text-caption text-medium-emphasis ms-1 d-none d-sm-inline">
                &bull; {{ cand.unitName }} {{ cand.lessonName ? `• ${cand.lessonName}` : '' }}
              </span>
            </div>

            <!-- Replacement Action Button -->
            <v-btn
              size="small"
              color="primary"
              variant="flat"
              rounded="sm"
              class="staged-action-btn font-weight-bold px-3"
              prepend-icon="mdi-check"
              @click="$emit('applyReplacement', cand)"
            >
              استبدال بهذا السؤال
            </v-btn>
          </div>

          <!-- Question Content -->
          <div class="text-body-1 font-weight-medium my-2 text-high-emphasis leading-relaxed" v-html="cand.content"></div>

          <!-- Options Rendering for Candidate -->
          <!-- 1. True / False Mode -->
          <div v-if="isTF(cand.questionType)" class="d-flex align-center gap-2 mt-2 flex-wrap">
            <div
              class="tf-option-pill"
              :class="{
                'is-correct': isOptionTrue(cand, 0),
                'is-neutral': !isOptionTrue(cand, 0)
              }"
            >
              <v-icon size="15" class="me-1.5" :color="isOptionTrue(cand, 0) ? 'success' : 'medium-emphasis'">
                {{ isOptionTrue(cand, 0) ? 'mdi-check-circle' : 'mdi-radiobox-blank' }}
              </v-icon>
              <span>صح / صواب</span>
              <span v-if="isOptionTrue(cand, 0)" class="ms-1.5 text-caption font-weight-bold text-success">(صحيحة)</span>
            </div>

            <div
              class="tf-option-pill"
              :class="{
                'is-correct': isOptionTrue(cand, 1),
                'is-neutral': !isOptionTrue(cand, 1)
              }"
            >
              <v-icon size="15" class="me-1.5" :color="isOptionTrue(cand, 1) ? 'success' : 'medium-emphasis'">
                {{ isOptionTrue(cand, 1) ? 'mdi-check-circle' : 'mdi-radiobox-blank' }}
              </v-icon>
              <span>خطأ</span>
              <span v-if="isOptionTrue(cand, 1)" class="ms-1.5 text-caption font-weight-bold text-success">(صحيحة)</span>
            </div>
          </div>

          <!-- 2. Multiple Choice (MCQ) Mode: Spacious 2-column grid -->
          <div v-else-if="cand.options && cand.options.length > 0" class="options-grid mt-2">
            <div
              v-for="(opt, oIdx) in cand.options"
              :key="oIdx"
              class="mcq-option-card"
              :class="{ 'is-correct': opt.isTrue, 'is-neutral': !opt.isTrue }"
            >
              <div class="d-flex align-center gap-2 overflow-hidden">
                <span class="opt-letter-avatar" :class="{ 'is-correct': opt.isTrue }">
                  {{ arabicOptionLetter(oIdx) }}
                </span>
                <span class="text-body-2 font-weight-medium text-truncate" :title="opt.text">{{ opt.text }}</span>
              </div>
              <div v-if="opt.isTrue" class="d-flex align-center gap-1 text-success text-caption font-weight-bold flex-shrink-0">
                <v-icon size="14">mdi-check</v-icon>
                <span>صحيحة</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <template #actions>
      <v-btn variant="text" color="medium-emphasis" class="font-weight-bold" @click="$emit('update:modelValue', false)">
        إغلاق
      </v-btn>
    </template>
  </CustomDialog>
</template>

<script setup>
import {
  difficultyColor,
  difficultyLabel,
  questionTypeLabel,
  questionTypeIcon,
  arabicOptionLetter,
  isTF,
  isOptionTrue
} from '../../composables/examHelpers'

defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  targetSwapQuestion: {
    type: Object,
    default: null
  },
  swapLoading: {
    type: Boolean,
    default: false
  },
  swapCandidates: {
    type: Array,
    default: () => []
  },
  swapScope: {
    type: String,
    default: 'lesson'
  },
  swapSearchQuery: {
    type: String,
    default: ''
  }
})

defineEmits([
  'update:modelValue',
  'update:swapSearchQuery',
  'setScope',
  'search',
  'openQuickCreate',
  'applyReplacement'
])
</script>
