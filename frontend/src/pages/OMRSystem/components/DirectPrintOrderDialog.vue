<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="650px"
    scrollable
    persistent
  >
    <v-card class="rounded-2xl overflow-hidden print-order-modal bg-surface elevation-8 border" style="background: rgb(var(--v-theme-surface)) !important;">
      <!-- ── شريط الهوية العلوي المعتمد ── -->
      <div class="modal-top-stripe" />

      <!-- ── 1. ترويسة النافذة الرسمية الموحدة ── -->
      <div class="px-5 py-4 d-flex align-center justify-space-between border-b bg-surface">
        <div class="d-flex align-center gap-3">
          <v-avatar color="primary" variant="tonal" size="44" rounded="lg">
            <v-icon size="24" color="primary">
              {{ currentStep === 'prepare' ? 'mdi-printer' : 'mdi-clipboard-check-outline' }}
            </v-icon>
          </v-avatar>
          <div>
            <div class="d-flex align-center gap-2">
              <h3 class="text-subtitle-1 font-weight-black text-high-emphasis mb-0">
                {{ currentStep === 'prepare' ? 'أمر الطباعة المباشر والسريع' : 'محضر التحقق واستلام المطبوعات الميداني' }}
              </h3>
              <div class="center-count-badge unified-badge-primary px-2.5 py-0.5 text-caption font-weight-bold">
                {{ currentStep === 'prepare' ? 'المرحلة 1: إرسال للماكينة' : 'المرحلة 2: مصادقة الاستلام الفعلي' }}
              </div>
            </div>
            <div class="text-caption text-medium-emphasis">
              {{ currentStep === 'prepare' ? 'سحب وثائق الاختبار المعتمدة وتغذية ماكينات المطبعة فوراً' : 'التأكد من خروج الأوراق المطبوعة بجودة سليمة قبل التوثيق الرسمي في السجل' }}
            </div>
          </div>
        </div>

        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          density="comfortable"
          color="medium-emphasis"
          rounded="lg"
          :disabled="loading"
          @click="close"
        />
      </div>

      <!-- ── 2. محتوى النافذة المنظم بالمكونات الموحدة ── -->
      <v-card-text class="pa-5 overflow-y-auto bg-surface" style="max-height: 80vh;">
        <!-- بطاقة معلومات الاختبار الأساسية -->
        <div class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-4 mx-auto elevation-1" style="max-width: 650px;">
          <!-- رقم إذن الصرف -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="primary">mdi-barcode</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">رقم إذن الصرف:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <div class="center-count-badge px-3 py-1 font-mono font-weight-black text-primary text-subtitle-2">
                {{ orderNumberDisplay }}
              </div>
              <div class="center-count-badge unified-badge-primary px-2.5 py-1 text-caption font-weight-bold">
                أمر طباعة معتمد
              </div>
            </div>
          </div>

          <!-- الاختبار والمادة -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="primary">mdi-book-education-outline</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">الاختبار والمادة:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <span class="font-weight-bold text-body-2 text-high-emphasis">{{ exam?.title || 'الاختبار' }}</span>
              <div class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold">
                المادة: {{ exam?.subject_name || 'عام' }}
              </div>
            </div>
          </div>

          <!-- كود الاختبار والجهة المنفذة -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="primary">mdi-identifier</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">كود الاختبار والجهة المنفذة:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <div class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold font-mono">
                {{ exam?.uniqueCode || '—' }}
              </div>
              <span class="text-caption text-medium-emphasis font-weight-medium">
                • {{ exam?.press_name || 'المطبعة السرية المركزية' }}
              </span>
            </div>
          </div>
        </div>

        <!-- ══════════════════════════════════════════════════════════════ -->
        <!-- المرحلة 1: خيارات سحب المستندات والمعاينة                       -->
        <!-- ══════════════════════════════════════════════════════════════ -->
        <div v-if="currentStep === 'prepare'" class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-2 mx-auto elevation-1" style="max-width: 650px;">
          <div class="d-flex align-center gap-2 mb-3 text-subtitle-2 font-weight-bold text-high-emphasis">
            <v-avatar color="primary" variant="tonal" size="30" rounded="lg">
              <v-icon size="18" color="primary">mdi-printer-settings</v-icon>
            </v-avatar>
            <span>المستندات المطلوب سحبها للماكينة:</span>
          </div>

          <!-- مربعات الاختيار للمستندات -->
          <v-row class="align-start filter-fields-row" dense>
            <v-col cols="12" sm="6" class="py-1">
              <v-checkbox
                v-model="options.sheets"
                color="primary"
                density="compact"
                hide-details
              >
                <template #label>
                  <span class="text-body-2 font-weight-medium">أوراق إجابة OMR ({{ totalTargetCount }} طالب)</span>
                </template>
              </v-checkbox>
            </v-col>
            <v-col cols="12" sm="6" class="py-1">
              <v-checkbox
                v-model="options.booklets"
                color="primary"
                density="compact"
                hide-details
              >
                <template #label>
                  <span class="text-body-2 font-weight-medium">كراسات الأسئلة (النماذج A, B...)</span>
                </template>
              </v-checkbox>
            </v-col>
            <v-col cols="12" sm="6" class="py-1">
              <v-checkbox
                v-model="options.roster"
                color="primary"
                density="compact"
                hide-details
              >
                <template #label>
                  <span class="text-body-2 font-weight-medium">كشوف المناداة ومحاضر المراكز</span>
                </template>
              </v-checkbox>
            </v-col>
            <v-col cols="12" sm="6" class="py-1">
              <v-checkbox
                v-model="options.manifest"
                color="primary"
                density="compact"
                hide-details
              >
                <template #label>
                  <span class="text-body-2 font-weight-medium">إذن الصرف وأمر الطباعة A4</span>
                </template>
              </v-checkbox>
            </v-col>
          </v-row>

          <!-- معاينة الوثائق قبل إرسال أمر السحب للماكينة -->
          <div class="mt-3 pt-3 border-t">
            <div class="text-caption font-weight-bold text-high-emphasis mb-2 d-flex align-center gap-1.5">
              <v-icon size="16" color="primary">mdi-eye-check-outline</v-icon>
              <span>معاينة الوثائق قبل إرسال أمر السحب للماكينة:</span>
            </div>
            <div class="d-flex align-center gap-2 flex-wrap">
              <v-btn
                size="small"
                color="primary"
                variant="tonal"
                rounded="lg"
                class="font-weight-bold"
                prepend-icon="mdi-eye-outline"
                @click="$emit('previewOmr', exam)"
              >
                معاينة ورقة OMR
              </v-btn>
              <v-btn
                size="small"
                color="primary"
                variant="tonal"
                rounded="lg"
                class="font-weight-bold"
                prepend-icon="mdi-file-eye-outline"
                @click="$emit('previewQuestionPaper', exam)"
              >
                معاينة كراسة الأسئلة
              </v-btn>
              <v-btn
                v-if="exam?.has_order || exam?.order_number"
                size="small"
                color="secondary"
                variant="tonal"
                rounded="lg"
                class="font-weight-bold"
                prepend-icon="mdi-text-box-search-outline"
                @click="$emit('previewManifest', exam)"
              >
                معاينة إذن الصرف A4
              </v-btn>
            </div>
          </div>

          <!-- تنبيه واقعي واضح -->
          <v-alert
            type="primary"
            variant="tonal"
            density="compact"
            rounded="lg"
            class="mt-3 py-2"
          >
            <template #prepend>
              <v-icon size="20">mdi-shield-check-outline</v-icon>
            </template>
            <div class="text-caption">
              <strong>ضمان النزاهة الامتحانية:</strong> عند الضغط على زر السحب، سيتم تشغيل أمر الطباعة للطابعة أولاً، ولن يتم إغلاق الدفعة في قاعدة البيانات إلا بعد تأكيد استلام الأوراق الفعلية الخارجة من الماكينة.
            </div>
          </v-alert>
        </div>

        <!-- ══════════════════════════════════════════════════════════════ -->
        <!-- المرحلة 2: محضر التحقق واستلام المخرجات الميدانية من الماكينة -->
        <!-- ══════════════════════════════════════════════════════════════ -->
        <div v-else class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-2 mx-auto elevation-1" style="max-width: 650px;">
          <div class="d-flex align-center gap-2 mb-3 text-subtitle-2 font-weight-bold text-high-emphasis">
            <v-avatar color="primary" variant="tonal" size="30" rounded="lg">
              <v-icon size="18" color="primary">mdi-check-all</v-icon>
            </v-avatar>
            <span>فحص مخرجات ماكينة الطباعة والمطابقة الميدانية</span>
          </div>

          <v-alert
            type="info"
            variant="tonal"
            density="compact"
            rounded="lg"
            class="mb-3 py-2"
          >
            <template #prepend>
              <v-icon size="20">mdi-printer-eye</v-icon>
            </template>
            <div class="text-caption">
              تم إرسال أمر السحب إلى الماكينة واستدعاء نافذة الطباعة. يرجى فحص مخرجات الطابعة والتأكد من العدد الفعلي وجودة التظليل والباركود.
            </div>
          </v-alert>

          <!-- زر إعادة فتح واستدعاء نافذة الطباعة الحقيقية -->
          <div class="d-flex align-center justify-space-between mb-4 pa-2.5 bg-grey-lighten-4 rounded-lg border flex-wrap gap-2">
            <div class="d-flex align-center gap-2">
              <v-icon color="primary" size="20">mdi-printer-refresh</v-icon>
              <span class="text-caption font-weight-bold text-high-emphasis">لم تظهر نافذة الطباعة لديك أو أغلقتها بالخطأ؟</span>
            </div>
            <v-btn
              size="small"
              color="primary"
              variant="flat"
              rounded="lg"
              class="font-weight-bold px-3"
              prepend-icon="mdi-printer"
              @click="retriggerPrint"
            >
              فتح نافذة الطباعة الحقيقية الآن
            </v-btn>
          </div>

          <!-- حقل إدخال العدد الفعلي المستلم من الماكينة -->
          <div class="mb-3">
            <label class="text-caption font-weight-bold text-high-emphasis d-block mb-1">
              عدد الأوراق السليمة التي خرجت فعلياً من الماكينة:
            </label>
            <v-text-field
              v-model.number="actualPrintedCount"
              type="number"
              :min="0"
              :max="totalTargetCount"
              variant="outlined"
              density="compact"
              rounded="lg"
              prepend-inner-icon="mdi-counter"
              suffix="ورقة"
              hide-details
              class="mb-2"
            />
            
            <!-- مؤشر حالة السحب التفاعلي -->
            <div class="d-flex align-center justify-space-between mt-2 flex-wrap gap-2">
              <div v-if="actualPrintedCount >= totalTargetCount" class="center-count-badge unified-badge-primary px-3 py-1 text-caption font-weight-bold">
                ✓ سحب مكتمل بالكامل (100% - {{ totalTargetCount }} من {{ totalTargetCount }})
              </div>
              <div v-else-if="actualPrintedCount > 0" class="center-count-badge unified-badge-warning px-3 py-1 text-caption font-weight-bold">
                ⚠ سحب جزئي: تم طباعة {{ actualPrintedCount }} ورقة، وسيتبقى {{ totalTargetCount - actualPrintedCount }} في قائمة المستحقة
              </div>
              <div v-else class="center-count-badge unified-badge-warning px-3 py-1 text-caption font-weight-bold">
                ✕ لم تطبع أي ورقة (سحب ملغى / تعذر عمل الطابعة)
              </div>

              <span class="text-caption text-medium-emphasis">
                المستهدف الكلي: <strong>{{ totalTargetCount }} ورقة</strong>
              </span>
            </div>
          </div>

          <!-- ملاحظات الفحص والتشغيل -->
          <div class="mt-3">
            <label class="text-caption font-weight-bold text-high-emphasis d-block mb-1">
              ملاحظات التشغيل والماكينة (اختياري في حال وجود انحشار أو خطأ):
            </label>
            <v-text-field
              v-model="operatorNotes"
              placeholder="مثال: تمت الطباعة بجودة ممتازة / أو: انحشار ورقة واحدة رقم 4"
              variant="outlined"
              density="compact"
              rounded="lg"
              prepend-inner-icon="mdi-text"
              hide-details
            />
          </div>
        </div>
      </v-card-text>

      <!-- ── 3. أزرار التحكم الرسمية الموحدة باللون الأساسي (primary) بدون أي أخضر ── -->
      <div class="px-5 py-3.5 d-flex align-center justify-space-between border-t bg-surface flex-wrap gap-2">
        <!-- أزرار المرحلة 1 -->
        <template v-if="currentStep === 'prepare'">
          <div class="d-flex align-center gap-2">
            <v-btn
              variant="tonal"
              color="secondary"
              rounded="lg"
              class="font-weight-bold px-4"
              prepend-icon="mdi-close"
              :disabled="loading"
              @click="close"
            >
              إلغاء
            </v-btn>
            <v-btn
              color="primary"
              variant="tonal"
              rounded="lg"
              class="font-weight-bold px-3"
              prepend-icon="mdi-printer-eye"
              @click="$emit('openStudio', exam)"
            >
              استوديو الطباعة التفصيلي
            </v-btn>
          </div>

          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-bold px-6 text-white"
            prepend-icon="mdi-printer"
            :loading="loading"
            @click="startPrintDispatch"
          >
            بدء سحب وثائق الاختبار على الماكينة
          </v-btn>
        </template>

        <!-- أزرار المرحلة 2: محضر التحقق الميداني -->
        <template v-else>
          <v-btn
            color="error"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold px-4"
            prepend-icon="mdi-close-circle-outline"
            @click="onFailedOrCancelled"
          >
            تعذر السحب / إلغاء (لم تطبع الأوراق)
          </v-btn>

          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-bold px-6 text-white"
            prepend-icon="mdi-check-decagram-outline"
            :loading="loading"
            @click="onConfirmVerification"
          >
            اعتماد ومصادقة الاستلام الفعلي في السجل
          </v-btn>
        </template>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  exam: {
    type: Object,
    default: () => null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits([
  'update:modelValue',
  'startPrint',
  'confirmExecution',
  'openStudio',
  'previewOmr',
  'previewQuestionPaper',
  'previewManifest',
])

const currentStep = ref('prepare') // 'prepare' | 'verify'
const actualPrintedCount = ref(0)
const operatorNotes = ref('')

const options = ref({
  sheets: true,
  booklets: true,
  roster: true,
  manifest: true,
})

const totalTargetCount = computed(() => {
  return props.exam?.total_registered || props.exam?.total_students || 8
})

const orderNumberDisplay = computed(() => {
  if (!props.exam) return 'PRN-REQ-EXAM'
  return props.exam.order_number || `PRN-REQ-${props.exam.uniqueCode || props.exam.id}`
})

watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    currentStep.value = 'prepare'
    actualPrintedCount.value = totalTargetCount.value
    operatorNotes.value = ''
    options.value = {
      sheets: true,
      booklets: true,
      roster: true,
      manifest: true,
    }
  }
})

const close = () => {
  emit('update:modelValue', false)
}

// المرحلة 1: تشغيل أمر السحب الفعلي والانتقال للمرحلة 2
const startPrintDispatch = () => {
  actualPrintedCount.value = totalTargetCount.value
  emit('startPrint', {
    exam: props.exam,
    options: options.value,
  })
  currentStep.value = 'verify'
}

// إعادة فتح نافذة الطباعة الحقيقية إذا لم تظهر أو أغلقت بالخطأ
const retriggerPrint = () => {
  emit('startPrint', {
    exam: props.exam,
    options: options.value,
  })
}

// المرحلة 2: في حال تعذر السحب على الماكينة أو عدم وجود طابعة
const onFailedOrCancelled = () => {
  close()
}

// المرحلة 2: اعتماد وتوثيق ما خرج فعلياً فقط
const onConfirmVerification = () => {
  emit('confirmExecution', {
    exam: props.exam,
    options: options.value,
    actualPrintedCount: Number(actualPrintedCount.value || 0),
    notes: operatorNotes.value,
  })
}
</script>

<style scoped>
.modal-top-stripe {
  height: 4px;
  background: rgb(var(--v-theme-primary));
}

.summary-item-header {
  display: flex !important;
  align-items: center !important;
}

.summary-item-avatar {
  margin-inline-end: 12px !important;
  flex-shrink: 0 !important;
}

.center-count-badge {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  color: rgb(var(--v-theme-primary)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.22) !important;
  border-radius: 6px !important;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.unified-badge-primary {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  color: rgb(var(--v-theme-primary)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.25) !important;
}

.unified-badge-teal {
  background: rgba(0, 150, 136, 0.1) !important;
  color: #00897b !important;
  border: 1px solid rgba(0, 150, 136, 0.25) !important;
}

.unified-badge-warning {
  background: rgba(245, 124, 0, 0.1) !important;
  color: #e65100 !important;
  border: 1px solid rgba(245, 124, 0, 0.25) !important;
}

.unified-badge-default {
  background: rgba(var(--v-theme-on-surface), 0.06) !important;
  color: rgb(var(--v-theme-on-surface)) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.18) !important;
}

.font-mono {
  font-family: monospace, monospace;
}

.filter-fields-row {
  margin-inline: -8px !important;
}

.filter-fields-row > [class*="v-col"] {
  padding-inline: 8px !important;
}

.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}
</style>
