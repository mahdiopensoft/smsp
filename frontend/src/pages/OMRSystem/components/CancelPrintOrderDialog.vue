<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="600px"
    scrollable
    persistent
  >
    <v-card class="rounded-2xl overflow-hidden print-order-modal bg-surface elevation-8 border" style="background: rgb(var(--v-theme-surface)) !important;">
      <!-- ── شريط الهوية العلوي المعتمد ── -->
      <div class="modal-top-stripe-error" />

      <!-- ── 1. ترويسة النافذة الرسمية الموحدة ── -->
      <div class="px-5 py-4 d-flex align-center justify-space-between border-b bg-surface">
        <div class="d-flex align-center gap-3">
          <v-avatar color="error" variant="tonal" size="44" rounded="lg">
            <v-icon size="24" color="error">mdi-cancel</v-icon>
          </v-avatar>
          <div>
            <div class="d-flex align-center gap-2">
              <h3 class="text-subtitle-1 font-weight-black text-high-emphasis mb-0">إلغاء أمر الطباعة رسمياً</h3>
              <div class="center-count-badge unified-badge-error px-2.5 py-0.5 text-caption font-weight-bold">
                إلغاء رسمي معتمد
              </div>
            </div>
            <div class="text-caption text-medium-emphasis">
              توثيق قرار الإلغاء ونقل الطلب إلى تبويب [الملغية]
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
        <!-- بطاقة تفاصيل الاختبار المراد إلغاء أمره -->
        <div class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-4 mx-auto elevation-1" style="max-width: 600px;">
          <!-- اسم الاختبار والمادة -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="error" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="error">mdi-book-education-outline</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">الاختبار والمادة:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <span class="font-weight-bold text-body-2 text-high-emphasis">{{ exam?.title || 'الاختبار' }}</span>
              <div class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold">
                المادة: {{ exam?.subject_name || 'شبكات الحاسوب والتقنيات الرقمية' }}
              </div>
            </div>
          </div>

          <!-- كود الاختبار والطلاب المقيدون -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="error" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="error">mdi-identifier</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">كود الاختبار والطلاب:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <div class="center-count-badge px-3 py-1 font-mono font-weight-bold text-caption text-high-emphasis">
                {{ exam?.uniqueCode || 'EXAM-INST-001' }}
              </div>
              <div class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold font-mono">
                المقيدون: {{ exam?.total_registered || exam?.total_students || 8 }} طالب
              </div>
            </div>
          </div>
        </div>

        <!-- بطاقة الحقول الموحدة لمبرر الإلغاء ورقم القرار -->
        <div class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-2 mx-auto elevation-1" style="max-width: 600px;">
          <div class="d-flex align-center gap-2 mb-3 text-subtitle-2 font-weight-bold text-high-emphasis">
            <v-avatar color="error" variant="tonal" size="30" rounded="lg">
              <v-icon size="18" color="error">mdi-alert-octagon-outline</v-icon>
            </v-avatar>
            <span>بيانات وقرار إلغاء أمر الطباعة</span>
          </div>

          <v-row class="align-start filter-fields-row" dense>
            <!-- سبب الإلغاء الرسمي عبر AutoList الموحد -->
            <auto-list
              v-model="reasonSelected"
              :objects="reasonObjects"
              name="ScreenTypeChoices"
              label="سبب الإلغاء الرسمي *"
              placeholder="اختر سبب الإلغاء الرسمي"
              cols="12"
              icon="alert-octagon-outline"
              :add="false"
              :hideDetails="true"
            />

            <!-- ملاحظات أو رقم قرار اللجنة (اختياري) باستخدام CustomTextField الموحد -->
            <custom-text-field
              v-model="notes"
              label="ملاحظات أو رقم قرار اللجنة (اختياري)"
              placeholder="مثال: محضر اجتماع الكنترول رقم 14 بتاريخ اليوم..."
              icon="text-box-edit-outline"
              cols="12"
              :hideDetails="true"
            />
          </v-row>

          <!-- تنبيه توضيحي رسمي بلون error -->
          <v-alert
            type="error"
            variant="tonal"
            density="compact"
            rounded="lg"
            class="mt-4 py-2"
          >
            <template #prepend>
              <v-icon size="20">mdi-alert-circle</v-icon>
            </template>
            <div class="text-caption">
              عند تأكيد الإلغاء، سيتم إيقاف أمر السحب ونقل هذا الاختبار فوراً إلى تبويب <strong>[الملغية]</strong> ولن يظهر في الطلبات النشطة أو المستحقة.
            </div>
          </v-alert>
        </div>
      </v-card-text>

      <!-- ── 3. أزرار التحكم الرسمية الموحدة ── -->
      <div class="px-5 py-3.5 d-flex align-center justify-space-between border-t bg-surface">
        <v-btn
          variant="tonal"
          color="secondary"
          rounded="lg"
          class="font-weight-bold px-4"
          prepend-icon="mdi-arrow-right"
          :disabled="loading"
          @click="close"
        >
          تراجع
        </v-btn>

        <v-btn
          color="error"
          variant="flat"
          rounded="lg"
          class="font-weight-bold px-6 text-white"
          prepend-icon="mdi-cancel"
          :loading="loading"
          @click="submit"
        >
          تأكيد إلغاء أمر الطباعة
        </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    exam?: any
    loading?: boolean
  }>(),
  {
    modelValue: false,
    exam: null,
    loading: false,
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'confirm', payload: { exam: any; reason: string; notes: string }): void
}>()

const reasonsList = [
  'تم إلغاء الاختبار بقرار من إدارة الامتحانات والكنترول',
  'تعديل في نماذج الأسئلة أو كراسات الاختبار',
  'تكرار أمر الطباعة أو وجود طلب سابق',
  'تغيير موعد الاختبار وتأجيله لموعد غير محدد',
  'تعذر طباعة الوثائق لظروف طارئة بالمطبعة',
  'أسباب إدارية وتنظيمية أخرى',
]

const reasonObjects = computed(() => {
  return reasonsList.map(r => ({
    id: r,
    name: r,
    name_ar: r,
  }))
})

const reasonSelected = ref(reasonsList[0])
const notes = ref('')

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      reasonSelected.value = reasonsList[0]
      notes.value = ''
    }
  }
)

const close = () => {
  emit('update:modelValue', false)
}

const submit = () => {
  emit('confirm', {
    exam: props.exam,
    reason: reasonSelected.value,
    notes: notes.value,
  })
}
</script>

<style scoped>
.modal-top-stripe-error {
  height: 4px;
  background: rgb(var(--v-theme-error));
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

.unified-badge-error {
  background: rgba(var(--v-theme-error), 0.1) !important;
  color: rgb(var(--v-theme-error)) !important;
  border: 1px solid rgba(var(--v-theme-error), 0.25) !important;
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

