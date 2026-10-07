<script setup lang="ts">
import { computed } from 'vue'
import { EAGLE_OFFICIAL_BASE64 } from '@/assets/eagleBase64'

const props = withDefaults(
  defineProps<{
    layoutMode?: 'full_a4' | 'compact_a5'
    studentName?: string
    seatNumber?: string | number
    serialNumber?: string | number
    examSubject?: string
    subjectCode?: string | number
    examYear?: string
    centerName?: string
    centerCode?: string | number
    envelopeNo?: string | number
    governorate?: string
    directorate?: string
    barcodeValue?: string
    qrValue?: string
    studentAnswers?: Record<number, any>
    answerKey?: Record<number, string>
    showInspectionOverlay?: boolean
    interactive?: boolean
    hoveredBubbleId?: string
    aiResults?: Record<number, any>
    primaryColor?: string
    absenceStatus?: string // 'غائب' | 'غش' | 'شغب' | 'تلفون' | 'أخرى'
    // Dynamic Bubble Schemes & Customization
    mcqBubbleType?: 'numbers' | 'arabic_letters' | 'english_letters' | 'custom'
    tfBubbleType?: 'arabic' | 'arabic_words' | 'english' | 'symbols'
    customMcqChoices?: string[]
    customTfChoices?: { trueChoice: string; falseChoice: string }
    choicesCount?: number
    bubbleRadius?: number
    // Footer & Student Handwriting Customization
    footerRightText?: string
    footerCenterLogo?: string
    footerLeftText?: string
    documentLabel?: string
    studentSignature?: string
    showSimulatedHandwriting?: boolean
    // Dynamic Header & Institution Customization
    republicName?: string
    ministryName?: string
    sectorName?: string
    committeeName?: string
    examStageTitle?: string
    // Dynamic Metadata Labels
    labelSeatNumber?: string
    labelSerialNumber?: string
    labelSubject?: string
    labelGovernorate?: string
    labelDirectorate?: string
    labelCenter?: string
    labelCenterCode?: string
    labelEnvelope?: string
    // Backward compatibility aliases
    modelCode?: string | number
    schoolName?: string
    // Dynamic Instructions
    instruction1?: string
    instruction2?: string
    instruction3?: string
    instruction4?: string
    instructionCorrectLabel?: string
    // Dynamic Questions & Sections
    totalQuestions?: number
    columnsCount?: number
    rowSpacing?: number
    sections?: Array<{
      id?: string
      title?: string
      type?: 'true_false' | 'mcq'
      from_q?: number
      to_q?: number
      choices?: string[]
      mark?: number
    }>
  }>(),
  {
    layoutMode: 'compact_a5',
    studentName: 'عمرو عبدالباسط عبدالله قائد الزمر',
    seatNumber: '418485',
    serialNumber: '148',
    examSubject: 'القرآن الكريم',
    subjectCode: '1',
    examYear: '1444هـ — 2022-2023م',
    centerName: 'سالم قطن — معين',
    centerCode: '164',
    envelopeNo: '2',
    governorate: 'أمانة العاصمة',
    directorate: 'معين',
    barcodeValue: '41848501164148',
    qrValue: 'YE-MOE-1444-418485-SUB1',
    studentAnswers: () => ({}),
    answerKey: () => ({}),
    showInspectionOverlay: false,
    interactive: false,
    hoveredBubbleId: '',
    aiResults: () => ({}),
    primaryColor: '#000000',
    absenceStatus: '',
    mcqBubbleType: 'numbers',
    tfBubbleType: 'arabic',
    customMcqChoices: () => ['1', '2', '3', '4'],
    customTfChoices: () => ({ trueChoice: 'صح', falseChoice: 'خطأ' }),
    choicesCount: 4,
    bubbleRadius: 2.1,
    footerRightText: '',
    footerCenterLogo: '',
    footerLeftText: '',
    documentLabel: '',
    studentSignature: '',
    showSimulatedHandwriting: false,
    republicName: 'الجمهورية اليمنية',
    ministryName: 'وزارة التربية والتعليم',
    sectorName: 'قطاع المناهج والتوجيه — لجان الاختبارات',
    committeeName: 'لجنة المطبعة السرية المركزية',
    examStageTitle: 'اختبار الشهادة الثانوية العامة (القسم العلمي)',
    labelSeatNumber: 'رقم الجلوس',
    labelSerialNumber: 'رقم تسلسلي',
    labelSubject: 'المادة',
    labelGovernorate: 'المحافظة',
    labelDirectorate: 'مديرية',
    labelCenter: 'المركز',
    labelCenterCode: 'رقم المركز',
    labelEnvelope: 'مظروف',
    instruction1: '1- يجب أن يكون تظليل الدائرة بقلم جاف أسود أو أزرق بشكل كامل مثال:',
    instruction2: '2 - تأكد من تظليل إجاباتك في الأماكن المخصصة لها.',
    instruction3: '3 - يمنع استخدام المصحح.',
    instruction4: '4 - لن تقبل الإجابات مالم تسجل على هذه الورقة، اترك لنفسك وقتاً كافياً لنقل الإجابات.',
    instructionCorrectLabel: 'واجب',
  }
)

const displaySerialNumber = computed(() => props.serialNumber || props.modelCode || '148')
const displayCenterName = computed(() => props.centerName || props.schoolName || 'سالم قطن — معين')
const displayExamYear = computed(() => {
  const y = String(props.examYear || '').trim()
  if (!y || y === '1' || y === '0' || y.length < 4) {
    return '1445هـ — 2023-2024م'
  }
  return y
})

const emit = defineEmits<{
  (e: 'bubble-click', question: number, choice: string): void
  (e: 'bubble-hover', question: number, choice: string): void
  (e: 'bubble-leave'): void
  (e: 'absence-click', status: string): void
}>()

// Fiducials for Full A4 (10mm margins)
const fiducialsA4 = [
  { id: 'TL', x: 10, y: 10 },
  { id: 'TR', x: 194, y: 10 },
  { id: 'BL', x: 10, y: 281 },
  { id: 'BR', x: 194, y: 281 },
]

// Fiducials for Compact A5 (10mm margins on 210x148.5)
const fiducialsA5 = [
  { id: 'TL', x: 10, y: 10 },
  { id: 'TR', x: 194, y: 10 },
  { id: 'BL', x: 10, y: 133 },
  { id: 'BR', x: 194, y: 133 },
]

interface ChoicePos {
  choice: string
  label: string
  x: number
}

interface ColumnDef {
  id: string
  title: string
  type: 'true_false' | 'mcq'
  startQ: number
  endQ: number
  totalQuestions: number
  x: number
  qNumX: number
  headers: Array<{ label: string; x: number }>
  choicePositions: ChoicePos[]
}

const activeMcqChoices = computed<string[]>(() => {
  const count = Math.max(2, Math.min(5, props.choicesCount || 4))
  const bType = props.mcqBubbleType || 'numbers'
  if (bType === 'arabic_letters') {
    return ['أ', 'ب', 'ج', 'د', 'هـ'].slice(0, count)
  }
  if (bType === 'english_letters' || (bType as string) === 'letters') {
    return ['A', 'B', 'C', 'D', 'E'].slice(0, count)
  }
  if (bType === 'custom' && props.customMcqChoices && props.customMcqChoices.length > 0) {
    return props.customMcqChoices.slice(0, count)
  }
  return ['1', '2', '3', '4', '5'].slice(0, count)
})

const activeTfChoices = computed(() => {
  const bType = props.tfBubbleType || 'arabic'
  if (bType === 'english') {
    return {
      keys: ['T', 'F'],
      labels: { T: 'T', F: 'F' } as Record<string, string>,
      headerLabels: ['F', 'T'] as [string, string],
    }
  }
  if (bType === 'symbols') {
    return {
      keys: ['✓', '✗'],
      labels: { '✓': '✓', '✗': '✗' } as Record<string, string>,
      headerLabels: ['✗', '✓'] as [string, string],
    }
  }
  if (bType === 'arabic_words') {
    return {
      keys: ['صح', 'خطأ'],
      labels: { 'صح': 'صح', 'خطأ': 'خطأ' } as Record<string, string>,
      headerLabels: ['خطأ', 'صح'] as [string, string],
    }
  }
  // Default: 'arabic' -> labels inside bubble: 'ص' and 'خ', headers: 'خطأ' and 'صح'
  return {
    keys: ['صح', 'خطأ'],
    labels: { 'صح': 'ص', 'خطأ': 'خ' } as Record<string, string>,
    headerLabels: ['خطأ', 'صح'] as [string, string],
  }
})

function createMcqColumn(id: string, title: string, startQ: number, endQ: number, colX: number): ColumnDef {
  const choices = activeMcqChoices.value
  const n = choices.length
  const qNumX = 23.5
  const totalQuestions = endQ - startQ + 1

  // Distribute choices inside column width (26mm wide)
  // In RTL: choice[0] is closest to qNumX (on the right)
  // choice[n-1] is on the far left
  const choicePositions: ChoicePos[] = []
  
  if (n === 4) {
    const xs = [19.0, 13.5, 8.0, 2.5]
    for (let i = 0; i < 4; i++) {
      choicePositions.push({ choice: choices[i], label: choices[i], x: xs[i] })
    }
  } else if (n === 5) {
    const xs = [20.0, 15.5, 11.0, 6.5, 2.0]
    for (let i = 0; i < 5; i++) {
      choicePositions.push({ choice: choices[i], label: choices[i], x: xs[i] })
    }
  } else if (n === 3) {
    const xs = [18.0, 11.0, 4.0]
    for (let i = 0; i < 3; i++) {
      choicePositions.push({ choice: choices[i], label: choices[i], x: xs[i] })
    }
  } else {
    const step = 18.0 / (n || 1)
    for (let i = 0; i < n; i++) {
      const x = Math.round((qNumX - 4.5 - i * step) * 10) / 10
      choicePositions.push({ choice: choices[i], label: choices[i], x })
    }
  }

  // Headers visually ordered left-to-right:
  // Far left is choicePositions[n-1], down to choicePositions[0], then 'س' at qNumX
  const headers = [...choicePositions].reverse().map(cp => ({ label: cp.label, x: cp.x }))
  headers.push({ label: 'س', x: qNumX })

  return {
    id,
    title,
    type: 'mcq',
    startQ,
    endQ,
    totalQuestions,
    x: colX,
    qNumX,
    headers,
    choicePositions,
  }
}

function createTfColumn(id: string, title: string, startQ: number, endQ: number, colX: number): ColumnDef {
  const tf = activeTfChoices.value
  const qNumX = 19.0
  const totalQuestions = endQ - startQ + 1

  // Choice 0 (True) on right at x=11.5
  // Choice 1 (False) on left at x=3.5
  const choicePositions: ChoicePos[] = [
    { choice: tf.keys[0], label: tf.labels[tf.keys[0]], x: 11.5 },
    { choice: tf.keys[1], label: tf.labels[tf.keys[1]], x: 3.5 },
  ]

  const headers = [
    { label: tf.headerLabels[0], x: 3.5 },  // Left: False
    { label: tf.headerLabels[1], x: 11.5 }, // Right: True
    { label: 'س', x: qNumX },
  ]

  return {
    id,
    title,
    type: 'true_false',
    startQ,
    endQ,
    totalQuestions,
    x: colX,
    qNumX,
    headers,
    choicePositions,
  }
}

// Columns for Compact A5 (210 x 148.5)
const columnsConfig = computed<ColumnDef[]>(() => {
  const targetCols = props.columnsCount || 4

  if (props.sections && props.sections.length > 0) {
    const cols: ColumnDef[] = []
    let colIdx = 1

    let totalQ = 0
    for (const sec of props.sections) {
      const fromQ = sec.from_q || 1
      const toQ = sec.to_q || fromQ
      totalQ += Math.max(1, toQ - fromQ + 1)
    }

    const nSecs = props.sections.length
    const secColsCount: number[] = []
    let allocatedCols = 0

    // Allocate columns proportionally to sections
    for (let i = 0; i < nSecs; i++) {
      const sec = props.sections[i]
      const count = Math.max(1, (sec.to_q || 1) - (sec.from_q || 1) + 1)
      let c = Math.max(1, Math.round((count / (totalQ || 1)) * targetCols))
      secColsCount.push(c)
      allocatedCols += c
    }

    while (allocatedCols > targetCols) {
      let maxIdx = 0
      for (let i = 1; i < nSecs; i++) {
        if (secColsCount[i] > secColsCount[maxIdx]) maxIdx = i
      }
      if (secColsCount[maxIdx] > 1) {
        secColsCount[maxIdx]--
        allocatedCols--
      } else {
        break
      }
    }
    while (allocatedCols < targetCols) {
      let maxRatioIdx = 0
      let maxRatio = 0
      for (let i = 0; i < nSecs; i++) {
        const count = Math.max(1, (props.sections[i].to_q || 1) - (props.sections[i].from_q || 1) + 1)
        const ratio = count / secColsCount[i]
        if (ratio > maxRatio) {
          maxRatio = ratio
          maxRatioIdx = i
        }
      }
      secColsCount[maxRatioIdx]++
      allocatedCols++
    }

    for (let i = 0; i < nSecs; i++) {
      const sec = props.sections[i]
      const fromQ = sec.from_q || 1
      const toQ = sec.to_q || fromQ
      const secTotalQ = toQ - fromQ + 1
      const isTf = sec.type === 'true_false' || (sec.choices && sec.choices.length === 2 && (sec.choices.includes('صح') || sec.choices.includes('T')))
      const numCols = secColsCount[i]

      const basePerCol = Math.floor(secTotalQ / numCols)
      const remainder = secTotalQ % numCols

      let curFrom = fromQ
      for (let c = 0; c < numCols; c++) {
        const countForCol = basePerCol + (c < remainder ? 1 : 0)
        const start = curFrom
        const end = start + countForCol - 1
        curFrom = end + 1

        const colId = `col-dyn-${colIdx++}`
        const title = `س${start} إلى س${end}`

        if (isTf) {
          cols.push(createTfColumn(colId, title, start, end, 0))
        } else {
          cols.push(createMcqColumn(colId, title, start, end, 0))
        }
      }
    }

    // Position columns from right to left (col 1 is on right at 102, col N is on left at 12)
    const nCols = cols.length
    if (nCols === 1) {
      cols[0].x = 102
    } else if (nCols <= 4) {
      const standardXs = [102, 72, 42, 12]
      for (let i = 0; i < nCols; i++) {
        cols[i].x = standardXs[i]
      }
    } else {
      const step = (102 - 12) / (nCols - 1)
      for (let i = 0; i < nCols; i++) {
        cols[i].x = Math.round((102 - i * step) * 10) / 10
      }
    }

    return cols
  }

  // Default fallback: detect strictly from totalQuestions prop
  const total = props.totalQuestions || 50

  if (total <= 10) {
    // 10 questions: 1 column only (Q1 to Q10)
    return [
      createMcqColumn('col-1', `س1 إلى س${total}`, 1, total, 102),
    ]
  }

  if (total <= 20) {
    // Up to 20 questions: 2 columns
    const half = Math.ceil(total / 2)
    return [
      createMcqColumn('col-2', `س${half + 1} إلى س${total}`, half + 1, total, 72),
      createMcqColumn('col-1', `س1 إلى س${half}`, 1, half, 102),
    ]
  }

  if (total <= 30) {
    // Up to 30 questions: 3 columns
    const perCol = Math.ceil(total / 3)
    const q1_end = perCol
    const q2_end = Math.min(total, perCol * 2)
    return [
      createMcqColumn('col-3', `س${q2_end + 1} إلى س${total}`, q2_end + 1, total, 42),
      createMcqColumn('col-2', `س${q1_end + 1} إلى س${q2_end}`, q1_end + 1, q2_end, 72),
      createMcqColumn('col-1', `س1 إلى س${q1_end}`, 1, q1_end, 102),
    ]
  }

  if (total <= 40) {
    // Up to 40 questions: 4 columns
    const perCol = Math.ceil(total / 4)
    const c1 = perCol
    const c2 = Math.min(total, perCol * 2)
    const c3 = Math.min(total, perCol * 3)
    return [
      createMcqColumn('col-4', `س${c3 + 1} إلى س${total}`, c3 + 1, total, 12),
      createMcqColumn('col-3', `س${c2 + 1} إلى س${c3}`, c2 + 1, c3, 42),
      createTfColumn('col-2', `س${c1 + 1} إلى س${c2}`, c1 + 1, c2, 72),
      createTfColumn('col-1', `س1 إلى س${c1}`, 1, c1, 102),
    ]
  }

  if (total === 50) {
    // 50-question layout (Yemeni Ministry Standard: 20 TF + 30 MCQ)
    return [
      createMcqColumn('col-4', 'س36 إلى س50', 36, 50, 12),
      createMcqColumn('col-3', 'س21 إلى س35', 21, 35, 42),
      createTfColumn('col-2', 'س11 إلى س20', 11, 20, 72),
      createTfColumn('col-1', 'س1 إلى س10', 1, 10, 102),
    ]
  }

  if (total >= 60) {
    // 60-question layout
    const perCol = Math.ceil(total / 4)
    const c1 = perCol
    const c2 = Math.min(total, perCol * 2)
    const c3 = Math.min(total, perCol * 3)
    return [
      createMcqColumn('col-4', `س${c3 + 1} إلى س${total}`, c3 + 1, total, 12),
      createMcqColumn('col-3', `س${c2 + 1} إلى س${c3}`, c2 + 1, c3, 42),
      createTfColumn('col-2', `س${c1 + 1} إلى س${c2}`, c1 + 1, c2, 72),
      createTfColumn('col-1', `س1 إلى س${c1}`, 1, c1, 102),
    ]
  }

  // Fallback for any other count
  const perCol = Math.ceil(total / 4)
  const c1 = perCol
  const c2 = Math.min(total, perCol * 2)
  const c3 = Math.min(total, perCol * 3)
  return [
    createMcqColumn('col-4', `س${c3 + 1} إلى س${total}`, c3 + 1, total, 12),
    createMcqColumn('col-3', `س${c2 + 1} إلى س${c3}`, c2 + 1, c3, 42),
    createTfColumn('col-2', `س${c1 + 1} إلى س${c2}`, c1 + 1, c2, 72),
    createTfColumn('col-1', `س1 إلى س${c1}`, 1, c1, 102),
  ]
})


// Columns for Full A4 (210 x 297)
const columnsConfigA4 = computed<ColumnDef[]>(() => {
  const targetCols = props.columnsCount || 4

  if (props.sections && props.sections.length > 0) {
    const cols: ColumnDef[] = []
    let colIdx = 1

    let totalQ = 0
    for (const sec of props.sections) {
      const fromQ = sec.from_q || 1
      const toQ = sec.to_q || fromQ
      totalQ += Math.max(1, toQ - fromQ + 1)
    }

    const nSecs = props.sections.length
    const secColsCount: number[] = []
    let allocatedCols = 0

    for (let i = 0; i < nSecs; i++) {
      const sec = props.sections[i]
      const count = Math.max(1, (sec.to_q || 1) - (sec.from_q || 1) + 1)
      let c = Math.max(1, Math.round((count / (totalQ || 1)) * targetCols))
      secColsCount.push(c)
      allocatedCols += c
    }

    while (allocatedCols > targetCols) {
      let maxIdx = 0
      for (let i = 1; i < nSecs; i++) {
        if (secColsCount[i] > secColsCount[maxIdx]) maxIdx = i
      }
      if (secColsCount[maxIdx] > 1) {
        secColsCount[maxIdx]--
        allocatedCols--
      } else {
        break
      }
    }
    while (allocatedCols < targetCols) {
      let maxRatioIdx = 0
      let maxRatio = 0
      for (let i = 0; i < nSecs; i++) {
        const count = Math.max(1, (props.sections[i].to_q || 1) - (props.sections[i].from_q || 1) + 1)
        const ratio = count / secColsCount[i]
        if (ratio > maxRatio) {
          maxRatio = ratio
          maxRatioIdx = i
        }
      }
      secColsCount[maxRatioIdx]++
      allocatedCols++
    }

    for (let i = 0; i < nSecs; i++) {
      const sec = props.sections[i]
      const fromQ = sec.from_q || 1
      const toQ = sec.to_q || fromQ
      const secTotalQ = toQ - fromQ + 1
      const isTf = sec.type === 'true_false' || (sec.choices && sec.choices.length === 2 && (sec.choices.includes('صح') || sec.choices.includes('T')))
      const numCols = secColsCount[i]

      const basePerCol = Math.floor(secTotalQ / numCols)
      const remainder = secTotalQ % numCols

      let curFrom = fromQ
      for (let c = 0; c < numCols; c++) {
        const countForCol = basePerCol + (c < remainder ? 1 : 0)
        const start = curFrom
        const end = start + countForCol - 1
        curFrom = end + 1

        const colId = `col-a4-dyn-${colIdx++}`
        const title = `س${start} إلى س${end}`

        if (isTf) {
          cols.push(createTfColumn(colId, title, start, end, 0))
        } else {
          cols.push(createMcqColumn(colId, title, start, end, 0))
        }
      }
    }

    const nCols = cols.length
    if (nCols === 1) {
      cols[0].x = 81
    } else if (nCols <= 4) {
      const standardXs = [81, 54, 27, 0]
      for (let i = 0; i < nCols; i++) {
        cols[i].x = standardXs[i]
      }
    } else {
      const step = 81 / (nCols - 1)
      for (let i = 0; i < nCols; i++) {
        cols[i].x = Math.round((81 - i * step) * 10) / 10
      }
    }

    return cols
  }

  return [
    createMcqColumn('col-4-a4', 'س36 إلى س50', 36, 50, 0),
    createMcqColumn('col-3-a4', 'س21 إلى س35', 21, 35, 27),
    createTfColumn('col-2-a4', 'س11 إلى س20', 11, 20, 54),
    createTfColumn('col-1-a4', 'س1 إلى س10', 1, 10, 81),
  ]
})

const effectiveRowSpacing = computed(() => {
  if (props.rowSpacing && props.rowSpacing > 0 && props.rowSpacing < 6.5) {
    const maxRows = Math.max(...columnsConfig.value.map(c => c.totalQuestions), 10)
    if (maxRows * props.rowSpacing > 105) {
      return Math.max(3.8, Math.floor((105 / maxRows) * 10) / 10)
    }
    return props.rowSpacing
  }
  const maxRows = Math.max(...columnsConfig.value.map(c => c.totalQuestions), 10)
  return Math.max(3.8, Math.min(5.2, Math.floor((100 / maxRows) * 10) / 10))
})

const effectiveRowSpacingA4 = computed(() => {
  const maxRows = Math.max(...columnsConfigA4.value.map(c => c.totalQuestions), 10)
  return Math.max(4.5, Math.min(12.8, Math.floor((210 / maxRows) * 10) / 10))
})

const absenceOptions = [
  { label: 'غائب', x: 192 },
  { label: 'غش', x: 179 },
  { label: 'شغب', x: 166 },
  { label: 'تلفون', x: 153 },
  { label: 'أخرى', x: 140 },
]

function getBubbleState(q: number, choice: string): string {
  const ans = props.studentAnswers[q]
  if (ans === undefined || ans === null || ans === '') return 'empty'

  if (typeof ans === 'string') {
    if (ans === choice) return 'filled'

    // Equivalency mapping across numbering schemes:
    const numIdx = ['1', '2', '3', '4', '5'].indexOf(choice)
    const arIdx = ['أ', 'ب', 'ج', 'د', 'هـ'].indexOf(choice)
    const enIdx = ['A', 'B', 'C', 'D', 'E'].indexOf(choice)
    const choiceIdx = numIdx !== -1 ? numIdx : (arIdx !== -1 ? arIdx : enIdx)

    const ansNumIdx = ['1', '2', '3', '4', '5'].indexOf(ans)
    const ansArIdx = ['أ', 'ب', 'ج', 'د', 'هـ'].indexOf(ans)
    const ansEnIdx = ['A', 'B', 'C', 'D', 'E'].indexOf(ans)
    const ansIdx = ansNumIdx !== -1 ? ansNumIdx : (ansArIdx !== -1 ? ansArIdx : ansEnIdx)

    if (choiceIdx !== -1 && choiceIdx === ansIdx) return 'filled'

    // True/False equivalency:
    const trueVariants = ['صح', 'ص', 'T', 'True', 'true', '1', '✓']
    const falseVariants = ['خطأ', 'خ', 'F', 'False', 'false', '2', '✗']
    if (trueVariants.includes(choice) && trueVariants.includes(ans)) return 'filled'
    if (falseVariants.includes(choice) && falseVariants.includes(ans)) return 'filled'

    return 'empty'
  }

  if (typeof ans === 'object') {
    if (ans[choice] === 'filled' || ans[choice] === true) return 'filled'
    for (const [k, v] of Object.entries(ans)) {
      if (v === 'filled' || v === true) {
        if (k === choice) return 'filled'
      }
    }
  }

  return 'empty'
}

function isCorrectChoice(q: number, choice: string): boolean {
  if (!props.showInspectionOverlay) return false
  const correct = props.answerKey[q]
  if (!correct) return false
  if (correct === choice) return true

  const numIdx = ['1', '2', '3', '4', '5'].indexOf(choice)
  const arIdx = ['أ', 'ب', 'ج', 'د', 'هـ'].indexOf(choice)
  const enIdx = ['A', 'B', 'C', 'D', 'E'].indexOf(choice)
  const choiceIdx = numIdx !== -1 ? numIdx : (arIdx !== -1 ? arIdx : enIdx)

  const corrNumIdx = ['1', '2', '3', '4', '5'].indexOf(correct)
  const corrArIdx = ['أ', 'ب', 'ج', 'د', 'هـ'].indexOf(correct)
  const corrEnIdx = ['A', 'B', 'C', 'D', 'E'].indexOf(correct)
  const corrIdx = corrNumIdx !== -1 ? corrNumIdx : (corrArIdx !== -1 ? corrArIdx : corrEnIdx)

  if (choiceIdx !== -1 && choiceIdx === corrIdx) return true

  const trueVariants = ['صح', 'ص', 'T', 'True', 'true', '1', '✓']
  const falseVariants = ['خطأ', 'خ', 'F', 'False', 'false', '2', '✗']
  if (trueVariants.includes(choice) && trueVariants.includes(correct)) return true
  if (falseVariants.includes(choice) && falseVariants.includes(correct)) return true

  return false
}

function isBubbleCorrect(q: number, choice: string): boolean | null {
  if (!props.showInspectionOverlay) return null
  const state = getBubbleState(q, choice)
  if (state === 'filled') {
    return isCorrectChoice(q, choice)
  }
  return null
}

function handleBubbleClick(q: number, choice: string) {
  if (props.interactive) {
    emit('bubble-click', q, choice)
  }
}
</script>

<template>
  <!-- ══════════════════════════════════════════════════════════════════════ -->
  <!-- ── OPTION A: FULL A4 EXAM PAPER (ورقة اختبار كاملة تمتد لكامل صفحة A4) -->
  <!-- ══════════════════════════════════════════════════════════════════════ -->
  <svg
    v-if="layoutMode === 'full_a4'"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    viewBox="0 0 210 297"
    width="210mm"
    height="297mm"
    class="yemeni-ministry-sheet-svg a4-sheet"
    dir="rtl"
    style="background: #ffffff; display: block; margin: 0 auto; user-select: none; max-width: 100%; aspect-ratio: 210 / 297;"
  >
    <!-- Outer Printable Border -->
    <rect x="8" y="8" width="194" height="281" fill="#ffffff" stroke="#000000" stroke-width="0.8" />

    <!-- Corner Optical Fiducials -->
    <g class="fiducial-marks">
      <rect v-for="f in fiducialsA4" :key="f.id" :x="f.x" :y="f.y" width="5.5" height="5.5" fill="#000000" />
    </g>

    <!-- ── 1. Official Header Across Top ───────────────────────────── -->
    <g id="top-header-banner" transform="translate(14, 12)">
      <!-- Eagle Emblem -->
      <image :href="EAGLE_OFFICIAL_BASE64" :xlink:href="EAGLE_OFFICIAL_BASE64" x="160" y="0" width="22" height="17" preserveAspectRatio="xMidYMid meet" />

      <!-- Official Text -->
      <text x="95" y="4" font-size="3" font-weight="bold" text-anchor="middle" font-family="Arial, sans-serif">الجمهورية اليمنية</text>
      <text x="95" y="7.8" font-size="2.6" font-weight="bold" text-anchor="middle" font-family="Arial, sans-serif">وزارة التربية والتعليم — قطاع المناهج والتوجيه</text>
      <text x="95" y="11.2" font-size="2.1" text-anchor="middle" font-family="Arial, sans-serif">الإدارة العامة للاختبارات — لجنة المطبعة السرية المركزية</text>

      <!-- Exam Title Banner -->
      <rect x="0" y="13" width="182" height="6.5" fill="#f8fafc" stroke="#000000" stroke-width="0.4" />
      <text x="91" y="17.2" font-size="2.4" font-weight="bold" text-anchor="middle" font-family="Arial, sans-serif">
        اختبار الشهادة الثانوية العامة (القسم العلمي) للعام الدراسي {{ displayExamYear }}
      </text>
    </g>

    <!-- ── 2. Right Side: Student Card & Committee Box ────────────── -->
    <g id="right-column-panel" transform="translate(124, 34)">
      <!-- Card 1: Exam & Student Metadata Table -->
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="72" height="42" fill="#ffffff" stroke="#000000" stroke-width="0.5" />
        
        <!-- Row 1: المادة -->
        <rect x="52" y="0" width="20" height="7.5" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
        <text x="62" y="5" font-size="2.2" font-weight="bold" text-anchor="middle">المادة</text>
        <text x="26" y="5.2" font-size="2.8" font-weight="bold" text-anchor="middle">{{ examSubject }}</text>
        <line x1="0" y1="7.5" x2="72" y2="7.5" stroke="#000000" stroke-width="0.3" />

        <!-- Row 2: المحافظة والمديرية -->
        <rect x="54" y="7.5" width="18" height="7" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
        <text x="63" y="12" font-size="1.9" font-weight="bold" text-anchor="middle">المحافظة</text>
        <text x="41" y="12" font-size="2.1" text-anchor="middle">{{ governorate }}</text>
        <line x1="28" y1="7.5" x2="28" y2="14.5" stroke="#000000" stroke-width="0.3" />
        <rect x="18" y="7.5" width="10" height="7" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
        <text x="23" y="12" font-size="1.9" font-weight="bold" text-anchor="middle">مديرية</text>
        <text x="9" y="12" font-size="2.1" text-anchor="middle">{{ directorate }}</text>
        <line x1="0" y1="14.5" x2="72" y2="14.5" stroke="#000000" stroke-width="0.3" />

        <!-- Row 3: المركز ورقم المركز -->
        <rect x="54" y="14.5" width="18" height="7" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
        <text x="63" y="19" font-size="1.9" font-weight="bold" text-anchor="middle">المركز</text>
        <text x="27" y="19" font-size="2.1" text-anchor="middle">{{ centerName }}</text>
        <line x1="0" y1="21.5" x2="72" y2="21.5" stroke="#000000" stroke-width="0.3" />

        <!-- Row 4: رقم المركز والمظروف -->
        <rect x="54" y="21.5" width="18" height="7" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
        <text x="63" y="26" font-size="1.9" font-weight="bold" text-anchor="middle">رقم المركز</text>
        <text x="41" y="26.2" font-size="2.6" font-weight="bold" text-anchor="middle">{{ centerCode }}</text>
        <line x1="28" y1="21.5" x2="28" y2="28.5" stroke="#000000" stroke-width="0.3" />
        <rect x="18" y="21.5" width="10" height="7" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
        <text x="23" y="26" font-size="1.9" font-weight="bold" text-anchor="middle">مظروف</text>
        <text x="9" y="26.2" font-size="2.6" font-weight="bold" text-anchor="middle">{{ envelopeNo }}</text>
        <line x1="0" y1="28.5" x2="72" y2="28.5" stroke="#000000" stroke-width="0.3" />

        <!-- Row 5: اسم الطالب -->
        <rect x="54" y="28.5" width="18" height="13.5" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
        <text x="63" y="36.5" font-size="2" font-weight="bold" text-anchor="middle">اسم الطالب</text>
        <text x="27" y="37" font-size="2.5" font-weight="black" text-anchor="middle">{{ studentName }}</text>
      </g>

      <!-- Card 2: Student Signature Area -->
      <g transform="translate(0, 44)">
        <rect x="0" y="0" width="72" height="12" fill="#fafafa" stroke="#000000" stroke-width="0.4" stroke-dasharray="1 1" />
        <text x="36" y="4.5" font-size="2" fill="#64748b" text-anchor="middle">توقيع الطالب بخط اليد</text>
        <path d="M 16 9 Q 34 5 48 9 T 64 8" fill="none" stroke="#1e293b" stroke-width="0.6" stroke-linecap="round" />
      </g>

      <!-- Card 3: Large Bold Seat Number Box (رقم الجلوس) -->
      <g transform="translate(0, 58)">
        <rect x="0" y="0" width="72" height="24" fill="#ffffff" stroke="#000000" stroke-width="0.8" />
        <text x="36" y="5" font-size="2.4" text-anchor="middle" font-family="Arial, sans-serif">رقم الجلوس</text>
        <text x="36" y="17" font-size="11" font-weight="900" text-anchor="middle" font-family="'Courier New', monospace" letter-spacing="1">
          {{ seatNumber }}
        </text>
        <line x1="0" y1="18.5" x2="72" y2="18.5" stroke="#000000" stroke-width="0.4" />
        <text x="54" y="22" font-size="2" text-anchor="middle">رقم تسلسلي</text>
        <line x1="40" y1="18.5" x2="40" y2="24" stroke="#000000" stroke-width="0.4" />
        <text x="20" y="22.2" font-size="2.6" font-weight="bold" text-anchor="middle">{{ serialNumber }}</text>
      </g>

      <!-- Card 4: Absence & Violations Bubbles -->
      <g transform="translate(0, 84)">
        <rect x="0" y="0" width="72" height="20" fill="#ffffff" stroke="#000000" stroke-width="0.4" />
        <text x="36" y="4" font-size="2" font-weight="bold" text-anchor="middle" fill="#334155">حالات الملاحظة ولجنة النظام والمراقبة</text>
        <g v-for="(status, idx) in absenceOptions" :key="status.label" :transform="`translate(${idx * 13.5 + 4}, 11)`">
          <circle
            cx="4.5"
            cy="0"
            r="2.4"
            fill="#ffffff"
            stroke="#000000"
            stroke-width="0.5"
            :class="{ 'cursor-pointer': interactive }"
            @click="emit('absence-click', status.label)"
          />
          <circle v-if="absenceStatus === status.label" cx="4.5" cy="0" r="2" fill="#1e293b" />
          <text x="4.5" y="6" font-size="2" text-anchor="middle" font-family="Arial, sans-serif">{{ status.label }}</text>
        </g>
      </g>

      <!-- Card 5: Center Committee Seal & Notes Area (Fills space down to y: 200) -->
      <g transform="translate(0, 106)">
        <rect x="0" y="0" width="72" height="96" fill="#fdfdfd" stroke="#000000" stroke-width="0.4" />
        <rect x="0" y="0" width="72" height="6" fill="#f1f5f9" stroke="#000000" stroke-width="0.3" />
        <text x="36" y="4.2" font-size="2.1" font-weight="bold" text-anchor="middle">خاص بلجنة النظام والمراقبة والختم</text>

        <!-- Official Seal Circle -->
        <circle cx="36" cy="34" r="19" fill="none" stroke="#94a3b8" stroke-width="0.6" stroke-dasharray="2 1" />
        <circle cx="36" cy="34" r="16" fill="none" stroke="#cbd5e1" stroke-width="0.4" />
        <text x="36" y="32.5" font-size="1.9" fill="#94a3b8" text-anchor="middle">ختم المركز الاختباري</text>
        <text x="36" y="36.5" font-size="1.6" fill="#94a3b8" text-anchor="middle">المعتمد</text>

        <!-- Signatures of Invigilators -->
        <g transform="translate(4, 60)" font-size="2" font-family="Arial, sans-serif">
          <line x1="0" y1="0" x2="64" y2="0" stroke="#e2e8f0" stroke-width="0.4" />
          <text x="64" y="6" text-anchor="end">الملاحظ الأول: ................................</text>
          <text x="64" y="14" text-anchor="end">الملاحظ الثاني: ................................</text>
          <text x="64" y="22" text-anchor="end">رئيس المركز: ...................................</text>
          <text x="64" y="29" font-size="1.6" fill="#64748b" text-anchor="end">يمنع منعاً باتاً نزع أو تمزيق أي جزء من هذه الورقة</text>
        </g>
      </g>
    </g>

    <!-- ── 3. Left Side: Full 50-Question OMR Matrix (A4) ──────────────── -->
    <g id="questions-matrix-a4" transform="translate(14, 34)">
      <g
        v-for="col in columnsConfigA4"
        :key="col.id"
        :transform="`translate(${col.x}, 0)`"
      >
        <!-- Column Header Labels -->
        <text
          v-for="h in col.headers"
          :key="'a4-h-' + h.label + '-' + h.x"
          :x="h.x"
          y="4.5"
          font-size="2.2"
          font-weight="bold"
          text-anchor="middle"
          dominant-baseline="central"
          alignment-baseline="central"
          font-family="'Cairo', Arial, sans-serif"
          fill="#000000"
        >
          {{ h.label }}
        </text>

        <!-- Question Rows -->
        <g
          v-for="rowIdx in col.totalQuestions"
          :key="'a4-q-' + (col.startQ + rowIdx - 1)"
          :transform="`translate(0, ${rowIdx * effectiveRowSpacingA4 - 2.5})`"
        >
          <!-- Question Number on Right -->
          <text
            :x="col.qNumX"
            y="5"
            font-size="2.6"
            font-weight="black"
            text-anchor="middle"
            dominant-baseline="central"
            alignment-baseline="central"
            font-family="'Cairo', Arial, sans-serif"
            fill="#000000"
          >
            {{ col.startQ + rowIdx - 1 }}
          </text>

          <!-- Choice Bubbles -->
          <g
            v-for="cp in col.choicePositions"
            :key="'a4-cp-' + cp.choice"
            :transform="`translate(${cp.x}, 5)`"
            class="bubble-group"
            :class="{ 'cursor-pointer': interactive }"
            @click="handleBubbleClick(col.startQ + rowIdx - 1, cp.choice)"
          >
            <!-- Filled -->
            <circle
              v-if="getBubbleState(col.startQ + rowIdx - 1, cp.choice) === 'filled'"
              cx="0"
              cy="0"
              :r="bubbleRadius"
              fill="#000000"
            />
            <!-- Empty with Centered Label -->
            <g v-else>
              <circle
                cx="0"
                cy="0"
                :r="bubbleRadius"
                fill="#ffffff"
                stroke="#000000"
                stroke-width="0.5"
              />
              <text
                x="0"
                y="0"
                :font-size="cp.label.length > 1 ? 1.5 : (bubbleRadius * 0.95)"
                font-weight="bold"
                text-anchor="middle"
                dominant-baseline="central"
                alignment-baseline="central"
                font-family="'Cairo', Arial, sans-serif"
                fill="#000000"
                style="user-select: none; pointer-events: none;"
              >
                {{ cp.label }}
              </text>
            </g>

            <!-- Inspection Feedback Overlay -->
            <circle
              v-if="isBubbleCorrect(col.startQ + rowIdx - 1, cp.choice) === true"
              cx="0"
              cy="0"
              :r="bubbleRadius + 0.6"
              fill="none"
              stroke="#10b981"
              stroke-width="0.8"
            />
            <circle
              v-else-if="isBubbleCorrect(col.startQ + rowIdx - 1, cp.choice) === false"
              cx="0"
              cy="0"
              :r="bubbleRadius + 0.6"
              fill="none"
              stroke="#ef4444"
              stroke-width="0.8"
            />
          </g>
        </g>
      </g>
    </g>

    <!-- ── 4. Bottom Instructions, Barcode & QR Code (A4 Wide Zone) ─ -->
    <g id="bottom-zone-a4" transform="translate(14, 238)">
      <rect x="0" y="0" width="182" height="38" fill="#ffffff" stroke="#000000" stroke-width="0.6" />

      <!-- Left: 1D Linear Barcode -->
      <g transform="translate(3, 4)">
        <rect x="0" y="0" width="62" height="28" fill="#ffffff" stroke="#000000" stroke-width="0.2" />
        <g transform="translate(3, 3)">
          <line v-for="i in 34" :key="'bc-a4-' + i" :x1="i * 1.65" y1="1" :x2="i * 1.65" y2="18" stroke="#000000" :stroke-width="i % 3 === 0 ? '1.4' : i % 2 === 0 ? '0.9' : '0.4'" />
        </g>
        <text x="31" y="25.5" font-size="2.4" font-family="'Courier New', monospace" text-anchor="middle">{{ barcodeValue }}</text>
      </g>

      <!-- Center: Shading Guidelines Box -->
      <g transform="translate(68, 3)" font-family="Arial, sans-serif">
        <text x="56" y="4" font-size="2" font-weight="bold" text-anchor="end">1- يجب أن يكون تظليل الدائرة بقلم جاف أسود أو أزرق بشكل كامل مثال: </text>
        <circle cx="59" cy="3.5" r="1.8" fill="#1e293b" />
        <circle cx="64" cy="3.5" r="1.8" fill="#ffffff" stroke="#000000" stroke-width="0.5" />
        <line x1="62.5" y1="2" x2="65.5" y2="5" stroke="#000000" stroke-width="0.5" />

        <text x="56" y="10" font-size="1.9" text-anchor="end">2- تأكد من تظليل إجاباتك في الأماكن المخصصة لها.</text>
        <text x="56" y="16" font-size="1.9" text-anchor="end">3- يمنع استخدام المصحح أو طمس أكثر من إجابة لنفس السؤال.</text>
        <text x="56" y="22" font-size="1.9" text-anchor="end">4- لن تقبل الإجابات مالم تسجل على هذه الورقة، اترك لنفسك وقتاً كافياً لنقل الإجابات.</text>
        <text x="56" y="27.5" font-size="1.7" fill="#64748b" text-anchor="end">إدارة الاختبارات والتقويم الآلي — سرية تامة ومطابقة آلية معتمدة</text>
      </g>

      <!-- Right: 2D QR Code Box -->
      <g transform="translate(154, 4)">
        <rect x="0" y="0" width="24" height="24" fill="#ffffff" stroke="#000000" stroke-width="0.5" />
        <rect x="2" y="2" width="5.5" height="5.5" fill="#000000" />
        <rect x="3.2" y="3.2" width="3.1" height="3.1" fill="#ffffff" />
        <rect x="4" y="4" width="1.5" height="1.5" fill="#000000" />

        <rect x="16.5" y="2" width="5.5" height="5.5" fill="#000000" />
        <rect x="17.7" y="3.2" width="3.1" height="3.1" fill="#ffffff" />
        <rect x="18.5" y="4" width="1.5" height="1.5" fill="#000000" />

        <rect x="2" y="16.5" width="5.5" height="5.5" fill="#000000" />
        <rect x="3.2" y="17.7" width="3.1" height="3.1" fill="#ffffff" />
        <rect x="4" y="18.5" width="1.5" height="1.5" fill="#000000" />

        <rect x="9" y="3" width="1.6" height="1.6" fill="#000" />
        <rect x="12" y="5" width="1.6" height="1.6" fill="#000" />
        <rect x="10" y="10" width="4.5" height="4.5" fill="#000" />
        <rect x="11.5" y="11.5" width="1.5" height="1.5" fill="#fff" />
        <rect x="16.5" y="10" width="1.6" height="1.6" fill="#000" />
        <rect x="9" y="17" width="1.6" height="1.6" fill="#000" />
        <rect x="13" y="19" width="1.6" height="1.6" fill="#000" />
        <text x="12" y="30.5" font-size="1.9" font-weight="bold" text-anchor="middle">QR CODE</text>
      </g>
    </g>

    <!-- Bottom Center Document Label -->
    <text v-if="documentLabel" x="105" y="284" font-size="2.4" font-family="'Times New Roman', serif" text-anchor="middle">
      {{ documentLabel }}
    </text>
  </svg>

  <!-- ══════════════════════════════════════════════════════════════════════ -->
  <!-- ── OPTION B: COMPACT A5 SHEET (نصف ورقة معيارية 210 × 148.5 مم)       -->
  <!-- ══════════════════════════════════════════════════════════════════════ -->
  <svg
    v-else
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    viewBox="0 0 210 148.5"
    width="210mm"
    height="148.5mm"
    class="yemeni-ministry-sheet-svg a5-sheet"
    dir="rtl"
    style="background: #ffffff; display: block; margin: 0 auto; user-select: none; max-width: 100%; aspect-ratio: 210 / 148.5;"
  >
    <!-- Outer Printable Border -->
    <rect x="4" y="4" width="202" height="140.5" fill="#ffffff" stroke="#000000" stroke-width="0.7" />

    <!-- Four Corner Optical Fiducials (5.5 x 5.5 mm with strict OpenCV Quiet Zones) -->
    <g class="fiducial-marks">
      <rect x="6" y="6" width="5.5" height="5.5" fill="#000000" />
      <rect x="198.5" y="6" width="5.5" height="5.5" fill="#000000" />
      <rect x="6" y="137.0" width="5.5" height="5.5" fill="#000000" />
      <rect x="198.5" y="137.0" width="5.5" height="5.5" fill="#000000" />
    </g>

    <!-- ── Right Side: Authentic Student Information Card (12mm Margin: x=136 to 198) ── -->
    <g id="student-info-card-a5">
      <!-- 1. Header Box (Eagle on Right, Official Texts on Left) -->
      <rect x="136" y="19.5" width="62" height="15.5" fill="#ffffff" stroke="#000000" stroke-width="0.5" />
      <line x1="168" y1="19.5" x2="168" y2="35.0" stroke="#000000" stroke-width="0.4" />
      <!-- Republic Eagle Emblem (Right Half: x=168 to 198) -->
      <image :href="EAGLE_OFFICIAL_BASE64" :xlink:href="EAGLE_OFFICIAL_BASE64" x="170.0" y="20.2" width="26" height="14.0" preserveAspectRatio="xMidYMid meet" />
      <!-- Ministry Official Text (Left Half: x=136 to 168) -->
      <text x="152.0" y="22.8" font-size="2.2" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ republicName }}</text>
      <text x="152.0" y="26.0" font-size="1.8" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ ministryName }}</text>
      <text x="152.0" y="29.0" font-size="1.3" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ sectorName }}</text>
      <text x="152.0" y="32.0" font-size="1.3" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ committeeName }}</text>

      <!-- 2. Title Banner Box -->
      <rect x="136" y="35.0" width="62" height="6.5" fill="#ffffff" stroke="#000000" stroke-width="0.5" />
      <text x="167.0" y="38.0" font-size="2.0" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">
        {{ examStageTitle }}
      </text>
      <text x="167.0" y="40.4" font-size="1.45" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">
        للعام الدراسي {{ displayExamYear }}
      </text>

      <!-- 3. Metadata Table (4 Rows: x=136 to 198) -->
      <rect x="136" y="41.5" width="62" height="16.0" fill="#ffffff" stroke="#000000" stroke-width="0.5" />
      <line x1="187" y1="41.5" x2="187" y2="57.5" stroke="#000000" stroke-width="0.4" />
      <line x1="136" y1="45.5" x2="198" y2="45.5" stroke="#000000" stroke-width="0.35" />
      <line x1="136" y1="49.5" x2="198" y2="49.5" stroke="#000000" stroke-width="0.35" />
      <line x1="136" y1="53.5" x2="198" y2="53.5" stroke="#000000" stroke-width="0.35" />

      <!-- Row 1: المادة -->
      <text x="192.5" y="44.2" font-size="1.5" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ labelSubject }}</text>
      <text x="161.5" y="44.3" font-size="2.2" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ examSubject }}</text>

      <!-- Row 2: المحافظة والمديرية -->
      <text x="192.5" y="48.2" font-size="1.4" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ labelGovernorate }}</text>
      <text x="179.5" y="48.2" font-size="1.6" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ governorate }}</text>
      <line x1="172" y1="45.5" x2="172" y2="49.5" stroke="#000000" stroke-width="0.3" />
      <text x="166.0" y="48.2" font-size="1.4" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ labelDirectorate }}</text>
      <line x1="160" y1="45.5" x2="160" y2="49.5" stroke="#000000" stroke-width="0.3" />
      <text x="148.0" y="48.2" font-size="1.6" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ directorate }}</text>

      <!-- Row 3: المركز -->
      <text x="192.5" y="52.2" font-size="1.4" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ labelCenter }}</text>
      <text x="161.5" y="52.2" font-size="1.8" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ displayCenterName }}</text>

      <!-- Row 4: رقم المركز والمظروف -->
      <text x="192.5" y="56.2" font-size="1.3" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ labelCenterCode }}</text>
      <text x="175.5" y="56.2" font-size="2.2" font-weight="bold" text-anchor="middle" font-family="'Courier New', monospace">{{ centerCode }}</text>
      <line x1="164" y1="53.5" x2="164" y2="57.5" stroke="#000000" stroke-width="0.3" />
      <text x="157.0" y="56.2" font-size="1.3" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ labelEnvelope }}</text>
      <line x1="150" y1="53.5" x2="150" y2="57.5" stroke="#000000" stroke-width="0.3" />
      <text x="143.0" y="56.2" font-size="2.2" font-weight="bold" text-anchor="middle" font-family="'Courier New', monospace">{{ envelopeNo }}</text>

      <!-- 4. Student Printed Name Row 1 (Computer-Printed) -->
      <rect x="136" y="57.5" width="62" height="5.5" fill="#ffffff" stroke="#000000" stroke-width="0.4" />
      <text x="167.0" y="61.3" font-size="2.2" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">
        {{ studentName }}
      </text>

      <!-- 5. Student Handwritten Signature Row 2 (Blank for Pen Signature) -->
      <rect x="136" y="63.0" width="62" height="6.0" fill="#ffffff" stroke="#000000" stroke-width="0.4" />
      <text
        v-if="studentSignature || showSimulatedHandwriting"
        x="167.0"
        y="67.3"
        font-family="'Amiri', 'Scheherazade New', 'Traditional Arabic', cursive"
        font-size="2.2"
        font-weight="bold"
        text-anchor="middle"
        fill="#1e293b"
      >
        {{ studentSignature || studentName }}
      </text>

      <!-- 6 & 7. Authentic Seat Number Box, Serial Number Box, and Separate Right Marker Box (Matches media_1789821869125.png) -->
      <!-- Seat Number Box (width: 44mm, x=136 to 180) -->
      <rect x="136" y="69.0" width="44" height="11.5" fill="#ffffff" stroke="#000000" stroke-width="0.5" />
      <text x="158.0" y="72.2" font-size="2.1" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ labelSeatNumber }}</text>
      <line x1="137" y1="73.8" x2="179" y2="73.8" stroke="#888888" stroke-width="0.3" stroke-dasharray="0.8 0.8" />
      <text x="158.0" y="78.8" font-size="5.6" font-weight="bold" font-family="'Arial', 'Cairo', sans-serif" letter-spacing="1.0" text-anchor="middle">
        {{ seatNumber }}
      </text>

      <!-- Serial Number Row (width: 44mm, x=136 to 180) -->
      <rect x="136" y="80.5" width="44" height="5.0" fill="#ffffff" stroke="#000000" stroke-width="0.4" />
      <line x1="158" y1="80.5" x2="158" y2="85.5" stroke="#000000" stroke-width="0.4" />
      <text x="169.0" y="84.2" font-size="2.0" font-weight="bold" text-anchor="middle" font-family="'Cairo', Arial, sans-serif">{{ labelSerialNumber }}</text>
      <text x="147.0" y="84.4" font-size="2.8" font-weight="bold" text-anchor="middle" font-family="'Courier New', monospace">{{ displaySerialNumber }}</text>

      <!-- Right Marker Box: Separate Column (x=180 to 198, width: 18mm, height: 16.5mm) with Registration Triangle -->
      <rect x="180" y="69.0" width="18" height="16.5" fill="#ffffff" stroke="#000000" stroke-width="0.5" />
      <polygon points="181.5,84.5 187.5,84.5 181.5,78.5" fill="#000000" />

      <!-- 8. Absence Status Circles (Cleanly below the card, y: 88 to 95) -->
      <g id="absence-status-row">
        <g
          v-for="status in absenceOptions"
          :key="status.label"
          class="cursor-pointer"
          @click="emit('absence-click', status.label)"
        >
          <circle
            :cx="status.x"
            cy="90.5"
            r="2.1"
            fill="#ffffff"
            stroke="#000000"
            stroke-width="0.5"
          />
          <circle
            v-if="absenceStatus === status.label"
            :cx="status.x"
            cy="90.5"
            r="1.5"
            fill="#000000"
          />
          <text
            :x="status.x"
            y="94.6"
            font-size="1.7"
            text-anchor="middle"
            font-family="'Cairo', Arial, sans-serif"
          >
            {{ status.label }}
          </text>
        </g>
      </g>
    </g>

    <!-- ── Left Side: Dynamic Unbordered Question Columns (Matches Official Scan) ── -->
    <g id="omr-questions-grid-a5">
      <g
        v-for="col in columnsConfig"
        :key="col.id"
        :transform="`translate(${col.x}, 20)`"
      >
        <!-- Column Header Labels (Pure Typography, Open Style, RTL Order) -->
        <text
          v-for="h in col.headers"
          :key="h.label + '-' + h.x"
          :x="h.x"
          y="0"
          font-size="2.4"
          font-weight="bold"
          text-anchor="middle"
          dominant-baseline="central"
          alignment-baseline="central"
          font-family="'Cairo', Arial, sans-serif"
          fill="#000000"
        >
          {{ h.label }}
        </text>

        <!-- Question Rows (Uniform 5.0mm Pitch, No Table Outlines) -->
        <g
          v-for="rowIdx in col.totalQuestions"
          :key="col.startQ + rowIdx - 1"
          :transform="`translate(0, ${rowIdx * effectiveRowSpacing})`"
        >
          <!-- Question Number on the RIGHT -->
          <text
            :x="col.qNumX"
            y="0"
            font-size="2.5"
            font-weight="bold"
            text-anchor="middle"
            dominant-baseline="central"
            alignment-baseline="central"
            font-family="'Cairo', Arial, sans-serif"
            fill="#000000"
          >
            {{ col.startQ + rowIdx - 1 }}
          </text>

          <!-- Choice Bubbles -->
          <g
            v-for="cp in col.choicePositions"
            :key="cp.choice"
            :transform="`translate(${cp.x}, 0)`"
            class="bubble-group"
            :class="{ 'cursor-pointer': interactive }"
            @click="handleBubbleClick(col.startQ + rowIdx - 1, cp.choice)"
          >
            <!-- Filled / Shaded Bubble: Solid Black Circle -->
            <circle
              v-if="getBubbleState(col.startQ + rowIdx - 1, cp.choice) === 'filled'"
              cx="0"
              cy="0"
              :r="bubbleRadius"
              fill="#000000"
            />
            <!-- Empty Bubble: Thin Circle with Number or Letter perfectly centered -->
            <g v-else>
              <circle
                cx="0"
                cy="0"
                :r="bubbleRadius"
                fill="#ffffff"
                stroke="#000000"
                stroke-width="0.5"
              />
              <text
                x="0"
                y="0"
                :font-size="cp.label.length > 1 ? 1.5 : (bubbleRadius * 0.95)"
                font-weight="bold"
                text-anchor="middle"
                dominant-baseline="central"
                alignment-baseline="central"
                font-family="'Cairo', Arial, sans-serif"
                fill="#000000"
                style="user-select: none; pointer-events: none;"
              >
                {{ cp.label }}
              </text>
            </g>

            <!-- Inspection Feedback Overlay -->
            <circle
              v-if="isBubbleCorrect(col.startQ + rowIdx - 1, cp.choice) === true"
              cx="0"
              cy="0"
              :r="bubbleRadius + 0.6"
              fill="none"
              stroke="#10b981"
              stroke-width="0.8"
            />
            <circle
              v-else-if="isBubbleCorrect(col.startQ + rowIdx - 1, cp.choice) === false"
              cx="0"
              cy="0"
              :r="bubbleRadius + 0.6"
              fill="none"
              stroke="#ef4444"
              stroke-width="0.8"
            />
          </g>
        </g>
      </g>
    </g>

    <!-- ── Bottom Control Zone: 12mm Side Margins (x: 12 to 198) ── -->
    <g id="bottom-instructions-barcodes-a5">
      <!-- Outer Rectangle (x: 12 to 175, width: 163, height: 17.0mm) -->
      <rect x="12" y="114.0" width="163" height="17.0" fill="#ffffff" stroke="#000000" stroke-width="0.5" />

      <!-- Left Compartment: Inner Frame around Barcode -->
      <rect x="14.5" y="115.5" width="46" height="14.0" fill="#ffffff" stroke="#000000" stroke-width="0.35" />
      <g transform="translate(16, 116.5)">
        <line v-for="i in 34" :key="'bc-a5-' + i" :x1="i * 1.25" y1="0" :x2="i * 1.25" y2="9.5" stroke="#000000" :stroke-width="i % 4 === 0 ? '0.9' : i % 2 === 0 ? '0.6' : '0.35'" />
        <text x="21.5" y="12.0" font-size="1.8" font-family="'Courier New', monospace" font-weight="bold" text-anchor="middle">{{ barcodeValue || '41848501164148' }}</text>
      </g>

      <!-- Clean Vertical Divider separating Barcode from Instructions (x=65) -->
      <line x1="65" y1="114.0" x2="65" y2="131.0" stroke="#000000" stroke-width="0.4" />

      <!-- Right Compartment: Ministry Instructions (x: 65 to 175) -->
      <!-- Row 1: Rule 1 text centered at x=149 -->
      <text
        x="149"
        y="118.5"
        font-size="1.32"
        font-weight="bold"
        text-anchor="middle"
        font-family="'Cairo', Arial, Tahoma, sans-serif"
        fill="#000000"
      >
        {{ instruction1 }}
      </text>

      <!-- 5 Sample Bubbles: between x=84 and x=122 -->
      <!-- Circle 1: Correct Full Shading -->
      <circle cx="120.0" cy="118.0" r="1.35" fill="#000000" />
      <text
        x="115.0"
        y="118.5"
        font-size="1.15"
        font-weight="bold"
        text-anchor="middle"
        font-family="'Cairo', Arial, Tahoma, sans-serif"
        fill="#000000"
      >
        {{ instructionCorrectLabel || 'واجب' }}
      </text>

      <!-- Circle 2: Half Shaded -->
      <circle cx="108.0" cy="118.0" r="1.35" fill="#ffffff" stroke="#000000" stroke-width="0.45" />
      <path d="M 108.0 116.65 A 1.35 1.35 0 0 0 108.0 119.35 Z" fill="#000000" />

      <!-- Circle 3: Center Dot -->
      <circle cx="100.0" cy="118.0" r="1.35" fill="#ffffff" stroke="#000000" stroke-width="0.45" />
      <circle cx="100.0" cy="118.0" r="0.55" fill="#000000" />

      <!-- Circle 4: Checkmark -->
      <circle cx="92.0" cy="118.0" r="1.35" fill="#ffffff" stroke="#000000" stroke-width="0.45" />
      <path d="M 91.3 117.9 L 91.8 118.6 L 92.9 117.3" fill="none" stroke="#000000" stroke-width="0.45" stroke-linecap="round" />

      <!-- Circle 5: Cross -->
      <circle cx="84.0" cy="118.0" r="1.35" fill="#ffffff" stroke="#000000" stroke-width="0.45" />
      <line x1="83.0" y1="117.0" x2="85.0" y2="119.0" stroke="#000000" stroke-width="0.45" stroke-linecap="round" />
      <line x1="85.0" y1="117.0" x2="83.0" y2="119.0" stroke="#000000" stroke-width="0.45" stroke-linecap="round" />

      <!-- Row 2: Two Columns -->
      <text
        x="149"
        y="123.7"
        font-size="1.38"
        font-weight="bold"
        text-anchor="middle"
        font-family="'Cairo', Arial, Tahoma, sans-serif"
        fill="#000000"
      >
        {{ instruction2 }}
      </text>
      <text
        x="98"
        y="123.7"
        font-size="1.38"
        font-weight="bold"
        text-anchor="middle"
        font-family="'Cairo', Arial, Tahoma, sans-serif"
        fill="#000000"
      >
        {{ instruction3 }}
      </text>

      <!-- Row 3: Final Rule centered across the instruction box -->
      <text
        x="120"
        y="128.8"
        font-size="1.35"
        font-weight="bold"
        text-anchor="middle"
        font-family="'Cairo', Arial, Tahoma, sans-serif"
        fill="#000000"
      >
        {{ instruction4 }}
      </text>

      <!-- Standalone 2D QR Code on the Right (Aligned with box from x=181 to 198, y=114.0 to 131.0) -->
      <g transform="translate(181, 114.0)">
        <rect x="0" y="0" width="17" height="17" fill="#ffffff" stroke="#000000" stroke-width="0.4" />
        <rect x="1.0" y="1.0" width="4.8" height="4.8" fill="#000" />
        <rect x="2.0" y="2.0" width="2.8" height="2.8" fill="#fff" />
        <rect x="2.7" y="2.7" width="1.4" height="1.4" fill="#000" />

        <rect x="11.2" y="1.0" width="4.8" height="4.8" fill="#000" />
        <rect x="12.2" y="2.0" width="2.8" height="2.8" fill="#fff" />
        <rect x="12.9" y="2.7" width="1.4" height="1.4" fill="#000" />

        <rect x="1.0" y="11.2" width="4.8" height="4.8" fill="#000" />
        <rect x="2.0" y="12.2" width="2.8" height="2.8" fill="#fff" />
        <rect x="2.7" y="12.9" width="1.4" height="1.4" fill="#000" />

        <!-- Interior QR modules -->
        <rect x="7.0" y="1.8" width="2.0" height="2.0" fill="#000" />
        <rect x="9.5" y="3.8" width="2.0" height="2.0" fill="#000" />
        <rect x="7.0" y="7.0" width="3.2" height="3.2" fill="#000" />
        <rect x="11.2" y="8.0" width="2.0" height="2.0" fill="#000" />
        <rect x="7.0" y="11.8" width="2.0" height="2.0" fill="#000" />
        <rect x="10.0" y="11.8" width="2.0" height="2.0" fill="#000" />
      </g>
    </g>
  </svg>
</template>

<style scoped>
.yemeni-ministry-sheet-svg {
  filter: drop-shadow(0 6px 18px rgba(0,0,0,0.12));
  max-width: 100%;
}
.yemeni-ministry-sheet-svg.a5-sheet {
  width: 210mm;
  height: 148.5mm;
  aspect-ratio: 210 / 148.5;
}
.yemeni-ministry-sheet-svg.a4-sheet {
  width: 210mm;
  height: 297mm;
  aspect-ratio: 210 / 297;
}
.cursor-pointer {
  cursor: pointer;
}
.bubble-group:hover circle {
  filter: brightness(0.9);
}
</style>
