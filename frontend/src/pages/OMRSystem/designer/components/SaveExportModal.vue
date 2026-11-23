<template>
  <custom-dialog
    :model-value="modelValue"
    title="حفظ القالب الهندسي في النظام"
    width="560"
    height="auto"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <v-row dense class="mb-2">
      <custom-text-field
        v-model="form.name"
        label="اسم القالب المعياري *"
        placeholder="مثال: نموذج اختبار الشهادة الثانوية العامة (50 سؤال)"
        icon="file-document-outline"
        cols="12"
        :clearable="false"
        @update:model-value="onNameInput"
      />
      <custom-text-field
        v-model="form.subject_name"
        label="المادة الدراسية / التخصص *"
        placeholder="مثال: القرآن الكريم والتربية الإسلامية"
        icon="book-open-outline"
        cols="12"
        :clearable="false"
        @update:model-value="userManuallyEditedSubject = true"
      />
      <custom-text-field
        v-model="form.version"
        label="رقم الإصدار"
        placeholder="1.0"
        icon="tag-outline"
        cols="6"
        :clearable="false"
      />
      <custom-text-field
        :model-value="totalQuestions"
        label="إجمالي الأسئلة"
        icon="help-circle-outline"
        cols="6"
        :clearable="false"
        :disabled="true"
      />
      <custom-text-note
        v-model="form.description"
        label="الوصف والملاحظات الفنية"
        icon="text-box-outline"
        cols="12"
        :rows="3"
        :hideDetails="true"
        :clearable="false"
      />
    </v-row>

    <template #actions>
      <v-btn variant="text" rounded="lg" class="font-weight-bold" @click="emit('update:modelValue', false)">
        إلغاء
      </v-btn>
      <v-btn
        color="primary"
        rounded="lg"
        class="font-weight-bold px-6"
        :loading="isSaving"
        :disabled="!form.name?.trim()"
        @click="handleSave"
      >
        تأكيد الحفظ والتوثيق
      </v-btn>
    </template>
  </custom-dialog>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

const props = defineProps<{
  modelValue: boolean
  isSaving?: boolean
  initialName?: string
  initialSubject?: string
  initialDescription?: string
  initialVersion?: string
  totalQuestions?: number
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: boolean): void
  (e: 'save', form: any): void
}>()

let userManuallyEditedSubject = false

const form = reactive({
  name: props.initialName || '',
  subject_name: props.initialSubject || '',
  version: props.initialVersion || '1.0',
  description: props.initialDescription || '',
})

watch(() => props.modelValue, (val) => {
  if (val) {
    form.name = props.initialName || ''
    form.subject_name = props.initialSubject || props.initialName || ''
    form.version = props.initialVersion || '1.0'
    form.description = props.initialDescription || ''
    userManuallyEditedSubject = false
  }
})

function onNameInput(val: string) {
  if (!userManuallyEditedSubject || !form.subject_name || form.subject_name === 'القرآن الكريم') {
    form.subject_name = val
  }
}

function handleSave() {
  if (!form.name?.trim()) return
  if (!form.subject_name?.trim()) {
    form.subject_name = form.name.trim()
  }
  emit('save', {
    ...form,
    name: form.name.trim(),
    subject_name: form.subject_name.trim(),
    version: form.version?.trim() || '1.0',
    description: form.description?.trim() || '',
  })
}
</script>
