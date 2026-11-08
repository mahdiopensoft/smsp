<template>
  <v-dialog :model-value="modelValue" max-width="600" @update:model-value="$emit('update:modelValue', $event)">
    <v-card class="pa-6 rounded-2xl">
      <div class="d-flex align-center justify-space-between mb-4 pb-2 border-b">
        <div class="d-flex align-center gap-2">
          <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
            <v-icon color="primary" size="20">mdi-database-import-outline</v-icon>
          </v-avatar>
          <h3 class="text-h6 font-weight-black mb-0">استيراد مواصفات اختبار وبناء القالب آلياً</h3>
        </div>
        <v-btn icon size="small" variant="text" @click="$emit('update:modelValue', false)">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </div>

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
        :hideDetails="true"
        :loading="loading"
        class="mb-3"
      />

      <div class="d-flex justify-end gap-2 mt-4">
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
      </div>
    </v-card>
  </v-dialog>
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
