<template>
  <custom-dialog
    :model-value="modelValue"
    title="استيراد مواصفات اختبار وبناء القالب آلياً"
    width="600"
    height="auto"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <p class="text-caption text-medium-emphasis mb-4">
      اختر أحد الاختبارات المعتمدة من بنك الأسئلة ليتم استيراد ترويسته، عدد أسئلته، أقسامه، ونماذجه تلقائياً في المصمم.
    </p>

    <auto-list
      v-model="selectedExamId"
      name="ScreenTypeChoices"
      :objects="formattedExamsList"
      label="اختر الاختبار المراد استيراد مواصفاته *"
      placeholder="ابحث باسم الاختبار أو رمزه أو المادة..."
      cols="12"
      :add="false"
      :loading="loading"
      class="mb-3"
    />

    <template #actions>
      <v-btn variant="text" rounded="lg" class="font-weight-bold" @click="$emit('update:modelValue', false)">
        إلغاء
      </v-btn>
      <v-btn
        color="primary"
        rounded="lg"
        class="font-weight-bold px-6"
        :disabled="!selectedExamId"
        @click="confirmSelection"
      >
        استيراد وتوليد القالب
      </v-btn>
    </template>
  </custom-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import api from '@/services/omr/client.js'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'import-exam', examId: number): void
}>()

const selectedExamId = ref<number | null>(null)
const examsList = ref<any[]>([])
const loading = ref(false)

const formattedExamsList = computed(() => {
  return examsList.value.map((exam) => ({
    id: exam.id,
    name: `${exam.title} (${exam.subject_name || 'بدون مادة'} - ${exam.uniqueCode || ''} - ${exam.total_questions || 50} سؤال)`,
    title: `${exam.title} (${exam.subject_name || 'بدون مادة'} - ${exam.uniqueCode || ''} - ${exam.total_questions || 50} سؤال)`,
  }))
})

async function fetchExams() {
  if (examsList.value.length > 0) return
  loading.value = true
  try {
    const resp = await api.get('/api/omr/exam-linking/')
    if (resp.data?.results) {
      examsList.value = resp.data.results
    }
  } catch (err) {
    console.error('Failed to load exams for import:', err)
  } finally {
    loading.value = false
  }
}

watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    fetchExams()
  } else {
    selectedExamId.value = null
  }
})

function confirmSelection() {
  if (selectedExamId.value) {
    emit('import-exam', selectedExamId.value)
    emit('update:modelValue', false)
  }
}
</script>
