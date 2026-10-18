<template>
  <v-menu
    transition="slide-y-transition"
    location="bottom end"
    offset="8"
    :close-on-content-click="true"
    style="z-index: 3000 !important"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        variant="tonal"
        color="primary"
        size="small"
        class="ms-2 rounded-lg"
        style="height: 38px; min-width: 38px"
      >
        <VIcon size="20">mdi-cog-sync-outline</VIcon>
        <VTooltip activator="parent" location="top">
          {{ $i18n.locale == "ar" ? "العمليات العامة" : "General Operations" }}
        </VTooltip>
      </v-btn>
    </template>

    <v-card
      elevation="24"
      rounded="lg"
      class="premium-menu-card border-thin overflow-hidden"
      style="min-width: 260px"
    >
      <!-- رأس القائمة -->
      <div
        class="pa-3 border-b d-flex align-center"
        style="background-color: rgba(var(--v-theme-primary), 0.08)"
      >
        <v-icon color="primary" class="me-2" size="20">mdi-cog-sync-outline</v-icon>
        <div
          class="text-caption font-weight-bold"
          style="color: rgb(var(--v-theme-on-surface))"
        >
          {{ $i18n.locale == "ar" ? "العمليات العامة" : "General Operations" }}
        </div>
      </div>

      <v-card-text class="pa-1">
        <v-list density="compact" class="bg-transparent pa-0">
          <!-- 1. مجموعة: العناصر المحددة (تظهر فقط عند التحديد) -->
          <template v-if="selectedItems.length > 0">
            <v-list-subheader class="modern-subheader px-2 mt-1 mb-1">
              {{
                $i18n.locale == "ar" ? "العمليات على المحدد" : "Selected Items Operations"
              }}
              ({{ selectedItems.length }})
            </v-list-subheader>

            <!-- طباعة المحدد -->
            <v-list-item
              v-if="hasPrint"
              @click="$emit('typePrint', 'selected')"
              class="premium-list-item"
            >
              <template #prepend>
                <v-icon color="secondary" size="18" class="me-2"
                  >mdi-printer-pos-check-outline</v-icon
                >
              </template>
              <v-list-item-title class="text-caption font-weight-medium">
                {{ $i18n.locale == "ar" ? "طباعة المحدد" : "Print Selected" }}
              </v-list-item-title>
            </v-list-item>

            <!-- طباعة غير المحدد -->
            <v-list-item
              v-if="hasPrint && items.length - selectedItems.length > 0"
              @click="$emit('typePrint', 'unselected')"
              class="premium-list-item"
            >
              <template #prepend>
                <v-icon color="success" size="18" class="me-2"
                  >mdi-printer-pos-remove-outline</v-icon
                >
              </template>
              <v-list-item-title class="text-caption font-weight-medium">
                {{ $i18n.locale == "ar" ? "طباعة غير المحدد" : "Print Unselected" }}
              </v-list-item-title>
            </v-list-item>

            <!-- تصدير المحدد -->
            <v-list-item
              v-if="hasExportExcel"
              @click="$emit('exportExcel', true)"
              class="premium-list-item"
            >
              <template #prepend>
                <v-icon color="primary" size="18" class="me-2"
                  >mdi-file-excel-outline</v-icon
                >
              </template>
              <v-list-item-title class="text-caption font-weight-medium">{{
                $i18n.locale == "ar" ? "تصدير المحدد إكسل" : "Export Selected"
              }}</v-list-item-title>
            </v-list-item>

            <!-- إجراءات مخصصة -->
            <template
              v-for="(i, key) in (addToActionsList || []).filter((e) => e.type != 'list')"
              :key="key"
            >
              <v-list-item @click="multipleMethodes(i)" class="premium-list-item">
                <template #prepend>
                  <v-icon color="primary" size="18" class="me-2">mdi-auto-fix</v-icon>
                </template>
                <v-list-item-title class="text-caption font-weight-medium">
                  {{ $i18n.locale == "ar" ? i["title_ar"] : i["title_en"] }}
                </v-list-item-title>
              </v-list-item>
            </template>

            <!-- حذف المحدد -->
            <v-list-item
              v-if="hasDelete"
              @click="deleteItem()"
              class="premium-list-item text-error"
            >
              <template #prepend>
                <v-icon color="error" size="18" class="me-2"
                  >mdi-trash-can-outline</v-icon
                >
              </template>
              <v-list-item-title class="text-caption font-weight-medium">
                {{ $i18n.locale == "ar" ? "حذف المحدد" : "Delete Selected" }}
              </v-list-item-title>
            </v-list-item>
          </template>

          <!-- 2. مجموعة: تقارير وتصدير البيانات -->
          <template v-if="hasPrint || hasExportExcel">
            <v-list-subheader class="modern-subheader px-2 mt-2 mb-1">
              {{ $i18n.locale == "ar" ? "تقارير وتصدير البيانات" : "Reports & Exports" }}
            </v-list-subheader>

            <v-list-item
              v-if="hasPrint"
              @click="$emit('typePrint', 'all')"
              class="premium-list-item"
            >
              <template #prepend>
                <v-icon color="primary" size="18" class="me-2"
                  >mdi-printer-outline</v-icon
                >
              </template>
              <v-list-item-title class="text-caption font-weight-medium">{{
                $i18n.locale == "ar" ? "طباعة كل العناصر" : "Print All Items"
              }}</v-list-item-title>
            </v-list-item>

            <v-list-item
              v-if="hasExportExcel"
              @click="$emit('exportExcel')"
              class="premium-list-item"
            >
              <template #prepend>
                <v-icon color="success" size="18" class="me-2"
                  >mdi-microsoft-excel</v-icon
                >
              </template>
              <v-list-item-title class="text-caption font-weight-medium">{{
                $i18n.locale == "ar" ? "تصدير الكل إكسل" : "Export All to Excel"
              }}</v-list-item-title>
            </v-list-item>
          </template>

          <!-- 3. مجموعة: إدارة السجلات والتدقيق -->
          <template v-if="hasRestore || hasLog">
            <v-list-subheader class="modern-subheader px-2 mt-2 mb-1">
              {{ $i18n.locale == "ar" ? "إدارة السجلات والتدقيق" : "Data Management" }}
            </v-list-subheader>

            <v-list-item
              v-if="hasRestore"
              @click="recoverDelete"
              class="premium-list-item"
            >
              <template #prepend>
                <v-icon color="primary" size="18" class="me-2"
                  >mdi-database-refresh-outline</v-icon
                >
              </template>
              <v-list-item-title class="text-caption font-weight-medium">{{
                $i18n.locale == "ar" ? "استعادة المحذوفات" : "Restore Deleted"
              }}</v-list-item-title>
            </v-list-item>

            <v-list-item
              v-if="hasLog"
              @click="log_dialog = true"
              class="premium-list-item"
            >
              <template #prepend>
                <v-icon color="primary" size="18" class="me-2"
                  >mdi-clipboard-pulse-outline</v-icon
                >
              </template>
              <v-list-item-title class="text-caption font-weight-medium">{{
                $i18n.locale == "ar" ? "سجل العمليات" : "Operation Log"
              }}</v-list-item-title>
            </v-list-item>
          </template>
        </v-list>
      </v-card-text>
    </v-card>
  </v-menu>

  <!-- الحوارات (Dialogs) -->
  <custom-dialog
    v-model="log_dialog"
    :title="
      label ? label : $i18n.locale == 'ar' ? 'سجل العمليات للشاشة' : 'Operation Log'
    "
    class="mt-5"
    fullscreen
  >
    <LogTable :url="url" :headers_log="headers" />
  </custom-dialog>

  <custom-dialog
    v-model="dialog_restore"
    :title="label ? label : $i18n.locale == 'ar' ? 'السجلات المحذوفة' : 'Deleted Records'"
    class="mt-5"
    fullscreen
  >
    <VCard class="print">
      <restore-table
        :headers="headers"
        :url="url"
        :getDataAfterRestore="getData"
        :customTable="customTable"
        get
      />
    </VCard>
  </custom-dialog>
</template>
<script>
import { state } from "@/store/state";
import { ExportToExcel } from "../../../../../src/utils/Globals";
import { useHeaderFooterStore } from "../../../../../src/stores/headerFooterStore";

export default {
  props: {
    selectedItems: {
      type: Array,
      default: [],
    },

    items: {
      type: Array,
      default: [],
    },
    headers: {
      type: Array,
      default: [],
    },
    fields: {
      type: Array,
      default: [],
    },
    url: {
      type: [Function, Boolean, String],
      default() {
        return false;
      },
    },
    label: {
      type: String,
      default: null,
    },
    print: null,
    hasImportExcel: false,
    hasExportExcel: false,
    hasPrint: false,
    hasDelete: {
      type: Boolean,
      default: false,
    },
    hasLog: {
      type: Boolean,
      default: false,
    },
    hasRestore: {
      type: Boolean,
      default: false,
    },
    customTable: {
      type: Boolean,
      default: true,
    },
    getData: Function,
    deleteItem: Function,
    multipleMethodes: Function,
    addToActionsList: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      log_dialog: false,
      dialog_restore: false,
    };
  },
  methods: {
    async printReport(type_print = undefined) {
      const headerFooterStore = useHeaderFooterStore();
      await headerFooterStore.changeHeaderFooter({
        fk_screen: this.$route?.meta?.fk_screen,
      });
      console.log(headerFooterStore.headerFooterData);

      this.$emit("typePrint", type_print);

      // إضافة تأخير بسيط جداً (Buffer) لضمان استقرار المتصفح
      await new Promise((resolve) => setTimeout(resolve, 200));
      const elementToPrint = document.querySelector(`#${this.print}`).innerHTML;

      if (!elementToPrint) {
        console.error("العنصر موجود ولكن لا يحتوي على محتوى (innerHTML)");
        return;
      }

      // ننتظر قليلاً لضمان ظهور عنصر printView في الـ DOM
      await new Promise((resolve) => setTimeout(resolve, 500));

      const printView = document.getElementById("printView");
      if (!printView) {
        console.error("عنصر printView غير موجود في الـ DOM");
        state.print = false;

        return;
      }

      // نسخ المحتوى إلى حاوية الطباعة
      printView.innerHTML = elementToPrint;

      // --- الجزء الجديد: انتظار تحميل الصور ---
      const images = printView.querySelectorAll("img");
      const imagePromises = Array.from(images).map((img) => {
        if (img.complete) {
          return Promise.resolve(); // الصورة محملة مسبقاً
        }
        return new Promise((resolve) => {
          img.onload = resolve; // نجاح التحميل
          img.onerror = resolve; // حتى لو فشل التحميل، نكمل لكي لا تتعطل الطباعة
        });
      });

      try {
        // انتظار جميع الصور حتى تنتهي من التحميل

        await Promise.all(imagePromises);

        // إضافة تأخير بسيط جداً (Buffer) لضمان استقرار المتصفح
        await new Promise((resolve) => setTimeout(resolve, 500));

        // تشغيل أمر الطباعة
        window.print();
      } catch (err) {
        console.error("خطأ أثناء انتظار الصور:", err);
      } finally {
        // التنظيف وإعادة الحالة
        printView.innerHTML = "";

        state.print = false;
        this.$emit("typePrint", null);

        headerFooterStore.headerFooterData = {};
      }
    },
    exportExcel() {
      const title =
        this.$i18n.locale == "ar"
          ? this.$route?.matched?.find((e) => e.name == this.$route.name).props?.default
              ?.name_ar
          : this.$route?.matched?.find((e) => e.name == this.$route.name).props?.default
              ?.name_en;

      if (this.items && this.items.length > 0) {
        ExportToExcel(
          this.headers
            .filter((e) => e.type != "img" && e.key != "actions" && e.key != "numbering")
            .map((e) => {
              return { header: e.title, key: e.key };
            }),
          this.items,
          title || ""
        );
      } else this.$snack("empty");

      this.type_export = undefined;
    },

    recoverDelete() {
      this.dialog_restore = true;
    },
  },
};
</script>
<style scoped>
.premium-list-item {
  transition: all 0.15s ease;
  margin: 2px 6px !important;
  border-radius: 6px !important;
  min-height: 34px !important;
  padding: 0 8px !important;
}
.premium-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.05) !important;
}
.modern-subheader {
  font-size: 0.65rem !important;
  text-transform: uppercase;
  font-weight: 800;
  color: rgb(var(--v-theme-on-surface));
  display: flex;
  align-items: center;
}
.modern-subheader::after {
  content: "";
  flex: 1;
  height: 1px;
  background: rgba(var(--v-theme-on-surface), 0.05);
  margin-left: 8px;
}
</style>
