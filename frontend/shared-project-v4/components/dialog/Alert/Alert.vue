<template>
  <VDialog
    v-if="model"
    v-model="model"
    max-width="500"
    transition="dialog-transition"
    class="universal-dialog"
    focus
    scrollable
    :eager="false"
    :theme="state?.theme?.name_en"
  >
    <VCard :class="['message-card', 'border-thin', currentTheme.color]" elevation="4">
      <!-- Header Section -->
      <div
        class="header-section d-flex align-start px-6 pt-6 pb-4 position-relative"
        :style="{ backgroundColor: `rgba(var(--v-theme-${currentTheme.color}), 0.08)` }"
      >
        <VAvatar
          :color="currentTheme.color"
          variant="tonal"
          size="46"
          class="me-4 flex-shrink-0 rounded-lg"
        >
          <VIcon size="26">{{ currentTheme.icon }}</VIcon>
        </VAvatar>

        <div class="d-flex flex-column flex-grow-1 pt-1">
          <h3
            class="text-h6 font-weight-bold mb-1"
            style="color: rgba(var(--v-theme-on-surface), 0.9); line-height: 1.2"
          >
            {{ title || currentTheme.defaultTitle }}
          </h3>
          <span
            class="text-caption font-weight-medium text-disabled text-uppercase letter-spacing-1"
          >
            Server Response
          </span>
        </div>

        <VBtn
          icon="mdi-close"
          variant="text"
          size="small"
          density="comfortable"
          @click="close"
          color="grey-darken-1"
          class="ms-2 mt-n1 me-n2 flex-shrink-0"
        >
          <VIcon>mdi-close</VIcon>
          <VTooltip activator="parent" location="top">إغلاق</VTooltip>
        </VBtn>
      </div>

      <!-- Content Section -->
      <VCardText
        class="px-6 py-4 content-area text-body-1"
        style="max-height: 60vh; overflow-y: auto"
      >
        <!-- <VSheet v-if="details.component">
          <component :is="details.component" v-bind="details.props" />
        </VSheet> -->

        <componen-by-value :value="rowData" />
      </VCardText>

      <!-- Actions Section -->
      <VCardActions class="px-6 pb-6 pt-2 bg-surface">
        <VBtn
          v-if="rowData"
          prepend-icon="mdi-content-copy"
          variant="text"
          @click="copyToClipboard"
          color="grey-darken-1"
          class="px-4 font-weight-medium rounded-lg"
        >
          نسخ التفاصيل
        </VBtn>
        <VSpacer />
        <VBtn
          variant="flat"
          :color="currentTheme.color"
          class="px-6 font-weight-bold letter-spacing-1 rounded-lg"
          @click="close"
        >
          حسناً
        </VBtn>
      </VCardActions>
    </VCard>

    <VSnackbar
      v-model="copied"
      timeout="2000"
      color="surface"
      rounded="lg"
      class="border-thin"
      location="top"
    >
      تم نسخ التفاصيل الى الحافظة !
    </VSnackbar>
  </VDialog>
</template>
<script setup>
import ComponenByValue from "./ComponenByValue.vue";
import { state } from "@/store/state";
import { ref, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
const { locale } = useI18n();

const props = defineProps({
  details: {
    type: [String, Array, Object],
    default: {
      type: "info",
    },
  },
  title: String,
});
const model = defineModel();

const emit = defineEmits(["update:modelValue"]);

const copied = ref(false);
const panels = ref([1]);

const themes = {
  success: {
    color: "success",
    icon: "mdi-check-decagram",
    bg: "#E8F5E9",
    defaultTitle: "تمت العملية بنجاح",
  },

  warning: {
    color: "warning",
    icon: "mdi-alert",
    bg: "#FFF3E0",
    defaultTitle: "تنبيه هام",
  },
  info: {
    color: "info",
    icon: "mdi-information-outline",
    bg: "#E3F2FD",
    defaultTitle: "معلومات النظام",
  },

  success: {
    color: "success",
    icon: "mdi-check-circle",
    defaultTitle:
      locale.value == "ar"
        ? "✅ تمت العملية بنجاحتمت العملية بنجاح"
        : "The operation was completed successfully",
  },
  add: {
    color: "success",
    icon: "mdi-check-circle",

    defaultTitle:
      locale.value == "ar" ? "تم إضافة البيانات بنجاح" : "Data added successfully",
  },
  update: {
    color: "success",
    icon: "mdi-check-circle",

    defaultTitle:
      locale.value == "ar"
        ? "تم تعديل البيانات بنجاح"
        : "The data has been modified successfully",
  },
  errorData: {
    color: "error",
    icon: "mdi-cancel",

    defaultTitle: locale.value == "ar" ? "خطاء في البيانات" : "Error in data",
  },
  dublicateData: {
    color: "error",
    icon: "mdi-cancel",

    defaultTitle: locale.value == "ar" ? "البيانات مكررة" : "Data is duplicated",
  },
  empty: {
    color: "green",
    icon: "mdi-message-alert-outline",
    defaultTitle: locale.value == "ar" ? "لايوجد بيانات" : "No Data",
  },
  del: {
    color: "success",
    icon: "mdi-check-circle",

    defaultTitle:
      locale.value == "ar"
        ? "تم حذف البيانات بنجاح"
        : "The data has been deleted successfully",
  },

  notFound: {
    color: "error",
    icon: "mdi-cancel",

    defaultTitle: locale.value == "ar" ? "المسار غير موجود" : "path not exist",
  },
};

const currentTheme = computed(() => themes[props.details.type] || themes.info);
const rowData = computed(() => props.details.message);

const formatValue = (val) => {
  if (typeof val === "object") return JSON.stringify(val, null, 2);
  return val;
};
const close = () => {
  emit("update:modelValue", false);
};

const copyToClipboard = () => {
  const text = JSON.stringify(rowData.value, null, 2);
  navigator.clipboard.writeText(text);
  copied.value = true;
};
</script>
<style scoped>
.universal-dialog {
  /* Inherit global backdrop settings from Vuetify */
}

.message-card {
  border-radius: 8px !important;
  overflow: hidden;
}

.message-card.border-thin {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}

.letter-spacing-1 {
  letter-spacing: 0.5px !important;
}

.content-area {
  background-color: rgb(var(--v-theme-surface));
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.bg-surface {
  background-color: rgb(var(--v-theme-surface));
}

.list-item-custom {
  background: rgba(var(--v-theme-on-surface), 0.03);
  transition: all 0.3s ease;
}

.list-item-custom:hover {
  background: rgba(var(--v-theme-on-surface), 0.08);
  transform: translateX(-5px);
}

.json-text {
  font-family: "Fira Code", monospace;
  font-size: 0.85rem;
  white-space: pre-wrap;
  word-break: break-all;
}

.object-panel {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  margin-bottom: 8px !important;
  border-radius: 8px !important;
}

.object-panel::before {
  display: none;
}

.opacity-70 {
  opacity: 0.7;
}
</style>
