<template>
  <v-dialog
    v-model="value"
    :width="$vuetify.display.mobile ? '100%' : width"
    :height="$vuetify.display.mobile ? '100%' : height"
    :fullscreen="$vuetify.display.mobile"
    transition="dialog-transition"
    class="print"
  >
    <template v-slot:activator="{ props: activatorProps }">
      <slot name="activator" :props="activatorProps" />
    </template>
    <template v-slot:default="{ isActive }">
      <v-card
        class="premium-base-card overflow-hidden d-flex flex-column bg-surface border-thin"
        elevation="24"
        height="100%"
      >
        <!-- Premium Minimalist Header -->
        <div
          class="d-flex align-center justify-space-between px-8 py-5 flex-shrink-0 header-border"
        >
          <div class="d-flex align-center w-100">
            <v-card-title
              class="pa-0 text-h5 font-weight-bold d-flex"
              align-center
              style="
                color: rgb(var(--v-theme-on-surface));
                letter-spacing: -0.5px;
                line-height: 1.2;
              "
            >
              <div v-if="title" class="d-flex flex-column justify-center">
                <span>{{ title }}</span>
                <p v-if="subTitle" class="text-body-2 g-text-med">
                  {{ subTitle }}
                </p>
              </div>
              <slot name="title"></slot>
            </v-card-title>
            <custom-btn
              v-if="print"
              type="print"
              :print="print"
              isIcon
              variant="tonal"
              color="grey-darken-2"
              class="ms-7"
              @print="afterPrintAction"
            ></custom-btn>
          </div>
          <v-btn
            v-if="showClose"
            icon="mdi-close"
            variant="tonal"
            size="small"
            color="grey-darken-2"
            class="rounded-circle ms-4 flex-shrink-0"
            elevation="0"
            @click="$emit('update:modelValue', false), (isActive.value = false)"
          ></v-btn>
        </div>

        <!-- Body Content -->
        <v-card-text
          class="px-2 py-2 overflow-auto flex-grow-1 custom-scrollbar text-body-1"
          style="color: rgba(var(--v-theme-on-surface), 0.7)"
        >
          <slot></slot>
        </v-card-text>

        <!-- Actions Footer -->
        <v-card-actions
          v-if="$slots.actions"
          class="px-8 py-5 justify-end gap-4 flex-shrink-0 footer-zone"
        >
          <slot name="actions"></slot>
        </v-card-actions>
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
    showClose: {
      type: Boolean,
      default: true,
    },

    title: {
      type: String,
      default: "",
    },

    subTitle: {
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
    print: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      localValue: false,
    };
  },
  created() {},
  computed: {
    value: {
      get() {
        return this.modelValue !== undefined ? this.modelValue : this.localValue;
      },
      set(value) {
        if (this.modelValue !== undefined) {
          this.$emit("update:modelValue", value);
        } else {
          this.localValue = value;
        }
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
  methods: {
    afterPrintAction() {
      this.$emit("print");
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
