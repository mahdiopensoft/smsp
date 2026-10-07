<script setup lang="ts">
import { ref } from 'vue';
import OmrSheetMultigraphics from '../../components/omr_templates/OmrSheetMultigraphics.vue';

// Reactive State
const studentName = ref('أحمد علي عبد الله المحمدي');
const examName = ref('الكيمياء العامة - المنهج الوزاري');
const barcodeValue = ref('9671020324');

const layoutDirection = ref<'ltr' | 'rtl'>('rtl');
const bubbleType = ref<'letters' | 'numbers'>('letters');
const showInspection = ref(false);
const studentAnswers = ref<Record<number, string>>({});
const answerKey = ref<Record<number, string>>({});
const hoveredBubble = ref<{ questionId: number; choice: string; x: number; y: number } | null>(null);

// Grading Results
const gradingResult = ref<{
  totalQuestions: number;
  totalAnswered: number;
  correctCount: number;
  wrongCount: number;
  unansweredCount: number;
  scorePercent: number;
  details: Array<{ questionId: number; studentChoice: string; correctChoice: string; isCorrect: boolean; darknessPercent: number; aiStatus: string }>;
} | null>(null);

// Toggle or Set Bubble Fill
function onBubbleClick(payload: { questionId: number; choice: string }) {
  const current = studentAnswers.value[payload.questionId];
  if (current === payload.choice) {
    delete studentAnswers.value[payload.questionId];
  } else {
    studentAnswers.value[payload.questionId] = payload.choice;
  }
}

function onBubbleHover(payload: { questionId: number; choice: string; x: number; y: number } | null) {
  hoveredBubble.value = payload;
}

// Auto Actions
function fillSampleStudentAnswers() {
  const choices = ['1', '2', '3', '4'];
  const newAns: Record<number, string> = {};
  for (let q = 1; q <= 180; q++) {
    const correct = answerKey.value[q] || choices[(q - 1) % 4];
    if (q % 20 === 0) {
      newAns[q] = choices[(choices.indexOf(correct) + 1) % 4]; // intentionally wrong
    } else if (q % 35 === 0) {
      // Leave empty
    } else {
      newAns[q] = correct;
    }
  }
  studentAnswers.value = newAns;
}

function generateSampleAnswerKey() {
  const choices = ['1', '2', '3', '4'];
  const newKey: Record<number, string> = {};
  for (let q = 1; q <= 180; q++) {
    newKey[q] = choices[(q * 7) % 4];
  }
  answerKey.value = newKey;
}

function clearAll() {
  studentAnswers.value = {};
  answerKey.value = {};
  gradingResult.value = null;
}

// Run Local OMR Pipeline Grading Simulation
function runOmrPipeline() {
  if (Object.keys(answerKey.value).length === 0) {
    generateSampleAnswerKey();
  }

  let correct = 0;
  let wrong = 0;
  let unanswered = 0;
  const details = [];

  for (let q = 1; q <= 180; q++) {
    const sAns = studentAnswers.value[q] || '';
    const kAns = answerKey.value[q] || '';

    let isCorr = false;
    let darkness = 0;
    let aiState = 'EMPTY';

    if (!sAns) {
      unanswered++;
      darkness = 12.4;
      aiState = 'EMPTY';
    } else if (sAns === kAns) {
      correct++;
      isCorr = true;
      darkness = 94.2 + (q % 5);
      aiState = 'FILLED';
    } else {
      wrong++;
      darkness = 89.1 + (q % 5);
      aiState = 'FILLED';
      // Simulate advanced AI states for some incorrect answers
      if (q % 13 === 0) {
         aiState = 'CROSSED';
      } else if (q % 17 === 0) {
         aiState = 'ERASED';
      }
    }

    details.push({
      questionId: q,
      studentChoice: sAns || '-',
      correctChoice: kAns || '-',
      isCorrect: isCorr,
      darknessPercent: darkness,
      aiStatus: aiState,
    });
  }

  const totalAns = correct + wrong;
  const scorePct = Number(((correct / 180) * 100).toFixed(1));

  gradingResult.value = {
    totalQuestions: 180,
    totalAnswered: totalAns,
    correctCount: correct,
    wrongCount: wrong,
    unansweredCount: unanswered,
    scorePercent: scorePct,
    details,
  };
}

// Export SVG to High-Res PNG Image @ 300 DPI (Base64 Encoded to avoid canvas tainting)
async function exportHighResImage() {
  const svgEl = document.querySelector('.omr-sheet-yemen') as SVGElement;
  if (!svgEl) return;

  const svgString = new XMLSerializer().serializeToString(svgEl);
  const svgBase64 = 'data:image/svg+xml;charset=utf-8;base64,' + btoa(unescape(encodeURIComponent(svgString)));

  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.onload = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 2480;
    canvas.height = 3508;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      
      const a = document.createElement('a');
      a.download = `OMR_Yemen_Sheet_${barcodeValue.value}.png`;
      a.href = canvas.toDataURL('image/png');
      a.click();
    }
  };
  img.src = svgBase64;
}


// Initialize answer key
generateSampleAnswerKey();

import { computed } from 'vue';

const aiResultsMap = computed(() => {
  const map: Record<number, any> = {};
  if (gradingResult.value) {
    gradingResult.value.details.forEach(d => {
      map[d.questionId] = d;
    });
  }
  return map;
});
</script>

<template>
  <div class="qb-omr-demo-v4" dir="rtl">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">mdi-tune-vertical-variant</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">منصة معايرة وقراءة نموذج تصحيح جامعة صنعاء</h1>
          <p class="text-caption text-medium-emphasis mb-0">اختبار الفحص المليمتري وتوليد نماذج الإجابة عالية الدقة</p>
        </div>
      </div>

      <!-- Action Toolbar -->
      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          variant="outlined"
          rounded="lg"
          class="font-weight-bold"
          @click="layoutDirection = layoutDirection === 'rtl' ? 'ltr' : 'rtl'"
        >
          {{ layoutDirection === 'rtl' ? 'النموذج عربي (RTL)' : 'النموذج إنجليزي (LTR)' }}
        </v-btn>

        <v-btn
          variant="outlined"
          rounded="lg"
          class="font-weight-bold"
          @click="bubbleType = bubbleType === 'letters' ? 'numbers' : 'letters'"
        >
          {{ bubbleType === 'letters' ? 'الخيارات: (A,B,C,D)' : 'الخيارات: (1,2,3,4)' }}
        </v-btn>

        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-pencil"
          @click="fillSampleStudentAnswers"
        >
          تظليل إجابات الطالب
        </v-btn>

        <v-btn
          color="primary"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-lightning-bolt"
          @click="runOmrPipeline"
        >
          تشغيل المحرك والذكاء الاصطناعي
        </v-btn>

        <v-btn
          color="success"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-download"
          @click="exportHighResImage"
        >
          تصدير صورة 300DPI
        </v-btn>

        <v-btn
          color="error"
          variant="tonal"
          rounded="lg"
          icon="mdi-delete-outline"
          class="font-weight-bold"
          @click="clearAll"
          title="تصفير"
        />
      </div>
    </div>

    <!-- Main Workspace Grid -->
    <div class="studio-body">
      <!-- Sidebar Control & HUD Panel -->
      <aside class="studio-sidebar">
        <!-- Precision Inspection HUD Card -->
        <div class="panel-card hud-card" :class="{ highlighted: hoveredBubble }">
          <div class="card-header-icon">
            <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/></svg>
            <h3>لوحة المعايرة الهندسية (Precision HUD)</h3>
          </div>
          <div v-if="hoveredBubble" class="hud-details">
            <div class="hud-row">
              <span class="lbl">السؤال المفحوص:</span>
              <span class="val highlight">سؤال {{ hoveredBubble.questionId }}</span>
            </div>
            <div class="hud-row">
              <span class="lbl">رمز الخيار:</span>
              <span class="val highlight">خيار [ {{ hoveredBubble.choice }} ]</span>
            </div>
            <div class="hud-row">
              <span class="lbl">الإحداثيات الهندسية:</span>
              <span class="val">({{ hoveredBubble.x.toFixed(1) }}mm, {{ hoveredBubble.y.toFixed(1) }}mm)</span>
            </div>
            <div class="hud-row">
              <span class="lbl">نطاق Safe Region:</span>
              <span class="val green">r = 1.10mm (قطر 2.2mm)</span>
            </div>
            <div class="hud-row">
              <span class="lbl">نطاق Expanded Region:</span>
              <span class="val amber">r = 2.20mm (قطر 4.4mm)</span>
            </div>
            <div class="hud-row">
              <span class="lbl">حالة التظليل:</span>
              <span class="val" :class="studentAnswers[hoveredBubble.questionId] === hoveredBubble.choice ? 'status-filled' : 'status-empty'">
                {{ studentAnswers[hoveredBubble.questionId] === hoveredBubble.choice ? 'مظللة بالكامل (FILLED)' : 'فارغة (EMPTY)' }}
              </span>
            </div>
          </div>
          <div v-else class="hud-placeholder">
            <p>قم بتمرير مؤشر الماوس فوق أي دائرة خيار في الورقة لعرض إحداثياتها الهندسية المليمتري الصريحة ونطاقات الحماية الآمنة.</p>
          </div>
        </div>

        <!-- Student & Test Metadata Form -->
        <div class="panel-card">
          <div class="card-header-icon">
            <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            <h3>بيانات النموذج والتشفير</h3>
          </div>
          <div class="form-group">
            <label>اسم الطالب الرباعي:</label>
            <input v-model="studentName" type="text" class="input-control" />
          </div>
          <div class="form-group">
            <label>المادة / المقرر الدراسية:</label>
            <input v-model="examName" type="text" class="input-control" />
          </div>
          <div class="form-group">
            <label>رمز الباركود وتشفير النموذج:</label>
            <input v-model="barcodeValue" type="text" class="input-control" />
          </div>
        </div>

        <!-- OMR Grading Summary Report -->
        <div v-if="gradingResult" class="panel-card score-card">
          <div class="card-header-icon">
            <svg class="section-icon text-green" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <h3>نتيجة التصحيح الآلي المعتمدة</h3>
          </div>
          <div class="score-main">
            <div class="score-number">{{ gradingResult.scorePercent }}%</div>
            <div class="score-label">إجمالي النتيجة ({{ gradingResult.correctCount }} من {{ gradingResult.totalQuestions }})</div>
          </div>
          <div class="score-stats">
            <div class="stat-item green">
              <span class="num">{{ gradingResult.correctCount }}</span>
              <span class="lbl">صحيحة</span>
            </div>
            <div class="stat-item red">
              <span class="num">{{ gradingResult.wrongCount }}</span>
              <span class="lbl">خاطئة</span>
            </div>
            <div class="stat-item gray">
              <span class="num">{{ gradingResult.unansweredCount }}</span>
              <span class="lbl">غير مجاب</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- Central Sheet Canvas Viewer -->
      <main class="sheet-canvas-container">
        <div class="canvas-paper">
          <OmrSheetMultigraphics
            :layout-direction="layoutDirection"
            :bubble-type="bubbleType"
            :student-name="studentName"
            :exam-name="examName"
            :barcode-value="barcodeValue"
            :student-answers="studentAnswers"
            :answer-key="answerKey"
            :show-inspection-overlay="showInspection"
            :ai-results="aiResultsMap"
            @bubble-click="onBubbleClick"
            @bubble-hover="onBubbleHover"
          />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.omr-studio-view {
  min-height: 100vh;
  background-color: #0f172a;
  color: #f8fafc;
  font-family: 'Cairo', system-ui, -apple-system, sans-serif;
}

.studio-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1e293b;
  border-bottom: 1px solid #334155;
}

.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.7rem;
  font-weight: 800;
  color: #e6007e;
  letter-spacing: 0.05em;
  margin-bottom: 0.2rem;
}
.icon-brand {
  width: 14px;
  height: 14px;
}

.brand-title h1 {
  font-size: 1.15rem;
  font-weight: 800;
  color: #f8fafc;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.6rem;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.9rem;
  border-radius: 0.375rem;
  font-family: inherit;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.btn-toggle-inspection {
  background-color: #334155;
  color: #f8fafc;
  border: 1px solid #475569;
}
.btn-toggle-inspection.active {
  background-color: #166534;
  color: #86efac;
  border-color: #22c55e;
}

.btn-primary { background-color: #e6007e; color: #ffffff; }
.btn-primary:hover { background-color: #c00069; }

.btn-accent { background-color: #0284c7; color: #ffffff; }
.btn-accent:hover { background-color: #0369a1; }

.btn-success { background-color: #16a34a; color: #ffffff; }
.btn-success:hover { background-color: #15803d; }

.btn-danger { background-color: #dc2626; color: #ffffff; }
.btn-danger:hover { background-color: #b91c1c; }

.studio-body {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
}

.studio-sidebar {
  width: 380px;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  flex-shrink: 0;
}

.panel-card {
  background-color: #1e293b;
  border: 1px solid #334155;
  border-radius: 0.5rem;
  padding: 1.25rem;
}

.card-header-icon {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.section-icon {
  width: 18px;
  height: 18px;
  color: #38bdf8;
}

.panel-card h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #f8fafc;
  margin: 0;
}

.hud-card {
  border-color: #0284c7;
  background-color: rgba(2, 132, 199, 0.05);
}
.hud-card.highlighted {
  border-color: #e6007e;
  background-color: rgba(230, 0, 126, 0.08);
}

.hud-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.82rem;
}

.hud-row {
  display: flex;
  justify-content: space-between;
}
.hud-row .lbl { color: #94a3b8; }
.hud-row .val { font-weight: 700; color: #f8fafc; }
.hud-row .val.highlight { color: #e6007e; }
.hud-row .val.green { color: #4ade80; }
.hud-row .val.amber { color: #fbbf24; }

.status-filled { color: #e6007e; font-weight: 800; }
.status-empty { color: #64748b; }

.hud-placeholder p {
  color: #64748b;
  font-size: 0.82rem;
  margin: 0;
  line-height: 1.5;
}

.form-group {
  margin-bottom: 0.85rem;
}
.form-group label {
  display: block;
  font-size: 0.78rem;
  color: #94a3b8;
  margin-bottom: 0.35rem;
}
.input-control {
  width: 100%;
  padding: 0.45rem 0.65rem;
  background-color: #0f172a;
  border: 1px solid #334155;
  border-radius: 0.25rem;
  color: #f8fafc;
  font-family: inherit;
  font-size: 0.82rem;
}

.score-card {
  border-color: #22c55e;
  background-color: rgba(34, 197, 94, 0.05);
  text-align: center;
}
.score-main { margin-bottom: 1rem; }
.score-number { font-size: 2.2rem; font-weight: 900; color: #4ade80; }
.score-label { font-size: 0.82rem; color: #94a3b8; }

.score-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 0.75rem;
  border-top: 1px solid #334155;
}
.stat-item {
  display: flex;
  flex-direction: column;
}
.stat-item .num { font-size: 1.15rem; font-weight: 800; }
.stat-item .lbl { font-size: 0.75rem; color: #94a3b8; }
.stat-item.green .num { color: #4ade80; }
.stat-item.red .num { color: #f87171; }
.stat-item.gray .num { color: #94a3b8; }

.sheet-canvas-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  overflow: auto;
}

.canvas-paper {
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
}
</style>
