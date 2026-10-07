<template>
  <div class="scientific-formula-editor">
    <!-- Header with Label, Collapsible Toolbar Toggle, and View Modes -->
    <div class="editor-header d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
      <div class="d-flex align-center gap-2 flex-wrap">
        <v-icon color="primary" size="20">mdi-format-text</v-icon>
        <span class="text-subtitle-1 font-weight-bold editor-title-text">{{ label || 'نص السؤال' }}</span>

        <!-- Toggle Button for Scientific Formula Toolbar (Collapsible: Only shows symbols when clicked) -->
        <v-btn
          size="small"
          :variant="showToolbar ? 'flat' : 'tonal'"
          color="primary"
          class="font-weight-bold rounded-lg ms-1 formula-toggle-btn"
          :prepend-icon="showToolbar ? 'mdi-close-circle-outline' : 'mdi-function-variant'"
          @click="showToolbar = !showToolbar"
        >
          {{ showToolbar ? 'إخفاء شريط الأدوات' : 'شريط الأدوات والرموز العلمية' }}
          <v-icon end size="16">{{ showToolbar ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-btn>
      </div>

      <!-- View Modes: Edit / Split / Preview (Theme Compatible) -->
      <div class="view-mode-toggle d-flex align-center gap-1 pa-1 rounded-lg">
        <v-btn
          size="x-small"
          :variant="viewMode === 'edit' ? 'flat' : 'text'"
          :color="viewMode === 'edit' ? 'primary' : undefined"
          class="font-weight-bold view-toggle-btn"
          rounded="md"
          prepend-icon="mdi-pencil-outline"
          @click="viewMode = 'edit'"
        >
          تحرير
        </v-btn>
        <v-btn
          size="x-small"
          :variant="viewMode === 'split' ? 'flat' : 'text'"
          :color="viewMode === 'split' ? 'primary' : undefined"
          class="font-weight-bold view-toggle-btn"
          rounded="md"
          prepend-icon="mdi-view-split-vertical"
          @click="viewMode = 'split'"
        >
          منقسم
        </v-btn>
        <v-btn
          size="x-small"
          :variant="viewMode === 'preview' ? 'flat' : 'text'"
          :color="viewMode === 'preview' ? 'primary' : undefined"
          class="font-weight-bold view-toggle-btn"
          rounded="md"
          prepend-icon="mdi-eye-check-outline"
          @click="viewMode = 'preview'"
        >
          معاينة ورقة الامتحان
        </v-btn>
      </div>
    </div>

    <!-- Scientific Formula & Symbols Toolbar (Hidden by default, expands when clicked) -->
    <v-expand-transition>
      <div v-if="showToolbar" class="formula-toolbar rounded-xl mb-3 overflow-hidden">
        <!-- Category Tabs -->
        <div class="toolbar-tabs-strip d-flex align-center px-2 py-1 flex-wrap gap-1">
          <button
            v-for="cat in categories"
            :key="cat.id"
            type="button"
            class="category-tab-btn d-flex align-center gap-1 px-3 py-1 text-caption font-weight-bold rounded-lg"
            :class="{ 'is-active': activeCategory === cat.id }"
            @click="activeCategory = cat.id"
          >
            <v-icon size="15" :color="activeCategory === cat.id ? 'primary' : undefined">
              {{ cat.icon }}
            </v-icon>
            <span>{{ cat.name }}</span>
          </button>

          <v-spacer />

          <!-- Helper Actions -->
          <div class="d-flex align-center gap-1">
            <v-btn
              size="x-small"
              variant="tonal"
              color="secondary"
              class="font-weight-bold"
              prepend-icon="mdi-help-circle-outline"
              @click="helpDialog = true"
            >
              دليل الصيغ
            </v-btn>
          </div>
        </div>

        <!-- Quick Symbol Buttons for the Active Category -->
        <div class="symbols-palette pa-2 d-flex flex-wrap align-center gap-1">
          <button
            v-for="(item, idx) in currentCategoryItems"
            :key="idx"
            type="button"
            class="symbol-action-btn d-flex align-center justify-center rounded-lg"
            :title="item.title"
            @click="insertSymbol(item)"
          >
            <span v-if="item.displayHtml" v-html="item.displayHtml"></span>
            <span v-else class="font-mono text-caption font-weight-bold">{{ item.label }}</span>
          </button>
        </div>
      </div>
    </v-expand-transition>

    <!-- Main Workspace (Editor / Preview / Split) -->
    <div class="editor-workspace" :class="`workspace-${viewMode}`">
      <!-- Editor Column -->
      <div v-show="viewMode === 'edit' || viewMode === 'split'" class="editor-pane">
        <div class="position-relative">
          <textarea
            ref="textareaRef"
            :value="modelValue"
            class="scientific-textarea w-100 rounded-lg pa-3"
            :rows="rows || 5"
            :placeholder="placeholder || 'اكتب نص السؤال هنا... يمكنك إدراج الكسور والمعادلات من الشريط بالأعلى أو كتابة رموز LaTeX بين علامتي $ مثل: $x^2 + \\frac{1}{2}$'"
            @input="onInput"
          ></textarea>

          <!-- Character & Formula Counter / Hint -->
          <div class="editor-footer-hint d-flex align-center justify-space-between px-2 pt-1 text-caption text-medium-emphasis">
            <span>
              نصيحة: ضع الصيغ الرياضية بين علامتي <code>$معادلة$</code> للعرض المضمن أو <code>$$معادلة$$</code> للعرض المنفصل في سطر مستقل.
            </span>
            <span class="font-mono">{{ modelValue ? modelValue.length : 0 }} حرف</span>
          </div>
        </div>
      </div>

      <!-- Live Exam Preview Column -->
      <div v-show="viewMode === 'preview' || viewMode === 'split'" class="preview-pane">
        <div class="exam-paper-preview rounded-lg pa-4 border-subtle">
          <div class="d-flex align-center justify-space-between mb-2 border-b-subtle pb-2">
            <span class="text-caption font-weight-bold text-success d-flex align-center gap-1">
              <v-icon size="14" color="success">mdi-check-decagram</v-icon>
              المعاينة الحية لورقة الاختبار (كما تظهر للطالب)
            </span>
            <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
              معاينة تلقائية فورية
            </v-chip>
          </div>

          <div v-if="!modelValue || !modelValue.trim()" class="text-center py-6 text-medium-emphasis">
            <v-icon size="32" class="mb-2 opacity-40">mdi-eye-outline</v-icon>
            <div class="text-caption">اكتب نص السؤال أو اضغط على أي رمز بالأعلى لرؤية النتيجة المباشرة هنا</div>
          </div>

          <!-- Formatted Rendered Output -->
          <div v-else class="scientific-rendered-content text-body-1" v-html="renderedHtml"></div>
        </div>
      </div>
    </div>

    <!-- Formula Syntax Help Dialog -->
    <v-dialog v-model="helpDialog" max-width="700">
      <v-card class="pa-5 rounded-2xl">
        <div class="d-flex align-center justify-space-between mb-3">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary">mdi-school</v-icon>
            <h3 class="text-h6 font-weight-bold mb-0">دليل كتابة المعادلات والرموز العلمية</h3>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="helpDialog = false" />
        </div>

        <p class="text-caption text-medium-emphasis mb-4">
          يدعم النظام كافة صيغ LaTeX ورموز الكيمياء والفيزياء العالمية المعيارية لجميع المراحل المدرسية والجامعية:
        </p>

        <v-table density="compact" class="rounded-xl border-subtle mb-4">
          <thead>
            <tr class="bg-surface-variant">
              <th class="font-weight-bold">الموضوع العلمي</th>
              <th class="font-weight-bold">طريقة الكتابة</th>
              <th class="font-weight-bold">النتيجة في الامتحان</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>الكسور الاعتيادية</td>
              <td class="font-mono text-caption text-primary">$\frac{a}{b}$ أو $\frac{x+1}{x-1}$</td>
              <td>كسر هندسي كامل ببسط ومقام وخط أفقي</td>
            </tr>
            <tr>
              <td>الجذور التربيعية والنونية</td>
              <td class="font-mono text-caption text-primary">$\sqrt{x}$ أو $\sqrt[3]{27}$</td>
              <td>رمز الجذر مع الخط العلوي الممتد</td>
            </tr>
            <tr>
              <td>الأسس والدليل السفلي</td>
              <td class="font-mono text-caption text-primary">$x^2$ و $x_i$ و $e^{-x}$</td>
              <td>قوى وأدلة سفلية منسقة بدقة</td>
            </tr>
            <tr>
              <td>التكاملات والمشتقات</td>
              <td class="font-mono text-caption text-primary">$\int_{0}^{\pi} \sin(x) dx$</td>
              <td>رمز التكامل مع حدي التكامل العلوي والسفلي</td>
            </tr>
            <tr>
              <td>النهايات والمجاميع</td>
              <td class="font-mono text-caption text-primary">$\lim_{x \to \infty} f(x)$ و $\sum_{i=1}^{n} x_i$</td>
              <td>رمز النهاية والمجموع مع المتغير</td>
            </tr>
            <tr>
              <td>المعادلات الكيميائية</td>
              <td class="font-mono text-caption text-primary">2H_2 + O_2 -> 2H_2O أو $\rightleftharpoons$</td>
              <td>أسهم تفاعل كيميائي، اتزان ديناميكي، وحالات المادة (s, l, g, aq)</td>
            </tr>
            <tr>
              <td>الأيونات والشحنات</td>
              <td class="font-mono text-caption text-primary">$\text{Ca}^{2+} + \text{SO}_4^{2-}$</td>
              <td>أيونات وشحنات كهربائية دقيقة</td>
            </tr>
            <tr>
              <td>المصفوفات والمحددات</td>
              <td class="font-mono text-caption text-primary">$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$</td>
              <td>مصفوفات 2×2 و 3×3 بأقواس دائرية أو خطية</td>
            </tr>
            <tr>
              <td>الرموز الإغريقية</td>
              <td class="font-mono text-caption text-primary">$\alpha, \beta, \theta, \lambda, \pi, \Omega$</td>
              <td>ألفا، بيتا، سيتا، لامدا، باي، أوم للمقاومة</td>
            </tr>
            <tr>
              <td>كتل البرمجة (CS)</td>
              <td class="font-mono text-caption text-primary">```python\nprint("Hello")\n```</td>
              <td>كتلة كود برمجي بخط أحادي وتنسيق داكن</td>
            </tr>
          </tbody>
        </v-table>

        <div class="d-flex justify-end">
          <v-btn color="primary" class="font-weight-bold" rounded="lg" @click="helpDialog = false">
            فهمت ذلك
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { parseScientificMarkup, ensureKaTeXLoaded } from '@/utils/scientificRenderer'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: 'نص السؤال'
  },
  placeholder: {
    type: String,
    default: ''
  },
  rows: {
    type: Number,
    default: 5
  },
  compact: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const textareaRef = ref(null)
const showToolbar = ref(false) // Hidden by default, toggles on button click
const viewMode = ref('edit') // 'edit', 'split', 'preview'
const activeCategory = ref('math')
const helpDialog = ref(false)

// Dynamically load KaTeX from CDN for ultra-fast LaTeX typography if available
onMounted(() => {
  ensureKaTeXLoaded()
})

// Categories
const categories = [
  { id: 'math', name: 'رياضيات وجبر', icon: 'mdi-calculator-variant' },
  { id: 'calculus', name: 'تفاضل ومصفوفات', icon: 'mdi-chart-bell-curve-cumulative' },
  { id: 'chemistry', name: 'كيمياء وتفاعلات', icon: 'mdi-flask-outline' },
  { id: 'physics', name: 'فيزياء وإغريقي', icon: 'mdi-atom' },
  { id: 'cs', name: 'برمجة ومنطق', icon: 'mdi-code-braces' }
]

// Symbols and Snippets Database
const symbolsDB = {
  math: [
    { label: 'a/b', title: 'كسر اعتيادي', snippet: '\\frac{a}{b}', displayHtml: '<span class="d-inline-flex flex-column align-center lh-1" style="font-size: 11px;"><span style="border-bottom: 1px solid currentColor;">a</span><span>b</span></span>' },
    { label: '√x', title: 'جذر تربيعي', snippet: '\\sqrt{x}', displayHtml: '<span>&radic;x</span>' },
    { label: 'ⁿ√x', title: 'جذر نوني', snippet: '\\sqrt[n]{x}', displayHtml: '<span><sup>n</sup>&radic;x</span>' },
    { label: 'x²', title: 'أس تربيعي', snippet: 'x^{2}', displayHtml: '<span>x<sup>2</sup></span>' },
    { label: 'xⁿ', title: 'أس نوني', snippet: 'x^{n}', displayHtml: '<span>x<sup>n</sup></span>' },
    { label: 'x₁', title: 'دليل سفلي', snippet: 'x_{1}', displayHtml: '<span>x<sub>1</sub></span>' },
    { label: '(x)', title: 'أقواس دائرية', snippet: '\\left( x \\right)', displayHtml: '<span>(x)</span>' },
    { label: '[x]', title: 'أقواس مربعة', snippet: '\\left[ x \\right]', displayHtml: '<span>[x]</span>' },
    { label: '|x|', title: 'قيمة مطلقة', snippet: '\\left| x \\right|', displayHtml: '<span>|x|</span>' },
    { label: '±', title: 'زائد أو ناقص', snippet: '\\pm ', displayHtml: '<span>&plusmn;</span>' },
    { label: '×', title: 'ضرب', snippet: '\\times ', displayHtml: '<span>&times;</span>' },
    { label: '÷', title: 'قسمة', snippet: '\\div ', displayHtml: '<span>&divide;</span>' },
    { label: '≠', title: 'لا يساوي', snippet: '\\ne ', displayHtml: '<span>&ne;</span>' },
    { label: '≤', title: 'أصغر من أو يساوي', snippet: '\\le ', displayHtml: '<span>&le;</span>' },
    { label: '≥', title: 'أكبر من أو يساوي', snippet: '\\ge ', displayHtml: '<span>&ge;</span>' },
    { label: '≈', title: 'تقريباً', snippet: '\\approx ', displayHtml: '<span>&asymp;</span>' },
    { label: 'π', title: 'باي (نسبة تقريبية)', snippet: '\\pi ', displayHtml: '<span>&pi;</span>' },
    { label: '∞', title: 'مالانهاية', snippet: '\\infty ', displayHtml: '<span>&infin;</span>' },
    { label: '°', title: 'درجة زاوية/حرارة', snippet: '^{\\circ}', displayHtml: '<span>&deg;</span>' },
    { label: '∠', title: 'زاوية هندسية', snippet: '\\angle ', displayHtml: '<span>&ang;</span>' },
    { label: 'Δ', title: 'دلتا / مثلث', snippet: '\\Delta ', displayHtml: '<span>&Delta;</span>' },
    { label: '⊥', title: 'عمودي على', snippet: '\\perp ', displayHtml: '<span>&perp;</span>' },
    { label: '∥', title: 'يوازي', snippet: '\\parallel ', displayHtml: '<span>&#8741;</span>' }
  ],

  calculus: [
    { label: '∫ dx', title: 'تكامل غير محدد', snippet: '\\int f(x) \\, dx', displayHtml: '<span>&int; dx</span>' },
    { label: '∫ᵇₐ', title: 'تكامل محدد من a إلى b', snippet: '\\int_{a}^{b} f(x) \\, dx', displayHtml: '<span>&int;<sub>a</sub><sup>b</sup></span>' },
    { label: '∬', title: 'تكامل ثنائي', snippet: '\\iint_{D} f(x, y) \\, dA', displayHtml: '<span>&int;&int;</span>' },
    { label: '∮', title: 'تكامل خطي مغلق', snippet: '\\oint_{C} f(z) \\, dz', displayHtml: '<span>&#8750;</span>' },
    { label: 'dy/dx', title: 'مشتقة أولى', snippet: '\\frac{dy}{dx}', displayHtml: '<span>dy/dx</span>' },
    { label: '∂f/∂x', title: 'مشتقة جزئية', snippet: '\\frac{\\partial f}{\\partial x}', displayHtml: '<span>&part;f/&part;x</span>' },
    { label: 'lim', title: 'نهاية عند اللانهاية', snippet: '\\lim_{x \\to \\infty} f(x)', displayHtml: '<span>lim<sub>x&rarr;&infin;</sub></span>' },
    { label: 'lim₀', title: 'نهاية عند الصفر', snippet: '\\lim_{x \\to 0} f(x)', displayHtml: '<span>lim<sub>x&rarr;0</sub></span>' },
    { label: '∑', title: 'مجموع من 1 إلى n', snippet: '\\sum_{i=1}^{n} x_i', displayHtml: '<span>&sum;<sub>i=1</sub><sup>n</sup></span>' },
    { label: '∏', title: 'جداء من 1 إلى n', snippet: '\\prod_{i=1}^{n} x_i', displayHtml: '<span>&prod;</span>' },
    { label: 'v⃗', title: 'متجه', snippet: '\\vec{v}', displayHtml: '<span>v&#8407;</span>' },
    { label: '∇', title: 'معامل نَبلا / تدرج', snippet: '\\nabla ', displayHtml: '<span>&nabla;</span>' },
    { label: '[2×2]', title: 'مصفوفة 2 في 2', snippet: '\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}', displayHtml: '<span>[2&times;2]</span>' },
    { label: '[3×3]', title: 'مصفوفة 3 في 3', snippet: '\\begin{pmatrix} a_{11} & a_{12} & a_{13} \\\\ a_{21} & a_{22} & a_{23} \\\\ a_{31} & a_{32} & a_{33} \\end{pmatrix}', displayHtml: '<span>[3&times;3]</span>' },
    { label: '|det|', title: 'محدد مصفوفة', snippet: '\\begin{vmatrix} a & b \\\\ c & d \\end{vmatrix}', displayHtml: '<span>|det|</span>' },
    { label: 'ℝ', title: 'مجموعة الأعداد الحقيقية', snippet: '\\mathbb{R}', displayHtml: '<span>&#8477;</span>' },
    { label: 'ℤ', title: 'مجموعة الأعداد الصحيحة', snippet: '\\mathbb{Z}', displayHtml: '<span>&#8484;</span>' },
    { label: '∈', title: 'ينتمي إلى', snippet: '\\in ', displayHtml: '<span>&isin;</span>' },
    { label: '∉', title: 'لا ينتمي إلى', snippet: '\\notin ', displayHtml: '<span>&notin;</span>' },
    { label: '⊂', title: 'مجموعة جزئية', snippet: '\\subset ', displayHtml: '<span>&sub;</span>' },
    { label: '∪', title: 'اتحاد', snippet: '\\cup ', displayHtml: '<span>&cup;</span>' },
    { label: '∩', title: 'تقاطع', snippet: '\\cap ', displayHtml: '<span>&cap;</span>' },
    { label: '∅', title: 'المجموعة الخالية فاي', snippet: '\\emptyset ', displayHtml: '<span>&empty;</span>' }
  ],

  chemistry: [
    { label: '→', title: 'سهم تفاعل أمامي', snippet: ' \\rightarrow ', displayHtml: '<span>&rarr;</span>' },
    { label: '⇄', title: 'سهم اتزان كيميائي', snippet: ' \\rightleftharpoons ', displayHtml: '<span>&#8652;</span>' },
    { label: 'Δ→', title: 'تفاعل حراري (تسخين)', snippet: ' \\xrightarrow{\\Delta} ', displayHtml: '<span>&Delta;&rarr;</span>' },
    { label: 'hν→', title: 'تفاعل ضوئي', snippet: ' \\xrightarrow{h\\nu} ', displayHtml: '<span>h&nu;&rarr;</span>' },
    { label: 'cat→', title: 'تفاعل مع عامل حفاز', snippet: ' \\xrightarrow{\\text{catalyst}} ', displayHtml: '<span>cat&rarr;</span>' },
    { label: '↑', title: 'تصاعد غاز', snippet: '\\uparrow ', displayHtml: '<span>&uarr;</span>' },
    { label: '↓', title: 'تكون راسب', snippet: '\\downarrow ', displayHtml: '<span>&darr;</span>' },
    { label: '(s)', title: 'حالة صلبة Solid', snippet: '_{(s)} ', displayHtml: '<span>(s)</span>' },
    { label: '(l)', title: 'حالة سائلة Liquid', snippet: '_{(l)} ', displayHtml: '<span>(l)</span>' },
    { label: '(g)', title: 'حالة غازية Gas', snippet: '_{(g)} ', displayHtml: '<span>(g)</span>' },
    { label: '(aq)', title: 'محلول مائي Aqueous', snippet: '_{(aq)} ', displayHtml: '<span>(aq)</span>' },
    { label: 'H₂O', title: 'الماء', snippet: '\\text{H}_2\\text{O}', displayHtml: '<span>H<sub>2</sub>O</span>' },
    { label: 'CO₂', title: 'ثاني أكسيد الكربون', snippet: '\\text{CO}_2', displayHtml: '<span>CO<sub>2</sub></span>' },
    { label: 'H₂SO₄', title: 'حمض الكبريتيك', snippet: '\\text{H}_2\\text{SO}_4', displayHtml: '<span>H<sub>2</sub>SO<sub>4</sub></span>' },
    { label: 'H⁺', title: 'أيون الهيدروجين / بروتون', snippet: '\\text{H}^+', displayHtml: '<span>H<sup>+</sup></span>' },
    { label: 'OH⁻', title: 'أيون الهيدروكسيد', snippet: '\\text{OH}^-', displayHtml: '<span>OH<sup>-</sup></span>' },
    { label: 'Ca²⁺', title: 'أيون الكالسيوم', snippet: '\\text{Ca}^{2+}', displayHtml: '<span>Ca<sup>2+</sup></span>' },
    { label: 'SO₄²⁻', title: 'أيون الكبريتات', snippet: '\\text{SO}_4^{2-}', displayHtml: '<span>SO<sub>4</sub><sup>2-</sup></span>' },
    { label: 'Fe³⁺', title: 'أيون الحديد الثلاثي', snippet: '\\text{Fe}^{3+}', displayHtml: '<span>Fe<sup>3+</sup></span>' },
    { label: '²³⁵U', title: 'نظير اليورانيوم', snippet: '^{235}_{\\ 92}\\text{U}', displayHtml: '<span><sup>235</sup>U</span>' },
    { label: 'ΔH°', title: 'حرارة التفاعل القياسية', snippet: '\\Delta H^\\circ', displayHtml: '<span>&Delta;H&deg;</span>' },
    { label: 'pH', title: 'الرقم الهيدروجيني', snippet: '\\text{pH} = -\\log[\\text{H}^+]', displayHtml: '<span>pH</span>' }
  ],

  physics: [
    { label: 'α', title: 'ألفا', snippet: '\\alpha ', displayHtml: '<span>&alpha;</span>' },
    { label: 'β', title: 'بيتا', snippet: '\\beta ', displayHtml: '<span>&beta;</span>' },
    { label: 'γ', title: 'جاما', snippet: '\\gamma ', displayHtml: '<span>&gamma;</span>' },
    { label: 'θ', title: 'ثيتا (زاوية)', snippet: '\\theta ', displayHtml: '<span>&theta;</span>' },
    { label: 'λ', title: 'لامدا (طول موجي)', snippet: '\\lambda ', displayHtml: '<span>&lambda;</span>' },
    { label: 'μ', title: 'ميكرو / معامل احتكاك', snippet: '\\mu ', displayHtml: '<span>&mu;</span>' },
    { label: 'ρ', title: 'رو (كثافة / مقاومية)', snippet: '\\rho ', displayHtml: '<span>&rho;</span>' },
    { label: 'σ', title: 'سيجما (إجهاد / توصيلية)', snippet: '\\sigma ', displayHtml: '<span>&sigma;</span>' },
    { label: 'ω', title: 'أوميجا (سرعة زاوية)', snippet: '\\omega ', displayHtml: '<span>&omega;</span>' },
    { label: 'Ω', title: 'أوم (مقاومة كهربائية)', snippet: '\\Omega ', displayHtml: '<span>&Omega;</span>' },
    { label: 'm/s', title: 'متر لكل ثانية (سرعة)', snippet: '\\text{ m/s}', displayHtml: '<span>m/s</span>' },
    { label: 'm/s²', title: 'عجلة / تسارع', snippet: '\\text{ m/s}^2', displayHtml: '<span>m/s<sup>2</sup></span>' },
    { label: 'N', title: 'نيوتن (قوة)', snippet: '\\text{ N}', displayHtml: '<span>N</span>' },
    { label: 'J', title: 'جول (طاقة / شغل)', snippet: '\\text{ J}', displayHtml: '<span>J</span>' },
    { label: 'W', title: 'واط (قدرة)', snippet: '\\text{ W}', displayHtml: '<span>W</span>' },
    { label: 'Hz', title: 'هيرتز (تردد)', snippet: '\\text{ Hz}', displayHtml: '<span>Hz</span>' },
    { label: 'μF', title: 'ميكروفاراد (سعة مكثف)', snippet: '\\mu\\text{F}', displayHtml: '<span>&mu;F</span>' },
    { label: 'F⃗=ma⃗', title: 'قانون نيوتن الثاني', snippet: '\\vec{F} = m\\vec{a}', displayHtml: '<span>F=ma</span>' },
    { label: 'E=mc²', title: 'معادلة أينشتاين للطاقة', snippet: 'E = mc^2', displayHtml: '<span>E=mc<sup>2</sup></span>' },
    { label: '°C', title: 'درجة مئوية', snippet: '^\\circ\\text{C}', displayHtml: '<span>&deg;C</span>' },
    { label: 'K', title: 'كلفن (حرارة مطلقة)', snippet: '\\text{ K}', displayHtml: '<span>K</span>' }
  ],

  cs: [
    { label: '∧', title: 'منطق AND (عطف)', snippet: ' \\land ', displayHtml: '<span>&and;</span>' },
    { label: '∨', title: 'منطق OR (فصل)', snippet: ' \\lor ', displayHtml: '<span>&or;</span>' },
    { label: '¬', title: 'منطق NOT (نفي)', snippet: '\\neg ', displayHtml: '<span>&not;</span>' },
    { label: '⊕', title: 'منطق XOR', snippet: ' \\oplus ', displayHtml: '<span>&oplus;</span>' },
    { label: '⇒', title: 'يقتضي (إذا كان... فإن)', snippet: ' \\implies ', displayHtml: '<span>&rArr;</span>' },
    { label: '⇔', title: 'يكافئ منطقياً (إذا وفقط إذا)', snippet: ' \\iff ', displayHtml: '<span>&hArr;</span>' },
    { label: '∀', title: 'لكل (مسوّر كلي)', snippet: '\\forall ', displayHtml: '<span>&forall;</span>' },
    { label: '∃', title: 'يوجد (مسوّر جزئي)', snippet: '\\exists ', displayHtml: '<span>&exist;</span>' },
    { label: '```code```', title: 'كتلة كود برمجي', snippet: '\n```python\n# اكتب الكود هنا\ndef solution(x):\n    return x * 2\n```\n', displayHtml: '<span>{ code }</span>' },
    { label: '`inline`', title: 'كود مضمن بالسطر', snippet: '`var x = 10;`', displayHtml: '<span>`var`</span>' },
    {
      label: 'جدول صواب',
      title: 'جدول الصواب والخطأ Truth Table',
      snippet: '\n| A | B | A ∧ B | A ∨ B |\n|---|---|-------|-------|\n| 0 | 0 | 0     | 0     |\n| 0 | 1 | 0     | 1     |\n| 1 | 0 | 0     | 1     |\n| 1 | 1 | 1     | 1     |\n',
      displayHtml: '<span>Table</span>'
    }
  ]
}

const currentCategoryItems = computed(() => {
  return symbolsDB[activeCategory.value] || []
})

// Input Handler
function onInput(e) {
  emit('update:modelValue', e.target.value)
}

// Insert Symbol or Snippet at cursor position
function insertSymbol(item) {
  const textarea = textareaRef.value
  if (!textarea) {
    emit('update:modelValue', (props.modelValue || '') + item.snippet)
    return
  }

  const start = textarea.selectionStart || 0
  const end = textarea.selectionEnd || 0
  const original = props.modelValue || ''

  let textToInsert = item.snippet
  // If user has highlighted text and clicks fraction or root, wrap selection!
  if (start !== end) {
    const selected = original.substring(start, end)
    if (item.snippet.includes('\\frac{a}{b}')) {
      textToInsert = `\\frac{${selected}}{b}`
    } else if (item.snippet.includes('\\sqrt{x}')) {
      textToInsert = `\\sqrt{${selected}}`
    } else if (item.snippet.includes('x^{2}')) {
      textToInsert = `${selected}^{2}`
    } else {
      textToInsert = item.snippet
    }
  }

  // Wrap with $ $ if it is a LaTeX formula and not already in math delimiters
  const before = original.substring(0, start)
  const after = original.substring(end)
  
  // Check if we are already inside a $...$ block
  const dollarCountBefore = (before.match(/\$/g) || []).length
  const isInsideMath = dollarCountBefore % 2 === 1

  if (!isInsideMath && !textToInsert.startsWith('$') && !textToInsert.startsWith('`') && !textToInsert.startsWith('\n|') && (textToInsert.includes('\\') || textToInsert.includes('^') || textToInsert.includes('_'))) {
    textToInsert = `$${textToInsert}$`
  }

  const newText = before + textToInsert + after
  emit('update:modelValue', newText)

  // Restore focus and cursor position after insertion
  nextTick(() => {
    textarea.focus()
    const newPos = start + textToInsert.length
    textarea.setSelectionRange(newPos, newPos)
  })
}

// =========================================================================
// Real-Time Scientific Renderer (KaTeX + Built-in Mathematical Typography)
// =========================================================================
const renderedHtml = computed(() => {
  return parseScientificMarkup(props.modelValue || '')
})
</script>

<style scoped>
.scientific-formula-editor {
  width: 100%;
}

.editor-title-text {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== View Mode Toggle (Theme-Adaptive) ===== */
.view-mode-toggle {
  background: rgba(var(--v-theme-on-surface), 0.05);
  border: 1px solid rgba(var(--v-border-color), 0.14);
}

.view-toggle-btn {
  color: rgba(var(--v-theme-on-surface), 0.75);
}

/* ===== Collapsible Formula Toolbar (Theme-Adaptive) ===== */
.formula-toolbar {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), 0.16);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.toolbar-tabs-strip {
  background: rgba(var(--v-theme-on-surface), 0.03);
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
}

.category-tab-btn {
  border: none;
  background: transparent;
  color: rgba(var(--v-theme-on-surface), 0.7);
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.category-tab-btn:hover {
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
}

.category-tab-btn.is-active {
  background: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-primary));
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.symbols-palette {
  background: rgb(var(--v-theme-surface));
  max-height: 130px;
  overflow-y: auto;
}

.symbol-action-btn {
  min-width: 36px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid rgba(var(--v-border-color), 0.14);
  background: rgba(var(--v-theme-on-surface), 0.03);
  color: rgb(var(--v-theme-on-surface));
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
}

.symbol-action-btn:hover {
  background: rgba(var(--v-theme-primary), 0.12);
  border-color: rgba(var(--v-theme-primary), 0.45);
  color: rgb(var(--v-theme-primary));
  transform: translateY(-1px);
}

/* ===== Workspace & Textarea (Theme-Adaptive) ===== */
.editor-workspace {
  display: grid;
  gap: 16px;
}

.workspace-edit {
  grid-template-columns: 1fr;
}

.workspace-preview {
  grid-template-columns: 1fr;
}

.workspace-split {
  grid-template-columns: 1fr 1fr;
}

@media (max-width: 960px) {
  .workspace-split {
    grid-template-columns: 1fr;
  }
}

.scientific-textarea {
  border: 1.5px solid rgba(var(--v-border-color), 0.2);
  background: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-on-surface));
  font-family: inherit;
  font-size: 0.98rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.scientific-textarea:focus {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.15);
}

.scientific-textarea::placeholder {
  color: rgba(var(--v-theme-on-surface), 0.4);
}

/* ===== Exam Paper Preview Panel ===== */
.exam-paper-preview {
  background: rgb(var(--v-theme-surface));
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25);
  min-height: 150px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
  color: rgb(var(--v-theme-on-surface));
}

.scientific-rendered-content {
  line-height: 1.9;
  font-size: 1.05rem;
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Built-in Math Fallback Styling ===== */
:deep(.inline-fraction) {
  display: inline-flex;
  flex-direction: column;
  vertical-align: middle;
  text-align: center;
  padding: 0 4px;
  font-size: 0.9em;
  line-height: 1.1;
  color: inherit;
}

:deep(.fraction-bar) {
  border-top: 1.5px solid currentColor;
  width: 100%;
  margin: 1px 0;
}

:deep(.math-root) {
  display: inline-flex;
  align-items: center;
  font-size: 1.1em;
  color: inherit;
}

:deep(.root-overbar) {
  border-top: 1.5px solid currentColor;
  padding: 0 2px;
}

:deep(.math-big-symbol) {
  font-size: 1.35em;
  line-height: 1;
  padding: 0 2px;
  vertical-align: -0.15em;
  color: inherit;
}

:deep(.math-op) {
  font-weight: bold;
  padding: 0 2px;
  color: inherit;
}

:deep(.math-arrow-cond) {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  padding: 0 4px;
  font-size: 0.85em;
  color: inherit;
}

:deep(.scientific-table) {
  border-collapse: collapse;
  margin: 8px 0;
  color: inherit;
}

:deep(.scientific-table th), :deep(.scientific-table td) {
  border: 1px solid rgba(var(--v-border-color), 0.18);
  color: inherit;
}
</style>
