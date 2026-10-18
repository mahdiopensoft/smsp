<template>
  <!-- added by samer -->

  <!-- Icon-only button — using shared component design with specific dimensions -->
  <VBtn
    v-if="isIcon && data.show"
    :disabled="disabled"
    @click="onClick"
    :color="data.color"
    :variant="data.variant || variant"
    size="small"
    density="comfortable"
    :elevation="elevation"
    class="print custom-icon-btn rounded-lg"
    style="height: 32px; min-width: 32px; width: 32px"
    :loading="loading || localLoading"
  >
    <template v-slot:default>
      <VIcon :color="iconColor" size="18">{{ data.icon }}</VIcon>

      <VTooltip activator="parent" location="top" open-delay="500">{{
        data.label
      }}</VTooltip>
    </template>
  </VBtn>
  <VBtn
    v-else-if="data.show"
    :type="is_submit ? 'submit' : 'button'"
    density="comfortable"
    :color="data.color"
    :loading="loading || localLoading"
    @click.prevent="onClick"
    :variant="data.variant || variant"
    class="print custom-text-btn"
    :class="{ 'ms-2': type == 'cancel' }"
    :disabled="disabled"
    :elevation="elevation"
    :width="width"
    min-width="100"
  >
    <template v-slot:default>
      <span class="custom-btn-label" :style="'color:' + text_color || data.text_color"
        >{{ data.label }}
      </span>
    </template>
    <template v-slot:append>
      <VIcon v-if="data.icon" :icon="data.icon" class="custom-btn-icon"></VIcon>
    </template>
  </VBtn>
</template>
<script>
import { state } from "@/../src/store/state";
import { useHeaderFooterStore } from "../../src/stores/headerFooterStore";

export default {
  data() {
    return {
      localLoading: false,
      route_name: this.$route.name,
    };
  },
  props: {
    elevation: String,
    text: String,
    click: {
      type: Function,

      default() {
        return () => {};
      },
    },
    text_color: String,

    isIcon: {
      type: Boolean,
      default() {
        return false;
      },
    },
    is_submit: {
      type: Boolean,
      default() {
        return false;
      },
    },
    disabled: false,
    type: String,
    variant: {
      type: String,
      default: "outlined",
      validator: (value) =>
        ["outlined", "tonal", "text", "plain", "elevated", "flat"].includes(value),
    },
    width: {
      type: String,
      default() {
        return "auto";
      },
    },

    icon: {
      type: String,
    },
    label: {
      type: String,
      default() {
        return "";
      },
    },
    color: {
      type: String,
      default() {
        return "";
      },
    },
    iconColor: {
      type: String,
      default() {
        return "";
      },
    },
    print: { type: String, default: "" },
    perm: Boolean,
    print_id: Object,
    loading: Boolean,
  },
  methods: {
    async onClick() {
      if (this.localLoading) return;
      this.localLoading = true;
      try {
        if (this.type != "print") {
          try {
            // const isAsync = this.click.constructor.name === "AsyncFunction";

            // // if(isAsync)

            // isAsync ? await this.click() : this.click();
            await Promise.resolve(this.click());
          } finally {
            this.localLoading = false;
          }
        } else {
          if (this.click) {
            await Promise.resolve(this.click());
          }

          await this.printReport(this.print);
        }
      } catch {
        this.localLoading = false;
      } finally {
        this.localLoading = false;
      }
    },

    async printReport(print) {
      this.localLoading = true;
      let screen_id = {};
      if (this.print_id) screen_id.fk_print_report_setting = this.print_id;
      else {
        screen_id.fk_screen = this.$route?.meta?.fk_screen;
      }

      const headerFooterStore = useHeaderFooterStore();

      await headerFooterStore.changeHeaderFooter(screen_id);
      if (!headerFooterStore.headerFooterData) {
        this.$snack("errorData", {
          message: "يرجى ربط الشاشة مع header , footer",
        });
        return;
      }

      state.print = true;

      // إضافة تأخير بسيط جداً (Buffer) لضمان استقرار المتصفح
      // await new Promise((resolve) => setTimeout(resolve, 200));
      await this.$nextTick();
      const elementToPrint = document.querySelector(`#${print}`).innerHTML;

      if (!elementToPrint) {
        console.error("العنصر موجود ولكن لا يحتوي على محتوى (innerHTML)");
        return;
      }

      // ننتظر قليلاً لضمان ظهور عنصر printView في الـ DOM
      // await new Promise((resolve) => setTimeout(resolve, 300));
      state.print = true;
      await this.$nextTick();

      const printView = document.getElementById("printView");
      if (!printView) {
        console.error("عنصر printView غير موجود في الـ DOM");
        state.print = false;
        return;
      }

      // نسخ المحتوى إلى حاوية الطباعة
      printView.innerHTML = elementToPrint;
      await this.$nextTick();

      try {
        await document.fonts.ready;
        // --- الجزء الجديد: انتظار تحميل الصور ---
        const images = Array.from(printView.querySelectorAll("img"));
        const imagePromises = images?.map((img) => {
          if (img?.complete && img?.naturalWidth !== 0) {
            return img?.decode ? img?.decode()?.catch(() => {}) : Promise?.resolve();
          }
          return new Promise((resolve) => {
            const handleDone = async () => {
              if (img?.decode) {
                try {
                  await img?.decode();
                } catch (error) {}
              }
              resolve();
            };
            img.onload = handleDone;
            img.onerror = handleDone;
          });
        });
        // const images = printView.querySelectorAll("img");
        // const imagePromises = Array.from(images).map((img) => {
        //   if (img.complete) {
        //     return Promise.resolve(); // الصورة محملة مسبقاً
        //   }
        //   return new Promise((resolve) => {
        //     img.onload = resolve; // نجاح التحميل
        //     img.onerror = resolve; // حتى لو فشل التحميل، نكمل لكي لا تتعطل الطباعة
        //   });
        // });

        // انتظار جميع الصور حتى تنتهي من التحميل

        await Promise.all(imagePromises);

        // إضافة تأخير بسيط جداً (Buffer) لضمان استقرار المتصفح
        // await new Promise((resolve) => setTimeout(resolve, 200));
        await this.$nextTick();

        await new Promise((resolve) => requestAnimationFrame(resolve));
        await new Promise((resolve) => setTimeout(resolve, 300));

        // تشغيل أمر الطباعة
        window.print();
        this.$emit("print");
      } catch (err) {
        console.error("خطأ أثناء انتظار الصور:", err);
      } finally {
        // التنظيف وإعادة الحالة
        printView.innerHTML = "";

        state.print = false;
        this.localLoading = false;

        headerFooterStore.headerFooterData = {};
      }
    },
  },
  computed: {
    data() {
      switch (this.type) {
        case "create":
          return {
            icon: this.icon || "mdi-plus",
            label: this.label || (this.$i18n.locale == "ar" ? "إنشاء" : "Create"),
            color: this.color || "primary",
            show: this.perm || true,
          };
          break;
        case "add":
          return {
            icon: this.icon || "mdi-plus",
            label: this.label || (this.$i18n.locale == "ar" ? "إضافة" : "Add"),
            color: this.color || "primary",
            show: this.perm || true,
            variant: "flat",
          };
          break;
        case "save":
          return {
            icon: this.icon || "mdi-content-save",
            label: this.label || (this.$i18n.locale == "ar" ? "حفظ" : "Save"),
            color: this.color || "primary",
            show: this.perm || true,
          };
          break;
        case "ok":
          return {
            icon: this.icon || "mdi-check-bold",
            label: this.label || (this.$i18n.locale == "ar" ? "حسنناٌ" : "Ok"),
            color: this.color || "primary",
            show: true,
          };
          break;
        case "update":
          return {
            icon: this.icon || "mdi-pencil-outline",
            label: this.label || (this.$i18n.locale == "ar" ? "تعديل" : "Update"),
            color: this.color || "success",

            show: this.perm || true,
          };
          break;
        case "export":
          return {
            icon: this.icon || "mdi-export-variant",
            label: this.label || (this.$i18n.locale == "ar" ? "تصدير" : "Export"),
            color: this.color || "grey",
            show: this.perm || true,
          };
          break;
        case "additional_exports":
          return {
            icon: this.icon || "mdi-export-variant",
            label: this.label || this.$t("additional_exports"),
            color: this.color || "grey",
            show: true,
          };
          break;
        case "del":
          return {
            icon: this.icon || "mdi-trash-can-outline",
            label: this.label || (this.$i18n.locale == "ar" ? "حذف" : "Delete"),
            color: this.color || "red",
            show: this.perm || true,
          };
          break;
        case "done":
          return {
            icon: this.icon || "mdi-check",
            label: this.label || (this.$i18n.locale == "ar" ? "" : "Done"),
            color: "primary",
            show: true,
          };
          break;
        case "reset":
          return {
            icon: this.icon || "mdi-broom",
            label: this.label || (this.$i18n.locale == "ar" ? "إعادة" : "Reset"),
            color: this.color || "error",
            show: true,
          };
          break;
        case "show":
          return {
            icon: this.icon || "mdi-eye-outline",
            label: this.label || (this.$i18n.locale == "ar" ? "عرض" : "Show"),
            color: this.color || "primary",
            show: true,
          };
          break;
        case "imports":
          return {
            icon: this.icon || "mdi-database-import-outline",
            label:
              this.label ||
              (this.$i18n.locale == "ar" ? "إستيراد من اكسل" : "Import from Excel"),
            color: this.color || "grey",
            show: this.perm || true,
          };
          break;
        case "print":
          return {
            icon: this.icon || "mdi-printer",
            label: this.label || (this.$i18n.locale == "ar" ? "طباعة" : "Print"),
            color: this.color || "secoundry",
            show: this.perm || true,
          };
          break;
        case "filter":
          return {
            icon: this.icon || "mdi-filter-variant",
            label: this.label || (this.$i18n.locale == "ar" ? "فلتر" : "Filter"),
            color: this.color || "primary",
            show: true,
          };
          break;
        case "cancel_filter":
          return {
            icon: this.icon || "mdi-filter-off",
            label:
              this.label || this.$i18n.locale == "ar"
                ? "الغاء الفلترة"
                : "Cancel filtering",
            color: this.color || "primary",
            show: true,
          };
          break;
        case "next":
          return {
            icon: this.$vuetify.display.mobile ? "mdi-chevron-down" : "mdi-chevron-left",
            label: this.label || (this.$i18n.locale == "ar" ? "التالي" : "next"),
            color: this.color || "primary",
            show: true,
          };
          break;
        case "prev":
          return {
            label: this.label || (this.$i18n.locale == "ar" ? "السابق" : "previo"),
            icon: this.$vuetify.display.mobile ? "mdi-chevron-up" : "mdi-chevron-right",
            color: this.color || "primary",
            show: true,
          };
          break;
        case "refresh":
          return {
            icon: "mdi-refresh",
            label: this.label || (this.$i18n.locale == "ar" ? "تحديث" : "Refresh"),
            color: this.color || "#6C757D",
            show: true,
          };
          break;
        case "cancel":
          return {
            icon: "mdi-cancel",
            label: this.label || (this.$i18n.locale == "ar" ? "إلغاء" : "Cancel"),
            show: true,
          };
          break;
        case "restore":
          return {
            icon: "mdi-backup-restore",
            label: this.label
              ? this.label
              : this.$i18n.locale == "ar"
              ? "السجلات المحذوفة"
              : "Deleted records",
            color: this.color || "#28A745",
            show: this.perm || true,
          };
        case "log":
          return {
            icon: "mdi-file-document-outline",
            label: this.label
              ? this.label
              : this.$i18n.locale == "ar"
              ? "سجل العمليات للشاشة"
              : "Log",
            color: this.color || "#17A2B8",
            show: this.perm || true,
          };

        default:
          return {
            icon: this.icon ? "mdi-" + this.icon : "",
            label: this.label,
            color: this.color,
            show: this.perm || true,
          };
      }
    },
  },
};
</script>

<style scoped>
/* 
  CustomBtn Component Specific Styles
  Relying on global components/buttons.css for base design
*/

.custom-btn-label {
  display: flex;
  align-items: center;
}

/* Specific icon size inside the custom label structure */
.custom-btn-icon {
  font-size: 1.125rem !important;
}

/* Vertical alignment and interaction for both button types */
.v-btn.custom-text-btn,
.v-btn.custom-icon-btn {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.v-btn.custom-text-btn:hover,
.v-btn.custom-icon-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px -2px rgba(var(--v-shadow-key-umbra-color), 0.12) !important;
}

/* Ensure icon is perfectly centered */
.custom-icon-btn {
  padding: 0 !important;
}
</style>
