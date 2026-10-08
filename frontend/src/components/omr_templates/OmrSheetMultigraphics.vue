<script setup lang="ts">
import { computed } from 'vue';
import OmrBarcode from './OmrBarcode.vue';
import type { BarcodeField } from '../types';

const props = withDefaults(
  defineProps<{
    studentName?: string;
    examName?: string;
    barcodeValue?: string;
    studentAnswers?: Record<number, string>;
    answerKey?: Record<number, string>;
    showInspectionOverlay?: boolean;
    hoveredBubbleId?: string;
    aiResults?: Record<number, any>;
    layoutDirection?: 'ltr' | 'rtl';
    bubbleType?: 'letters' | 'numbers' | 'arabic_letters';
    totalQuestions?: number;

    questionsPerColumn?: number;
    totalColumns?: number;
    rowSpacing?: number;
    bubbleRadius?: number;
    choicesPerQuestion?: number;
    primaryColor?: string;
    institutionName?: string;
    subTitle?: string;
    bubbleTextStyle?: 'faint' | 'solid' | 'empty';
    mcqQuestions?: any[];
    startY?: number;
  }>(),
  {
    studentName: '................................',
    examName: 'اختبار تجريبي معياري',
    barcodeValue: '0000000000',
    studentAnswers: () => ({}),
    answerKey: () => ({}),
    showInspectionOverlay: false,
    hoveredBubbleId: '',
    aiResults: () => ({}),
    layoutDirection: 'rtl',
    bubbleType: 'numbers',
    bubbleTextStyle: 'faint',
    totalQuestions: 180,
    questionsPerColumn: 45,
    totalColumns: 4,
    rowSpacing: 4.2,
    bubbleRadius: 1.7,
    choicesPerQuestion: 4,
    primaryColor: '#e6007e',
    institutionName: 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي',
    subTitle: 'جامعة صنعاء — الإدارة العامة للامتحانات والتقويم الآلي',
    mcqQuestions: () => [],
    startY: 88,
  }


);

const pColor = computed(() => props.primaryColor || '#e6007e');
const pColorFaint = computed(() => pColor.value + '10');

// ── Responsive Parametric Geometry ────────────────────────────────
const MARGIN = 8;
const PAPER_W = 210;

const colCount = computed(() => Math.max(1, Math.min(6, props.totalColumns ?? 4)));
const rowCount = computed(() => Math.max(1, props.questionsPerColumn ?? 45));

// Usable column width based on total columns (e.g., 4cols -> 48.5mm, 3cols -> 64.6mm)
const totalUsableWidth = 190; // 210 - 10 - 10
const colWidth = computed(() => totalUsableWidth / colCount.value);

// Question number area vs Answer Area
const qNumWidth = computed(() => Math.min(10, colWidth.value * 0.22));
const answerAreaWidth = computed(() => colWidth.value - qNumWidth.value);

// Choices count and labels list
const choicesCount = computed(() => Math.max(3, Math.min(5, props.choicesPerQuestion ?? 4)));
const choiceLabelsList = computed(() => {
  const n = choicesCount.value;
  if (props.bubbleType === 'arabic_letters') return ['أ', 'ب', 'ج', 'د', 'هـ'].slice(0, n);
  if (props.bubbleType === 'letters') return ['A', 'B', 'C', 'D', 'E'].slice(0, n);
  return ['1', '2', '3', '4', '5'].slice(0, n);
});


// Step size between choices inside answer area (capped at 9.5mm max to prevent ugly stretching in 2-col or 3-col layouts)
const choiceStep = computed(() => Math.min(9.5, answerAreaWidth.value / (choicesCount.value + 1)));
const choiceBlockWidth = computed(() => choiceStep.value * (choicesCount.value + 1));


// Available height between startY and Footer at Y=278
const MAX_GRID_HEIGHT = computed(() => Math.max(50, 278 - (props.startY ?? 88)));
const HEADER_H = 6;
const MAX_ROWS_HEIGHT = computed(() => MAX_GRID_HEIGHT.value - HEADER_H);

// Dynamic Clamped Row Spacing (prevents ANY overlap into footer)
const effectiveRowSpacing = computed(() => {
  const reqSpacing = props.rowSpacing ?? 4.2;
  const maxAllowedSpacing = MAX_ROWS_HEIGHT.value / rowCount.value;
  return Math.min(reqSpacing, maxAllowedSpacing);
});

// Dynamic Total Grid Height (Column Box Height)
const dynamicGridHeight = computed(() => HEADER_H + rowCount.value * effectiveRowSpacing.value);

// Effective bubble radius (auto-clamped with 0.45mm safe margin top/bottom so it NEVER touches horizontal lines)
const effectiveBubbleRadius = computed(() => {
  const reqRadius = props.bubbleRadius ?? 1.7;
  const maxVert = Math.max(1.0, (effectiveRowSpacing.value * 0.5) - 0.45);
  const maxHoriz = Math.max(1.0, (choiceStep.value * 0.5) - 0.45);
  return Math.min(reqRadius, maxVert, maxHoriz);
});





// Dynamic Bubble CX calculation (Centered inside answer area if column is wide)
function getBubbleCX(optIdx: number): number {
  const isRtl = props.layoutDirection !== 'ltr';
  // Extra padding to center choices block inside answer area
  const extraPadding = Math.max(0, (answerAreaWidth.value - choiceBlockWidth.value) * 0.5);

  if (isRtl) {
    // RTL layout:
    // Question number is on the RIGHT (colWidth - qNumWidth to colWidth)
    // Answer area is on the LEFT (0 to colWidth - qNumWidth)
    const answerAreaRight = (colWidth.value - qNumWidth.value) - extraPadding;
    return answerAreaRight - choiceStep.value * (optIdx + 1);
  } else {
    // LTR layout:
    // Question number is on the LEFT (0 to qNumWidth)
    // Answer area is on the RIGHT (qNumWidth to colWidth)
    const answerAreaLeft = qNumWidth.value + extraPadding;
    return answerAreaLeft + choiceStep.value * (optIdx + 1);
  }
}


// Question number X
function getQNumX(): number {
  const isRtl = props.layoutDirection !== 'ltr';
  return isRtl ? (colWidth.value - qNumWidth.value * 0.5) : (qNumWidth.value * 0.5);
}

// Vertical divider line X
function getDividerLineX(): number {
  const isRtl = props.layoutDirection !== 'ltr';
  return isRtl ? (colWidth.value - qNumWidth.value) : qNumWidth.value;
}



const emit = defineEmits<{
  (e: 'bubble-click', payload: { questionId: number; choice: string }): void;
  (e: 'bubble-hover', payload: { questionId: number; choice: string; x: number; y: number } | null): void;
}>();

const barcodeField = computed<BarcodeField>(() => ({
  value: props.barcodeValue,
  rect: { x: 15, y: 52, width: 18, height: 32 },
  rotate: 90,
  format: 'CODE128',
  displayValue: false,
}));

function getChoiceState(qId: number, choice: string): string {
  const ans = props.studentAnswers?.[qId];
  if (!ans) return 'empty';

  if (typeof ans === 'string') {
    const letters = ['A', 'B', 'C', 'D', 'E'];
    const numbers = ['1', '2', '3', '4', '5'];
    const arabic  = ['أ', 'ب', 'ج', 'د', 'هـ'];

    let idx = letters.indexOf(ans);
    if (idx === -1) idx = numbers.indexOf(ans);
    if (idx === -1) idx = arabic.indexOf(ans);

    if (idx !== -1) {
      if (choice === letters[idx] || choice === numbers[idx] || choice === arabic[idx]) {
        return 'filled';
      }
    }
    if (ans === choice) return 'filled';
    return 'empty';
  }
  
  if (typeof ans === 'object') {
    return ans[choice] || 'empty';
  }

  return 'empty';
}

function handleBubbleClick(qId: number, choice: string) {
  emit('bubble-click', { questionId: qId, choice });
}


const hasExplicitCoordinates = computed(() => {
  if (!props.mcqQuestions || props.mcqQuestions.length === 0) return false;
  const firstQ = props.mcqQuestions[0];
  if (!firstQ || !firstQ.choices || firstQ.choices.length === 0) return false;
  const firstC = firstQ.choices[0];
  const reg = firstC.bubble_region || firstC.region || firstC.safe_region;
  return !!(reg && (reg.dx_mm !== undefined || reg.dx_px !== undefined));
});

function getChoiceCX(choiceObj: any): number {
  const reg = choiceObj.bubble_region || choiceObj.region || choiceObj.safe_region;
  if (!reg) return 0;
  return reg.dx_mm + (reg.width_mm || 3.4) * 0.5;
}

function getChoiceCY(choiceObj: any): number {
  const reg = choiceObj.bubble_region || choiceObj.region || choiceObj.safe_region;
  if (!reg) return 0;
  return reg.dy_mm + (reg.height_mm || 3.4) * 0.5;
}

function getChoiceRadius(choiceObj: any): number {
  const reg = choiceObj.bubble_region || choiceObj.region || choiceObj.safe_region;
  if (!reg) return 1.7;
  return (reg.width_mm || 3.4) * 0.5;
}

function handleBubbleMouseEnter(qId: number, choice: string, cx: number, cy: number) {
  emit('bubble-hover', { questionId: qId, choice, x: cx, y: cy });
}

function handleBubbleMouseLeave() {
  emit('bubble-hover', null);
}
</script>


<template>
  <svg
    class="omr-sheet-yemen"
    xmlns="http://www.w3.org/2000/svg"
    width="210mm"
    height="297mm"
    viewBox="0 0 210 297"
    shape-rendering="geometricPrecision"
    text-rendering="geometricPrecision"
    dir="ltr"
    style="direction: ltr !important;"
  >
    <!-- Paper Background -->
    <rect x="0" y="0" width="210" height="297" fill="#ffffff" />

    <!-- Outer Border Pink (Original Exact Layout Dimensions: x=6, y=5, w=198, h=291) -->
    <rect x="6" y="5" width="198" height="291" fill="none" :stroke="pColor" stroke-width="0.5" />

    <!-- 4 Corner Fiducial Anchor Marks (Placed in Corner Margins with Zero Border Collision) -->
    <g class="corner-fiducials">
      <!-- Top-Left (TL) -->
      <rect x="1.8" y="1.2" width="3.5" height="3.5" fill="#000000" />
      <rect x="2.5" y="1.9" width="2.1" height="2.1" fill="#ffffff" />
      <rect x="3.0" y="2.4" width="1.1" height="1.1" fill="#000000" />

      <!-- Top-Right (TR) -->
      <rect x="204.7" y="1.2" width="3.5" height="3.5" fill="#000000" />
      <rect x="205.4" y="1.9" width="2.1" height="2.1" fill="#ffffff" />
      <rect x="205.9" y="2.4" width="1.1" height="1.1" fill="#000000" />

      <!-- Bottom-Left (BL) -->
      <rect x="1.8" y="292.3" width="3.5" height="3.5" fill="#000000" />
      <rect x="2.5" y="293.0" width="2.1" height="2.1" fill="#ffffff" />
      <rect x="3.0" y="293.5" width="1.1" height="1.1" fill="#000000" />

      <!-- Bottom-Right (BR) -->
      <rect x="204.7" y="292.3" width="3.5" height="3.5" fill="#000000" />
      <rect x="205.4" y="293.0" width="2.1" height="2.1" fill="#ffffff" />
      <rect x="205.9" y="293.5" width="1.1" height="1.1" fill="#000000" />
    </g>




    <!-- Left & Right Timing Tracks -->
    <g class="timing-tracks">
      <rect
        v-for="i in 46"
        :key="'tt-left-' + i"
        x="2.2"
        :y="34 + (i - 1) * 5.3"
        width="3"
        height="2.5"
        fill="#000000"
      />
      <rect
        v-for="i in 46"
        :key="'tt-right-' + i"
        x="204.8"
        :y="34 + (i - 1) * 5.3"
        width="3"
        height="2.5"
        fill="#000000"
      />
    </g>

    <!-- HEADER LOGO & TITLE -->
    <g class="header-brand">
      <g transform="translate(184, 5.5)">
        <circle cx="9" cy="8" r="7" fill="#ffffff" :stroke="pColor" stroke-width="0.4" />
        <circle cx="9" cy="8" r="6" fill="none" :stroke="pColor" stroke-width="0.2" stroke-dasharray="0.8 0.6" />
        <rect x="5" y="4.5" width="8" height="2.3" fill="#ce1126" />
        <rect x="5" y="6.8" width="8" height="2.3" fill="#ffffff" stroke="#e2e8f0" stroke-width="0.1" />
        <rect x="5" y="9.1" width="8" height="2.3" fill="#000000" />
        <text x="9" y="14" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.4" :fill="pColor" text-anchor="middle">&#x202B;صنعاء&#x202C;</text>
      </g>

      <text x="100" y="9.5" font-family="'Cairo', sans-serif" font-weight="800" font-size="4" :fill="pColor" text-anchor="middle">&#x202B;{{ props.institutionName || 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي' }}&#x202C;</text>
      <text x="100" y="14" font-family="'Cairo', sans-serif" font-weight="700" font-size="2.6" fill="#1e293b" text-anchor="middle">&#x202B;{{ props.subTitle || 'جامعة صنعاء — الإدارة العامة للامتحانات والتقويم الآلي' }}&#x202C;</text>
      
      <rect x="40" y="16.2" width="120" height="5" :fill="pColorFaint" rx="1" :stroke="pColor" stroke-width="0.25" />
      <text x="100" y="19.8" font-family="'Cairo', sans-serif" font-weight="800" font-size="3" text-anchor="middle" :fill="pColor">&#x202B;ورقة إجابة التصحيح الضوئي الآلي (OMR ANSWER SHEET)&#x202C;</text>
    </g>

    <!-- INSTRUCTIONS BOX -->

    <g class="instructions-box">
      <rect x="8" y="22.5" width="194" height="13.5" fill="none" :stroke="pColor" stroke-width="0.35" />
      
      <text x="198" y="25.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.6" :fill="pColor" text-anchor="end">&#x202B;تعليمات التظليل المعتمدة :&#x202C;</text>
      <text x="198" y="28.2" font-family="'Cairo', sans-serif" font-size="1.2" fill="#000000" text-anchor="end">&#x202B;• تظليل الدوائر بالقلم الرصاص (2B) أو الجاف فقط&#x202C;</text>
      <text x="198" y="30.8" font-family="'Cairo', sans-serif" font-size="1.2" fill="#000000" text-anchor="end">&#x202B;• يمنع طي الورقة أو الشطب أو استخدام المزيّل عليها&#x202C;</text>
      <text x="198" y="33.4" font-family="'Cairo', sans-serif" font-size="1.2" fill="#000000" text-anchor="end">&#x202B;• تظليل أكثر من دائرة للسؤال الواحد يُلغي إجابته&#x202C;</text>

      <line x1="115" y1="22.5" x2="115" y2="36" :stroke="pColor" stroke-width="0.25" stroke-dasharray="0.8 0.6" />

      <text x="110" y="26.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.3" :fill="pColor" text-anchor="end">&#x202B;• ظـلّـل الـدائــرة الـمـنـاسـبـة بـالـكـامـل&#x202C;</text>
      <text x="110" y="30" font-family="'Cairo', sans-serif" font-size="1.2" fill="#000000" text-anchor="end">&#x202B;كما هو موضح في نموذج التظليل&#x202C;</text>

      <line x1="75" y1="22.5" x2="75" y2="36" :stroke="pColor" stroke-width="0.35" />

      <g class="method-table">
        <text x="70" y="25.5" font-family="'Cairo', sans-serif" font-size="1.3" fill="#000000" text-anchor="end">&#x202B;طريقة صحيحة&#x202C;</text>
        <text x="70" y="28.2" font-family="'Cairo', sans-serif" font-size="1.3" fill="#000000" text-anchor="end">&#x202B;طريقة خاطئة&#x202C;</text>
        <text x="70" y="30.9" font-family="'Cairo', sans-serif" font-size="1.3" fill="#000000" text-anchor="end">&#x202B;طريقة خاطئة&#x202C;</text>
        <text x="70" y="33.6" font-family="'Cairo', sans-serif" font-size="1.3" fill="#000000" text-anchor="end">&#x202B;طريقة خاطئة&#x202C;</text>

        <!-- Correct method row -->
        <g>
          <circle cx="38" cy="25" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="38" y="25.4" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">1</text>
          <circle cx="30" cy="25" r="1.1" :fill="pColor" />
          <text x="30" y="25.4" font-size="1.1" text-anchor="middle" fill="#ffffff" font-weight="bold">2</text>
          <circle cx="22" cy="25" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="22" y="25.4" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">3</text>
          <circle cx="14" cy="25" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="14" y="25.4" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">4</text>
        </g>
        <!-- Wrong method 1 (Checkmark) -->
        <g>
          <circle cx="38" cy="27.7" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="38" y="28.1" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">1</text>
          <circle cx="30" cy="27.7" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <path d="M 29.3 27.7 L 29.8 28.3 L 30.8 27.1" :stroke="pColor" stroke-width="0.3" fill="none" />
          <circle cx="22" cy="27.7" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="22" y="28.1" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">3</text>
          <circle cx="14" cy="27.7" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="14" y="28.1" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">4</text>
        </g>
        <!-- Wrong method 2 (Half fill) -->
        <g>
          <circle cx="38" cy="30.4" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="38" y="30.8" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">1</text>
          <circle cx="30" cy="30.4" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <circle cx="30" cy="30.4" r="0.6" :fill="pColor" />
          <circle cx="22" cy="30.4" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="22" y="30.8" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">3</text>
          <circle cx="14" cy="30.4" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="14" y="30.4" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">4</text>
        </g>
        <!-- Wrong method 3 (Cross) -->
        <g>
          <circle cx="38" cy="33.1" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="38" y="33.5" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">1</text>
          <circle cx="30" cy="33.1" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <line x1="29.3" y1="32.4" x2="30.7" y2="33.8" :stroke="pColor" stroke-width="0.3" />
          <line x1="30.7" y1="32.4" x2="29.3" y2="33.8" :stroke="pColor" stroke-width="0.3" />
          <circle cx="22" cy="33.1" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="22" y="33.5" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">3</text>
          <circle cx="14" cy="33.1" r="1.1" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text x="14" y="33.5" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">4</text>
        </g>
      </g>
    </g>

    <!-- ROLL NUMBER BOX -->
    <g class="roll-number-section" transform="translate(162, 38)">
      <rect x="0" y="0" width="40" height="49" fill="none" :stroke="pColor" stroke-width="0.35" />
      <rect x="0" y="0" width="40" height="9" fill="none" :stroke="pColor" stroke-width="0.3" />
      
      <text x="38" y="5.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.6" text-anchor="end" :fill="pColor">&#x202B;رقم الجلوس&#x202C;</text>
      <text x="2" y="5.5" font-family="Arial, sans-serif" font-weight="bold" font-size="1.4" text-anchor="start" :fill="pColor">(Seat No)</text>

      <g transform="translate(0, 9)">
        <rect v-for="c in 6" :key="'rn-box-' + c" :x="(c - 1) * 6.66" y="0" width="6.66" height="5" fill="none" :stroke="pColor" stroke-width="0.25" />
      </g>
      <g transform="translate(0, 14)">
        <g v-for="row in 10" :key="'rn-row-' + row">
          <g v-for="col in 6" :key="'rn-b-' + col + '-' + row">
            <circle :cx="(col - 1) * 6.66 + 3.33" :cy="(row - 1) * 3.5 + 1.7" r="1.4" fill="none" :stroke="pColor" stroke-width="0.25" />
            <text :x="(col - 1) * 6.66 + 3.33" :y="(row - 1) * 3.5 + 2.2" font-family="Arial, sans-serif" font-size="1.4" text-anchor="middle" :fill="pColor" font-weight="bold">{{ row - 1 }}</text>
          </g>
        </g>
      </g>
    </g>

    <!-- STUDENT & EXAM DETAILS -->
    <g class="student-details-section">
      <rect x="8" y="38" width="150" height="49" fill="none" :stroke="pColor" stroke-width="0.35" />

      <g transform="translate(156, 43)">
        <text x="0" y="0" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.8" :fill="pColor" text-anchor="end">&#x202B;اسم الطالب الرباعي :&#x202C;</text>
      </g>
      <g transform="translate(10, 43)">
        <text x="0" y="0" font-family="Arial, sans-serif" font-size="1.4" :fill="pColor" text-anchor="start">(Student Name)</text>
      </g>
      
      <line x1="42" y1="45" x2="114" y2="45" :stroke="pColor" stroke-width="0.35" stroke-dasharray="0.8 0.8" />
      
      <text v-if="props.studentName" x="112" y="44" font-family="'Cairo', sans-serif" font-weight="bold" font-size="2.1" fill="#000000" text-anchor="end">&#x202B;{{ props.studentName }}&#x202C;</text>

      <line x1="8" y1="46.5" x2="158" y2="46.5" :stroke="pColor" stroke-width="0.3" />

      <!-- SUB-COL 1 (Test Booklet Code) -->
      <g transform="translate(120, 46.5)">
        <rect x="0" y="0" width="36" height="15" fill="none" :stroke="pColor" stroke-width="0.3" />
        <rect x="0" y="0" width="36" height="7" fill="none" :stroke="pColor" stroke-width="0.25" />
        
        <text x="34" y="4.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.2" text-anchor="end" :fill="pColor">&#x202B;رمز النموذج&#x202C;</text>
        <text x="2" y="4.5" font-family="Arial, sans-serif" font-weight="bold" font-size="1.0" text-anchor="start" :fill="pColor">(Booklet)</text>
        
        <g v-for="(val, idx) in ['11', '22', '33', '44']" :key="'tbc-num-' + idx">
          <circle :cx="4.5 + idx * 9" cy="9.5" r="1.4" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text :x="4.5 + idx * 9" y="9.9" font-family="Arial, sans-serif" font-size="1.1" text-anchor="middle" :fill="pColor" font-weight="bold">{{ val }}</text>
        </g>
        <g v-for="(val, idx) in ['1', '2', '3', '4']" :key="'tbc-num2-' + idx">
          <circle :cx="4.5 + idx * 9" cy="13.5" r="1.4" fill="none" :stroke="pColor" stroke-width="0.25" />
          <text :x="4.5 + idx * 9" y="13.9" font-family="Arial, sans-serif" font-size="1.3" text-anchor="middle" :fill="pColor" font-weight="bold">{{ val }}</text>
        </g>

        <rect x="0" y="16" width="36" height="23.5" fill="none" :stroke="pColor" stroke-width="0.3" />
        <text x="34" y="19" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.2" :fill="pColor" text-anchor="end">&#x202B;تنبيه هام قبل التسليم :&#x202C;</text>
        <text x="34" y="21.5" font-family="'Cairo', sans-serif" font-size="1.0" fill="#000000" text-anchor="end">&#x202B;يجب على الطالب التأكد من&#x202C;</text>
        <text x="34" y="24" font-family="'Cairo', sans-serif" font-size="1.0" fill="#000000" text-anchor="end">&#x202B;تظليل رقم الجلوس ورمز&#x202C;</text>
        <text x="34" y="26.5" font-family="'Cairo', sans-serif" font-size="1.0" fill="#000000" text-anchor="end">&#x202B;النموذج بشكل صحيح ودقيق&#x202C;</text>
        <text x="34" y="29" font-family="'Cairo', sans-serif" font-size="1.0" fill="#000000" text-anchor="end">&#x202B;قبل التوقيع وتسليم الورقة&#x202C;</text>
        <text x="34" y="31.5" font-family="'Cairo', sans-serif" font-size="1.0" fill="#000000" text-anchor="end">&#x202B;للملاحظ بالقاعة الامتحانية&#x202C;</text>
      </g>

      <!-- SUB-COL 2 (Subject Name) -->
      <g transform="translate(82, 46.5)">
        <rect x="0" y="0" width="36" height="22" fill="none" :stroke="pColor" stroke-width="0.3" />
        <text x="34" y="4.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.4" text-anchor="end" :fill="pColor">&#x202B;المادة / المقرر&#x202C;</text>
        <text x="2" y="4.5" font-family="Arial, sans-serif" font-weight="bold" font-size="1.1" text-anchor="start" :fill="pColor">(Subject)</text>
        <line x1="2" y1="11.5" x2="34" y2="11.5" :stroke="pColor" stroke-width="0.25" stroke-dasharray="0.6 0.8" />
        <line x1="2" y1="16.5" x2="34" y2="16.5" :stroke="pColor" stroke-width="0.25" stroke-dasharray="0.6 0.8" />
        <line x1="2" y1="21.5" x2="34" y2="21.5" :stroke="pColor" stroke-width="0.25" stroke-dasharray="0.6 0.8" />
        <text v-if="props.examName" x="34" y="10.5" font-family="'Cairo', sans-serif" font-size="1.2" font-weight="bold" fill="#000000" text-anchor="end">&#x202B;{{ props.examName }}&#x202C;</text>

        <rect x="0" y="23.5" width="36" height="16" fill="none" :stroke="pColor" stroke-width="0.3" />
        <text x="34" y="28" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.3" text-anchor="end" :fill="pColor">&#x202B;فترة الاختبار&#x202C;</text>
        <text x="2" y="28" font-family="Arial, sans-serif" font-weight="bold" font-size="1.1" text-anchor="start" :fill="pColor">(Shift)</text>
        <line x1="2" y1="36" x2="34" y2="36" :stroke="pColor" stroke-width="0.25" stroke-dasharray="0.6 0.8" />
      </g>

      <!-- SUB-COL 3 (Date of Exam) -->
      <g transform="translate(44, 46.5)">
        <rect x="0" y="0" width="36" height="15" fill="none" :stroke="pColor" stroke-width="0.3" />
        <rect x="0" y="0" width="36" height="7" fill="none" :stroke="pColor" stroke-width="0.3" />
        
        <text x="34" y="4.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.2" text-anchor="end" :fill="pColor">&#x202B;تاريخ الاختبار&#x202C;</text>
        <text x="2" y="4.5" font-family="Arial, sans-serif" font-weight="bold" font-size="1.0" text-anchor="start" :fill="pColor">(Date)</text>
        
        <!-- Day (DD) -->
        <text x="7.1" y="9.2" font-family="'Cairo', sans-serif" font-size="0.9" text-anchor="middle" :fill="pColor">&#x202B;يوم&#x202C; (DD)</text>
        <rect x="3.3" y="10" width="3.8" height="4.5" fill="none" :stroke="pColor" stroke-width="0.25" />
        <rect x="7.1" y="10" width="3.8" height="4.5" fill="none" :stroke="pColor" stroke-width="0.25" />
        
        <!-- Month (MM) -->
        <text x="18.0" y="9.2" font-family="'Cairo', sans-serif" font-size="0.9" text-anchor="middle" :fill="pColor">&#x202B;شهر&#x202C; (MM)</text>
        <rect x="14.2" y="10" width="3.8" height="4.5" fill="none" :stroke="pColor" stroke-width="0.25" />
        <rect x="18.0" y="10" width="3.8" height="4.5" fill="none" :stroke="pColor" stroke-width="0.25" />

        <!-- Year (YY) -->
        <text x="28.9" y="9.2" font-family="'Cairo', sans-serif" font-size="0.9" text-anchor="middle" :fill="pColor">&#x202B;سنة&#x202C; (YY)</text>
        <rect x="25.1" y="10" width="3.8" height="4.5" fill="none" :stroke="pColor" stroke-width="0.25" />
        <rect x="28.9" y="10" width="3.8" height="4.5" fill="none" :stroke="pColor" stroke-width="0.25" />

        <rect x="0" y="16" width="36" height="23.5" fill="none" :stroke="pColor" stroke-width="0.3" />
        <text x="34" y="20.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.2" text-anchor="end" :fill="pColor">&#x202B;الصف / المستوى&#x202C;</text>
        <text x="2" y="20.5" font-family="Arial, sans-serif" font-weight="bold" font-size="1.0" text-anchor="start" :fill="pColor">(Class)</text>
        <g v-for="(cls, idx) in ['ثالث ثانوي (علمي)', 'ثالث ثانوي (أدبي)', 'بكالوريوس (جامعي)', 'دراسات عليا']" :key="'cls-' + idx">
          <text :x="34" :y="24.5 + idx * 4" font-family="'Cairo', sans-serif" font-size="1.1" fill="#000000" text-anchor="end">&#x202B;{{ cls }}&#x202C;</text>
          <circle :cx="4" :cy="24 + idx * 4" r="1.2" fill="none" :stroke="pColor" stroke-width="0.25" />
        </g>
      </g>

      <!-- SUB-COL 4 (Barcode) -->
      <g>
        <rect x="10" y="46.5" width="32" height="39.5" fill="none" :stroke="pColor" stroke-width="0.3" />
        <text x="40" y="49.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="1.5" text-anchor="end" :fill="pColor">&#x202B;رمز تشفير الورقة&#x202C;</text>
        <OmrBarcode :field="barcodeField" color="#000000" />
        <text x="38" y="68" font-family="monospace" font-size="1.8" text-anchor="middle" fill="#000000" transform="rotate(-90, 38, 68)">{{ props.barcodeValue }}</text>
      </g>
    </g>


    <!-- RESPONSES SECTION (Fully Responsive & Parametric Grid) -->
    <g id="responses-section" :transform="`translate(10, ${props.startY ?? 88})`">
      <g
        v-for="col in colCount"
        :key="'col-' + col"
        :transform="`translate(${props.layoutDirection === 'ltr' ? (col - 1) * colWidth : (colCount - col) * colWidth}, 0)`"
      >
        <!-- Outer Column Border (Auto-fit height, max 190mm) -->
        <rect x="0" y="0" :width="colWidth" :height="dynamicGridHeight" fill="none" :stroke="pColor" stroke-width="0.26" />
        
        <!-- HEADER SECTION -->
        <rect x="0" y="0" :width="colWidth" height="6" :fill="pColorFaint" />
        <line x1="0" y1="6" :x2="colWidth" y2="6" :stroke="pColor" stroke-width="0.26" />
        
        <!-- Header Texts -->
        <text :x="getQNumX()" y="4.2" font-family="sans-serif" font-weight="bold" font-size="2.6" text-anchor="middle" :fill="pColor">Q.No</text>
        <text :x="props.layoutDirection === 'ltr' ? (qNumWidth + (colWidth - qNumWidth) * 0.5) : ((colWidth - qNumWidth) * 0.5)" y="4.2" font-family="sans-serif" font-weight="bold" font-size="2.6" text-anchor="middle" :fill="pColor">Answer</text>



        <g transform="translate(0, 6)">
          <!-- Draw Zebra Striping Backgrounds FIRST -->
          <g v-for="row in rowCount" :key="'bg-' + col + '-' + row">
            <rect
              v-if="row % 2 === 0"
              x="0" :y="(row - 1) * effectiveRowSpacing"
              :width="colWidth" :height="effectiveRowSpacing"
              :fill="pColorFaint"
            />
          </g>

          <!-- Draw Horizontal Separator Lines -->
          <g v-for="row in (rowCount - 1)" :key="'hline-' + col + '-' + row">
            <line
              x1="0" :y1="row * effectiveRowSpacing"
              :x2="colWidth" :y2="row * effectiveRowSpacing"
              :stroke="pColor" stroke-width="0.26"
            />
          </g>

          <!-- Draw Vertical Separator Line (Auto-fits column height) -->
          <line :x1="getDividerLineX()" y1="-6" :x2="getDividerLineX()" :y2="dynamicGridHeight - 6" :stroke="pColor" stroke-width="0.26" />

          <g v-for="row in rowCount" :key="'q-row-' + col + '-' + row">
            <template v-if="((col - 1) * rowCount + row) <= (props.totalQuestions || 180)">
              <!-- Question number -->
              <text
                :x="getQNumX()"
                :y="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.65"
                font-family="sans-serif"
                font-weight="bold"
                :font-size="Math.min(2.6, effectiveRowSpacing * 0.6)"
                text-anchor="middle"
                fill="#1a1a1a"
              >{{ (col - 1) * rowCount + row }}</text>

              <!-- Choice Bubbles — ONLY rendered when there are NO explicit coordinates -->
              <!-- (If mcqQuestions has explicit dx_mm coords, bubbles are rendered in the explicit layer below) -->
              <g
                v-if="!hasExplicitCoordinates"
                v-for="(optNum, optIdx) in choiceLabelsList" 
                :key="'q-opt-' + row + '-' + optNum"
                class="bubble-item-group"
                style="cursor: pointer;"
                @click.stop="handleBubbleClick((col - 1) * rowCount + row, optNum)"
                @mouseenter="handleBubbleMouseEnter((col - 1) * rowCount + row, optNum, (8 + (props.layoutDirection === 'ltr' ? (col - 1) * colWidth : (colCount - col) * colWidth) + getBubbleCX(optIdx)), ((props.startY ?? 88) + 6 + (row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5))"
                @mouseleave="handleBubbleMouseLeave"
              >
                <!-- Inspection overlay: safe zone -->
                <circle
                  v-if="props.showInspectionOverlay"
                  :cx="getBubbleCX(optIdx)"
                  :cy="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5"
                  :r="effectiveBubbleRadius"
                  fill="none"
                  stroke="#22c55e"
                  stroke-width="0.12"
                  stroke-dasharray="0.3 0.3"
                  style="pointer-events: none;"
                />
                <!-- Inspection overlay: expanded zone -->
                <circle
                  v-if="props.showInspectionOverlay"
                  :cx="getBubbleCX(optIdx)"
                  :cy="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5"
                  :r="effectiveBubbleRadius * 1.8"
                  fill="none"
                  stroke="#f59e0b"
                  stroke-width="0.1"
                  stroke-dasharray="0.3 0.3"
                  style="pointer-events: none;"
                />

                <!-- Main bubble circle -->
                <circle
                  :cx="getBubbleCX(optIdx)"
                  :cy="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5"
                  :r="effectiveBubbleRadius"
                  :fill="getChoiceState((col - 1) * rowCount + row, optNum) === 'filled' ? '#0f172a' : 'none'"
                  :stroke="getChoiceState((col - 1) * rowCount + row, optNum) === 'filled' ? '#0f172a' : pColor"
                  stroke-width="0.28"
                />
                
                <!-- Crossed State X -->
                <g v-if="getChoiceState((col - 1) * rowCount + row, optNum) === 'crossed'">
                  <line 
                    :x1="getBubbleCX(optIdx) - effectiveBubbleRadius * 0.75" 
                    :y1="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 - effectiveBubbleRadius * 0.75" 
                    :x2="getBubbleCX(optIdx) + effectiveBubbleRadius * 0.75" 
                    :y2="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 + effectiveBubbleRadius * 0.75" 
                    stroke="#0f172a" stroke-width="0.7" stroke-linecap="round" />
                  <line 
                    :x1="getBubbleCX(optIdx) + effectiveBubbleRadius * 0.75" 
                    :y1="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 - effectiveBubbleRadius * 0.75" 
                    :x2="getBubbleCX(optIdx) - effectiveBubbleRadius * 0.75" 
                    :y2="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 + effectiveBubbleRadius * 0.75" 
                    stroke="#0f172a" stroke-width="0.7" stroke-linecap="round" />
                </g>

                <!-- Choice number label -->
                <text
                  :x="getBubbleCX(optIdx)"
                  :y="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 + effectiveBubbleRadius * 0.42"
                  font-family="sans-serif"
                  font-weight="bold"
                  :font-size="Math.min(3.2, effectiveBubbleRadius * 1.35)"
                  text-anchor="middle"
                  :fill="getChoiceState((col - 1) * rowCount + row, optNum) === 'filled' ? '#0f172a' : pColor"
                  style="pointer-events: none; user-select: none;"
                >{{ optNum }}</text>



                
                <!-- AI Verification & Grading Overlay -->
                <g v-if="props.aiResults && props.aiResults[(col - 1) * rowCount + row]">
                  <!-- Scratched/Crossed Overlay -->
                  <g v-if="(getChoiceState((col - 1) * rowCount + row, optNum) === 'filled' || getChoiceState((col - 1) * rowCount + row, optNum) === 'crossed') && props.aiResults[(col - 1) * rowCount + row].aiStatus === 'CROSSED'">
                    <line :x1="getBubbleCX(optIdx) - 1.4" :y1="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 - 1.4" :x2="getBubbleCX(optIdx) + 1.4" :y2="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 + 1.4" stroke="#ef4444" stroke-width="0.6" stroke-linecap="round" />
                    <line :x1="getBubbleCX(optIdx) + 1.4" :y1="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 - 1.4" :x2="getBubbleCX(optIdx) - 1.4" :y2="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 + 1.4" stroke="#ef4444" stroke-width="0.6" stroke-linecap="round" />
                  </g>
                  <!-- Erased Overlay -->
                  <g v-if="getChoiceState((col - 1) * rowCount + row, optNum) === 'filled' && props.aiResults[(col - 1) * rowCount + row].aiStatus === 'ERASED'">
                    <circle :cx="getBubbleCX(optIdx)" :cy="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5" r="1.4" fill="rgba(255, 255, 255, 0.75)" />
                    <line :x1="getBubbleCX(optIdx) - 1.1" :y1="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 - 1.1" :x2="getBubbleCX(optIdx) + 1.1" :y2="(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5 + 1.1" stroke="#9ca3af" stroke-width="0.4" stroke-linecap="round" />
                  </g>
                  
                  <!-- Final Result Checkmark -->
                  <path v-if="props.aiResults[(col - 1) * rowCount + row].intendedChoice === optNum && props.aiResults[(col - 1) * rowCount + row].aiStatus !== 'ERASED'" 
                        d="M -1.0 0 L -0.3 1.0 L 1.5 -1.5" 
                        :transform="`translate(${getBubbleCX(optIdx) - 3.2}, ${(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5})`" 
                        fill="none" stroke="#22c55e" stroke-width="0.6" stroke-linecap="round" stroke-linejoin="round" />
                        
                  <!-- Final Result Wrong X -->
                  <path v-if="props.aiResults[(col - 1) * rowCount + row].intendedChoice !== optNum && getChoiceState((col - 1) * rowCount + row, optNum) === 'filled' && props.aiResults[(col - 1) * rowCount + row].aiStatus !== 'ERASED'" 
                        d="M -1.0 -1.0 L 1.0 1.0 M 1.0 -1.0 L -1.0 1.0" 
                        :transform="`translate(${getBubbleCX(optIdx) - 3.2}, ${(row - 1) * effectiveRowSpacing + effectiveRowSpacing * 0.5})`" 
                        fill="none" stroke="#ef4444" stroke-width="0.6" stroke-linecap="round" />
                </g>
              </g>
            </template>
          </g>
        </g>
      </g>
    </g>

    <!-- ════════════════════════════════════════════════════════════════ -->

    <!-- Explicit Coordinates Layer (Driven directly by template contract) -->
    <!-- ════════════════════════════════════════════════════════════════ -->
    <g v-if="hasExplicitCoordinates" class="explicit-coordinates-layer">
      <g v-for="qObj in props.mcqQuestions" :key="'explicit-q-' + qObj.question_id">
        <g 
          v-for="choiceObj in qObj.choices" 
          :key="'explicit-c-' + qObj.question_id + '-' + choiceObj.choice"
          class="explicit-bubble-group"
          style="cursor: pointer;"
          @click.stop="handleBubbleClick(qObj.question_id, choiceObj.choice)"
          @mouseenter="handleBubbleMouseEnter(qObj.question_id, choiceObj.choice, getChoiceCX(choiceObj), getChoiceCY(choiceObj))"
          @mouseleave="handleBubbleMouseLeave"
        >
          <!-- Safe region overlay rectangle -->
          <rect
            v-if="props.showInspectionOverlay && choiceObj.safe_region"
            :x="choiceObj.safe_region.dx_mm"
            :y="choiceObj.safe_region.dy_mm"
            :width="choiceObj.safe_region.width_mm"
            :height="choiceObj.safe_region.height_mm"
            fill="none"
            stroke="#22c55e"
            stroke-width="0.15"
            stroke-dasharray="0.3 0.3"
            style="pointer-events: none;"
          />

          <!-- Bubble circle positioned at exact dx_mm, dy_mm -->
          <circle
            :cx="getChoiceCX(choiceObj)"
            :cy="getChoiceCY(choiceObj)"
            :r="getChoiceRadius(choiceObj)"
            :fill="getChoiceState(qObj.question_id, choiceObj.choice) === 'filled' ? '#0f172a' : 'none'"
            :stroke="getChoiceState(qObj.question_id, choiceObj.choice) === 'filled' ? '#0f172a' : pColor"
            stroke-width="0.28"
          />

          <!-- Crossed State X (Explicit layer) -->
          <g v-if="getChoiceState(qObj.question_id, choiceObj.choice) === 'crossed'">
            <line 
              :x1="getChoiceCX(choiceObj) - getChoiceRadius(choiceObj) * 0.75" 
              :y1="getChoiceCY(choiceObj) - getChoiceRadius(choiceObj) * 0.75" 
              :x2="getChoiceCX(choiceObj) + getChoiceRadius(choiceObj) * 0.75" 
              :y2="getChoiceCY(choiceObj) + getChoiceRadius(choiceObj) * 0.75" 
              stroke="#0f172a" stroke-width="0.7" stroke-linecap="round" />
            <line 
              :x1="getChoiceCX(choiceObj) + getChoiceRadius(choiceObj) * 0.75" 
              :y1="getChoiceCY(choiceObj) - getChoiceRadius(choiceObj) * 0.75" 
              :x2="getChoiceCX(choiceObj) - getChoiceRadius(choiceObj) * 0.75" 
              :y2="getChoiceCY(choiceObj) + getChoiceRadius(choiceObj) * 0.75" 
              stroke="#0f172a" stroke-width="0.7" stroke-linecap="round" />
          </g>

          <!-- Choice label inside bubble -->
          <text
            :x="getChoiceCX(choiceObj)"
            :y="getChoiceCY(choiceObj) + getChoiceRadius(choiceObj) * 0.42"
            font-family="sans-serif"
            font-weight="bold"
            :font-size="Math.min(3.2, getChoiceRadius(choiceObj) * 1.35)"
            text-anchor="middle"
            :fill="getChoiceState(qObj.question_id, choiceObj.choice) === 'filled' ? '#0f172a' : pColor"
            style="pointer-events: none; user-select: none;"
          >{{ choiceObj.choice }}</text>
        </g>
      </g>
    </g>




    <!-- FOOTER SIGNATURE BOXES -->
    <g class="footer-section">
      <rect x="8" y="284" width="82" height="11" fill="none" :stroke="pColor" stroke-width="0.35" />
      <text x="88" y="286.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="2" :fill="pColor" text-anchor="end">&#x202B;توقيع الطالب&#x202C;</text>
      <text x="10" y="286.5" font-family="Arial, sans-serif" font-weight="bold" font-size="1.8" :fill="pColor" text-anchor="start">(Student's Sign)</text>

      <rect x="98" y="284" width="104" height="11" fill="none" :stroke="pColor" stroke-width="0.35" />
      <text x="200" y="286.5" font-family="'Cairo', sans-serif" font-weight="bold" font-size="2" :fill="pColor" text-anchor="end">&#x202B;اسم وتوقيع الملاحظ&#x202C;</text>
      <text x="100" y="286.5" font-family="Arial, sans-serif" font-weight="bold" font-size="1.8" :fill="pColor" text-anchor="start">(Invigilator's Sign)</text>
    </g>

  </svg>
</template>

<script lang="ts">
export default { name: 'OmrSheetMultigraphics' };
</script>

<style scoped>
/* 
  FORCE LTR on all text elements and disable Bidi reordering 
  This ensures that when exported to Canvas (missing fonts/fallback fonts) 
  or Printed, the text elements expand predictably leftwards from the right edges, 
  and never cross boundaries. 
*/
.omr-sheet-yemen * {
  direction: ltr !important;
  unicode-bidi: normal !important;
}
.omr-sheet-yemen {
  display: block;
  background: #ffffff;
  margin: 0 auto;
  font-family: 'Cairo', system-ui, -apple-system, sans-serif;
}
</style>
