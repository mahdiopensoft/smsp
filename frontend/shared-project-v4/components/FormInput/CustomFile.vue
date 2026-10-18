<template>
  <VCol cols="12" :lg="cols" :md="cols" class="py-2">
    <VFileInput
      v-model="value"
      :label="label"
      prepend-icon=""
      prepend-inner-icon="mdi-paperclip"
      :variant="variant"
      :hide-details="hideDetails"
      :disabled="disabled"
      :readonly="readonly"
      density="compact"
      :width="width"
      class="my-0"
      :rules="required ? [...required_file, ...rules] : rules"
      show-size
      :multiple="multiple"
      counter
      color="primary"
      :accept="accept"
    >
      <template v-slot:selection="{ fileNames }">
        <template v-for="(fileName, index) in fileNames" :key="fileName">
          <v-chip
            v-if="index < 2"
            class="me-2"
            color="primary"
            size="small"
            label
            variant="tonal"
          >
            {{ fileName }}
          </v-chip>
          <span v-else-if="index === 2" class="text-overline text-grey-darken-3 mx-2">
            + {{ value.length - 2 }} ملف
          </span>
        </template>
      </template>
    </VFileInput>

    <div class="file-link-container" v-if="typeof value == 'string' && value">
      <a :href="base_url + value" target="_blank" class="uploaded-file-link">
        <v-icon
          icon="mdi-file-download-outline"
          size="18"
          class="file-link-icon flex-shrink-0 me-1"
        />
        <span class="file-link-text">{{ getFileName(value) }}</span>
        <v-tooltip activator="parent" location="top" open-delay="500">
          {{ value }}
        </v-tooltip>
      </a>
    </div>
  </VCol>
</template>
<script setup>
import { VFileInput, VCol } from "vuetify/components";
</script>
<script>
export default {
  props: {
    modelValue: {
      type: [Object, String, Array, File],
      default: null,
    },
    accept: {
      type: String,
    },

    label: {
      type: String,
      default: "",
    },
    cols: {
      type: String,
      default: "12",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    rules: {
      type: Array,
      default: [],
    },
    variant: {
      type: String,
      default: "outlined",
      validator: (value) => ["outlined", "underlined", "solo"].includes(value),
    },
    required: {
      type: Boolean,
      default: false,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    width: String,
    hideDetails: {
      type: [String, Boolean],
      default() {
        return false;
      },
    },
  },
  data() {
    return {
      required_file: [
        (value) =>
          (Array.isArray(value) ? !!value[0] : !!value) || this.$t("required_field"),
      ],
      base_url: this.setting.url_img,
    };
  },
  methods: {
    getFileName(path) {
      if (!path) return "";
      const parts = path.split("/");
      return parts[parts.length - 1];
    },
    handleTab(event) {
      if (event.key == "Enter" && event.shiftKey) {
        event.preventDefault();
      }
      if (
        (event.key == "Tab" && !event.shiftKey) ||
        (event.key == "Tab" && event.shiftKey)
      ) {
        event.preventDefault();
        const focusableElements = "input,button,select,texttarea,a[href]";
        const elements = Array.from(document.querySelectorAll(focusableElements)).filter(
          (el) => !el.disabled && el.tabIndex >= 0
        );
        const index = elements.indexOf(event.target);
        if (index > -1 && index < elements.length - 1) {
          if (event.key == "Tab" && !event.shiftKey) elements[index + 1].focus();
          if (event.key == "Tab" && event.shiftKey) elements[index - 1].focus();
        }
      }
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
/* ── Field Input Area ────────────────────────────────── */
:deep(.v-field__input) {
  flex-wrap: wrap;
  gap: 4px;
  padding-top: 6px !important;
  padding-bottom: 6px !important;
  min-height: 40px;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* ── Label Typography ────────────────────────────────── */
:deep(.v-label) {
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.1px;
}

/* ── File Name Chips ─────────────────────────────────── */
:deep(.v-chip) {
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.2px;
  height: 26px !important;
}

/* ── Overflow Count Indicator ────────────────────────── */
:deep(.text-overline) {
  font-size: 0.75rem !important;
  letter-spacing: 0.5px;
  opacity: 0.7;
}

/* ── Existing File Link ───────────────────────────────── */
.file-link-container {
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  display: block;
  margin-top: 6px;
}

.uploaded-file-link {
  font-size: 0.82rem;
  color: rgb(var(--v-theme-primary));
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  max-width: 100%;
  padding: 6px 12px;
  border-radius: 8px;
  background-color: rgba(var(--v-theme-primary), 0.06);
  transition: background-color 0.2s ease, transform 0.2s ease;
  border: 1px dashed rgba(var(--v-theme-primary), 0.2);
}

.uploaded-file-link:hover {
  background-color: rgba(var(--v-theme-primary), 0.12);
  text-decoration: none;
  transform: translateY(-1px);
}

.file-link-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  word-break: break-all;
  direction: ltr !important;
  text-align: left;
}

.file-link-icon {
  color: rgb(var(--v-theme-primary));
}

/* ── Counter ─────────────────────────────────────────── */
:deep(.v-counter) {
  font-size: 11px;
  opacity: 0.5;
  letter-spacing: 0.2px;
}

/* ── Disabled ────────────────────────────────────────── */
:deep(.v-field--disabled) {
  opacity: 0.55;
}

/* ── Paperclip Icon ──────────────────────────────────── */
:deep(.v-field:not(.v-field--focused) .v-icon) {
  opacity: 0.45;
  transition: opacity 0.2s ease;
}

:deep(.v-field--focused .v-icon) {
  opacity: 1;
}
</style>
