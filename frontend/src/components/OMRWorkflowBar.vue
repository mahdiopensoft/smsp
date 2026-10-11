<template>
  <div class="omr-workflow-bar-wrapper mb-6">
    <v-card elevation="0" class="omr-workflow-card border rounded-2xl overflow-hidden">
      <!-- Ribbon Header -->
      <div class="d-flex align-center justify-space-between px-4 py-2 bg-workflow-header border-b">
        <div class="d-flex align-center gap-2">
          <v-avatar size="28" color="primary" variant="tonal" class="rounded-lg">
            <v-icon size="16">mdi-sitemap-outline</v-icon>
          </v-avatar>
          <span class="text-subtitle-2 font-weight-black text-on-surface">
            مسار مراحل دورة التصحيح الآلي والكنترول (OMR Pipeline)
          </span>
          <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold ms-2">
            {{ activeStepTitle }}
          </v-chip>
        </div>

        <div class="d-flex align-center gap-2">
          <span class="text-caption text-medium-emphasis d-none d-md-inline">
            انقر على أي مرحلة للانتقال المباشر إليها
          </span>
          <v-btn
            size="x-small"
            variant="text"
            icon
            color="medium-emphasis"
            @click="isCollapsed = !isCollapsed"
            :title="isCollapsed ? 'توسيع شريط المراحل' : 'طي شريط المراحل'"
          >
            <v-icon size="18">{{ isCollapsed ? 'mdi-chevron-down' : 'mdi-chevron-up' }}</v-icon>
          </v-btn>
        </div>
      </div>

      <!-- Collapsible Stepper Content -->
      <v-expand-transition>
        <div v-show="!isCollapsed" class="pa-3 pa-md-4 bg-workflow-body">
          <div class="omr-stepper-container">
            <template v-for="(step, index) in steps" :key="step.id">
              <!-- Step Card Item -->
              <div
                class="omr-step-item"
                :class="{
                  'active-step': currentActiveStep === step.id,
                  'completed-step': currentActiveStep > step.id,
                  'future-step': currentActiveStep < step.id,
                }"
                @click="navigateToStep(step)"
                role="button"
                :title="step.description"
              >
                <!-- Step Circle / Icon -->
                <div class="step-badge-wrapper">
                  <div class="step-badge">
                    <v-icon v-if="currentActiveStep > step.id" size="16" color="white">mdi-check</v-icon>
                    <span v-else class="step-number">{{ step.id }}</span>
                  </div>
                  <v-icon :size="18" class="step-icon">{{ step.icon }}</v-icon>
                </div>

                <!-- Step Texts -->
                <div class="step-text-container">
                  <div class="step-title font-weight-black">
                    {{ step.title }}
                  </div>
                  <div class="step-subtitle text-caption text-truncate">
                    {{ step.subtitle }}
                  </div>
                </div>

                <!-- Active Indicator Pin -->
                <div v-if="currentActiveStep === step.id" class="step-active-tag">
                  أنت هنا
                </div>
              </div>

              <!-- Connecting Arrow (between items) -->
              <div v-if="index < steps.length - 1" class="step-connector">
                <v-icon size="18" color="medium-emphasis">mdi-chevron-left</v-icon>
              </div>
            </template>
          </div>
        </div>
      </v-expand-transition>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'OMRWorkflowBar',

  props: {
    activeStep: {
      type: Number,
      default: 6,
    },
    examId: {
      type: [String, Number],
      default: null,
    },
  },

  data() {
    return {
      isCollapsed: false,
      steps: [
        {
          id: 1,
          title: 'استلام الاختبار',
          subtitle: 'تجهيز الاختبار والنماذج',
          route: '/omr-exams',
          icon: 'mdi-file-document-edit-outline',
          description: 'المرحلة 1: استلام وتجهيز بيانات ونماذج الاختبار من بنك الأسئلة',
        },
        {
          id: 2,
          title: 'سجل الطباعة',
          subtitle: 'تصدير أوراق الإجابة',
          route: '/omr-print-registry',
          icon: 'mdi-printer-outline',
          description: 'المرحلة 2: توليد وتصدير أوراق البابل شيت المشفرة وتوزيعها للطلاب',
        },
        {
          id: 3,
          title: 'معمل المسح الآلي',
          subtitle: 'سحب الأوراق والتصحيح',
          route: '/omr-scanner-lab',
          icon: 'mdi-scanner',
          description: 'المرحلة 3: سحب ومسح الأوراق الضوئية ومعالجتها آلياً بمحرك OMR',
        },
        {
          id: 4,
          title: 'سجل الأوراق المصححة',
          subtitle: 'أوراق الطلاب والنتائج',
          route: '/omr-submissions',
          icon: 'mdi-file-check-outline',
          description: 'المرحلة 4: استعراض كافة أوراق الطلاب المصححة وتفاصيل الإجابات والدرجات',
        },
        {
          id: 5,
          title: 'التدقيق البشري',
          subtitle: 'معالجة الحالات المعلقة',
          route: '/omr-human-review',
          icon: 'mdi-account-check-outline',
          description: 'المرحلة 5: مراجعة وتدقيق أوراق الاستثناءات والتظليل المزدوج والالتباس',
        },
        {
          id: 6,
          title: 'كشف الدرجات والكنترول',
          subtitle: 'اعتماد وترحيل الدرجات',
          route: '/omr-gradebook',
          icon: 'mdi-clipboard-check-multiple-outline',
          description: 'المرحلة 6: مراجعة كشوف الرصد النهائية وترحيل الدرجات لنظام الكنترول',
        },
      ],
    }
  },

  computed: {
    currentActiveStep() {
      if (this.activeStep) return this.activeStep
      // Auto-detect based on current route
      const path = this.$route.path
      if (path.includes('exams')) return 1
      if (path.includes('print')) return 2
      if (path.includes('scanner')) return 3
      if (path.includes('submissions')) return 4
      if (path.includes('human-review')) return 5
      if (path.includes('gradebook')) return 6
      return 6
    },

    activeStepTitle() {
      const step = this.steps.find((s) => s.id === this.currentActiveStep)
      return step ? `المرحلة ${step.id}: ${step.title}` : 'مسار التصحيح'
    },
  },

  methods: {
    navigateToStep(step) {
      if (this.currentActiveStep === step.id) return
      const query = {}
      if (this.examId) {
        query.exam = this.examId
      }
      this.$router.push({ path: step.route, query })
    },
  },
}
</script>

<style scoped>
.omr-workflow-bar-wrapper {
  direction: rtl;
}

.omr-workflow-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-color: rgba(226, 232, 240, 0.9) !important;
  box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05) !important;
}

.bg-workflow-header {
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

.bg-workflow-body {
  background: #ffffff;
}

.omr-stepper-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  overflow-x: auto;
  padding: 4px 2px;
}

/* Step Item */
.omr-step-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.22s ease-in-out;
  flex: 1 1 0;
  min-width: 155px;
  position: relative;
  user-select: none;
}

.omr-step-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08);
  border-color: #cbd5e1;
}

/* Badge & Icon */
.step-badge-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
}

.step-badge {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #94a3b8;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.78rem;
  transition: all 0.2s ease;
}

.step-icon {
  color: #64748b;
  transition: color 0.2s ease;
}

.step-text-container {
  min-width: 0;
}

.step-title {
  font-size: 0.82rem;
  color: #1e293b;
  line-height: 1.25;
  white-space: nowrap;
}

.step-subtitle {
  font-size: 0.69rem;
  color: #64748b;
  line-height: 1.2;
}

/* Connector */
.step-connector {
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.55;
  flex-shrink: 0;
}

/* State: Completed Step */
.completed-step {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.completed-step .step-badge {
  background: #10b981;
}

.completed-step .step-icon {
  color: #059669;
}

.completed-step .step-title {
  color: #065f46;
}

/* State: Active Step */
.active-step {
  background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%);
  border-color: #6366f1 !important;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.2) !important;
  transform: scale(1.02);
}

.active-step .step-badge {
  background: #4f46e5;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.4);
}

.active-step .step-icon {
  color: #4f46e5;
}

.active-step .step-title {
  color: #312e81;
}

.active-step .step-subtitle {
  color: #4338ca;
  font-weight: 600;
}

.step-active-tag {
  position: absolute;
  top: -9px;
  left: 10px;
  background: #4f46e5;
  color: #ffffff;
  font-size: 0.62rem;
  font-weight: 900;
  padding: 1px 8px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(79, 70, 229, 0.35);
  letter-spacing: 0.2px;
}

/* State: Future Step */
.future-step {
  opacity: 0.85;
}

.future-step:hover {
  opacity: 1;
}

@media (max-width: 960px) {
  .omr-step-item {
    min-width: 140px;
    padding: 6px 10px;
  }
  .step-subtitle {
    display: none;
  }
}
</style>
