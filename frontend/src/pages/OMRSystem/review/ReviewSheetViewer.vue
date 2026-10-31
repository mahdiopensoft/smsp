<template>
  <div class="review-sheet-viewer-container d-flex flex-column h-100">
    <!-- ── شريط أدوات التحكم بالصورة والقالب ── -->
    <div class="image-controls-bar d-flex align-center justify-space-between flex-wrap gap-2 mb-2 px-2 py-1 bg-surface-variant-subtle rounded-xl border">
      <!-- تبديل نمط العرض: صورة الماسح vs الورقة الرقمية SVG -->
      <div class="d-flex align-center gap-1">
        <v-btn-toggle
          v-model="viewMode"
          mandatory
          density="compact"
          color="primary"
          rounded="lg"
          variant="tonal"
        >
          <v-btn value="scanner" size="small" prepend-icon="mdi-camera-outline">
            صورة المسح
          </v-btn>
          <v-btn value="digital" size="small" prepend-icon="mdi-file-document-check-outline">
            الورقة التفاعلية (SVG)
          </v-btn>
        </v-btn-toggle>

        <v-btn-toggle
          v-if="viewMode === 'scanner'"
          v-model="internalImageMode"
          mandatory
          density="compact"
          color="indigo"
          rounded="lg"
          variant="outlined"
          class="ms-1"
        >
          <v-btn value="aligned" size="x-small">المُحاذاة</v-btn>
          <v-btn value="original" size="x-small">الأصلية</v-btn>
        </v-btn-toggle>
      </div>

      <!-- أدوات التكبير والتدوير والتباين -->
      <div class="d-flex align-center gap-1">
        <v-btn
          icon="mdi-magnify-minus-outline"
          size="x-small"
          variant="tonal"
          density="comfortable"
          title="تصغير (-15%)"
          :disabled="imageZoom <= 0.4"
          @click="zoomImage(-0.15)"
        />
        <span class="text-caption font-weight-black text-center" style="min-width: 42px;">
          {{ Math.round(imageZoom * 100) }}%
        </span>
        <v-btn
          icon="mdi-magnify-plus-outline"
          size="x-small"
          variant="tonal"
          density="comfortable"
          title="تكبير (+15%)"
          :disabled="imageZoom >= 3.0"
          @click="zoomImage(0.15)"
        />
        <v-btn
          icon="mdi-restore"
          size="x-small"
          variant="tonal"
          density="comfortable"
          title="إعادة ضبط الحجم والتدوير"
          @click="resetImageControls"
        />
        <v-divider vertical class="mx-1" />
        <v-btn
          icon="mdi-rotate-right"
          size="x-small"
          variant="tonal"
          density="comfortable"
          title="تدوير 90 درجة مع عقارب الساعة"
          @click="rotateImage(90)"
        />
        <v-btn
          :icon="isHighContrast ? 'mdi-contrast-circle' : 'mdi-contrast'"
          size="x-small"
          :color="isHighContrast ? 'amber-darken-3' : undefined"
          variant="tonal"
          density="comfortable"
          title="تعزيز تباين الرصاص الخافت (High Contrast)"
          @click="isHighContrast = !isHighContrast"
        />
        <v-btn
          v-if="sheetImageUrl"
          icon="mdi-open-in-new"
          size="x-small"
          variant="tonal"
          density="comfortable"
          title="فتح الصورة في نافذة جديدة"
          :href="sheetImageUrl"
          target="_blank"
        />
      </div>
    </div>

    <!-- ── مساحة عرض الصورة أو الورقة التفاعلية ── -->
    <div
      class="image-viewport rounded-xl border bg-white position-relative overflow-auto d-flex align-center justify-center pa-2 flex-grow-1"
      style="min-height: 480px; max-height: calc(94vh - 230px); user-select: none;"
    >
      <!-- النمط 1: صورة الماسح الضوئي الممسوحة -->
      <template v-if="viewMode === 'scanner' && sheetImageUrl && !imageLoadError">
        <img
          :src="sheetImageUrl"
          :style="imageTransformStyle"
          alt="ورقة الإجابة الممسوحة"
          class="sheet-img transition-transform"
          @error="handleImageError"
        />
      </template>

      <!-- النمط 2: الورقة الرقمية التفاعلية SVG (كبديل مباشر عندما لا توجد صورة أو عند التبديل) -->
      <template v-else-if="viewMode === 'digital' || !sheetImageUrl || imageLoadError">
        <div class="digital-sheet-wrapper w-100 h-100 overflow-auto pa-2" :style="digitalSheetTransformStyle">
          <YemeniMinistrySheet
            layout-mode="compact_a5"
            :student-name="activeReviewSheet?.student_name || 'طالب اختبار'"
            :seat-number="activeReviewSheet?.seat_number || activeReviewSheet?.id || '000000'"
            :serial-number="activeReviewSheet?.id || '1'"
            :exam-subject="activeReviewSheet?.exam_title || 'مادة الاختبار'"
            :governorate="activeReviewSheet?.governorate_name || 'أمانة العاصمة'"
            :directorate="activeReviewSheet?.directorate_name || 'المركز الامتحاني'"
            :student-answers="studentAnswersMap"
            :answer-key="answerKeyMap"
            :show-inspection-overlay="true"
            :interactive="true"
            :hovered-bubble-id="hoveredBubbleId"
            :emblem-type="emblemType"
          />
        </div>
      </template>

      <!-- النمط 3: بطاقة معلومات توضيحية خفيفة في حال عدم توفر أي بيانات -->
      <div v-else class="text-center pa-8 text-medium-emphasis">
        <v-avatar color="primary" variant="tonal" size="64" rounded="xl" class="mb-3">
          <v-icon size="32" color="primary">mdi-image-off-outline</v-icon>
        </v-avatar>
        <div class="font-weight-black text-body-1 mb-1">
          لا تتوفر صورة ممسوحة مرفقة لهذه الورقة
        </div>
        <p class="text-caption mb-3" style="max-width: 340px; margin: 0 auto;">
          تمت قراءة البيانات من ملف الدفعة، ويمكنك تدقيق وتعديل الإجابات من الجدول مباشرة.
        </p>
        <v-btn
          color="primary"
          variant="outlined"
          size="small"
          prepend-icon="mdi-file-document-check-outline"
          @click="viewMode = 'digital'"
        >
          عرض الورقة التفاعلية (SVG)
        </v-btn>
      </div>
    </div>

    <!-- ── بطاقة فحص السؤال المحدد وكثافة التظليل (Spotlight Card) ── -->
    <div class="question-spotlight-bar mt-2 pa-2.5 rounded-xl border bg-surface" v-if="selectedQuestion">
      <div class="d-flex align-center justify-space-between flex-wrap gap-2">
        <!-- شارة رقم السؤال -->
        <div class="spotlight-badge question-badge d-flex align-center gap-1 px-2.5 py-1 rounded-lg bg-blue-lighten-5 text-primary font-weight-black">
          <v-icon size="14" color="primary">mdi-crosshairs-gps</v-icon>
          <span>السؤال #{{ selectedQuestion.question_number }}</span>
          <v-chip size="x-small" :color="selectedQuestion.is_true_false ? 'teal' : 'indigo'" variant="tonal" class="ms-1 font-weight-bold">
            {{ selectedQuestion.is_true_false ? 'صح وخطأ' : 'اختيارات' }}
          </v-chip>
        </div>

        <!-- حالة النتيجة -->
        <div class="d-flex align-center gap-1">
          <v-chip
            size="small"
            :color="statusChipColor"
            variant="tonal"
            class="font-weight-black"
          >
            <v-icon start size="14">{{ statusChipIcon }}</v-icon>
            {{ selectedQuestion.status || (selectedQuestion.is_correct ? 'صحيحة' : 'خاطئة') }}
          </v-chip>
        </div>

        <!-- تظليل الطالب -->
        <div class="spotlight-badge value-badge text-body-2">
          <span class="text-medium-emphasis me-1">تظليل الطالب:</span>
          <strong :class="selectedQuestion.is_correct ? 'text-success font-weight-black' : (selectedQuestion.marked_choice ? 'text-error font-weight-black' : 'text-medium-emphasis')">
            {{ selectedQuestion.marked_choice_display || selectedQuestion.marked_choice || 'فارغ' }}
          </strong>
        </div>

        <!-- الإجابة النموذجية -->
        <div class="spotlight-badge value-badge text-body-2">
          <span class="text-medium-emphasis me-1">النموذجية:</span>
          <strong class="text-success font-weight-black">
            {{ selectedQuestion.correct_choice_display || selectedQuestion.correct_choice || 'لم تُحدد' }}
          </strong>
        </div>

        <!-- الدرجة -->
        <div class="spotlight-badge value-badge text-body-2">
          <span class="text-medium-emphasis me-1">الدرجة:</span>
          <strong class="text-primary font-weight-black">
            {{ selectedQuestion.score || (selectedQuestion.is_correct ? '1.0' : '0.0') }}
          </strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'
import { resolveSheetImageUrl, getStatusChip } from './reviewUtils'

const props = defineProps<{
  activeReviewSheet: any
  selectedQuestion: any
}>()

const viewMode = ref<'scanner' | 'digital'>('scanner')
const internalImageMode = ref<'aligned' | 'original'>('aligned')
const imageZoom = ref<number>(1.0)
const imageRotation = ref<number>(0)
const isHighContrast = ref<boolean>(false)
const imageLoadError = ref<boolean>(false)

// Resolve Image URL safely
const sheetImageUrl = computed(() => {
  if (!props.activeReviewSheet) return ''
  return resolveSheetImageUrl(props.activeReviewSheet, internalImageMode.value)
})

// Auto-switch to digital sheet if no physical image URL is available
watch(
  () => sheetImageUrl.value,
  (newUrl) => {
    imageLoadError.value = false
    if (!newUrl) {
      viewMode.value = 'digital'
    } else {
      viewMode.value = 'scanner'
    }
  },
  { immediate: true }
)

function handleImageError() {
  imageLoadError.value = true
  viewMode.value = 'digital'
}

function zoomImage(delta: number) {
  imageZoom.value = Math.min(Math.max(0.4, Number((imageZoom.value + delta).toFixed(2))), 3.5)
}

function rotateImage(delta: number = 90) {
  imageRotation.value = (imageRotation.value + delta + 360) % 360
}

function resetImageControls() {
  imageZoom.value = 1.0
  imageRotation.value = 0
}

const imageTransformStyle = computed(() => {
  const filters: string[] = []
  if (isHighContrast.value) {
    filters.push('contrast(180%) brightness(95%) grayscale(100%)')
  }
  return {
    transform: `scale(${imageZoom.value}) rotate(${imageRotation.value}deg)`,
    transformOrigin: 'top center',
    filter: filters.length ? filters.join(' ') : 'none',
    maxWidth: '100%',
    transition: 'transform 0.2s ease-out, filter 0.2s ease-out',
    display: 'block',
    margin: '0 auto',
    boxShadow: '0 4px 16px rgba(0,0,0,0.08)'
  }
})

const digitalSheetTransformStyle = computed(() => {
  return {
    transform: `scale(${imageZoom.value}) rotate(${imageRotation.value}deg)`,
    transformOrigin: 'top center',
    transition: 'transform 0.2s ease-out'
  }
})

const studentAnswersMap = computed(() => {
  const map: Record<number, any> = {}
  if (!props.activeReviewSheet?.questions) return map
  for (const q of props.activeReviewSheet.questions) {
    map[q.question_number] = q.marked_choice
  }
  return map
})

const answerKeyMap = computed(() => {
  const map: Record<number, string> = {}
  if (!props.activeReviewSheet?.questions) return map
  for (const q of props.activeReviewSheet.questions) {
    if (q.correct_choice) {
      map[q.question_number] = q.correct_choice
    }
  }
  return map
})

const hoveredBubbleId = computed(() => {
  return props.selectedQuestion ? `q_${props.selectedQuestion.question_number}` : ''
})

const emblemType = computed(() => {
  const inst = props.activeReviewSheet?.institution_type
  if (inst === 'university') return 'university_seal'
  if (inst === 'institute') return 'institute_seal'
  return 'republic_eagle'
})

const statusChipColor = computed(() => {
  if (!props.selectedQuestion) return 'grey'
  return getStatusChip(props.selectedQuestion).color
})

const statusChipIcon = computed(() => {
  if (!props.selectedQuestion) return 'mdi-circle-outline'
  return getStatusChip(props.selectedQuestion).icon
})
</script>

<style scoped>
.review-sheet-viewer-container {
  min-width: 0;
}
.image-viewport {
  background-color: #fafbfc;
}
.sheet-img {
  object-fit: contain;
  cursor: grab;
}
.sheet-img:active {
  cursor: grabbing;
}
.digital-sheet-wrapper {
  max-width: 100%;
  display: flex;
  justify-content: center;
}
.question-spotlight-bar {
  border-color: rgba(var(--v-border-color), 0.12) !important;
}
</style>
