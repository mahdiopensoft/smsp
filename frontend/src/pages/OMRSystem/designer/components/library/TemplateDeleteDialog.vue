<template>
  <custom-dialog
    :model-value="modelValue"
    title="تأكيد حذف القالب"
    width="480"
    height="auto"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <p class="text-caption text-medium-emphasis mb-3">عملية الحذف نهائية ولا يمكن التراجع عنها</p>
    <p class="text-body-2 mb-0">
      هل أنت متأكد من رغبتك في حذف القالب المعياري
      <strong class="text-error">«{{ templateToDelete?.name }}»</strong>؟
    </p>
    <template #actions>
      <v-btn variant="text" rounded="lg" class="font-weight-bold" @click="$emit('update:modelValue', false)">
        إلغاء
      </v-btn>
      <v-btn
        color="error"
        rounded="lg"
        class="font-weight-bold px-6"
        :loading="isDeleting"
        @click="$emit('confirm')"
      >
        نعم، احذف القالب
      </v-btn>
    </template>
  </custom-dialog>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  templateToDelete: any
  isDeleting: boolean
}>()

defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'confirm'): void
}>()
</script>
