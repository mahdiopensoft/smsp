<template>
  <div class="qb-print-questions-v4 pa-4 pa-md-8">
    <!-- Non-printable Action Header -->
    <div class="d-print-none mb-6 d-flex align-center justify-space-between flex-wrap gap-3 pa-4 rounded-2xl main-card">
      <div class="d-flex align-center">
        <back-to class="me-2" @click="router.back()" />
        <v-avatar size="40" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="22">mdi-file-document-edit-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h6 font-weight-black mb-0">معاينة وطباعة ورقة الأسئلة</h1>
          <span class="text-caption text-medium-emphasis">نسخة ورقة الاختبار الرسمية المخصصة للطباعة والتوزيع</span>
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <custom-btn
          type="add"
          label="طباعة ورقة الأسئلة"
          icon="mdi-printer"
          color="primary"
          class="font-weight-bold px-6"
          :click="print"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12 main-card rounded-2xl">
      <v-progress-circular indeterminate color="primary" size="48" class="mb-3" />
      <p class="text-subtitle-1 font-weight-bold">جاري تحميل بيانات الاختبار والأسئلة...</p>
    </div>

    <!-- Printable Exam Paper Sheet -->
    <div class="print-paper-sheet pa-8 rounded-2xl mx-auto" v-else-if="exam">
      <!-- Exam Header -->
      <div class="exam-paper-header mb-8 pb-6 border-b-2 border-slate-300 text-center">
        <div class="text-caption text-medium-emphasis mb-1">{{ ministryHeading }}</div>
        <h1 class="text-h4 font-weight-black mb-3">{{ exam.title }}</h1>
        <div class="d-flex justify-center flex-wrap gap-4 text-body-1 font-weight-bold mb-4">
          <span class="paper-badge"><strong>المادة:</strong> {{ subjectName }}</span>
          <span class="paper-badge"><strong>{{ exam.institution_type === 'institute' ? 'التخصص:' : exam.institution_type === 'university' ? 'القسم:' : 'الصف:' }}</strong> {{ levelName }}</span>
          <span class="paper-badge"><strong>الزمن:</strong> ساعتان</span>
          <span class="paper-badge"><strong>الدرجة الكلية:</strong> {{ totalScore }}</span>
        </div>

        <div class="student-info-box pa-3 rounded-xl d-flex justify-space-between align-center flex-wrap gap-3 mt-4 text-body-2">
          <div class="flex-grow-1 text-start">
            اسم الطالب: <span class="dotted-underline flex-grow-1 d-inline-block" style="min-width: 250px;"></span>
          </div>
          <div class="text-end">
            رقم الجلوس: <span class="dotted-underline d-inline-block" style="min-width: 120px;"></span>
          </div>
        </div>
      </div>

      <!-- Questions List -->
      <div class="questions-list d-flex flex-column gap-6">
        <div
          v-for="(q, index) in enrichedQuestions"
          :key="q.id"
          class="question-paper-item break-inside-avoid pa-4 rounded-xl border-subtle"
        >
          <div class="d-flex align-start mb-2">
            <span class="q-number-badge font-weight-black me-3">{{ index + 1 }}</span>
            <div class="flex-grow-1">
              <div class="d-flex justify-space-between align-start gap-2 mb-3">
                <div class="text-body-1 font-weight-bold" v-html="q.content" style="line-height: 1.7;" />
                <span class="score-chip font-weight-bold">({{ q.assignedMark }} درجات)</span>
              </div>

              <!-- MCQ Options -->
              <div v-if="q.questionType === 'mcq' || q.questionType === 'Single Choice' || q.questionType === 'Multiple Choice' || (!q.questionType && q.options && q.options.length > 0)" class="options-grid mt-3">
                <div v-for="(opt, idx) in q.options" :key="opt.id || idx" class="option-pill d-flex align-center">
                  <span class="option-circle me-2">{{ ['أ', 'ب', 'ج', 'د'][idx] || idx + 1 }}</span>
                  <span class="font-weight-medium">{{ opt.text }}</span>
                </div>
              </div>

              <!-- True/False -->
              <div v-else-if="q.questionType === 'tf' || q.questionType === 'صح وخطأ' || q.questionType === 'True/False'" class="options-grid mt-3">
                <div class="d-flex gap-6">
                  <div class="option-pill d-flex align-center">
                    <span class="option-circle me-2">✓</span>
                    <span class="font-weight-medium">صواب</span>
                  </div>
                  <div class="option-pill d-flex align-center">
                    <span class="option-circle me-2">✗</span>
                    <span class="font-weight-medium">خطأ</span>
                  </div>
                </div>
              </div>

              <!-- Essay Lines -->
              <div v-else class="essay-space mt-4 d-flex flex-column gap-3">
                <div class="dotted-line"></div>
                <div class="dotted-line"></div>
                <div class="dotted-line"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="footer mt-12 text-center text-body-2 pt-6 border-t border-slate-200">
        <p class="font-weight-bold text-medium-emphasis mb-0">*** انتهت الأسئلة - مع تمنياتنا بالتوفيق والنجاح ***</p>
      </div>
    </div>

    <div v-else class="text-center py-12 main-card rounded-2xl">
      <v-icon size="48" color="error" class="mb-3">mdi-alert-circle-outline</v-icon>
      <p class="text-h6 font-weight-bold text-error">عذراً، لا توجد بيانات لعرضها. الرجاء العودة للصفحة السابقة.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDataStore } from '@/stores/dataStore'
import { examsService } from '@/services/examsService'

const router = useRouter()
const route = useRoute()
const store = useDataStore()

const loading = ref(true)
const exam = ref(null)
const enrichedQuestions = ref([])
const subjectName = ref('')
const levelName = ref('')

const ministryHeading = computed(() => {
  if (exam.value?.institution_type === 'institute') {
    return 'الجمهورية اليمنية - وزارة التعليم الفني والتدريب المهني'
  }
  if (exam.value?.institution_type === 'university') {
    return 'الجمهورية اليمنية - وزارة التعليم العالي والبحث العلمي'
  }
  return 'الجمهورية اليمنية - وزارة التربية والتعليم'
})

onMounted(async () => {
  loading.value = true
  try {
    const examId = Number(route.query.examId)
    if (!examId) return

    // 1. Fetch Exam
    let loadedExam = store.getById('exams', examId)
    if (!loadedExam) {
      try {
        const res = await examsService.getExamById(examId)
        loadedExam = res?.data || res
      } catch (e) {
        console.error("Error fetching exam:", e)
      }
    }
    if (!loadedExam) return
    exam.value = loadedExam

    // 2. Fetch Subjects and Levels if needed
    if (store.getAll('subjects').length === 0) {
      await store.fetchSubjects()
    }
    if (store.getAll('levels').length === 0) {
      await store.fetchLevels()
    }

    const subId = loadedExam.subject || loadedExam.subjectId
    const subject = store.getById('subjects', subId)
    subjectName.value = loadedExam.subject_name || subject?.name || subject?.name_ar || 'المادة التدريبية / الدراسية'

    const lvlId = loadedExam.level || loadedExam.levelId
    const level = store.getById('levels', lvlId)
    levelName.value = loadedExam.institution_type === 'institute'
      ? (loadedExam.specialization_name || loadedExam.curriculum_name || 'التخصص المهني')
      : (loadedExam.level_name || level?.name || level?.name_ar || 'الصف العام')

    // 3. Fetch Versions
    let versions = []
    try {
      const vRes = await examsService.getExamVersions({ exam: examId })
      versions = Array.isArray(vRes) ? vRes : (vRes?.results || vRes?.data || [])
    } catch (e) {
      console.error(e)
    }
    if (versions.length === 0) {
      versions = store.getAll('examVersions').filter(v => (v.examId || v.exam) == examId)
    }

    // 4. Fetch Question Orders
    let orders = []
    if (versions.length > 0) {
      const version = versions[0]
      try {
        const oRes = await examsService.getExamQuestionOrders({ examVersion: version.id })
        orders = Array.isArray(oRes) ? oRes : (oRes?.results || oRes?.data || [])
      } catch (e) {
        console.error(e)
      }
      if (orders.length === 0) {
        orders = store.getAll('examQuestionOrders').filter(o => (o.versionId || o.examVersion) == version.id)
      }
    }

    // 5. Fetch Questions & Answers if needed
    if (store.getAll('questions').length === 0) {
      await store.fetchQuestions()
    }
    if (store.getAll('answers').length === 0) {
      await store.fetchAnswers()
    }

    const allQuestions = store.getAll('questions')
    const allAnswers = store.getAll('answers')

    if (orders.length > 0) {
      orders.sort((a, b) => (a.orderIndex || a.order || 0) - (b.orderIndex || b.order || 0))
      enrichedQuestions.value = orders.map((order, idx) => {
        const qId = order.question || order.questionId
        const question = allQuestions.find(q => q.id == qId)
        const qAnswers = allAnswers.filter(a => (a.question || a.questionId) == qId)

        if (!question) {
          return {
            id: qId || idx + 1,
            content: `سؤال رقم ${idx + 1}`,
            assignedMark: order.assignedMark || 1,
            options: [
              { id: 1, text: 'الخيار الأول' },
              { id: 2, text: 'الخيار الثاني' },
              { id: 3, text: 'الخيار الثالث' },
              { id: 4, text: 'الخيار الرابع' },
            ]
          }
        }

        return {
          ...question,
          assignedMark: order.assignedMark || question.defaultMark || 1,
          options: qAnswers.length > 0 
            ? qAnswers.map(a => ({ id: a.id, text: a.text || a.answer_text, isTrue: a.isTrue || a.is_correct }))
            : (question.options || [
                { id: 1, text: 'الخيار الأول' },
                { id: 2, text: 'الخيار الثاني' },
                { id: 3, text: 'الخيار الثالث' },
                { id: 4, text: 'الخيار الرابع' },
              ])
        }
      })
    } else {
      const candidateQuestions = allQuestions.filter(q => (q.subject || q.subjectId) == subId)
      const list = candidateQuestions.length > 0 ? candidateQuestions.slice(0, 10) : []
      enrichedQuestions.value = list.map((q) => ({
        ...q,
        assignedMark: q.defaultMark || 1,
        options: allAnswers.filter(a => (a.question || a.questionId) == q.id)
      }))
    }
  } catch (err) {
    console.error("Error loading print view:", err)
  } finally {
    loading.value = false
  }
})

const totalScore = computed(() => {
  return enrichedQuestions.value.reduce((sum, q) => sum + (Number(q.assignedMark) || 0), 0)
})

const print = () => {
  window.print()
}
</script>

<style scoped>
.qb-print-questions-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.print-paper-sheet {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
  max-width: 900px;
}

.paper-badge {
  padding: 4px 12px;
  border-radius: 8px;
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.student-info-box {
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.dotted-underline {
  border-bottom: 2px dotted rgba(var(--v-border-color), 0.5);
  margin-right: 4px;
}

.border-subtle {
  border: 1px solid rgba(var(--v-border-color), 0.12);
  background: rgb(var(--v-theme-background));
}

.q-number-badge {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: rgb(var(--v-theme-primary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.score-chip {
  padding: 2px 8px;
  border-radius: 6px;
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
  font-size: 0.8rem;
  white-space: nowrap;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.option-pill {
  padding: 6px 12px;
  border-radius: 10px;
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.option-circle {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1px solid rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-primary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
}

.dotted-line {
  border-bottom: 1px dotted rgba(var(--v-border-color), 0.4);
  height: 12px;
  width: 100%;
}

@media print {
  .d-print-none {
    display: none !important;
  }

  .qb-print-questions-v4 {
    padding: 0 !important;
    background: white !important;
    color: black !important;
  }

  .print-paper-sheet {
    box-shadow: none !important;
    border: none !important;
    background: white !important;
    color: black !important;
    padding: 0 !important;
    max-width: 100% !important;
  }

  .q-number-badge {
    background: #000 !important;
    color: #fff !important;
  }

  .option-pill {
    background: white !important;
    border: 1px solid #ddd !important;
  }

  .option-circle {
    border-color: #000 !important;
    color: #000 !important;
  }

  .dotted-line {
    border-bottom: 1px dotted #000 !important;
  }

  :root {
    color-scheme: light;
  }
}
</style>
