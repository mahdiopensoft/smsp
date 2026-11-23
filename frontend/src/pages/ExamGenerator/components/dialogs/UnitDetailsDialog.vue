<template>
  <CustomDialog
    :model-value="modelValue"
    width="700"
    :title="(institutionType === 'university' ? 'محتوى مفردة المقرر: ' : 'محتوى الوحدة: ') + (unitDetails?.unitName || '')"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <!-- Unit Summary Bar (Lightweight & Clean) -->
    <div
      v-if="unitDetails?.totalQuestions !== undefined"
      class="d-flex align-center justify-space-between flex-wrap gap-2 pa-2 px-3 rounded-lg border mb-2 text-caption"
      style="background: rgba(var(--v-theme-surface-variant), 0.3);"
    >
      <div>
        <span>أسئلة الوحدة بالبنك: </span>
        <strong class="text-primary">{{ unitDetails.totalQuestions }} سؤال</strong>
      </div>
      <div v-if="unitDetails.requiredQuestions > 0">
        <span>المطلوب للاختبار: </span>
        <strong class="text-info">{{ unitDetails.requiredQuestions }}</strong>
      </div>
      <div v-if="unitDetails.requiredQuestions > 0">
        <span>المتبقي غير المختار (للبدائل): </span>
        <strong class="text-success">{{ unitDetails.remainingQuestions }}</strong>
      </div>
    </div>

    <!-- Explanatory note -->
    <div class="d-flex align-center gap-1 mb-3 px-1 text-caption text-medium-emphasis">
      <v-icon size="15" color="info">mdi-information-outline</v-icon>
      <span>
        هذه القائمة تعرض <strong>كامل مخزون بنك الأسئلة المتاح في الوحدة ({{ unitDetails?.totalQuestions }} سؤال)</strong>.
        سيقوم النظام بسحب <strong>({{ unitDetails?.requiredQuestions }} أسئلة)</strong> منها آلياً للاختبار عند الضغط على "الانتقال لمسودة واستعراض النماذج".
      </span>
    </div>

    <div v-if="unitDetails?.lessons && unitDetails.lessons.length > 0" class="d-flex flex-column gap-2 mb-4">
      <div
        v-for="(lesson, i) in unitDetails.lessons"
        :key="i"
        class="pa-3 rounded-lg border bg-surface"
      >
        <div class="d-flex align-center justify-space-between flex-wrap gap-2">
          <div>
            <span class="font-weight-bold text-body-2">{{ lesson.name }}</span>
            <span class="text-caption text-medium-emphasis ms-2">({{ lesson.questionsCount }} سؤال)</span>
          </div>
          <div class="d-flex align-center gap-1">
            <v-btn
              v-if="lesson.questionsCount > 0"
              size="small"
              variant="text"
              color="primary"
              class="font-weight-bold text-caption"
              :prepend-icon="expandedLessonId === lesson.id ? 'mdi-chevron-up' : 'mdi-eye-outline'"
              @click="$emit('toggleLessonQuestions', lesson.id)"
            >
              {{ expandedLessonId === lesson.id ? 'إخفاء' : 'عرض الأسئلة' }}
            </v-btn>
            <v-btn
              size="small"
              variant="text"
              color="medium-emphasis"
              class="text-caption"
              prepend-icon="mdi-plus"
              @click="$emit('goToAddQuestion', { unitId: unitDetails.unitId, lessonId: lesson.id })"
            >
              إضافة سؤال
            </v-btn>
          </div>
        </div>

        <!-- Expanded Questions Section (Lightweight & Minimal) -->
        <div v-if="expandedLessonId === lesson.id" class="mt-3 pt-2 border-t">
          <div v-if="lessonQuestionsLoading" class="text-center py-3 text-caption text-medium-emphasis">
            <v-progress-circular indeterminate color="primary" size="20" width="2" class="me-2" />
            جاري التحميل...
          </div>
          <div v-else-if="lessonQuestionsList[lesson.id] && lessonQuestionsList[lesson.id].length > 0">
            <div
              v-for="(q, qIdx) in lessonQuestionsList[lesson.id]"
              :key="q.id"
              class="py-2.5 border-b"
            >
              <!-- Question Number & Content -->
              <div class="d-flex align-start gap-2 mb-1">
                <span class="font-weight-bold text-body-2 text-medium-emphasis">{{ qIdx + 1 }}.</span>
                <div class="text-body-2 flex-grow-1" v-html="$sanitizeHtml(q.content)"></div>
                <v-btn
                  size="x-small"
                  variant="text"
                  icon="mdi-pencil-outline"
                  color="medium-emphasis"
                  title="تعديل هذا السؤال في بنك الأسئلة"
                  class="ms-1"
                  @click="$emit('goToEditQuestion', q.id)"
                />
              </div>

              <!-- Minimal Options / Choices -->
              <div v-if="q.options && q.options.length > 0" class="d-flex flex-wrap ms-4 mt-1">
                <div
                  v-for="(opt, optIdx) in q.options"
                  :key="optIdx"
                  class="me-6 py-0.5 text-caption"
                  :class="{ 'font-weight-bold text-success': opt.isTrue, 'text-medium-emphasis': !opt.isTrue }"
                >
                  <span class="me-1">{{ ['أ', 'ب', 'ج', 'د', 'هـ'][optIdx] || (optIdx + 1) }})</span>
                  <span>{{ opt.text }}</span>
                  <span v-if="opt.isTrue" class="ms-1 font-weight-bold">✓</span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center text-medium-emphasis py-2 text-caption">
            لا توجد أسئلة مسجلة لهذا الدرس
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-medium-emphasis pa-6">
      لا توجد دروس مضافة لهذه الوحدة بعد
    </div>

    <template #actions>
      <div class="d-flex align-center justify-space-between w-100 px-2">
        <v-btn
          variant="text"
          color="primary"
          class="text-caption font-weight-bold"
          prepend-icon="mdi-database-search"
          @click="$emit('openInQuestionBank', unitDetails?.unitId)"
        >
          فتح في بنك الأسئلة
        </v-btn>
        <v-btn variant="flat" color="primary" class="text-caption font-weight-bold px-4 rounded-lg" @click="$emit('update:modelValue', false)">
          فهمت، إغلاق والعودة للاختبار
        </v-btn>
      </div>
    </template>
  </CustomDialog>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  unitDetails: {
    type: Object,
    default: () => ({})
  },
  institutionType: {
    type: String,
    default: 'school'
  },
  expandedLessonId: {
    type: [Number, String],
    default: null
  },
  lessonQuestionsLoading: {
    type: Boolean,
    default: false
  },
  lessonQuestionsList: {
    type: Object,
    default: () => ({})
  }
})

defineEmits([
  'update:modelValue',
  'toggleLessonQuestions',
  'goToAddQuestion',
  'goToEditQuestion',
  'openInQuestionBank'
])
</script>
