<template>
  <div class="review-sheet-viewer-container d-flex flex-column h-100">
    <!-- ── شريط أدوات التحكم بالصورة الحقيقية الممسوحة ── -->
    <div class="image-controls-bar d-flex align-center justify-space-between flex-wrap gap-2 mb-2 px-3 py-1.5 bg-surface-variant-subtle rounded-xl border">
      <!-- تبديل نوع الصورة الممسوحة الحقيقية (المحاذاة vs الأصلية) -->
      <div class="d-flex align-center gap-2">
        <span class="text-caption font-weight-bold text-medium-emphasis">صورة المسح:</span>
        <v-btn-toggle
          v-model="imageMode"
          mandatory
          density="compact"
          color="primary"
          rounded="lg"
          variant="flat"
        >
          <v-btn value="aligned" size="x-small" prepend-icon="mdi-image-filter-center-focus">
            المُحاذاة (Aligned)
          </v-btn>
          <v-btn value="original" size="x-small" prepend-icon="mdi-image-outline">
            الأصلية (Raw)
          </v-btn>
        </v-btn-toggle>
      </div>

      <!-- أدوات التكبير والتدوير والتباين للصورة الحقيقية -->
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
          title="فتح الصورة الحقيقية بحجمها الكامل في نافذة جديدة"
          :href="sheetImageUrl"
          target="_blank"
        />
      </div>
    </div>

    <!-- ── مساحة عرض الصورة الممسوحة الحقيقية ── -->
    <div
      class="image-viewport rounded-xl border bg-white position-relative overflow-auto d-flex align-center justify-center pa-2 flex-grow-1"
      style="min-height: 480px; max-height: calc(94vh - 230px); user-select: none;"
    >
      <!-- عرض صورة الماسح الضوئي الحقيقية للملف -->
      <img
        v-if="sheetImageUrl && !imageLoadError"
        :src="sheetImageUrl"
        :style="imageTransformStyle"
        alt="ورقة الإجابة الممسوحة الحقيقية"
        class="sheet-img transition-transform"
        @error="handleImageError"
      />

      <!-- حالة تنبيه حقيقية وصادقة عند تعذر وجود أو تحميل ملف الصورة الحقيقي (بدون أي رسم وهمي) -->
      <div v-else class="text-center pa-8 text-medium-emphasis">
        <v-avatar color="warning" variant="tonal" size="64" rounded="xl" class="mb-3">
          <v-icon size="32" color="warning">mdi-image-off-outline</v-icon>
        </v-avatar>
        <div class="font-weight-black text-body-1 mb-1 text-on-surface">
          تعذر تحميل الصورة الممسوحة الحقيقية لهذه الورقة
        </div>
        <p class="text-caption mb-3" style="max-width: 420px; margin: 0 auto;">
          لم يتم العثور على ملف الصورة الحقيقي على خادم المسح الضوئي لهذا التسليم. تأكد من إتمام حفظ ملف المسح الأصلي.
        </p>
        <div v-if="attemptedUrl" class="text-caption font-mono text-medium-emphasis mb-3 bg-surface pa-2 rounded border" style="max-width: 480px; margin: 0 auto; word-break: break-all;">
          المسار المطلوب: {{ attemptedUrl }}
        </div>
        <div class="d-flex align-center justify-center gap-2">
          <v-btn
            size="small"
            variant="tonal"
            color="primary"
            prepend-icon="mdi-refresh"
            @click="retryLoadImage"
          >
            إعادة محاولة التحميل
          </v-btn>
          <v-chip size="small" variant="tonal" color="indigo" class="font-weight-bold">
            معرف التسليم: #{{ activeReviewSheet?.submission || activeReviewSheet?.id }}
          </v-chip>
        </div>
      </div>
    </div>

    <!-- ── بطاقة فحص السؤال المحدد وكثافة التظليل (Spotlight Card) ── -->
    <div class="question-spotlight-bar mt-2 pa-2.5 rounded-xl border bg-surface" v-if="selectedQuestion">
      <div class="d-flex align-center justify-space-between flex-wrap gap-2">
        <!-- شارة رقم السؤال ونوعه -->
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

        <!-- الدرجة المستحقة -->
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
import { resolveSheetImageUrl, getStatusChip } from './reviewUtils'

const props = defineProps<{
  activeReviewSheet: any
  selectedQuestion: any
}>()

const imageMode = ref<'aligned' | 'original'>('aligned')
const imageZoom = ref<number>(1.0)
const imageRotation = ref<number>(0)
const isHighContrast = ref<boolean>(false)
const imageLoadError = ref<boolean>(false)
const attemptedUrl = ref<string>('')

const sheetImageUrl = computed(() => {
  if (!props.activeReviewSheet) return ''
  return resolveSheetImageUrl(props.activeReviewSheet, imageMode.value)
})

watch(
  () => sheetImageUrl.value,
  (newUrl) => {
    imageLoadError.value = false
    attemptedUrl.value = newUrl
  },
  { immediate: true }
)

function handleImageError() {
  imageLoadError.value = true
}

function retryLoadImage() {
  imageLoadError.value = false
  // Force re-evaluation by toggling imageMode temporarily if needed
  const curr = imageMode.value
  imageMode.value = curr === 'aligned' ? 'original' : 'aligned'
  setTimeout(() => {
    imageMode.value = curr
  }, 100)
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
.question-spotlight-bar {
  border-color: rgba(var(--v-border-color), 0.12) !important;
}
</style>
