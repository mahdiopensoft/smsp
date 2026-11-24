<template>
  <div class="exam-pipeline-console">
    <!-- Top Executive Status Row (Inspired by OMR Scanner Live Pipeline Console) -->
    <div class="exam-pipeline-header d-flex align-center justify-space-between flex-wrap gap-3">
      <div class="d-flex align-center gap-3 min-w-0">
        <v-avatar
          :color="activeStatusColor"
          variant="tonal"
          size="46"
          class="rounded-xl flex-shrink-0 pipeline-header-avatar"
        >
          <v-icon size="25" :color="activeStatusColor">
            {{ activeStatus.type === 'error' ? 'mdi-alert-circle-outline' : (activeStepObj.icon || 'mdi-file-cog-outline') }}
          </v-icon>
        </v-avatar>

        <div class="min-w-0">
          <div class="d-flex align-center gap-2 flex-wrap">
            <span class="text-subtitle-1 font-weight-black pipeline-header-title" :class="activeTitleColorClass">
              المرحلة {{ currentStep }}: {{ activeStepObj.title }}
            </span>
            <v-chip
              size="x-small"
              :color="activeStatusColor"
              variant="flat"
              class="font-weight-bold text-white px-2.5"
            >
              {{ activeStatus.badge || 'نشط' }}
            </v-chip>
          </div>

          <div class="text-caption text-medium-emphasis d-flex align-center gap-2 mt-0.5 flex-wrap">
            <span>{{ activeStepObj.subtitle }}</span>
            <template v-if="examTitle && examTitle.trim()">
              <span class="opacity-50">•</span>
              <span class="font-weight-bold text-high-emphasis text-truncate" style="max-width: 340px;">
                {{ examTitle }}
              </span>
            </template>
          </div>
        </div>
      </div>

      <!-- Right/Left Metric Pills (Matching OMR Scanner Pills) -->
      <div class="d-flex align-center gap-2 flex-shrink-0">
        <div class="exam-step-counter-pill">
          <v-icon size="15" color="primary" class="me-1.5">mdi-layers-triple-outline</v-icon>
          <span class="font-weight-bold">المرحلة {{ currentStep }} من {{ wizardSteps.length }}</span>
        </div>
        <div
          class="exam-percentage-pill"
          :class="{
            'is-error-pill': activeStatus.type === 'error',
            'is-complete-pill': allCompleted
          }"
        >
          <span class="font-mono font-weight-black">{{ displayProgressPercent }}%</span>
        </div>
      </div>
    </div>

    <!-- Segmented Circular Stepper Pipeline (Zero Crossing Lines, Clean Node-to-Node Connectors) -->
    <div class="exam-stepper-pipeline mt-4 pt-2">
      <div class="exam-stepper-track">
        <div
          v-for="(s, idx) in wizardSteps"
          :key="s.value"
          class="exam-stepper-node"
          :class="[
            getStepNodeClasses(s.value),
            {
              'is-clickable': isStepClickable(s.value),
              'prev-completed': idx > 0 && getStepStatus(wizardSteps[idx - 1].value).type === 'completed',
              'prev-error': idx > 0 && getStepStatus(wizardSteps[idx - 1].value).type === 'error',
            }
          ]"
          role="button"
          tabindex="0"
          :aria-current="s.value === currentStep ? 'step' : undefined"
          @click="$emit('stepClick', s.value)"
          @keydown.enter.prevent="$emit('stepClick', s.value)"
        >
          <!-- Circular Node Anchor -->
          <div class="exam-circle-anchor">
            <div class="exam-stepper-circle">
              <!-- Completed: Crisp Emerald Checkmark -->
              <v-icon
                v-if="getStepStatus(s.value).type === 'completed'"
                size="26"
                color="success"
                class="checkmark-pop"
              >
                mdi-check-bold
              </v-icon>

              <!-- Error: Alert Icon -->
              <v-icon
                v-else-if="getStepStatus(s.value).type === 'error'"
                size="26"
              >
                mdi-alert-circle-outline
              </v-icon>

              <!-- Active / Pending: Semantic Step Icon -->
              <v-icon
                v-else
                size="26"
              >
                {{ s.icon }}
              </v-icon>
            </div>
          </div>

          <!-- Clean Node Typography & Inline Status -->
          <div class="exam-node-text mt-3 text-center">
            <div class="exam-node-title font-weight-black">
              {{ s.title }}
            </div>
            <div v-if="s.subtitle" class="exam-node-desc d-none d-lg-block">
              {{ s.subtitle }}
            </div>
            <div class="exam-node-status mt-1">
              <span
                v-if="getStepStatus(s.value).type === 'completed'"
                class="status-completed-text"
              >
                <v-icon size="13" class="me-0.5" color="success">mdi-check</v-icon>
                {{ getStepStatus(s.value).text }}
              </span>
              <span
                v-else-if="getStepStatus(s.value).type === 'error'"
                class="status-error-text"
              >
                <v-icon size="13" class="me-0.5" color="error">mdi-alert-circle-outline</v-icon>
                {{ getStepStatus(s.value).text }}
              </span>
              <span
                v-else-if="getStepStatus(s.value).type === 'active'"
                class="status-active-text"
              >
                {{ getStepStatus(s.value).text }}
              </span>
              <span v-else class="status-pending-text">
                في الانتظار
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentStep: {
    type: Number,
    required: true
  },
  wizardSteps: {
    type: Array,
    required: true
  },
  wizardProgressPercentage: {
    type: Number,
    default: 0
  },
  examTitle: {
    type: String,
    default: ''
  },
  isEditing: {
    type: Boolean,
    default: false
  },
  getStepNodeClasses: {
    type: Function,
    required: true
  },
  getStepStatus: {
    type: Function,
    required: true
  }
})

defineEmits(['stepClick'])

const activeStepObj = computed(() => {
  return props.wizardSteps.find(s => s.value === props.currentStep) || props.wizardSteps[0] || {}
})

const activeStatus = computed(() => {
  return props.getStepStatus(props.currentStep) || { type: 'active', badge: 'نشط', text: '' }
})

const allCompleted = computed(() => {
  return props.wizardSteps.length > 0 && props.wizardSteps.every(s => props.getStepStatus(s.value)?.type === 'completed')
})

const activeStatusColor = computed(() => {
  if (activeStatus.value.type === 'error') return 'error'
  if (activeStatus.value.type === 'completed' || allCompleted.value) return 'success'
  return 'primary'
})

const activeTitleColorClass = computed(() => {
  if (activeStatus.value.type === 'error') return 'text-error'
  if (activeStatus.value.type === 'completed' || allCompleted.value) return 'text-success'
  return 'text-primary'
})

const displayProgressPercent = computed(() => {
  if (allCompleted.value) return 100
  const total = props.wizardSteps.length || 4
  return Math.min(100, Math.max(0, Math.round((props.currentStep / total) * 100)))
})

function isStepClickable(stepVal) {
  return stepVal < props.currentStep || stepVal === props.currentStep + 1 || props.isEditing
}
</script>
