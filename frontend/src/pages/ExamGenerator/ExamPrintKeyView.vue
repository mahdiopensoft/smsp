<template>
  <div class="qb-print-key-v4 pa-4 pa-md-8">
    <!-- Non-printable Action Header -->
    <div class="d-print-none mb-6 d-flex align-center justify-space-between flex-wrap gap-3 pa-4 rounded-2xl main-card">
      <div class="d-flex align-center">
        <back-to class="me-2" @click="router.back()" />
        <v-avatar size="40" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="22">mdi-key-chain</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h6 font-weight-black mb-0">معاينة وطباعة مفتاح الإجابة</h1>
          <span class="text-caption text-medium-emphasis">نموذج الحلول المعتمدة المخصص للطباعة والمراجعة</span>
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <custom-btn
          type="add"
          label="طباعة النموذج"
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
      <p class="text-subtitle-1 font-weight-bold">جاري تحميل مفتاح الإجابة...</p>
    </div>

    <!-- Printable Content Paper Container -->
    <div class="print-paper-sheet pa-8 rounded-2xl mx-auto" v-else-if="exam">
      <!-- Exam Paper Header -->
      <div class="text-center mb-8 pb-6 border-b border-slate-200">
        <div class="text-caption text-medium-emphasis mb-1">{{ ministryHeading }}</div>
        <h1 class="text-h4 font-weight-black mb-2">{{ exam.title }}</h1>
        <h2 class="text-h5 font-weight-bold text-primary mb-4">نموذج الإجابة الرسمية المعتمد</h2>
        <div class="d-flex justify-center flex-wrap gap-4 text-body-1">
          <span class="paper-badge"><strong>المادة:</strong> {{ subjectName }}</span>
          <span class="paper-badge"><strong>{{ exam.institution_type === 'institute' ? 'التخصص:' : exam.institution_type === 'university' ? 'القسم:' : 'الصف:' }}</strong> {{ levelName }}</span>
          <span class="paper-badge"><strong>النموذج:</strong> {{ modelLabel }}</span>
        </div>
      </div>

      <!-- Key Answer Table -->
      <v-table density="comfortable" class="answer-key-table mb-8">
        <thead>
          <tr>
            <th class="text-center th-styled">رقم السؤال</th>
            <th class="text-center th-styled">الإجابة الصحيحة المعتمدة</th>
            <th class="text-center th-styled">الدرجة</th>
            <th class="text-center th-styled">المستوى المعرفي (بلوم)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(q, index) in enrichedQuestions" :key="q.id">
            <td class="text-center font-weight-black">{{ index + 1 }}</td>
            <td class="text-center font-weight-bold text-primary text-body-1">{{ getCorrectAnswer(q) }}</td>
            <td class="text-center font-weight-bold">{{ q.assignedMark }}</td>
            <td class="text-center">{{ getBloomText(q.bloomLevel) }}</td>
          </tr>
        </tbody>
      </v-table>

      <!-- Signature Section -->
      <div class="mt-12 pt-6 border-t border-slate-200">
        <v-row>
          <v-col cols="4" class="text-center">
            <p class="font-weight-bold mb-2">توقيع المصحح</p>
            <div class="signature-line"></div>
          </v-col>
          <v-col cols="4" class="text-center">
            <p class="font-weight-bold mb-2">توقيع المراجع</p>
            <div class="signature-line"></div>
          </v-col>
          <v-col cols="4" class="text-center">
            <p class="font-weight-bold mb-2">اعتماد مدير الإمتحانات</p>
            <div class="signature-line"></div>
          </v-col>
        </v-row>
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
const modelLabel = ref('أ')
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
      modelLabel.value = version.versionCode || version.versionLabel || 'أ'
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
        const answers = allAnswers.filter(a => (a.question || a.questionId) == qId)

        if (!question) {
          return {
            id: qId || idx + 1,
            content: `سؤال رقم ${idx + 1}`,
            assignedMark: order.assignedMark || 1,
            bloomLevel: 1,
            answers: [
              { id: 1, text: 'الإجابة الأولى (صحيحة)', isTrue: true },
              { id: 2, text: 'الإجابة الثانية', isTrue: false },
            ]
          }
        }

        return {
          ...question,
          assignedMark: order.assignedMark || question.defaultMark || 1,
          answers,
          options: answers.map(a => ({ id: a.id, text: a.text || a.answer_text, isTrue: a.isTrue || a.is_correct }))
        }
      })
    } else {
      const candidateQuestions = allQuestions.filter(q => (q.subject || q.subjectId) == subId)
      const list = candidateQuestions.length > 0 ? candidateQuestions.slice(0, 10) : []
      enrichedQuestions.value = list.map((q) => ({
        ...q,
        assignedMark: q.defaultMark || 1,
        answers: allAnswers.filter(a => (a.question || a.questionId) == q.id)
      }))
    }
  } catch (err) {
    console.error("Error loading key view:", err)
  } finally {
    loading.value = false
  }
})

const getCorrectAnswer = (q) => {
  if (q.answers && q.answers.length > 0) {
    const correct = q.answers.find(a => a.isTrue || a.is_correct)
    if (correct) {
      const idx = q.answers.indexOf(correct)
      const letters = ['أ', 'ب', 'ج', 'د']
      return `${letters[idx] || ''} - ${correct.text || correct.answer_text}`
    }
  }
  if (q.questionType === 'صح وخطأ' || q.questionType === 'tf' || q.questionType === 'True/False') {
    return q.isTrue ? 'صواب' : 'خطأ'
  }
  return 'أ - الخيار الصحيح'
}

const getBloomText = (level) => {
  if (typeof level === 'string' && isNaN(parseInt(level))) return level
  const texts = { 1: 'تذكر', 2: 'فهم', 3: 'تطبيق', 4: 'تحليل', 5: 'تقويم', 6: 'إبداع' }
  return texts[level] || level || 'تطبيق'
}

const print = () => {
  window.print()
}
</script>

<style scoped>
.qb-print-key-v4 {
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

.answer-key-table {
  border: 1px solid rgba(var(--v-border-color), 0.12);
  border-radius: 12px;
  overflow: hidden;
}

.th-styled {
  background: rgb(var(--v-theme-background)) !important;
  font-weight: 800 !important;
  font-size: 0.9rem !important;
}

.signature-line {
  border-bottom: 2px dotted rgba(var(--v-border-color), 0.4);
  height: 40px;
  width: 85%;
  margin: 0 auto;
}

@media print {
  .d-print-none {
    display: none !important;
  }

  .qb-print-key-v4 {
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

  .th-styled {
    background: #f1f5f9 !important;
    color: #000 !important;
  }

  .signature-line {
    border-bottom: 2px dotted #000 !important;
  }

  :root {
    color-scheme: light;
  }
}
</style>
