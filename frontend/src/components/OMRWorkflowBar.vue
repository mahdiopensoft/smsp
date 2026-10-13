<template>
  <div class="omr-workflow-bar mb-4">
    <div class="workflow-container">
      <div
        v-for="step in steps"
        :key="step.id"
        class="workflow-step"
        :class="{
          'is-active': currentActiveStep === step.id,
          'is-done': currentActiveStep > step.id,
          'is-upcoming': currentActiveStep < step.id,
        }"
        @click="navigateToStep(step)"
        role="button"
        tabindex="0"
      >
        <!-- Step Indicator (Number or Checkmark) -->
        <span class="step-indicator">
          <v-icon v-if="currentActiveStep > step.id" size="13" color="success">mdi-check</v-icon>
          <span v-else>{{ step.id }}</span>
        </span>

        <!-- Step Icon & Title -->
        <v-icon size="16" class="step-icon">{{ step.icon }}</v-icon>
        <span class="step-name">{{ step.title }}</span>
      </div>
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
      steps: [
        { id: 1, title: 'استلام الاختبار', route: '/omr-exams', icon: 'mdi-file-document-edit-outline' },
        { id: 2, title: 'طباعة النماذج', route: '/omr-print-registry', icon: 'mdi-printer-outline' },
        { id: 3, title: 'المسح والتصحيح', route: '/omr-scanner', icon: 'mdi-scanner' },
        { id: 4, title: 'سجل الأوراق', route: '/omr-submissions', icon: 'mdi-file-document-check-outline' },
        { id: 5, title: 'المراجعة البشرية', route: '/omr-human-review', icon: 'mdi-account-check-outline' },
        { id: 6, title: 'كشف الدرجات', route: '/omr-gradebook', icon: 'mdi-clipboard-check-multiple-outline' },
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
.omr-workflow-bar {
  direction: rtl;
}

.workflow-container {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 6px;
  gap: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.workflow-step {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
  background: transparent;
  transition: all 0.2s ease;
  user-select: none;
  white-space: nowrap;
}

.workflow-step:hover {
  background: #f8fafc;
  color: #334155;
}

.step-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #f1f5f9;
  font-size: 0.72rem;
  font-weight: 700;
  color: #64748b;
}

/* Active State */
.workflow-step.is-active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 800;
  border: 1px solid #bfdbfe;
}

.workflow-step.is-active .step-indicator {
  background: #2563eb;
  color: #ffffff;
}

/* Done State */
.workflow-step.is-done {
  color: #334155;
}

.workflow-step.is-done .step-indicator {
  background: #dcfce7;
}

/* Responsive */
@media (max-width: 900px) {
  .workflow-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 600px) {
  .workflow-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
