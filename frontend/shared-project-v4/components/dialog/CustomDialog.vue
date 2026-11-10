<template>
  <v-dialog
    v-model="value"
    :width="$vuetify.display.mobile ? '100%' : width"
    :height="$vuetify.display.mobile ? '100%' : height"
    :fullscreen="$vuetify.display.mobile"
    transition="dialog-transition"
    class="print"
  >
    <v-card class="premium-base-card overflow-hidden d-flex flex-column bg-surface border-thin" elevation="24" height="100%">
      
      <!-- Premium Minimalist Header -->
      <div class="d-flex align-center justify-space-between px-8 py-5 flex-shrink-0 header-border">
        <v-card-title class="pa-0 text-h5 font-weight-bold" style="color: rgb(var(--v-theme-on-surface)); letter-spacing: -0.5px; line-height: 1.2;">
          {{ title }}
        </v-card-title>
 
         <v-btn
           icon="mdi-close"
           variant="tonal"
           size="small"
          color="grey-darken-2"
           class="rounded-circle ms-4 flex-shrink-0"
           elevation="0"
           @click="$emit('update:modelValue', false)"
         ></v-btn>
       </div>
 
       <!-- Body Content -->
       <v-card-text class="px-8 py-6 overflow-auto flex-grow-1 custom-scrollbar text-body-1" style="color: rgba(var(--v-theme-on-surface), 0.7)">
        <slot></slot>
      </v-card-text>

      <!-- Actions Footer -->
      <v-card-actions v-if="$slots.actions" class="px-8 py-5 justify-end gap-4 flex-shrink-0 footer-zone">
        <slot name="actions"></slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },

    title: {
      type: String,
      default: "",
    },
    height: {
      type: String,
      default: "500",
    },
    width: {
      type: String,
      default: "700",
    },
  },
  created() {},
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    glassPrimary() {
      // لون الـ primary من الثيم
      const primary = this.$vuetify.theme.current.colors.primary || "#1976d2";
      // تحويل HEX → RGB
      const rgb = parseInt(primary.slice(1), 16);
      const r = (rgb >> 16) & 255;
      const g = (rgb >> 8) & 255;
      const b = rgb & 255;
      // نعيد اللون بصيغة rgba مع شفافية 0.2
     return `rgba(${r}, ${g}, ${b}, 0.9)`;
    },
  },
};
</script>
<style scoped>
.premium-base-card {
  border-radius: 12px !important;
}

.header-border {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.footer-zone {
  background-color: rgba(var(--v-theme-on-surface), 0.02);
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

.gap-4 {
  gap: 16px;
}

/* Premium Custom Scrollbar for Base Dialog */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.15);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.3);
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
