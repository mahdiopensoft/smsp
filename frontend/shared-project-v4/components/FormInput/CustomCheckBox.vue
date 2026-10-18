<template>
  <!-- Screen mode -->
  <v-col :cols="12" :lg="cols" :md="cols" class="py-2" v-if="!state.print">
    <div
      class="premium-checkbox-wrapper"
      :class="{
        'is-checked': value,
        'is-disabled': disabled || readonly,
      }"
      :style="{
        width: width,
      }"
      @click="value = !value"
    >
      <VCheckbox
        v-model="value"
        :label="label"
        :rules="rules"
        :width="width"
        :hide-details="hideDetails"
        :disabled="disabled"
        :readonly="readonly"
        color="success"
        class="premium-checkbox"
        density="compact"
        @update:modelValue="changeData"
      />
    </div>
  </v-col>

  <!-- Print mode -->
  <v-col :cols="12" :lg="cols" :md="cols" class="py-1" v-if="state.print">
    {{ value ? "true" : "false" }}
  </v-col>
</template>

<script setup>
import { state } from "@/../src/store/state";
</script>

<script>
export default {
  props: {
    cols: {
      type: [String],
      default: "12",
    },
    modelValue: {
      type: [Number, String],
      default: null,
    },
    label: {
      type: String,
      default: "",
    },
    rules: {
      type: Array,
      default: () => [],
    },
    width: String,
    hideDetails: {
      type: [String, Boolean],
      default: true,
    },
    disabled: false,
    readonly: false,
  },
  methods: {
    changeData(newValue) {
      this.$emit("@change", newValue);
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
/* ══════════════════════════════════════════════════
   PREMIUM CHECKBOX — Green Theme & Matched Sizing
   ══════════════════════════════════════════════════ */

.premium-checkbox-wrapper {
  display: flex;
  align-items: center;
  padding: 0 12px;
  min-height: 40px; /* Matches standard compact input height */
  border-radius: var(--radius-md, 8px);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  background: rgb(var(--v-theme-surface));
  cursor: pointer;
  transition: all 0.25s ease;
  user-select: none;
  min-width: 53px;
}

/* ── Active State (Success Green) ── */
.is-checked {
  border-color: rgba(var(--v-theme-success), 0.25);
  background: rgba(var(--v-theme-success), 0.04);
}

/* ── Hover ── */
.premium-checkbox-wrapper:hover:not(.is-disabled):not(.is-checked) {
  border-color: rgba(var(--v-theme-on-surface), 0.15);
  background: rgba(var(--v-theme-on-surface), 0.02);
}

/* ── Disabled ── */
.is-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* ── Internal Vuetify Overrides ── */
.premium-checkbox {
  width: 100%;
}

.premium-checkbox :deep(.v-selection-control) {
  min-height: 40px;
}

.premium-checkbox :deep(.v-label) {
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.65);
  padding-inline-start: 8px;
  opacity: 1 !important;
  transition: all 0.2s ease;
}

.is-checked .premium-checkbox :deep(.v-label) {
  color: rgb(var(--v-theme-success));
  font-weight: 700;
}

.premium-checkbox :deep(.v-checkbox-btn .v-selection-control__wrapper) {
  color: rgba(var(--v-theme-on-surface), 0.2);
}

.is-checked .premium-checkbox :deep(.v-checkbox-btn .v-selection-control__wrapper) {
  color: rgb(var(--v-theme-success));
}

/* RTL Support */
[dir="rtl"] .premium-checkbox :deep(.v-label) {
  font-family: "Tajawal", sans-serif !important;
}
</style>
