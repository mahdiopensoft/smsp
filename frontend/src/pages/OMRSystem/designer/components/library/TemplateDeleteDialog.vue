<template>
  <v-dialog :model-value="modelValue" max-width="480" @update:model-value="$emit('update:modelValue', $event)">
    <v-card class="pa-6 rounded-2xl">
      <div class="d-flex align-center gap-3 mb-4">
        <v-avatar color="error" variant="tonal" size="48" rounded="xl">
          <v-icon size="28" color="error">mdi-alert-outline</v-icon>
        </v-avatar>
        <div>
          <h3 class="text-h6 font-weight-black mb-0">تأكيد حذف القالب</h3>
          <span class="text-caption text-medium-emphasis">عملية الحذف نهائية ولا يمكن التراجع عنها</span>
        </div>
      </div>
      <p class="text-body-2 mb-6">
        هل أنت متأكد من رغبتك في حذف القالب المعياري
        <strong class="text-error">«{{ templateToDelete?.name }}»</strong>؟
      </p>
      <div class="d-flex justify-end gap-2">
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
      </div>
    </v-card>
  </v-dialog>
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
