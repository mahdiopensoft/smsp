<template>
  <VSnackbar
    v-model="value"
    :location="location || 'top end'"
    :timeout="timeout || 3000"
    variant="flat"
    class="ultimate-snack"
    :class="[`snack-type-${color || 'primary'}`]"
    transition="slide-y-reverse-transition"
  >
    <div class="snack-wrapper d-flex align-center w-100 overflow-hidden">
      <!-- High-Intensity Status Indicator -->
      <div class="status-indicator flex-shrink-0" :class="[`bg-${color || 'primary'}`]"></div>

      <div class="d-flex align-center w-100 pa-4 py-3">
        <!-- Icon Stage with subtle pulse -->
        <div 
          v-if="icon" 
          class="icon-stage me-4 d-flex align-center justify-center rounded-lg"
          :style="{ backgroundColor: `rgba(var(--v-theme-${color || 'primary'}), 0.1)` }"
        >
          <VIcon 
            :icon="'mdi-' + icon" 
            size="24" 
            :color="color || 'primary'"
            class="snack-icon-pulse"
          />
        </div>

        <!-- Text Content Block -->
        <div class="flex-grow-1 pe-4">
          <div class="text-subtitle-1 font-weight-bold snack-title" style="color: rgb(var(--v-theme-on-surface))">
            {{ title }}
          </div>
        </div>

        <!-- Action / Close Zone -->
        <div class="ms-auto d-flex align-center ps-2">
          <slot name="action"></slot>
          
          <VBtn
            v-if="!$slots.action"
            icon="mdi-close"
            variant="tonal"
            size="x-small"
            color="grey"
            class="close-btn-minimal"
            @click="value = false"
          />
        </div>
      </div>
    </div>
  </VSnackbar>
</template>

<script>
export default {
  props: {
    title: String,
    icon: String,
    color: {
      type: String,
      default: "primary"
    },
    location: {
      type: String,
      default: "top right"
    },
    timeout: {
      type: [Number, String],
      default: 3000
    },
    modelValue: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
};
</script>

<style scoped>
/* Reset and Refine Snackbar Wrapper */
.ultimate-snack :deep(.v-snackbar__wrapper) {
  background-color: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.12);
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1), 
    0 10px 30px -5px rgba(0, 0, 0, 0.2),
    inset 0 0 0 1px rgba(var(--v-theme-on-surface), 0.05) !important;
  border-radius: 14px !important;
  min-width: 320px !important;
  max-width: 480px !important;
  margin: 16px !important;
}

.ultimate-snack :deep(.v-snackbar__content) {
  padding: 0 !important;
}

.snack-wrapper {
  min-height: 70px;
  position: relative;
}

.status-indicator {
  width: 5px;
  align-self: stretch;
}

.icon-stage {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border: 1px solid rgba(var(--v-border-color), 0.03);
}

.snack-title {
  line-height: 1.3;
  letter-spacing: -0.3px;
  font-size: 0.95rem !important;
}

.close-btn-minimal {
  opacity: 0.4;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.close-btn-minimal:hover {
  opacity: 1;
  transform: rotate(90deg);
  background-color: rgba(var(--v-theme-on-surface), 0.05);
}

/* RTL Support for indicator */
[dir="rtl"] .status-indicator {
  order: 2;
}

/* Entrance Pulse for the icon */
@keyframes softPulse {
  0% { transform: scale(0.85); opacity: 0.8; }
  50% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}

.snack-icon-pulse {
  animation: softPulse 0.4s ease-out forwards;
}

/* Mobile Optimizations */
@media (max-width: 600px) {
  .ultimate-snack :deep(.v-snackbar__wrapper) {
    min-width: calc(100vw - 32px) !important;
    margin: 16px !important;
  }
}
</style>
