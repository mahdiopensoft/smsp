<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="700"
    persistent
  >
    <v-card rounded="xl" class="hf-select-dialog-card" dir="rtl">
      <!-- Dialog Header -->
      <div class="hf-select-dialog-header">
        <div class="d-flex align-center ga-2">
          <div class="hf-select-icon-box">
            <v-icon icon="mdi-page-layout-header-footer" size="22" color="primary" />
          </div>
          <div>
            <div class="text-subtitle-1 font-weight-black text-slate-800">
              اختيار قالب الهيدر والفوتر للشاشة
            </div>
            <div class="text-caption text-medium-emphasis">
              اختر القالب المطلوب لعرض وتطبيق الهيدر والفوتر على هذه الشاشة
            </div>
          </div>
        </div>
        <v-btn icon="mdi-close" size="small" variant="text" @click="closeDialog" />
      </div>

      <!-- Dialog Body -->
      <v-card-text class="pa-5">
        <!-- 1. Autocomplete for choosing template -->
        <div class="mb-4">
          <label class="hf-label mb-2 d-flex align-center ga-1 font-weight-bold">
            <v-icon icon="mdi-format-list-bulleted-type" size="16" color="primary" />
            <span>اختر القالب:</span>
          </label>

          <v-autocomplete
            v-model="chosenTemplateId"
            :items="templateList"
            item-title="name"
            item-value="id"
            placeholder="ابحث واختر قالب الهيدر والفوتر..."
            variant="outlined"
            density="comfortable"
            rounded="lg"
            color="primary"
            prepend-inner-icon="mdi-magnify"
            clearable
            hide-details="auto"
          >
            <template #item="{ props: itemProps, item }">
              <v-list-item v-bind="itemProps">
                <template #prepend>
                  <v-icon
                    icon="mdi-file-document-outline"
                    size="20"
                    color="primary"
                    class="me-2"
                  />
                </template>
                <template #append>
                  <span class="text-caption text-medium-emphasis">
                    {{ item.raw.header?.columns || 3 }} أعمدة
                  </span>
                </template>
              </v-list-item>
            </template>
          </v-autocomplete>
        </div>

        <!-- 2. Live Preview Section when Template is Selected -->
        <div class="hf-preview-wrapper mt-3">
          <label
            class="hf-label mb-2 d-flex align-center justify-space-between font-weight-bold"
          >
            <div class="d-flex align-center ga-1 text-primary">
              <v-icon icon="mdi-eye-outline" size="16" color="primary" />
              <span>معاينة الهيدر والفوتر للقالب المختار:</span>
            </div>
            <span
              v-if="chosenTemplate"
              class="text-caption font-weight-bold text-medium-emphasis"
            >
              {{ chosenTemplate.name }}
            </span>
          </label>

          <!-- Render Preview Sheet -->
          <div v-if="chosenTemplate && previewHtml" class="hf-select-preview-sheet">
            <!-- Header preview -->
            <div class="hf-select-preview-tag header-tag">
              <v-icon icon="mdi-page-layout-header" size="12" class="me-1" />
              الهيدر (Header)
            </div>
            <div v-html="previewHtml.header" class="hf-select-html-render" />

            <!-- Page content placeholder -->
            <div class="hf-select-page-placeholder">
              <v-icon
                icon="mdi-file-document-outline"
                size="18"
                class="me-1 opacity-50"
              />
              <span>[محتوى التقرير أو الشاشة الحالية]</span>
            </div>

            <!-- Footer preview -->
            <div class="hf-select-preview-tag footer-tag">
              <v-icon icon="mdi-page-layout-footer" size="12" class="me-1" />
              الفوتر (Footer)
            </div>
            <div v-html="previewHtml.footer" class="hf-select-html-render" />
          </div>

          <!-- Empty State (No Template Chosen) -->
          <div v-else class="hf-select-empty-preview">
            <v-icon
              icon="mdi-page-layout-header-footer"
              size="36"
              color="grey-lighten-1"
              class="mb-2"
            />
            <div class="text-caption font-weight-bold text-medium-emphasis">
              يرجى اختيار قالب من القائمة بالأعلى لعرض المعاينة هنا
            </div>
          </div>
        </div>
      </v-card-text>

      <!-- Dialog Footer Actions -->
      <v-card-actions
        class="pa-4 pt-2 d-flex align-center justify-space-between border-t"
      >
        <v-btn variant="text" @click="closeDialog"> إلغاء </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          prepend-icon="mdi-check"
          :disabled="!chosenTemplate"
          @click="confirmSelection"
        >
          تأكيد واختيار القالب
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useCustomHeaderFooter } from "../composables/useCustomHeaderFooter";

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  // Optionally pass the initially selected template ID
  initialTemplateId: {
    type: String,
    default: null,
  },
  // Optional custom template list (defaults to store templates)
  templates: {
    type: Array,
    default: null,
  },
});

const emit = defineEmits(["update:modelValue", "confirm", "select"]);

const store = useCustomHeaderFooter();

const templateList = computed(() => {
  if (props.templates && props.templates.length) {
    return props.templates;
  }
  return store.templates || [];
});

const chosenTemplateId = ref(
  props.initialTemplateId || templateList.value[0]?.id || null
);

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      if (props.initialTemplateId) {
        chosenTemplateId.value = props.initialTemplateId;
      } else if (!chosenTemplateId.value && templateList.value.length) {
        chosenTemplateId.value = templateList.value[0].id;
      }
    }
  }
);

const chosenTemplate = computed(() => {
  return templateList.value.find((t) => t.id === chosenTemplateId.value) || null;
});

const previewHtml = computed(() => {
  if (!chosenTemplate.value) return null;
  return store.generateHTMLForTemplate(chosenTemplate.value);
});

const closeDialog = () => {
  emit("update:modelValue", false);
};

const confirmSelection = () => {
  if (!chosenTemplate.value) return;

  emit("confirm", {
    templateId: chosenTemplate.value.id,
    template: chosenTemplate.value,
    html: previewHtml.value,
  });

  emit("select", chosenTemplate.value);
  emit("update:modelValue", false);
};
</script>

<style scoped>
.hf-select-dialog-card {
  background: #ffffff;
  overflow: hidden;
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
  background: var(--hf-primary-10);
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
  padding: 18px 12px;
  background: #f8fafc;
  border-top: 1px dashed #cbd5e1;
  border-bottom: 1px dashed #cbd5e1;
  font-size: 11.5px;
  color: #64748b;
  font-weight: 600;
}

.hf-select-empty-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  background: #f8fafc;
  border: 1.5px dashed #cbd5e1;
  border-radius: 8px;
  text-align: center;
}
</style>
