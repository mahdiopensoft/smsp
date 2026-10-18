<template>
  <!-- added by samer -->
  <v-col :cols="12" :lg="cols" :md="cols" class="py-2">
    <v-textarea
      v-model="value"
      :label="label + (isRequired ? '   *' : '')"
      density="compact"
      :prepend-inner-icon="icon ? 'mdi-' + icon : ''"
      counter
      :placeholder="placeholder"
      :rules="rules"
      :type="type"
      :max-length="maxLength"
      :readonly="readonly"
      :disabled="disabled"
      :error-messages="error_messages"
      :variant="variant"
      class="no-autofill-bg my-0"
      dir="ltr"
      :width="width"
      @append-outer-icon-click="append_click"
      :hide-details="hideDetails"
      :rows="rows"
    >
      <template #clear="{ props }">
        <VIcon v-if="clearable" v-bind="props" icon="mdi-close-circle" tabindex="-1" />
      </template>
    </v-textarea>
  </v-col>
</template>
<script setup>
import { VTextarea } from "vuetify/components";
</script>
<script>
export default {
  props: {
    // Layout & Appearance
    cols: {
      type: [String, Number],
      default: "12",
    },
    width: {
      type: String,
      default: "100%",
    },

    // Input & Behavior
    modelValue: {
      type: [String, Number],
      default: null,
    },
    clearable: {
      type: Boolean,
      default: true,
    },
    label: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "",
    },
    error_messages: {
      type: String,
      default: "",
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    icon: {
      type: String,
      default: "",
    },
    rules: {
      type: Array,
      default: () => [],
    },
    maxLength: {
      type: Number,
      default: 100, // Set default value for maxLength
    },
    type: {
      type: String,
      default: "text", // Default type is text
    },
    hideDetails: {
      type: [String, Boolean],
      default: false,
    },
    variant: {
      type: String,
      default: "outlined",
      validator: (value) => ["outlined", "underlined", "solo"].includes(value),
    },

    // Callback for outer icon click
    append_click: Function,
    rows: {
      type: Number,
      default: 3,
    },
  },
  data() {
    return {
      isRequired: false,
    };
  },
  created() {
    if (this.rules)
      this.rules?.forEach((e) => {
        if (typeof e === "function")
          if (e() == "هذا الحقل مطلوب" || e() === "This field is required")
            this.isRequired = true;
      });
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
/* ── Autofill Flash ──────────────────────────────────── */
.no-autofill-bg :deep(input:-webkit-autofill),
.no-autofill-bg :deep(input:-webkit-autofill:hover),
.no-autofill-bg :deep(input:-webkit-autofill:focus),
.no-autofill-bg :deep(input:-webkit-autofill:active) {
  -webkit-text-fill-color: inherit !important;
  transition: background-color 5000s ease-in-out 0s !important;
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
  box-shadow: 0 0 0 1000px transparent inset !important;
}

/* ── Label ───────────────────────────────────────────── */
.no-autofill-bg :deep(.v-label) {
  font-size: 0.875rem;
  font-weight: 500;
}

/* ── Textarea Text ───────────────────────────────────── */
.no-autofill-bg :deep(textarea) {
  resize: vertical;
  min-height: 88px;
  line-height: 1.65;
  font-size: 0.9rem;
  padding-top: 8px !important;
}

/* ── Placeholder ─────────────────────────────────────── */
.no-autofill-bg :deep(textarea::placeholder) {
  color: rgba(var(--v-theme-on-surface), 0.35);
  font-size: 0.875rem;
}

/* ── Icon: muted when not focused ───────────────────── */
.no-autofill-bg :deep(.v-field:not(.v-field--focused) .v-icon) {
  opacity: 0.45;
  transition: opacity 0.2s ease;
}

.no-autofill-bg :deep(.v-field--focused .v-icon) {
  opacity: 1;
}

/* ── Clearable Button ────────────────────────────────── */
.no-autofill-bg :deep(.v-field__clearable .v-icon) {
  opacity: 0.4;
  transition: opacity 0.2s ease, color 0.2s ease;
}

.no-autofill-bg :deep(.v-field__clearable .v-icon:hover) {
  opacity: 1;
  color: rgb(var(--v-theme-error));
}

/* ── Premium Scrollbar ───────────────────────────────── */
.no-autofill-bg :deep(textarea)::-webkit-scrollbar {
  width: 5px;
}

.no-autofill-bg :deep(textarea)::-webkit-scrollbar-track {
  background: transparent;
}

.no-autofill-bg :deep(textarea)::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.15);
  border-radius: 10px;
}

.no-autofill-bg :deep(textarea)::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.3);
}

/* ── Error Message ───────────────────────────────────── */
.no-autofill-bg :deep(.v-messages__message) {
  font-size: 11px !important;
  line-height: 1.5;
  letter-spacing: 0.2px;
}

/* ── Disabled ────────────────────────────────────────── */
.no-autofill-bg :deep(.v-field--disabled) {
  opacity: 0.55;
}
</style>
