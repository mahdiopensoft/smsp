<template>
  <custom-dialog
    :model-value="modelValue"
    title="تقديم موعد الطباعة استثنائياً"
    width="620"
    height="auto"
    persistent
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div class="d-flex align-center gap-2 mb-4 pb-3 border-b">
      <div class="center-count-badge unified-badge-warning px-2.5 py-0.5 text-caption font-weight-bold">
        صلاحية استثنائية
      </div>
      <span class="text-caption text-medium-emphasis">
        صلاحية استثنائية لتقديم التنفيذ مع توثيق السبب والمسؤول
      </span>
    </div>

    <!-- بطاقة تفاصيل الاختبار والجدولة الحالية -->
        <div class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-4 mx-auto elevation-1" style="max-width: 600px;">
          <!-- الاختبار والمادة -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="warning" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="warning">mdi-book-education-outline</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">اسم الاختبار:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <span class="font-weight-bold text-body-2 text-high-emphasis">{{ exam?.title || 'الاختبار المجدول' }}</span>
              <div v-if="exam?.subject_name" class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold">
                {{ exam.subject_name }}
              </div>
            </div>
          </div>

          <!-- كود الاختبار -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="warning" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="warning">mdi-identifier</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">كود الاختبار:</span>
            </div>
            <div class="center-count-badge px-3 py-1 font-mono font-weight-bold text-caption text-high-emphasis">
              {{ exam?.uniqueCode || '—' }}
            </div>
          </div>

          <!-- الموعد الحالي المجدول -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="warning" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="warning">mdi-calendar-clock</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">الموعد الحالي المجدول:</span>
            </div>
            <div class="center-count-badge unified-badge-warning px-3 py-1 font-mono font-weight-black text-subtitle-2">
              {{ exam?.scheduled_print_date || 'غير محدد' }}
            </div>
          </div>
        </div>

        <!-- بطاقة الحقول الموحدة للمبرر والتوجيه الرسمي -->
        <div class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-2 mx-auto elevation-1" style="max-width: 600px;">
          <div class="d-flex align-center gap-2 mb-3 text-subtitle-2 font-weight-bold text-high-emphasis">
            <v-avatar color="warning" variant="tonal" size="30" rounded="lg">
              <v-icon size="18" color="warning">mdi-shield-check-outline</v-icon>
            </v-avatar>
            <span>بيانات الإذن الاستثنائي والأساس النظامي</span>
          </div>

          <v-row class="align-start filter-fields-row" dense>
            <!-- مبرر تقديم الموعد (الأساس النظامي) عبر AutoList الموحد -->
            <auto-list
              v-model="reasonSelected"
              :objects="reasonObjects"
              name="ScreenTypeChoices"
              label="مبرر تقديم الموعد (الأساس النظامي) *"
              placeholder="اختر مبرر تقديم الموعد"
              cols="12"
              icon="shield-check-outline"
              :add="false"
            />

            <!-- رقم توجيه الإذن الاستثنائي / المذكرة الرسمية عبر CustomTextField الموحد -->
            <custom-text-field
              v-model="authDoc"
              label="رقم توجيه الإذن الاستثنائي / المذكرة الرسمية *"
              placeholder="مثال: إذن وزاري رقم ق/1446/78 بتاريخ اليوم"
              icon="file-certificate-outline"
              cols="12"
              :isRequired="true"
            />
          </v-row>

          <!-- تنبيه توضيحي رسمي -->
          <v-alert
            type="warning"
            variant="tonal"
            density="compact"
            rounded="lg"
            class="mt-4 py-2"
          >
            <template #prepend>
              <v-icon size="20">mdi-information</v-icon>
            </template>
            <div class="text-caption">
              عند تأكيد التقديم، سينتقل هذا الاختبار فوراً من قائمة <strong>المجدولة</strong> إلى قائمة <strong>المستحقة</strong> للتنفيذ اليوم.
            </div>
          </v-alert>
        </div>

    <template #actions>
      <div class="d-flex align-center justify-space-between w-100">
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
          color="warning"
          variant="flat"
          rounded="lg"
          class="font-weight-bold px-6 text-black"
          prepend-icon="mdi-fast-forward"
          :loading="loading"
          @click="submit"
        >
          تأكيد التقديم لليوم
        </v-btn>
      </div>
    </template>
  </custom-dialog>
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
  (e: 'confirm', payload: { exam: any; reason: string; authDoc: string }): void
}>()

const reasonsList = [
  'شحن وترحيل مبكر لمحافظات بعيدة أو نائية (سقطرى، المهرة، إلخ)',
  'توجيه استثنائي من وزير التربية والتعليم / رئيس اللجنة العليا',
  'توفير احتياط مبكر للمطبعة المركزية لتفادي ضغط جدول العمليات',
  'طلب رسمي مسبق من قيادة المركز الامتحاني بالمحافظة',
  'أسباب تنظيمية وطوارئ نقل وتأمين الوثائق',
]

const reasonObjects = computed(() => {
  return reasonsList.map(r => ({
    id: r,
    name: r,
    name_ar: r,
  }))
})

const reasonSelected = ref(reasonsList[0])
const authDoc = ref('')

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      reasonSelected.value = reasonsList[0]
      authDoc.value = ''
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
    authDoc: authDoc.value,
  })
}
</script>

<style scoped>
.modal-top-stripe-warning {
  height: 4px;
  background: rgb(var(--v-theme-warning));
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

.unified-badge-warning {
  background: rgba(245, 124, 0, 0.1) !important;
  color: #e65100 !important;
  border: 1px solid rgba(245, 124, 0, 0.25) !important;
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

