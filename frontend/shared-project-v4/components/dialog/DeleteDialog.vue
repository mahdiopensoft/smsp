<template>
  <v-dialog
    v-model="value"
    max-width="500"
    :dir="$i18n.locale == 'ar' ? 'rtl' : 'ltr'"
    transition="dialog-transition"
  >
    <v-card class="message-card border-thin error overflow-hidden bg-surface" elevation="1">
      <!-- Header Section (Alert Style) -->
      <div 
        class="header-section d-flex align-start px-6 pt-6 pb-4 position-relative"
        style="background-color: rgba(var(--v-theme-error), 0.08)"
      >
        <v-avatar
          color="error"
          variant="tonal"
          size="46"
          class="me-4 flex-shrink-0 rounded-lg"
        >
          <v-icon size="26">mdi-alert-circle-outline</v-icon>
        </v-avatar>
        
        <div class="d-flex flex-column flex-grow-1 pt-1">
          <v-card-title class="pa-0 text-h6 font-weight-bold line-height-1-2">
            {{ title ? title : $t("delete-confirm") }}
          </v-card-title>
        </div>
      </div>

      <v-card-text class="px-6 py-6 text-body-1" style="color: rgba(var(--v-theme-on-surface), 0.7)">
        <div class="mb-2">
          {{ message ? message : $t("confirm_delete") }}
        </div>
        <slot name="body"></slot>
      </v-card-text>

      <v-divider class="opacity-05" />

      <v-card-actions class="px-6 py-4 justify-end gap-3">
        <!-- Cancel Button (Standard Neutral Style) -->
        <custom-btn 
          type="cancel" 
          :click="cancelMethod" 
          color="grey-darken-1" 
          variant="text"
          class="font-weight-bold"
        />

        <!-- Delete Button (High Emphasis / Danger) -->
        <custom-btn
          :type="type_btn"
          :click="confirmDelete"
          color="error"
          variant="flat"
          class="px-8 font-weight-bold rounded-lg"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  props: {
    title: String,
    modelValue: {
      type: Boolean,
      default: false,
    },
    type_btn: {
      type: String,
      default: "del",
    },

    message: String,
    cancel: Function,
  },

  methods: {
    async confirmDelete() {
      await this.$emit("confirm-delete");

      this.value = false;
    },
  cancelMethod() {
    if(this.cancel)
   this.cancel();
    this.value = false;
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
.message-card {
  border-radius: 8px !important;
}

.header-section {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.05);
}

.line-height-1-2 {
  line-height: 1.2 !important;
}

.opacity-05 {
  opacity: 0.05;
}

.gap-3 {
  gap: 12px;
}

/* Animations */
.dialog-transition-enter-active,
.dialog-transition-leave-active {
  transition: transform 0.3s ease-out, opacity 0.3s;
}

.dialog-transition-enter-from,
.dialog-transition-leave-to {
  transform: scale(0.9) translateY(20px);
  opacity: 0;
}
</style>
