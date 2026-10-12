<template>
  <div class="omr-pipeline-wrapper mb-5">
    <div class="omr-pipeline-card">
      <!-- Top Slim Progress Bar -->
      <div class="pipeline-progress-track">
        <div
          class="pipeline-progress-fill"
          :style="{ width: `${progressPercentage}%` }"
        ></div>
      </div>

      <!-- Header Ribbon -->
      <div class="pipeline-header px-4 py-2 d-flex align-center justify-space-between">
        <div class="d-flex align-center gap-3">
          <div class="pipeline-icon-box">
            <v-icon size="17" color="primary">mdi-sitemap-outline</v-icon>
          </div>
          <div class="d-flex align-center gap-2">
            <span class="pipeline-title font-weight-black">مسار دورة التصحيح الآلي</span>
            <span class="pipeline-divider">/</span>
            <span class="pipeline-active-label font-weight-bold">
              المرحلة {{ currentActiveStep }} من {{ steps.length }}: {{ currentStepObj?.title }}
            </span>
          </div>
        </div>

        <div class="d-flex align-center gap-2">
          <v-chip
            size="x-small"
            variant="tonal"
            :color="currentActiveStep === 6 ? 'success' : 'primary'"
            class="font-weight-black px-2"
          >
            {{ progressPercentage }}% منجز
          </v-chip>

          <v-btn
            size="x-small"
            variant="text"
            icon
            density="comfortable"
            color="medium-emphasis"
            @click="isCollapsed = !isCollapsed"
            :title="isCollapsed ? 'إظهار مسار المراحل' : 'طي مسار المراحل'"
          >
            <v-icon size="16">{{ isCollapsed ? 'mdi-chevron-down' : 'mdi-chevron-up' }}</v-icon>
          </v-btn>
        </div>
      </div>

      <!-- Pipeline Steps (Collapsible) -->
      <v-expand-transition>
        <div v-show="!isCollapsed" class="pipeline-steps-wrapper pa-2 pa-md-3">
          <div class="pipeline-grid">
            <div
              v-for="(step, index) in steps"
              :key="step.id"
              class="pipeline-step-item"
              :class="{
                'is-active': currentActiveStep === step.id,
                'is-completed': currentActiveStep > step.id,
                'is-upcoming': currentActiveStep < step.id,
              }"
              @click="navigateToStep(step)"
              role="button"
              :tabindex="0"
              @keydown.enter="navigateToStep(step)"
            >
              <!-- Number & Status Indicator -->
              <div class="step-num-badge">
                <v-icon v-if="currentActiveStep > step.id" size="14" color="white">mdi-check</v-icon>
                <span v-else class="num-text">0{{ step.id }}</span>
              </div>

              <!-- Icon & Titles -->
              <div class="step-content">
                <div class="d-flex align-center gap-1">
                  <v-icon size="16" class="step-icon">{{ step.icon }}</v-icon>
                  <span class="step-main-title">{{ step.title }}</span>
                </div>
                <span class="step-sub-title text-truncate">{{ step.subtitle }}</span>
              </div>

              <!-- Current Step Inline Chip -->
              <div v-if="currentActiveStep === step.id" class="step-current-pill">
                الحالية
              </div>
            </div>
          </div>
        </div>
      </v-expand-transition>
    </div>
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
          subtitle: 'نماذج ومفاتيح الإجابة',
          route: '/omr-exams',
          icon: 'mdi-file-document-edit-outline',
        },
        {
          id: 2,
          title: 'طباعة النماذج',
          subtitle: 'توليد أوراق البابل شيت',
          route: '/omr-print-registry',
          icon: 'mdi-printer-outline',
        },
        {
          id: 3,
          title: 'المسح والتصحيح',
          subtitle: 'سحب الأوراق والمعالجة',
          route: '/omr-scanner',
          icon: 'mdi-scanner',
        },
        {
          id: 4,
          title: 'سجل الأوراق',
          subtitle: 'نتائج التصحيح والتدقيق',
          route: '/omr-submissions',
          icon: 'mdi-file-document-check-outline',
        },
        {
          id: 5,
          title: 'المراجعة البشرية',
          subtitle: 'معالجة الاستثناءات والشك',
          route: '/omr-human-review',
          icon: 'mdi-account-check-outline',
        },
        {
          id: 6,
          title: 'كشف الدرجات',
          subtitle: 'الرصد وترحيل الكنترول',
          route: '/omr-gradebook',
          icon: 'mdi-clipboard-check-multiple-outline',
        },
      ],
    }
  },

  computed: {
    currentActiveStep() {
      if (this.activeStep) return this.activeStep
      const path = this.$route.path
      if (path.includes('exams')) return 1
      if (path.includes('print')) return 2
      if (path.includes('scanner')) return 3
      if (path.includes('submissions')) return 4
      if (path.includes('human-review')) return 5
      if (path.includes('gradebook')) return 6
      return 6
    },

    currentStepObj() {
      return this.steps.find((s) => s.id === this.currentActiveStep) || this.steps[0]
    },

    progressPercentage() {
      return Math.round((this.currentActiveStep / this.steps.length) * 100)
    },
  },

  methods: {
    navigateToStep(step) {
      if (this.currentActiveStep === step.id) return
      const query = {}
      const targetExam = this.examId || this.$route.query.exam
      if (targetExam) {
        query.exam = targetExam
      }
      this.$router.push({ path: step.route, query })
    },
  },
}
</script>

<style scoped>
.omr-pipeline-wrapper {
  direction: rtl;
}

.omr-pipeline-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
  position: relative;
}

/* Progress Bar Track */
.pipeline-progress-track {
  width: 100%;
  height: 3px;
  background: #f1f5f9;
  position: relative;
  overflow: hidden;
}

.pipeline-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #3b82f6 50%, #4f46e5 100%);
  transition: width 0.4s ease-in-out;
}

/* Header */
.pipeline-header {
  background: #f8fafc;
  border-bottom: 1px solid #eef2f6;
}

.pipeline-icon-box {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  background: rgba(79, 70, 229, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.pipeline-title {
  font-size: 0.82rem;
  color: #334155;
}

.pipeline-divider {
  color: #cbd5e1;
  font-size: 0.8rem;
}

.pipeline-active-label {
  font-size: 0.82rem;
  color: #4f46e5;
}

/* Grid Layout for Steps */
.pipeline-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
}

/* Step Item */
.pipeline-step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  user-select: none;
  min-width: 0;
}

.pipeline-step-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
}

/* Step Number */
.step-num-badge {
  width: 24px;
  height: 24px;
  min-width: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.72rem;
  font-weight: 800;
  transition: all 0.2s ease;
}

.num-text {
  letter-spacing: -0.5px;
}

/* Content */
.step-content {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.step-main-title {
  font-size: 0.78rem;
  font-weight: 800;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.step-sub-title {
  font-size: 0.67rem;
  line-height: 1.2;
  margin-top: 2px;
}

.step-icon {
  flex-shrink: 0;
}

/* State: Completed */
.is-completed {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.is-completed .step-num-badge {
  background: #10b981;
  color: #ffffff;
}

.is-completed .step-icon {
  color: #10b981;
}

.is-completed .step-main-title {
  color: #334155;
}

.is-completed .step-sub-title {
  color: #64748b;
}

.is-completed:hover {
  border-color: #10b981;
  background: #f0fdf4;
}

/* State: Active */
.is-active {
  background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
  border-color: transparent !important;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.28) !important;
}

.is-active .step-num-badge {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
  backdrop-filter: blur(4px);
}

.is-active .step-icon {
  color: #ffffff;
}

.is-active .step-main-title {
  color: #ffffff;
}

.is-active .step-sub-title {
  color: rgba(255, 255, 255, 0.85);
}

.step-current-pill {
  position: absolute;
  top: 4px;
  left: 6px;
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
  font-size: 0.58rem;
  font-weight: 800;
  padding: 1px 5px;
  border-radius: 4px;
  line-height: 1.2;
}

/* State: Upcoming */
.is-upcoming {
  background: #fafbfc;
  border-color: #edf2f7;
  opacity: 0.82;
}

.is-upcoming .step-num-badge {
  background: #e2e8f0;
  color: #64748b;
}

.is-upcoming .step-icon {
  color: #94a3b8;
}

.is-upcoming .step-main-title {
  color: #475569;
}

.is-upcoming .step-sub-title {
  color: #94a3b8;
}

.is-upcoming:hover {
  opacity: 1;
  border-color: #cbd5e1;
  background: #ffffff;
}

/* Responsive */
@media (max-width: 1200px) {
  .pipeline-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .pipeline-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .step-sub-title {
    display: none;
  }
}
</style>
