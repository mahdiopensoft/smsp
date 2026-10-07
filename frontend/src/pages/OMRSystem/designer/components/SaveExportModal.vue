<template>
  <v-dialog :model-value="modelValue" max-width="560" @update:model-value="emit('update:modelValue', $event)">
    <v-card class="pa-6 rounded-2xl">
      <div class="d-flex align-center justify-space-between mb-4 pb-2 border-b">
        <div class="d-flex align-center gap-2">
          <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
            <v-icon color="primary" size="20">mdi-content-save-outline</v-icon>
          </v-avatar>
          <h3 class="text-h6 font-weight-black mb-0">حفظ القالب الهندسي في النظام</h3>
        </div>
        <v-btn icon size="small" variant="text" @click="emit('update:modelValue', false)">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </div>

      <div class="mb-4">
        <v-text-field
          v-model="form.name"
          label="اسم القالب المعياري *"
          placeholder="مثال: نموذج اختبار الشهادة الثانوية العامة (50 سؤال)"
          variant="outlined"
          density="comfortable"
          rounded="lg"
          class="mb-3"
          @update:model-value="onNameInput"
        />
        <v-text-field
          v-model="form.subject_name"
          label="المادة الدراسية / التخصص *"
          placeholder="مثال: القرآن الكريم والتربية الإسلامية"
          variant="outlined"
          density="comfortable"
          rounded="lg"
          class="mb-3"
          @update:model-value="userManuallyEditedSubject = true"
        />
        <v-row dense class="mb-3">
          <v-col cols="6">
            <v-text-field
              v-model="form.version"
              label="رقم الإصدار"
              placeholder="1.0"
              variant="outlined"
              density="comfortable"
              rounded="lg"
              hide-details
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              :model-value="totalQuestions"
              label="إجمالي الأسئلة"
              variant="outlined"
              density="comfortable"
              rounded="lg"
              disabled
              hide-details
            />
          </v-col>
        </v-row>
        <v-textarea
          v-model="form.description"
          label="الوصف والملاحظات الفنية"
          rows="3"
          variant="outlined"
          density="comfortable"
          rounded="lg"
        />
      </div>

      <div class="d-flex justify-end gap-2">
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
      </div>
    </v-card>
  </v-dialog>
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
