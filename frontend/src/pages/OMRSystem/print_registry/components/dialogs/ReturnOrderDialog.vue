<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="560px" persistent>
    <v-card rounded="2xl" class="border elevation-6 overflow-hidden main-card">
      <v-card-title class="d-flex align-center justify-space-between bg-surface pa-4 px-6 border-b">
        <div class="d-flex align-center gap-3">
          <v-avatar color="warning" variant="tonal" size="40" class="rounded-xl">
            <v-icon color="warning" size="22">mdi-keyboard-return</v-icon>
          </v-avatar>
          <div>
            <div class="text-subtitle-1 font-weight-black text-on-surface">إرجاع طلب الطباعة للتعديل</div>
            <div class="text-caption text-medium-emphasis">تسجيل ملاحظات وأسباب الإرجاع لمسؤول الإدخال</div>
          </div>
        </div>
        <v-btn icon="mdi-close" variant="text" size="small" @click="$emit('update:modelValue', false)" />
      </v-card-title>

      <v-card-text class="pa-5 bg-surface text-right">
        <div class="pa-3 rounded-xl bg-surface-variant-subtle border mb-4">
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
            :hideDetails="true"
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
      </v-card-text>

      <v-card-actions class="pa-4 bg-surface border-t d-flex justify-space-between align-center">
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
      </v-card-actions>
    </v-card>
  </v-dialog>
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
