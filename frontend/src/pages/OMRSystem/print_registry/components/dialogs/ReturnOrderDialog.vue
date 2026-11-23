<template>
  <custom-dialog
    :model-value="modelValue"
    title="إرجاع طلب الطباعة للتعديل"
    width="560"
    height="auto"
    persistent
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div class="text-caption text-medium-emphasis mb-3">
      تسجيل ملاحظات وأسباب الإرجاع لمسؤول الإدخال
    </div>

    <div class="pa-3 rounded-xl bg-surface-variant-subtle border mb-4 text-right">
      <div class="text-subtitle-2 font-weight-bold text-on-surface mb-1">
        {{ exam?.title }}
      </div>
      <div class="text-caption text-medium-emphasis">
        الكود: <span class="font-mono text-primary font-weight-bold">{{ exam?.uniqueCode }}</span>
      </div>
    </div>

    <!-- أسباب الإرجاع الشائعة عبر auto-list الموحد -->
    <div class="mb-4">
      <auto-list
        :model-value="reason"
        @update:model-value="$emit('update:reason', $event)"
        :objects="reasonObjects"
        name="ScreenTypeChoices"
        label="سبب الإرجاع الرئيسي"
        placeholder="اختر سبب الإرجاع الرئيسي"
        cols="12"
        :add="false"
      />
    </div>

    <!-- تفاصيل وملاحظات إضافية عبر custom-text-note الموحد -->
    <div class="mb-2">
      <custom-text-note
        :model-value="notes"
        @update:model-value="$emit('update:notes', $event)"
        rows="3"
        label="ملاحظات وتوجيهات التعديل المطلوبة"
        placeholder="يرجى كتابة التعديلات المطلوبة بدقة ليتمكن المُنشئ من معالجتها..."
        cols="12"
        :hideDetails="true"
      />
    </div>

    <template #actions>
      <div class="d-flex justify-space-between align-center w-100">
        <v-btn variant="tonal" color="grey" rounded="lg" class="font-weight-bold px-4" @click="$emit('update:modelValue', false)">
          إلغاء
        </v-btn>
        <v-btn
          color="warning"
          variant="flat"
          rounded="lg"
          class="font-weight-bold px-6"
          prepend-icon="mdi-keyboard-return"
          :loading="loading"
          @click="$emit('confirm')"
        >
          تأكيد إرجاع الطلب
        </v-btn>
      </div>
    </template>
  </custom-dialog>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  exam: any
  reason: any
  reasonObjects: any[]
  notes: string
  loading?: boolean
}>()

defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'update:reason', val: any): void
  (e: 'update:notes', val: string): void
  (e: 'confirm'): void
}>()
</script>
