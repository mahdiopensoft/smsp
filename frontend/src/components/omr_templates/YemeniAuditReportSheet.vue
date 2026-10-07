<template>
  <div class="yemeni-audit-report-sheet pa-4 bg-white" dir="rtl">
    <!-- ── Print Action Bar (Hidden on Print) ───────────────────── -->
    <div class="d-print-none report-action-bar no-print d-flex justify-space-between align-center mb-2 pb-1 border-b">
      <div class="d-flex align-center gap-2">
        <v-avatar color="primary" variant="tonal" size="28" rounded="lg">
          <v-icon size="16">mdi-file-document-check-outline</v-icon>
        </v-avatar>
        <span class="text-caption font-weight-black">نموذج التصحيح والتدقيق الإلكتروني المعتمد — وزارة التربية والتعليم</span>
      </div>
      <div class="d-flex gap-2">
        <v-btn color="primary" size="x-small" rounded="lg" prepend-icon="mdi-printer" class="font-weight-bold" @click="printReport">
          طباعة الوثيقة الرسمية
        </v-btn>
      </div>
    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- ── 1. Top Header Box & Student QR (Unified Official Table) ── -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div class="header-container mb-1">
      <table class="table-header-official w-100 border border-dark text-center">
        <tbody>
          <!-- Row 1: QR Code (Spans 4 Rows on Far Right) + نموذج التصحيح + رقم النموذج + المادة -->
          <tr>
            <!-- Far Right: QR Code Cell Spanning all 4 Rows -->
            <td rowspan="4" class="qr-cell bg-white text-center pa-1" style="width: 96px; min-width: 96px; vertical-align: middle;">
              <svg width="84" height="84" viewBox="0 0 88 88" class="d-block mx-auto">
                <rect width="88" height="88" fill="#fff" />
                <!-- Corner Position Markers -->
                <rect x="4" y="4" width="24" height="24" fill="#000" />
                <rect x="8" y="8" width="16" height="16" fill="#fff" />
                <rect x="12" y="12" width="8" height="8" fill="#000" />

                <rect x="60" y="4" width="24" height="24" fill="#000" />
                <rect x="64" y="8" width="16" height="16" fill="#fff" />
                <rect x="68" y="12" width="8" height="8" fill="#000" />

                <rect x="4" y="60" width="24" height="24" fill="#000" />
                <rect x="8" y="64" width="16" height="16" fill="#fff" />
                <rect x="12" y="68" width="8" height="8" fill="#000" />

                <!-- Dynamic QR modules simulation -->
                <rect x="34" y="8" width="6" height="6" fill="#000" />
                <rect x="44" y="14" width="6" height="6" fill="#000" />
                <rect x="34" y="24" width="6" height="6" fill="#000" />
                <rect x="32" y="34" width="24" height="20" fill="#000" />
                <rect x="38" y="38" width="12" height="12" fill="#fff" />
                <rect x="42" y="42" width="4" height="4" fill="#000" />
                <rect x="62" y="34" width="6" height="6" fill="#000" />
                <rect x="74" y="44" width="6" height="6" fill="#000" />
                <rect x="34" y="62" width="6" height="6" fill="#000" />
                <rect x="44" y="70" width="6" height="6" fill="#000" />
                <rect x="60" y="64" width="20" height="16" fill="#000" />
              </svg>
            </td>

            <td colspan="3" class="font-weight-black text-subtitle-1 py-1" style="width: 44%;">نموذج التصحيح الالكتروني</td>
            <td class="font-weight-bold font-mono" style="width: 10%;">{{ modelCode || formNumber || 1 }}</td>
            <td class="font-weight-bold bg-grey-lighten-4" style="width: 14%;">المادة</td>
            <td colspan="2" class="font-weight-bold text-subtitle-1" style="width: 32%;">{{ examSubject }}</td>
          </tr>

          <!-- Row 2: عنوان الامتحان والعام الدراسي -->
          <tr>
            <td colspan="7" class="font-weight-bold py-1 text-body-1">
              {{ examStageTitle || 'اختبار الشهادة الثانوية العامة (القسم العلمي)' }} للعام الدراسي {{ examYear }}
            </td>
          </tr>

          <!-- Row 3: الاسم ورقم الجلوس -->
          <tr>
            <td class="bg-grey-lighten-4 font-weight-bold" style="width: 12%;">الاسم</td>
            <td colspan="4" class="font-weight-bold text-body-1 text-end pe-3">{{ studentName }}</td>
            <td class="bg-grey-lighten-4 font-weight-bold" style="width: 14%;">رقم الجلوس</td>
            <td class="font-weight-black text-h6 font-mono" style="width: 22%;">{{ seatNumber }}</td>
          </tr>

          <!-- Row 4: المركز والرقم والحالة -->
          <tr>
            <td class="bg-grey-lighten-4 font-weight-bold" style="width: 12%;">المركز</td>
            <td colspan="2" class="font-weight-bold text-end pe-3">{{ centerName }}</td>
            <td class="bg-grey-lighten-4 font-weight-bold" style="width: 9%;">رقمه</td>
            <td class="font-weight-bold font-mono" style="width: 11%;">{{ centerCode }}</td>
            <td class="bg-grey-lighten-4 font-weight-bold" style="width: 10%;">الحالة</td>
            <td class="font-weight-bold text-success font-weight-black" style="width: 12%;">{{ studentStatus }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- ── 2. The Corrected Exam Sheet (Middle OMR Paper) ────────── -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div class="exam-sheet-frame mb-1 position-relative bg-white border border-dark overflow-hidden">
      <div v-if="annotatedImage" class="pa-0 w-100 h-100 text-center d-flex align-center justify-center">
        <img :src="annotatedImage" class="sheet-image-unified d-block" alt="الورقة المصححة" />
      </div>
      <div v-else class="pa-0 w-100 h-100 d-flex align-center justify-center sheet-slot-wrapper">
        <slot name="sheet">
          <YemeniMinistrySheet
            layout-mode="compact_a5"
            :student-name="studentName"
            :seat-number="seatNumber"
            :serial-number="serialNumber"
            :model-code="modelCode || formNumber"
            :exam-subject="examSubject"
            :exam-year="examYear"
            :center-name="centerName"
            :center-code="centerCode"
            :envelope-no="envelopeNo"
            :governorate="governorate"
            :directorate="directorate"
            :barcode-value="barcodeValue"
            :qr-value="qrValue"
            :student-answers="studentAnswers"
            :answer-key="answerKey"
            :show-inspection-overlay="true"
            :mcq-bubble-type="mcqBubbleType"
            :tf-bubble-type="tfBubbleType"
            :choices-count="choicesCount"
            :bubble-radius="bubbleRadius"
            :footer-right-text="footerRightText"
            :footer-center-logo="footerCenterLogo"
            :footer-left-text="footerLeftText"
            :document-label="documentLabel"
            :student-signature="studentSignature"
            :show-simulated-handwriting="showSimulatedHandwriting"
            :total-questions="totalQuestions"
            :sections="sections"
            :columns-count="columnsCount"
            :row-spacing="rowSpacing"
          />
        </slot>
      </div>
    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- ── 3. Question-by-Question Audit Table (Exact 80-mark scale) ─ -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div class="audit-matrix-grid mb-1">

      <!-- Column 1 (Right): Questions 1 to 20 (True/False, 1 mark each) -->
      <div class="matrix-column">
        <table class="table-audit w-100 border border-dark text-center">
          <colgroup>
            <col style="width: 10%;">
            <col style="width: 24%;">
            <col style="width: 24%;">
            <col style="width: 21%;">
            <col style="width: 21%;">
          </colgroup>
          <thead>
            <tr class="bg-grey-lighten-4 border-b border-dark font-weight-bold">
              <th style="width: 10%;">ر.س</th>
              <th style="width: 24%;">الإجابة<br>الصحيحة</th>
              <th style="width: 24%;">إجابة<br>الطالب</th>
              <th style="width: 21%;">درجة<br>السؤال</th>
              <th style="width: 21%;">الدرجة<br>المستحقة</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="q in auditCol1Questions"
              :key="'audit-q-' + q"
              :class="{ 'bg-red-lighten-5': isQuestionWrong(q) }"
            >
              <td class="font-weight-bold bg-grey-lighten-5">{{ q }}</td>
              <td class="font-weight-bold">{{ getCorrectChoice(q) }}</td>
              <td class="font-weight-bold" :class="isQuestionCorrect(q) ? 'text-dark' : 'text-error font-weight-black'">
                {{ getStudentChoice(q) }}
              </td>
              <td>{{ getQuestionMaxMark(q) }}</td>
              <td class="font-weight-black" :class="isQuestionCorrect(q) ? 'text-dark' : 'text-error'">
                {{ getAwardedMark(q) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Column 2 (Middle): Second Block of Questions -->
      <div class="matrix-column">
        <table class="table-audit w-100 border border-dark text-center">
          <colgroup>
            <col style="width: 10%;">
            <col style="width: 24%;">
            <col style="width: 24%;">
            <col style="width: 21%;">
            <col style="width: 21%;">
          </colgroup>
          <thead>
            <tr class="bg-grey-lighten-4 border-b border-dark font-weight-bold">
              <th style="width: 10%;">ر.س</th>
              <th style="width: 24%;">الإجابة<br>الصحيحة</th>
              <th style="width: 24%;">إجابة<br>الطالب</th>
              <th style="width: 21%;">درجة<br>السؤال</th>
              <th style="width: 21%;">الدرجة<br>المستحقة</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="q in auditCol2Questions"
              :key="'audit-q-' + q"
              :class="{ 'bg-red-lighten-5': isQuestionWrong(q) }"
            >
              <td class="font-weight-bold bg-grey-lighten-5">{{ q }}</td>
              <td class="font-weight-bold">{{ getCorrectChoice(q) }}</td>
              <td class="font-weight-bold" :class="isQuestionCorrect(q) ? 'text-dark' : 'text-error font-weight-black'">
                {{ getStudentChoice(q) }}
              </td>
              <td>{{ getQuestionMaxMark(q) }}</td>
              <td class="font-weight-black" :class="isQuestionCorrect(q) ? 'text-dark' : 'text-error'">
                {{ getAwardedMark(q) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Column 3 (Left): Remaining Questions + Summary Totals Box + Notes -->
      <div class="matrix-column">
        <table class="table-audit w-100 border border-dark text-center mb-1">
          <colgroup>
            <col style="width: 10%;">
            <col style="width: 24%;">
            <col style="width: 24%;">
            <col style="width: 21%;">
            <col style="width: 21%;">
          </colgroup>
          <thead>
            <tr class="bg-grey-lighten-4 border-b border-dark font-weight-bold">
              <th style="width: 10%;">ر.س</th>
              <th style="width: 24%;">الإجابة<br>الصحيحة</th>
              <th style="width: 24%;">إجابة<br>الطالب</th>
              <th style="width: 21%;">درجة<br>السؤال</th>
              <th style="width: 21%;">الدرجة<br>المستحقة</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="q in auditCol3Questions"
              :key="'audit-q-' + q"
              :class="{ 'bg-red-lighten-5': isQuestionWrong(q) }"
            >
              <td class="font-weight-bold bg-grey-lighten-5">{{ q }}</td>
              <td class="font-weight-bold">{{ getCorrectChoice(q) }}</td>
              <td class="font-weight-bold" :class="isQuestionCorrect(q) ? 'text-dark' : 'text-error font-weight-black'">
                {{ getStudentChoice(q) }}
              </td>
              <td>{{ getQuestionMaxMark(q) }}</td>
              <td class="font-weight-black" :class="isQuestionCorrect(q) ? 'text-dark' : 'text-error'">
                {{ getAwardedMark(q) }}
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Summary Totals Table (Matching crop_summary: عدد الأسئلة | العظمى | الدرجة) -->
        <table class="table-audit table-summary w-100 border border-dark text-center mb-1">
          <thead>
            <tr class="bg-grey-lighten-4 border-b border-dark font-weight-bold">
              <th style="width: 34%;">عدد الأسئلة</th>
              <th style="width: 33%;">العظمى</th>
              <th style="width: 33%;">الدرجات</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="font-weight-bold py-1">{{ totalQuestionsCount }}</td>
              <td class="font-weight-black text-subtitle-2 py-1">{{ computedTotalMaxMark }}</td>
              <td class="font-weight-black text-subtitle-2 py-1 text-primary">{{ computedTotalScore.toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Notes Area (Matching crop_summary: ملاحظات:) -->
        <div class="notes-box border border-dark pa-1 bg-white">
          <div class="text-caption font-weight-bold notes-label">ملاحظات:</div>
          <div class="text-caption text-medium-emphasis notes-text">{{ notes || 'لا توجد ملاحظات مسجلة' }}</div>
        </div>
      </div>

    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- ── 4. Official Footer (Conditional) ──────────────────────── -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div v-if="footerRightText || footerCenterLogo || footerLeftText" class="report-footer d-flex justify-space-between align-center mt-2 pt-1 border-t border-dark text-caption font-weight-bold">
      <!-- Right: Sheet Code -->
      <div>{{ footerRightText }}</div>

      <!-- Center: Bracketed System Emblem -->
      <div v-if="footerCenterLogo" class="d-flex align-center justify-center font-weight-black border border-dark px-2 py-0 rounded" style="font-family: Arial, sans-serif; font-size: 0.85rem; letter-spacing: 1px;">
        {{ footerCenterLogo }}
      </div>

      <!-- Left: Academic System Text -->
      <div>{{ footerLeftText }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import YemeniMinistrySheet from './YemeniMinistrySheet.vue'
import { printOmrElement } from '@/pages/OMRSystem/utils/omrPrint'

const props = withDefaults(
  defineProps<{
    studentName?: string
    seatNumber?: string | number
    serialNumber?: string | number
    examSubject?: string
    subjectCode?: string | number
    formNumber?: string | number
    examYear?: string
    centerName?: string
    centerCode?: string | number
    envelopeNo?: string | number
    governorate?: string
    directorate?: string
    barcodeValue?: string
    qrValue?: string
    studentStatus?: string
    annotatedImage?: string
    questionsResults?: any[]
    studentAnswers?: Record<number, any>
    answerKey?: Record<number, string>
    notes?: string
    printDateTime?: string
    mcqBubbleType?: 'numbers' | 'arabic_letters' | 'english_letters' | 'custom'
    tfBubbleType?: 'arabic' | 'arabic_words' | 'english' | 'symbols'
    choicesCount?: number
    bubbleRadius?: number
    footerRightText?: string
    footerCenterLogo?: string
    footerLeftText?: string
    documentLabel?: string
    studentSignature?: string
    showSimulatedHandwriting?: boolean
    totalQuestions?: number
    sections?: Array<{
      id?: string
      title?: string
      type?: 'true_false' | 'mcq'
      from_q?: number
      to_q?: number
      choices?: string[]
      mark?: number
    }>
    questionMarks?: Record<number, number>
    columnsCount?: number
    rowSpacing?: number
    modelCode?: string | number
    examStageTitle?: string
  }>(),
  {
    studentName: 'عمرو عبدالباسط عبدالله قائد الزمر',
    seatNumber: '418485',
    serialNumber: '148',
    examSubject: 'القرآن الكريم',
    subjectCode: '1',
    formNumber: '1',
    modelCode: 'A',
    examStageTitle: 'اختبار الشهادة الثانوية العامة (القسم العلمي)',
    examYear: '1444هـ-2022-2023م',
    centerName: 'سالم قطن - معين',
    centerCode: '164',
    envelopeNo: '2',
    governorate: 'أمانة العاصمة',
    directorate: 'معين',
    barcodeValue: '41848501164148',
    qrValue: 'YE-MOE-1444-418485-SUB1',
    studentStatus: 'حاضر',
    annotatedImage: '',
    questionsResults: () => [],
    studentAnswers: () => ({}),
    answerKey: () => ({}),
    notes: '',
    printDateTime: '11:21 2023/07/23',
    mcqBubbleType: 'numbers',
    tfBubbleType: 'arabic',
    choicesCount: 4,
    bubbleRadius: 2.1,
    footerRightText: '',
    footerCenterLogo: '',
    footerLeftText: '',
    documentLabel: '',
    studentSignature: '',
    showSimulatedHandwriting: false,
    totalQuestions: 50,
    sections: () => [],
    questionMarks: () => ({}),
    columnsCount: 4,
    rowSpacing: 5.2,
  }
)

async function printReport() {
  const el = document.querySelector('.yemeni-audit-report-sheet') as HTMLElement
  if (el) {
    await printOmrElement(el, { title: 'نموذج التصحيح والتدقيق الإلكتروني المعتمد — وزارة التربية والتعليم', isA5: false })
  } else {
    window.print()
  }
}

const totalQuestionsCount = computed(() => {
  return props.totalQuestions || 50
})

const auditCol1Questions = computed(() => {
  const total = totalQuestionsCount.value
  const count = Math.ceil(total * 0.4)
  const list: number[] = []
  for (let q = 1; q <= count; q++) list.push(q)
  return list
})

const auditCol2Questions = computed(() => {
  const total = totalQuestionsCount.value
  const start = auditCol1Questions.value.length + 1
  const count = Math.ceil(total * 0.4)
  const end = Math.min(total, start + count - 1)
  const list: number[] = []
  for (let q = start; q <= end; q++) list.push(q)
  return list
})

const auditCol3Questions = computed(() => {
  const total = totalQuestionsCount.value
  const start = auditCol1Questions.value.length + auditCol2Questions.value.length + 1
  const list: number[] = []
  for (let q = start; q <= total; q++) list.push(q)
  return list
})

function formatChoice(val: any, q?: number): string {
  if (val === undefined || val === null || val === '') return '—'
  const str = String(val).trim()

  let isTf = false
  if (q !== undefined) {
    if (props.sections && props.sections.length > 0) {
      for (const sec of props.sections) {
        const from = sec.from_q || 1
        const to = sec.to_q || from
        if (q >= from && q <= to) {
          isTf = sec.type === 'true_false' || (sec.choices && sec.choices.length === 2 && (sec.choices.includes('صح') || sec.choices.includes('T')))
          break
        }
      }
    } else {
      isTf = q <= 20
    }
  }

  if (isTf) {
    if (props.tfBubbleType === 'english') {
      if (['صح', 'ص', '1', 'T', 'True', 'true'].includes(str)) return 'T'
      if (['خطأ', 'خ', '2', 'F', 'False', 'false'].includes(str)) return 'F'
    } else if (props.tfBubbleType === 'symbols') {
      if (['صح', 'ص', '1', 'T', 'True', 'true'].includes(str)) return '✓'
      if (['خطأ', 'خ', '2', 'F', 'False', 'false'].includes(str)) return '✗'
    } else {
      // الوضع العربي الافتراضي والمعتمد وزارياً: صح / خطأ
      if (['صح', 'ص', '1', 'T', 'True', 'true'].includes(str)) return 'صح'
      if (['خطأ', 'خ', '2', 'F', 'False', 'false'].includes(str)) return 'خطأ'
    }
  } else {
    const numIdx = ['1', '2', '3', '4', '5'].indexOf(str)
    const arIdx = ['أ', 'ب', 'ج', 'د', 'هـ'].indexOf(str)
    const enIdx = ['A', 'B', 'C', 'D', 'E'].indexOf(str)
    const choiceIdx = numIdx !== -1 ? numIdx : (arIdx !== -1 ? arIdx : enIdx)

    if (choiceIdx !== -1) {
      if (props.mcqBubbleType === 'arabic_letters') {
        return ['أ', 'ب', 'ج', 'د', 'هـ'][choiceIdx] || str
      }
      if (props.mcqBubbleType === 'english_letters' || (props.mcqBubbleType as string) === 'letters') {
        return ['A', 'B', 'C', 'D', 'E'][choiceIdx] || str
      }
      return ['1', '2', '3', '4', '5'][choiceIdx] || str
    }
  }

  if (str === 'صح' || str === 'ص') return '1'
  if (str === 'خطأ' || str === 'خ') return '2'
  return str
}

function getStudentChoice(q: number): string {
  if (props.questionsResults && props.questionsResults.length > 0) {
    const item = props.questionsResults.find((r: any) => (r.q === q || r.question_id === q))
    if (item && item.marked) return formatChoice(item.marked, q)
  }
  const ans = props.studentAnswers[q]
  if (!ans) return '—'
  if (typeof ans === 'string') return formatChoice(ans, q)
  if (typeof ans === 'object') {
    const marked = Object.keys(ans).find(k => ans[k] === 'filled')
    return marked ? formatChoice(marked, q) : '—'
  }
  return '—'
}

function getCorrectChoice(q: number): string {
  const c = props.answerKey[q] || (props.questionsResults.find((r: any) => (r.q === q || r.question_id === q))?.correct)
  return c ? formatChoice(c, q) : '—'
}

function isQuestionCorrect(q: number): boolean {
  const std = getStudentChoice(q)
  const cor = getCorrectChoice(q)
  if (std === '—' || cor === '—') return false
  return std === cor
}

function isQuestionWrong(q: number): boolean {
  const std = getStudentChoice(q)
  const cor = getCorrectChoice(q)
  if (std === '—') return false
  return std !== cor
}

function getQuestionMaxMark(q: number): number {
  if (props.questionMarks && props.questionMarks[q] !== undefined) {
    return props.questionMarks[q]
  }
  if (props.sections && props.sections.length > 0) {
    for (const sec of props.sections) {
      const from = sec.from_q || 1
      const to = sec.to_q || from
      if (q >= from && q <= to) {
        return sec.mark !== undefined ? sec.mark : (sec.type === 'true_false' ? 1 : 2)
      }
    }
  }
  return q <= 20 ? 1 : 2
}

function getAwardedMark(q: number): number {
  return isQuestionCorrect(q) ? getQuestionMaxMark(q) : 0
}

const computedTotalMaxMark = computed(() => {
  let sum = 0
  const total = totalQuestionsCount.value
  for (let q = 1; q <= total; q++) {
    sum += getQuestionMaxMark(q)
  }
  return sum
})

const computedTotalScore = computed(() => {
  let sum = 0
  const total = totalQuestionsCount.value
  for (let q = 1; q <= total; q++) {
    sum += getAwardedMark(q)
  }
  return sum
})
</script>

<style scoped>
.yemeni-audit-report-sheet {
  font-family: 'Cairo', 'Segoe UI', Tahoma, Arial, sans-serif;
  color: #000000;
  max-width: 1060px;
  width: 100%;
  margin: 0 auto;
}

.border-dark {
  border-color: #000000 !important;
}

.exam-sheet-frame {
  width: 100% !important;
  aspect-ratio: 210 / 148.5 !important;
  height: auto !important;
  border: 1px solid #000000;
  box-sizing: border-box;
  background: #ffffff;
  overflow: hidden;
  margin-bottom: 2px;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.sheet-slot-wrapper {
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.sheet-slot-wrapper :deep(svg),
.sheet-slot-wrapper svg {
  width: 100% !important;
  height: 100% !important;
  max-width: 100% !important;
  max-height: 100% !important;
  display: block !important;
  margin: 0 auto !important;
}

.sheet-image-unified {
  width: 100% !important;
  height: 100% !important;
  max-width: 100% !important;
  display: block !important;
  margin: 0 auto !important;
  padding: 0 !important;
  box-sizing: border-box;
  object-fit: contain !important;
  image-rendering: -webkit-optimize-contrast;
}

.audit-matrix-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 3px;
  width: 100%;
  box-sizing: border-box;
}

.matrix-column {
  min-width: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.table-header-official {
  border-collapse: collapse;
  width: 100% !important;
  table-layout: fixed !important;
}

.table-header-official td {
  border: 1px solid #000000;
  padding: 1.5px 3px;
  font-size: 0.76rem;
  line-height: 1.15;
}

.table-audit {
  border-collapse: collapse;
  width: 100% !important;
  table-layout: fixed !important;
  font-family: Tahoma, 'Segoe UI', Arial, sans-serif !important;
}

.table-audit th {
  border: 1px solid #000000;
  padding: 2px 0.5px !important;
  font-size: 0.56rem !important;
  line-height: 1.15 !important;
  font-weight: 700 !important;
  white-space: normal !important;
  word-break: keep-all !important;
  overflow-wrap: normal !important;
  hyphens: none !important;
  vertical-align: middle !important;
  text-align: center !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
  letter-spacing: normal !important;
}

.table-audit td {
  border: 1px solid #000000;
  padding: 1.2px 1px !important;
  font-size: 0.68rem !important;
  line-height: 1.12 !important;
  vertical-align: middle !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  text-align: center !important;
  box-sizing: border-box !important;
}

.notes-box {
  flex-grow: 1;
  min-height: 38px;
  padding: 2px 4px;
  box-sizing: border-box;
  border: 1px solid #000000;
  overflow: hidden;
}

.notes-label {
  font-size: 0.72rem;
  line-height: 1.2;
}

.notes-text {
  font-size: 0.68rem;
  line-height: 1.2;
  word-break: break-word;
}

@media print {
  @page {
    size: A4 portrait;
    margin: 3mm 5mm !important;
  }

  body, html {
    background: #ffffff !important;
    margin: 0 !important;
    padding: 0 !important;
    height: auto !important;
    overflow: visible !important;
  }

  .d-print-none,
  .report-action-bar,
  .no-print,
  .v-btn,
  button {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  .yemeni-audit-report-sheet {
    max-width: 100% !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 auto !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .exam-sheet-frame {
    border: 1px solid #000000 !important;
    width: 100% !important;
    aspect-ratio: 210 / 148.5 !important;
    height: auto !important;
    max-height: 142mm !important;
    overflow: hidden !important;
    margin-bottom: 2px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .sheet-slot-wrapper {
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }

  .sheet-slot-wrapper :deep(svg),
  .sheet-slot-wrapper svg {
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;
    display: block !important;
    margin: 0 auto !important;
  }

  .sheet-image-unified {
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 142mm !important;
    display: block !important;
    object-fit: contain !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .audit-matrix-grid {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 3px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .matrix-column {
    min-width: 0 !important;
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    box-sizing: border-box !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .table-header-official {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    table-layout: fixed !important;
  }

  .table-header-official td {
    padding: 1.5px 2.5px !important;
    font-size: 0.72rem !important;
    line-height: 1.15 !important;
  }

  .table-audit {
    font-family: Tahoma, 'Segoe UI', Arial, sans-serif !important;
    border-collapse: collapse !important;
    width: 100% !important;
    table-layout: fixed !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .table-audit tr {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .table-audit th {
    padding: 1.5px 0.5px !important;
    font-size: 0.54rem !important;
    line-height: 1.12 !important;
    font-weight: 700 !important;
    white-space: normal !important;
    word-break: keep-all !important;
    overflow-wrap: normal !important;
    hyphens: none !important;
    vertical-align: middle !important;
    text-align: center !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    letter-spacing: normal !important;
  }

  .table-audit td {
    padding: 1px 1px !important;
    font-size: 0.65rem !important;
    line-height: 1.10 !important;
    white-space: nowrap !important;
    vertical-align: middle !important;
    text-align: center !important;
    box-sizing: border-box !important;
  }

  .notes-box {
    flex-grow: 1 !important;
    min-height: 34px !important;
    padding: 2px 4px !important;
    font-size: 0.68rem !important;
    box-sizing: border-box !important;
    border: 1px solid #000000 !important;
    overflow: hidden !important;
  }
}
</style>