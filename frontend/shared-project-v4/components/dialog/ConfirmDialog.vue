<template>
  <v-dialog v-model="value" max-width="420" persistent transition="scale-transition">
    <template v-slot:activator="{ props: activatorProps }">
      <slot name="activator" :props="activatorProps" />
    </template>
    <template v-slot:default="{ isActive }">
      <v-card class="clean-confirm-card pa-8">
        <!-- Icon Section -->
        <div class="d-flex justify-center mb-6">
          <v-avatar
            :color="displayColor"
            variant="tonal"
            size="64"
            class="rounded-lg"
          >
            <v-icon size="32">
              {{ "mdi-" + displayIcon }}
            </v-icon>
          </v-avatar>
        </div>

        <!-- Content Section -->
        <div class="text-center mb-8">
          <h3 class="clean-title mb-2">
            {{ displayTitle }}
          </h3>

          <div class="clean-message-container">
            <template v-if="typeof displayMessage === 'string'">
              <p class="clean-text-body">{{ displayMessage }}</p>
            </template>

            <!-- Structured Data Display -->
            <template
              v-else-if="
                typeof displayMessage === 'object' &&
                !Array.isArray(displayMessage)
              "
            >
              <div class="clean-info-box mt-4">
                <div
                  v-for="(val, key) in displayMessage"
                  :key="key"
                  class="clean-info-row"
                >
                  <span class="info-key">{{ key }}</span>
                  <span class="info-value">{{ val }}</span>
                </div>
              </div>
            </template>

            <!-- List Display -->
            <template v-else-if="Array.isArray(displayMessage)">
              <div class="clean-info-box mt-4">
                <div
                  v-for="item in displayMessage"
                  :key="item"
                  class="clean-list-item"
                >
                  <v-icon size="10" class="me-2" color="disabled"
                    >mdi-circle</v-icon
                  >
                  <span>{{ item }}</span>
                </div>
              </div>
            </template>
          </div>

          <slot name="body" />
        </div>

        <!-- Actions Section -->
        <div class="d-flex justify-center flex-row-reverse" style="gap: 12px">
          <v-btn
            min-width="120"
            height="44"
            elevation="0"
            variant="flat"
            :color="displayColor"
            class="clean-btn clean-btn--confirm"
            :loading="loadingBtn"
            @click="
              () => {
                confirm();
                confrimFun();
              }
            "
          >
            {{ text_right ? text_right : $t("yes") }}
          </v-btn>

          <v-btn
            min-width="120"
            height="44"
            variant="tonal"
            color="grey-darken-1"
            class="clean-btn clean-btn--cancel"
            @click="cancel"
          >
            {{ text_left ? text_left : $t("no") }}
          </v-btn>
        </div>
      </v-card>
    </template>
  </v-dialog>
</template>
<script>
export default {
  props: {
    modelValue: {
      type: Boolean,
      default: undefined,
    },
    title: { type: String, default: "" },
    message: { type: [String, Array, Object], default: "" },
    icon: { type: String, default: "" },
    type: String,
    color: { type: String, default: "" },
    text_right: String,
    text_left: String,
    loading: { type: Boolean, default: false },
    confirmBtn: { type: Function, default: () => {} },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      localValue: false,

      loadingBtn: false,
    };
  },

  methods: {
    async confrimFun() {
      try {
        const isAsync = this.confirmBtn.constructor.name === "AsyncFunction";
        this.loadingBtn = true;
        isAsync ? await this.confirmBtn() : this.confirmBtn();

        this.loadingBtn = false;
        this.value = false;
      } catch {
        this.value = false;
        this.loadingBtn = false;
      }
    },
    confirm() {
      this.$emit("confirm");
    },
    cancel() {
      this.$emit("cancel");

      this.value = false;
    },
  },
  computed: {
    value: {
      get() {
        return this.modelValue !== undefined
          ? this.modelValue
          : this.localValue;
      },
      set(value) {
        if (this.modelValue !== undefined) {
          this.$emit("update:modelValue", value);
        } else {
          this.localValue = value;
        }
      },
    },
    // Centralized configuration based on type
    config() {
      const isAr = this.$i18n.locale === "ar";
      switch (this.type) {
        case "warning":
          return {
            icon: "alert-outline",
            color: "warning",
            title: this.$t("warning") || (isAr ? "تحذير" : "Warning"),
            message:
              this.$t("default_warning_message") ||
              (isAr
                ? "هل أنت متأكد من القيام بهذه العملية؟"
                : "Are you sure you want to proceed?"),
          };
        case "info":
          return {
            icon: "information-outline",
            color: "info",
            title: this.$t("info") || (isAr ? "تنبيه" : "Information"),
            message:
              this.$t("default_info_message") ||
              (isAr
                ? "يرجى مراجعة البيانات."
                : "Please review the information."),
          };
        case "error":
          return {
            icon: "close-circle-outline",
            color: "error",
            title: this.$t("error") || (isAr ? "خطأ" : "Error"),
            message:
              this.$t("default_error_message") ||
              (isAr ? "حدث خطأ غير متوقع." : "An unexpected error occurred."),
          };
        case "success":
          return {
            icon: "check-circle-outline",
            color: "success",
            title: this.$t("success") || (isAr ? "تم بنجاح" : "Success"),
            message:
              this.$t("default_success_message") ||
              (isAr
                ? "تمت العملية بنجاح."
                : "Operation completed successfully."),
          };
        case "delete":
          return {
            icon: "trash-can-outline",
            color: "error",
            title: this.$t("delete") || (isAr ? "حذف" : "Delete"),
            message:
              this.$t("default_delete_message") ||
              (isAr
                ? "هل أنت متأكد من حذف هذا العنصر؟"
                : "Are you sure you want to delete this item?"),
          };
        default:
          return {
            icon: "help-circle-outline",
            color: "primary",
            title: isAr ? "تأكيد" : "Confirm",
            message: isAr ? "هل تريد الاستمرار؟" : "Do you want to continue?",
          };
      }
    },
    // Priority logic: Props > Config
    displayTitle() {
      return this.title || this.config.title;
    },
    displayMessage() {
      return this.message || this.config.message;
    },
    displayIcon() {
      return this.icon || this.config.icon;
    },
    displayColor() {
      return this.color || this.config.color;
    },
  },
};
</script>

<style scoped>
.clean-confirm-card {
  border-radius: 12px !important;
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1) !important;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.05) !important;
}

/* --- Typography --- */
.clean-title {
  font-size: 1.25rem !important;
  font-weight: 700 !important;
  color: rgb(var(--v-theme-on-surface)) !important;
  line-height: 1.4;
}

.clean-text-body {
  font-size: 0.95rem !important;
  color: rgba(var(--v-theme-on-surface), 0.65) !important;
  line-height: 1.5;
}

/* --- Info Containers --- */
.clean-info-box {
  background: rgba(var(--v-theme-on-surface), 0.02);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  border-radius: 8px;
  padding: 16px;
  text-align: right; /* RTL Standard */
}

[dir="ltr"] .clean-info-box {
  text-align: left;
}

.clean-info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.85rem;
}

.clean-info-row:last-child {
  margin-bottom: 0;
}

.info-key {
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.5);
}

.info-value {
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface));
}

.clean-list-item {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  margin-bottom: 6px;
  color: rgb(var(--v-theme-on-surface));
}

/* --- Buttons --- */
.clean-btn {
  font-weight: 700 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  border-radius: 8px !important;
  font-size: 0.9rem !important;
  transition: opacity 0.2s ease;
}

.clean-btn:hover {
  opacity: 0.9;
}

.clean-btn--cancel {
  color: rgba(var(--v-theme-on-surface), 0.7) !important;
}
</style>
