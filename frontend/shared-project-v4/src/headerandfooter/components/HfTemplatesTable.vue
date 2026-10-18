<template>
  <CustomDataTable
    :headers="[
      { key: 'name', title: 'اسم القالب' },
      { key: 'header_columns', title: 'أعمدة الهيدر' },
      { key: 'footer_columns', title: 'أعمدة الفوتر' },
      { key: 'is_main', title: 'is_main' },
    ]"
    :items="items"
    :editItem="(item) => $emit('edit-template', item.id)"
    :getData="getData"
    :create="() => $emit('open-create')"
    :hasInfo="false"
    delItem="common/print-report-setting/"
  >
    <template v-slot:action-row="{ item }">
      <custom-btn
        type="show"
        icon="mdi-content-copy"
        is-icon
        label="نسخ وتكرار القالب"
        @click="$emit('duplicate-template', item.id)"
        :loading="item.loading"
        color="secondary"
        class="me-1"
      />
      <custom-btn type="show" is-icon @click="openPreview(item)" />
    </template>
    <template v-slot:item-slot="{ item, key }">
      <span v-if="key === 'header_columns'">
        <div class="d-flex align-center ga-2">
          <v-chip size="small" variant="tonal" color="info" class="font-weight-bold">
            <v-icon icon="mdi-page-layout-header" size="14" class="me-1" />
            {{ item.header?.columns || 3 }} أعمدة
          </v-chip>
          <span
            class="hf-color-dot"
            :style="{ backgroundColor: item.header?.backgroundColor || '#ffffff' }"
            :title="`لون خلفية الهيدر: ${item.header?.backgroundColor || '#ffffff'}`"
          />
        </div>
      </span>
      <span v-if="key === 'footer_columns'">
        <div class="d-flex align-center ga-2">
          <v-chip size="small" variant="tonal" color="indigo" class="font-weight-bold">
            <v-icon icon="mdi-page-layout-footer" size="14" class="me-1" />
            {{ item.footer?.columns || 3 }} أعمدة
          </v-chip>
          <span
            class="hf-color-dot"
            :style="{ backgroundColor: item.footer?.backgroundColor || '#ffffff' }"
            :title="`لون خلفية الفوتر: ${item.footer?.backgroundColor || '#ffffff'}`"
          />
        </div>
      </span>
    </template>
  </CustomDataTable>

  <!-- ═══════════════════════════════════════════════════
         QUICK PREVIEW DIALOG
    ═══════════════════════════════════════════════════ -->
  <v-dialog v-model="previewDialog" max-width="760">
    <v-card rounded="xl" v-if="previewTpl" dir="rtl">
      <div class="hf-select-dialog-header">
        <div class="d-flex align-center ga-2">
          <div class="hf-select-icon-box">
            <v-icon icon="mdi-eye-outline" size="22" color="primary" />
          </div>
          <div>
            <div class="text-subtitle-1 font-weight-black text-slate-800">
              معاينة القالب: {{ previewTpl.name }}
            </div>
            <div class="text-caption text-medium-emphasis">
              عرض حي لمحتوى الهيدر والفوتر كما سيظهر في الطباعة والتقارير
            </div>
          </div>
        </div>
        <v-btn
          icon="mdi-close"
          size="small"
          variant="text"
          @click="previewDialog = false"
        />
      </div>

      <v-card-text class="pa-5">
        <div class="hf-select-preview-sheet">
          <!-- Header preview -->
          <div class="hf-select-preview-tag header-tag">
            <v-icon icon="mdi-page-layout-header" size="12" class="me-1" />
            الهيدر ({{ previewTpl.header?.columns || 3 }} أعمدة)
          </div>
          <div v-html="previewHtml.header" class="hf-select-html-render" />

          <!-- Body placeholder -->
          <div class="hf-select-page-placeholder">
            <v-icon icon="mdi-file-document-outline" size="20" class="me-1 opacity-50" />
            <span>[ محتوى التقرير / بيانات الشاشة الحالية ]</span>
          </div>

          <!-- Footer preview -->
          <div class="hf-select-preview-tag footer-tag">
            <v-icon icon="mdi-page-layout-footer" size="12" class="me-1" />
            الفوتر ({{ previewTpl.footer?.columns || 3 }} أعمدة)
          </div>
          <div v-html="previewHtml.footer" class="hf-select-html-render" />
        </div>
      </v-card-text>

      <v-card-actions
        class="pa-4 pt-2 border-t d-flex align-center justify-space-between"
      >
        <v-btn variant="text" @click="previewDialog = false">إغلاق</v-btn>
        <div class="d-flex align-center ga-2">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            prepend-icon="mdi-pencil-ruler"
            @click="onEditFromPreview"
          >
            فتح في محرر التصميم
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from "vue";
import { useCustomHeaderFooter } from "../composables/useCustomHeaderFooter";

const emit = defineEmits(["open-create"]);

const items = computed(() => {
  return store.templates;
});

const store = useCustomHeaderFooter();

const previewDialog = ref(false);
const previewTpl = ref(null);

const previewHtml = computed(() => {
  if (!previewTpl.value) return { header: "", footer: "" };
  return store.generateHTMLForTemplate(previewTpl.value);
});

const openPreview = (tpl) => {
  previewTpl.value = tpl;
  previewDialog.value = true;
};

const onEditFromPreview = () => {
  if (previewTpl.value) {
    const id = previewTpl.value.id;
    previewDialog.value = false;
    emit("edit-template", id);
  }
};

const getData = async () => {
  await store.fetchTemplatesFromApi();
};
</script>

<style scoped>
.hf-table-view-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.hf-table-header-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 18px 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.hf-table-icon-badge {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(
    135deg,
    rgb(var(--v-theme-primary)) 0%,
    rgba(var(--v-theme-primary), 0.8) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(var(--v-theme-primary), 0.3);
}

.hf-table-search {
  max-width: 240px;
  min-width: 180px;
}

.hf-data-table-card {
  background: #ffffff;
  overflow: hidden;
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.hf-custom-table {
  width: 100%;
  border-collapse: collapse;
  text-align: right;
  font-size: 13.5px;
}

.hf-custom-table th {
  background: #f8fafc;
  color: #475569;
  font-weight: 700;
  padding: 14px 18px;
  border-bottom: 2px solid #e2e8f0;
  white-space: nowrap;
}

.hf-custom-table td {
  padding: 14px 18px;
  border-bottom: 1px solid #edf2f7;
  color: #1e293b;
  vertical-align: middle;
}

.hf-custom-table tbody tr {
  transition: background-color 0.15s ease;
}

.hf-custom-table tbody tr:hover {
  background-color: #f8fafc;
}

.hf-row-active {
  background-color: rgba(var(--v-theme-primary), 0.03) !important;
}

.hf-tpl-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #f1f5f9;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.hf-tpl-icon-active {
  background: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
}

.hf-color-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 1.5px solid #cbd5e1;
  display: inline-block;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.hf-select-dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.hf-select-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(var(--v-theme-primary), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.hf-select-preview-sheet {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.hf-select-preview-tag {
  font-size: 10px;
  font-weight: 700;
  padding: 3px 10px;
  display: flex;
  align-items: center;
}

.hf-select-preview-tag.header-tag {
  background: #eff6ff;
  color: #2563eb;
  border-bottom: 1px solid #dbeafe;
}

.hf-select-preview-tag.footer-tag {
  background: #eef2ff;
  color: #4f46e5;
  border-top: 1px solid #e0e7ff;
}

.hf-select-html-render {
  min-height: 38px;
  width: 100%;
}

.hf-select-page-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 12px;
  background: #f8fafc;
  border-top: 1px dashed #cbd5e1;
  border-bottom: 1px dashed #cbd5e1;
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
}
</style>
