<template>
  <div class="qb-print-sheets-v4 pa-4 pa-md-8">
    <!-- Non-printable Action Header -->
    <div class="d-print-none mb-6 d-flex align-center justify-space-between flex-wrap gap-3 pa-4 rounded-2xl main-card">
      <div class="d-flex align-center">
        <back-to class="me-2" @click="router.back()" />
        <v-avatar size="40" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="22">mdi-checkbox-marked-circle-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h6 font-weight-black mb-0">طباعة أوراق التظليل (Bubble Sheet)</h1>
          <span class="text-caption text-medium-emphasis">أوراق الإجابة والمقابلة الآلية المخصصة لأجهزة الماسح الضوئي</span>
        </div>
      </div>

      <div class="d-flex align-center gap-3 flex-wrap">
        <!-- Segmented Toggle Mode Button -->
        <div class="segmented-mode-bar pa-1 rounded-xl">
          <button
            class="segmented-mode-btn font-weight-bold"
            :class="{ 'is-active': sheetMode === 'blank' }"
            @click="sheetMode = 'blank'"
          >
            <v-icon start size="16">mdi-file-outline</v-icon>
            ورقة الطالب الفارغة
          </button>
          <button
            class="segmented-mode-btn font-weight-bold"
            :class="{ 'is-active': sheetMode === 'key' }"
            @click="sheetMode = 'key'"
          >
            <v-icon start size="16">mdi-key</v-icon>
            مفتاح الإجابة المظلل
          </button>
        </div>

        <custom-btn
          type="add"
          label="طباعة"
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
      <p class="text-subtitle-1 font-weight-bold">جاري تحميل أوراق التظليل...</p>
    </div>

    <!-- Printable Content Paper Container -->
    <div class="print-paper-sheet pa-8 rounded-2xl mx-auto" v-else-if="exam">
      <!-- Sheet Header -->
      <div class="exam-header mb-6 pb-4 border-b-2 border-slate-300">
        <v-row align="center">
          <v-col cols="8">
            <div class="text-caption text-medium-emphasis mb-1">نظام بنك الأسئلة - أوراق التظليل الآلية</div>
            <h1 class="text-h5 font-weight-black mb-1">{{ exam.title }}</h1>
            <p class="text-body-2 font-weight-bold text-primary mb-0">
              {{ sheetMode === 'key' ? 'مفتاح الإجابة النموذجية (Bubble Sheet Key)' : 'ورقة إجابة الطالب (Bubble Sheet Answer Sheet)' }}
            </p>
          </v-col>
          <v-col cols="4" class="text-left">
            <div class="box-border pa-3 text-center rounded-xl">
              <span class="text-caption font-weight-bold d-block mb-1">رقم الطالب الأكاديمي</span>
              <div class="id-grid justify-center">
                <div v-for="n in 6" :key="n" class="id-box"></div>
              </div>
            </div>
          </v-col>
        </v-row>

        <v-row class="mt-3 info-fields">
          <v-col cols="8">
            <div class="d-flex align-center mb-2">
              <span class="label font-weight-bold me-2">اسم الطالب:</span>
              <div class="dotted-underline flex-grow-1"></div>
            </div>
            <div class="d-flex align-center">
              <span class="label font-weight-bold me-2">{{ exam.institution_type === 'institute' ? 'الشعبة / التخصص:' : exam.institution_type === 'university' ? 'الدفعة / القسم:' : 'الشعبة / الصف:' }}</span>
              <div class="dotted-underline flex-grow-1 me-4"></div>
              <span class="label font-weight-bold me-2">المادة:</span>
              <span class="font-weight-black text-primary">{{ subjectName }}</span>
            </div>
          </v-col>

          <v-col cols="4">
            <div class="box-border pa-3 rounded-xl bg-surface-variant">
              <p class="text-caption font-weight-bold mb-1">تعليمات التظليل:</p>
              <ul class="text-caption text-medium-emphasis ps-3 mb-0" style="list-style-type: disc;">
                <li>استخدم قلم رصاص HB أو جاف أسود.</li>
                <li>ظلل الدائرة بالكامل ● ولا تخرج عن حدودها.</li>
              </ul>
            </div>
          </v-col>
        </v-row>
      </div>

      <!-- Bubble Grid Columns -->
      <div class="bubble-grid-container py-4">
        <div class="bubble-column pa-3 rounded-xl border-subtle" v-for="(colQuestions, colIndex) in questionColumns" :key="colIndex">
          <div v-for="q in colQuestions" :key="q.num" class="bubble-row d-flex align-center mb-2">
            <span class="q-num font-weight-black me-2">{{ q.num }}</span>
            <div class="bubbles d-flex gap-2">
              <div class="bubble-item" v-for="(opt, optIdx) in ['أ', 'ب', 'ج', 'د']" :key="opt">
                <div
                  class="bubble-circle font-weight-bold"
                  :class="{ 'bubble-filled': sheetMode === 'key' && q.correctIndex === optIdx }"
                >
                  {{ opt }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="footer mt-8 pt-4 border-t border-slate-200 d-flex justify-space-between text-caption text-medium-emphasis">
        <span>تاريخ الاختبار: ____ / ____ / ________</span>
        <span>نظام التصحيح الآلي المعتمد - بنك الأسئلة</span>
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
const questionItems = ref([])
const subjectName = ref('')
const sheetMode = ref('key')

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

    // 2. Fetch Subjects if needed
    if (store.getAll('subjects').length === 0) {
      await store.fetchSubjects()
    }
    const subId = loadedExam.subject || loadedExam.subjectId
    const subject = store.getById('subjects', subId)
    subjectName.value = loadedExam.subject_name || subject?.name || subject?.name_ar || 'المادة الدراسية / التدريبية'

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
      questionItems.value = orders.map((order, idx) => {
        const qId = order.question || order.questionId
        const question = allQuestions.find(q => q.id == qId)
        let correctIndex = 0

        if (question) {
          const answers = allAnswers.filter(a => (a.question || a.questionId) == qId)
          if (answers.length > 0) {
            const foundIdx = answers.findIndex(a => a.isTrue || a.is_correct)
            correctIndex = foundIdx !== -1 ? foundIdx : 0
          } else if (question.questionType === 'صح وخطأ' || question.questionType === 'tf' || question.questionType === 'True/False') {
            correctIndex = question.isTrue ? 0 : 1
          }
        }

        return { num: idx + 1, correctIndex }
      })
    } else {
      let count = 20
      questionItems.value = Array.from({ length: count }, (_, i) => ({ num: i + 1, correctIndex: i % 4 }))
    }
  } catch (err) {
    console.error("Error loading bubble sheets view:", err)
  } finally {
    loading.value = false
  }
})

const questionColumns = computed(() => {
  const total = questionItems.value.length
  if (total === 0) return []
  
  const itemsPerCol = 25
  const numCols = Math.ceil(total / itemsPerCol)
  
  const cols = []
  for (let i = 0; i < numCols; i++) {
    const start = i * itemsPerCol
    cols.push(questionItems.value.slice(start, start + itemsPerCol))
  }
  return cols
})

const print = () => {
  window.print()
}
</script>

<style scoped>
.qb-print-sheets-v4 {
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
  max-width: 950px;
}

.box-border {
  border: 1px solid rgba(var(--v-border-color), 0.18);
  background: rgb(var(--v-theme-background));
}

.id-grid {
  display: flex;
  gap: 4px;
}

.id-box {
  width: 24px;
  height: 28px;
  border: 1px solid rgba(var(--v-border-color), 0.3);
  border-radius: 4px;
  background: rgb(var(--v-theme-surface));
}

.dotted-underline {
  border-bottom: 2px dotted rgba(var(--v-border-color), 0.4);
  height: 18px;
}

.border-subtle {
  border: 1px solid rgba(var(--v-border-color), 0.12);
  background: rgb(var(--v-theme-background));
}

.bubble-grid-container {
  display: flex;
  gap: 16px;
  justify-content: space-around;
  flex-wrap: wrap;
}

.q-num {
  min-width: 24px;
  text-align: right;
}

.bubble-circle {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 1px solid rgba(var(--v-border-color), 0.4);
  background: rgb(var(--v-theme-surface));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  transition: all 0.2s ease;
}

.bubble-filled {
  background-color: #000 !important;
  color: #fff !important;
  border-color: #000 !important;
}

/* ===== Segmented Control Button Bar ===== */
.segmented-mode-bar {
  display: flex;
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
  gap: 4px;
}

.segmented-mode-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 0.85rem;
  color: rgba(var(--v-theme-on-surface), 0.7);
  transition: all 0.25s ease;
  white-space: nowrap;
}

.segmented-mode-btn.is-active {
  background: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-primary));
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

@media print {
  .d-print-none {
    display: none !important;
  }

  .qb-print-sheets-v4 {
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

  .box-border, .id-box, .border-subtle {
    border-color: #000 !important;
    background: white !important;
  }

  .bubble-circle {
    border-color: #000 !important;
    background: white !important;
    color: #000 !important;
  }

  .bubble-filled {
    background-color: #000 !important;
    color: #fff !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  :root {
    color-scheme: light;
  }
}
</style>
