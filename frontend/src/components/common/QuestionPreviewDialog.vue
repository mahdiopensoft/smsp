<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="700">
    <v-card class="glass-card pa-0 rounded-xl" v-if="question">
      <!-- Elegant Header -->
      <div class="px-6 py-4 d-flex justify-space-between align-center border-b" style="background: rgba(var(--v-theme-primary), 0.03);">
        <div class="d-flex align-center">
          <v-avatar color="primary-lighten-4" class="text-primary me-3 rounded-lg" size="40">
            <v-icon>mdi-file-document-outline</v-icon>
          </v-avatar>
          <span class="text-h6 font-weight-bold">تفاصيل السؤال</span>
        </div>
        <div class="d-flex align-center gap-2">
          <v-chip v-if="question.status" :color="getStatusColor(question.status)" variant="tonal" size="small" class="font-weight-bold elevation-1 px-3">
            {{ getStatusText(question.status) }}
          </v-chip>
          <v-btn icon variant="text" size="small" color="secondary" @click="$emit('update:modelValue', false)">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
      </div>

      <v-card-text class="pa-6">
        <!-- Question Text -->
        <div class="question-box pa-5 rounded-lg mb-6 border" style="background: rgba(var(--v-theme-surface-variant), 0.3);">
          <div class="d-flex align-center mb-3 text-primary">
            <v-icon start size="small">mdi-comment-question-outline</v-icon>
            <span class="text-subtitle-2 font-weight-bold">نص السؤال</span>
          </div>
          <div class="text-body-1 font-weight-medium" style="line-height: 1.8;" v-html="parseScientificMarkup(question.content)"></div>
          <v-img
            v-if="question.image"
            :src="question.image"
            max-height="300"
            class="mt-4 rounded-lg elevation-1"
            contain
          />
        </div>

        <!-- Options -->
         <div v-if="answers.length > 0" class="mb-6">
          <div class="d-flex align-center mb-3 text-secondary">
            <v-icon start size="small">mdi-format-list-checks</v-icon>
            <span class="text-subtitle-2 font-weight-bold">الإجابات</span>
          </div>
           <v-list class="bg-transparent pa-0">
            <v-list-item
              v-for="(answer, index) in answers"
              :key="answer.id || index"
              :class="answer.isTrue ? 'border-success bg-success-lighten-5' : 'border-opacity-25'"
              class="mb-2 rounded-lg border pa-2"
            >
              <template v-slot:prepend>
                <v-avatar
                  :color="answer.isTrue ? 'success' : 'surface-variant'"
                  size="32"
                  class="me-3"
                  :class="!answer.isTrue ? 'opacity-50' : ''"
                >
                  <span :class="answer.isTrue ? 'text-white font-weight-bold' : ''">{{ String.fromCharCode(65 + index) }}</span>
                </v-avatar>
              </template>
              <v-list-item-title class="text-body-2 font-weight-medium" :class="answer.isTrue ? 'text-success' : ''" v-html="parseScientificMarkup(answer.text)"></v-list-item-title>
              <template v-slot:append>
                <v-icon
                  v-if="answer.isTrue"
                  color="success"
                >
                  mdi-check-circle
                </v-icon>
              </template>
            </v-list-item>
          </v-list>
         </div>
         
         <div v-else-if="question.questionType === 'True/False'" class="mb-6">
             <div class="d-flex align-center mb-3 text-secondary">
                <v-icon start size="small">mdi-check-network-outline</v-icon>
                <span class="text-subtitle-2 font-weight-bold">الإجابة الصحيحة</span>
             </div>
              <v-chip
                :color="question.isTrue ? 'success' : 'error'"
                variant="tonal"
                size="large"
                class="font-weight-bold elevation-1 px-4"
              >
                <v-icon start>
                  {{ question.isTrue ? 'mdi-check-circle' : 'mdi-close-circle' }}
                </v-icon>
                {{ question.isTrue ? 'صواب' : 'خطأ' }}
              </v-chip>
         </div>


        <!-- Meta -->
        <div class="pa-4 rounded-lg bg-surface-variant bg-opacity-20 border">
          <v-row no-gutters>
            <v-col cols="6" sm="3" class="mb-2 mb-sm-0">
              <div class="text-caption text-medium-emphasis mb-1 d-flex align-center"><v-icon size="14" class="me-1">mdi-star-circle</v-icon> الدرجة</div>
              <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                {{ question.defaultMark || question.defaultScore || 1 }} {{ (question.defaultMark || question.defaultScore || 1) == 1 ? 'درجة' : 'درجات' }}
              </v-chip>
            </v-col>
            <v-col cols="6" sm="3" class="mb-2 mb-sm-0">
              <div class="text-caption text-medium-emphasis mb-1 d-flex align-center"><v-icon size="14" class="me-1">mdi-book-open-page-variant</v-icon> المادة</div>
              <v-chip size="small" color="info" variant="tonal" class="font-weight-bold">
                {{ getSubjectName(question) }}
              </v-chip>
            </v-col>
            <v-col cols="6" sm="3">
              <div class="text-caption text-medium-emphasis mb-1 d-flex align-center"><v-icon size="14" class="me-1">mdi-speedometer</v-icon> الصعوبة</div>
              <v-chip size="small" :color="getDifficultyColor(question.difficulty)" variant="tonal" class="font-weight-bold">
                {{ getDifficultyText(question.difficulty) }}
              </v-chip>
            </v-col>
            <v-col cols="6" sm="3">
              <div class="text-caption text-medium-emphasis mb-1 d-flex align-center"><v-icon size="14" class="me-1">mdi-brain</v-icon> مستوى بلوم</div>
              <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
                {{ getBloomText(question.bloomLevel) }}
              </v-chip>
            </v-col>
          </v-row>
        </div>
      </v-card-text>

      <v-card-actions class="px-6 pb-6 pt-0">
        <v-spacer />
        <v-btn variant="outlined" class="rounded-lg px-4" @click="$emit('update:modelValue', false)">إغلاق</v-btn>
        <v-btn v-if="showEdit" color="primary" variant="tonal" class="rounded-lg px-6 font-weight-bold elevation-1 ms-3" :disabled="question.status === 'معتمد'" @click="onEditClick">
          <v-icon start>mdi-pencil</v-icon>
          تعديل السؤال
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDataStore } from '@/stores/dataStore'
import { parseScientificMarkup, ensureKaTeXLoaded } from '@/utils/scientificRenderer'

onMounted(() => {
  ensureKaTeXLoaded()
})

const props = defineProps({
  modelValue: Boolean,
  question: Object,
  showEdit: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'edit'])

const store = useDataStore()

const extractId = (val) => {
    if (!val) return null
    if (typeof val === 'object' && val.id) return Number(val.id)
    return Number(val)
}

const answers = computed(() => {
    if (!props.question) return []
    // If answers are pre-loaded (e.g. from bulk import local state)
    if (props.question.options && Array.isArray(props.question.options) && props.question.options.length > 0 && typeof props.question.options[0] === 'object' && props.question.options[0].text) {
        return props.question.options
    }
    if (props.question.options && Array.isArray(props.question.options) && typeof props.question.options[0] === 'string') {
        // Handle raw string options (from import)
        return props.question.options.map((opt, idx) => ({
            text: opt,
            isTrue: props.question.correctAnswerIndex === idx || (props.question.correctAnswerIndices || []).includes(idx)
        }))
    }
    
    // Fallback: load from store (for index.vue)
    const allAnswers = store.getAll('answers')
    return allAnswers.filter(a => extractId(a.question) === extractId(props.question.id))
})

const getSubjectName = (q) => {
  if (!q) return 'غير محدد'
  // Try direct subject ID if it exists (from bulk import)
  if (q.subject_id) {
    const subject = store.getById('subjects', q.subject_id)
    return subject ? subject.name : 'غير محدد'
  }
  
  const lessonId = q.lesson_id || q.lesson
  if (!lessonId) return 'غير محدد'
  const extractedLessonId = extractId(lessonId)
  
  const lesson = store.getById('lessons', extractedLessonId)
  if (!lesson) return 'غير محدد'
  const unitId = typeof lesson.unit === 'object' ? lesson.unit.id : (lesson.unitId || lesson.unit)
  const unit = store.getById('units', unitId)
  if (!unit) return 'غير محدد'
  const lsbId = typeof unit.level_subject_branch === 'object' ? unit.level_subject_branch.id : (unit.levelSubjectBranchId || unit.level_subject_branch)
  const lsb = store.getById('levelSubjectBranches', lsbId)
  if (!lsb) return 'غير محدد'
  const subjectId = typeof lsb.subject === 'object' ? lsb.subject.id : (lsb.subjectId || lsb.subject)
  const subject = store.getById('subjects', subjectId)
  return subject ? subject.name : 'غير محدد'
}

const getStatusColor = (status) => {
    switch (status) {
        case 'معتمد': return 'success'
        case 'مرفوض': return 'error'
        case 'قيد المراجعة': return 'warning'
        case 'مسودة': return 'info'
        case 'مستورد': return 'secondary'
        default: return 'grey'
    }
}

const getStatusText = (status) => status || 'غير معروف'

const getDifficultyText = (level) => {
  if (level === 1 || level === 'سهل') return 'سهل'
  if (level === 2 || level === 'متوسط') return 'متوسط'
  if (level === 3 || level === 'صعب') return 'صعب'
  return level || '-'
}

const getDifficultyColor = (level) => {
  if (level === 1 || level === 'سهل') return 'success'
  if (level === 2 || level === 'متوسط') return 'warning'
  if (level === 3 || level === 'صعب') return 'error'
  return 'grey'
}

const getBloomText = (level) => level || '-'

const onEditClick = () => {
  emit('edit', props.question)
  emit('update:modelValue', false)
}
</script>
