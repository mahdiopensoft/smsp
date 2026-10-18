<template>
  <!-- added by samer -->

  <v-col :cols="12" :lg="cols" :md="cols" class="py-2" v-if="!state.print">
    <v-text-field
      v-model="value"
      :label="label + (isRequired ? '   *' : '')"
      density="compact"
      :counter="counter"
      :placeholder="placeholder"
      :rules="rules"
      :type="type === 'password' ? (showPassword ? 'text' : 'password') : type"
      :maxLength="maxLength"
      :readonly="readonly"
      :disabled="disabled"
      :rounded="rounded ? 'xl' : 's'"
      :variant="variant"
      class="no-autofill-bg my-0"
      aria-autocomplete="off"
      :autofocus="autofocus"
      :autocomplete="autocomplete"
      :width="width"
      @append-outer-icon-click="append_click"
      :hide-details="hideDetails"
      @keydown.tab="keyTabs"
      :ampm="false"
      :error-messages="error_messages"
      v-bind="$attrs"
    >
      <template #clear="{ props }">
        <VIcon
          v-if="clearable && !readonly"
          v-bind="props"
          icon="mdi-close-circle"
          tabindex="-1"
        />
      </template>

      <template v-slot:prepend-inner>
        <v-icon v-if="icon && !replace_icon">
          {{ "mdi-" + icon }}
        </v-icon>
        <v-label v-if="replace_icon">
          {{ replace_icon }}
        </v-label>
        <slot name="prepend" />
      </template>
      <template v-slot:append-inner>
        <v-icon v-if="appendIcon && !replace_append_icon">
          {{ "mdi-" + appendIcon }}
        </v-icon>
        <v-label v-if="replace_append_icon">
          {{ replace_append_icon }}
        </v-label>
        <v-icon
          v-if="type === 'password'"
          :icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
          @click="showPassword = !showPassword"
        />

        <slot name="append-inner" />
      </template>
    </v-text-field>
    <!-- @keyup="handleTab" -->
    <!-- <v-number-input
      v-else
      v-model="value"
      controlVariant="stacked"
      :label="label +( isRequired?'   *':'')"
      inset
      :variant="variant"
      density="compact"
      :rules="rules"
      :width="width"
      @keydown="handleTab"
      :hide-details="hideDetails"
      :disabled="disabled"
    /> -->
    <!-- :prepend-inner-icon="icon ? 'mdi-' + icon : ''"      -->
  </v-col>
  <v-col :cols="12" :lg="cols" :md="cols" class="py-1" v-else>
    {{ value }}
  </v-col>
</template>
<script setup>
import { state } from "@/../src/store/state";
</script>
<script>
export default {
  name: "CustomAutoComplete",
  props: {
    cols: {
      type: [String],
      default: "12",
    },
    append_click: Function,
    autofocus: Boolean,
    autocomplete: String,
    modelValue: {
      type: [Number, String],
      default: null,
    },
    rounded: {
      type: Boolean,
      default: false,
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
    appendIcon: String,

    replace_icon: String,
    replace_append_icon: String,

    rules: {
      type: Array,
      default: () => [],
    },
    counter: {
      type: Number,
    },
    maxLength: {
      type: Number,
    },
    type: {
      type: String,
      default: "text",
    },
    width: String,
    hideDetails: {
      type: [String, Boolean],
      default: false,
    },
    variant: {
      type: String,
      default: "outlined",
      validator: (value) => ["outlined", "underlined", "solo"].includes(value),
    },
    keyTab: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      isRequired: false,
      showPassword: false,
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
  methods: {
    keyTabs(event) {
      this.keyTab(event);
    },
    updateDate(newValue) {
      this.$emit("update:modelValue", newValue);
    },
    handleTab(event) {
      if (event.key === "Enter" && event.shiftKey) {
        event.preventDefault();
      }

      if (event.key === "Tab") {
        event.preventDefault();
        const focusableElements = "input,button,select,a[href]";
        const elements = Array.from(document.querySelectorAll(focusableElements)).filter(
          (el) => !el.disabled && el.tabIndex >= 0
        );
        const index = elements.indexOf(event.target);

        if (index > -1 && index < elements.length - 1) {
          const nextElement = event.shiftKey ? elements[index - 1] : elements[index + 1];
          nextElement.focus();
        }
      }
    },
  },
};
</script>
<style scoped>
/* ── Autofill Flash Prevention ───────────────────────── */
.no-autofill-bg :deep(input:-webkit-autofill),
.no-autofill-bg :deep(input:-webkit-autofill:hover),
.no-autofill-bg :deep(input:-webkit-autofill:focus),
.no-autofill-bg :deep(input:-webkit-autofill:active) {
  -webkit-text-fill-color: inherit !important;
  transition: background-color 5000s ease-in-out 0s !important;
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
  box-shadow: 0 0 0 1000px transparent inset !important;
}

/* ── Label Typography ────────────────────────────────── */
.no-autofill-bg :deep(.v-label) {
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.1px;
}

/* ── Placeholder ─────────────────────────────────────── */
.no-autofill-bg :deep(input::placeholder) {
  color: rgba(var(--v-theme-on-surface), 0.35);
  font-size: 0.875rem;
}

/* ── Input Text ──────────────────────────────────────── */
.no-autofill-bg :deep(.v-field__input) {
  font-size: 0.9rem;
  line-height: 1.5;
}

/* ── Smooth Focus Transition ─────────────────────────── */
.no-autofill-bg :deep(.v-field__outline) {
  transition: color 0.2s ease;
}

/* ── Icons: slightly muted when not focused ──────────── */
.no-autofill-bg :deep(.v-field:not(.v-field--focused) .v-icon) {
  opacity: 0.5;
  transition: opacity 0.2s ease;
}

.no-autofill-bg :deep(.v-field--focused .v-icon) {
  opacity: 1;
}

/* ── Error Message ───────────────────────────────────── */
.no-autofill-bg :deep(.v-messages__message) {
  font-size: 11px !important;
  line-height: 1.5;
  letter-spacing: 0.2px;
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

/* ── Disabled State ──────────────────────────────────── */
.no-autofill-bg :deep(.v-field--disabled) {
  opacity: 0.55;
}
</style>
