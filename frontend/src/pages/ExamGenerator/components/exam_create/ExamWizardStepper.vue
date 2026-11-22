<template>
  <div class="premium-wizard-wrapper">
    <div class="premium-wizard-container">
      <!-- Connecting Progress Line with RTL support -->
      <div class="wizard-progress-track">
        <div
          class="wizard-progress-fill"
          :style="{ width: wizardProgressPercentage + '%' }"
        >
          <span class="wizard-beam-glow"></span>
        </div>
      </div>

      <!-- Step Nodes -->
      <div
        v-for="s in wizardSteps"
        :key="s.value"
        class="premium-wizard-node"
        :class="getStepNodeClasses(s.value)"
        @click="$emit('stepClick', s.value)"
      >
        <!-- Circular Node Anchor -->
        <div class="stepper-circle-anchor">
          <!-- Number badge on top-right corner -->
          <span class="node-step-number">{{ s.value }}</span>

          <!-- Active pulsing wave ring for active or warning steps -->
          <span
            v-if="getStepStatus(s.value).type === 'active'"
            class="stepper-pulse-ring pulse-primary"
          ></span>
          <span
            v-else-if="getStepStatus(s.value).type === 'error'"
            class="stepper-pulse-ring pulse-error"
          ></span>

          <div class="stepper-circle">
            <!-- If Completed/Success: Show Animated Green Checkmark -->
            <v-icon
              v-if="getStepStatus(s.value).type === 'completed'"
              size="22"
              color="success"
              class="checkmark-pop text-success"
            >
              mdi-check-bold
            </v-icon>

            <!-- If Error/Failure: Show Alert Icon -->
            <v-icon
              v-else-if="getStepStatus(s.value).type === 'error'"
              size="22"
              class="error-icon-shake"
            >
              mdi-alert-circle
            </v-icon>

            <!-- Otherwise (Active / Pending): Show Step Custom Icon -->
            <v-icon
              v-else
              size="20"
              :class="{ 'icon-active-breath': getStepStatus(s.value).type === 'active' }"
            >
              {{ s.icon }}
            </v-icon>
          </div>
        </div>

        <!-- Step Titles & Explicit Status Pill -->
        <div class="node-content text-center mt-2">
          <span class="node-title font-weight-black">{{ s.title }}</span>
          <span v-if="s.subtitle" class="node-subtitle text-caption text-medium-emphasis d-none d-lg-block">
            {{ s.subtitle }}
          </span>

          <!-- Explicit Status Indicator (نجاح / فشل / قيد الضبط / انتظار) -->
          <div class="node-status-badge-wrapper mt-1">
            <span
              class="node-status-pill font-weight-bold"
              :class="`status-${getStepStatus(s.value).type}`"
            >
              <v-icon
                size="11"
                class="me-1"
                :color="getStepStatus(s.value).type === 'completed' ? 'success' : undefined"
              >
                {{ getStepStatus(s.value).statusIcon }}
              </v-icon>
              {{ getStepStatus(s.value).text }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
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
</script>
