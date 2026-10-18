<template>
  <div class="hf-bottom-panel">
    <div class="hf-bottom-preview">
      <div class="hf-bottom-panel-title d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon
            icon="mdi-file-document-check-outline"
            size="15"
            color="success"
            class="me-1"
          />
          <span>المعاينة الحية للتقرير والطباعة (Live Preview)</span>
        </div>
      </div>

      <div class="hf-full-preview">
        <div class="hf-full-preview-inner">
          <!-- Header preview -->
          <div class="hf-fp-label d-flex align-center justify-space-between">
            <div class="d-flex align-center">
              <v-icon icon="mdi-page-layout-header" size="12" class="me-1" />
              <span>معاينة الهيدر (Header)</span>
            </div>
            <span v-if="interactive" class="hf-preview-hint"
              >انقر على أي عمود لتحديده وتعديله ↖</span
            >
          </div>
          <div
            v-html="liveHtml.header"
            class="hf-fp-render"
            :class="{ 'hf-clickable-preview': interactive }"
            :title="interactive ? 'انقر على أي عمود لتحديده وتعديله' : ''"
            @click="onPreviewClick($event, 'header')"
          />

          <!-- Page content placeholder -->
          <div class="hf-fp-page">
            <v-icon
              icon="mdi-file-document-outline"
              size="15"
              class="me-1"
              style="opacity: 0.4"
            />
            <span style="opacity: 0.6; font-size: 12px">
              [محتوى التقرير أو الصفحة يتم عرضه هنا عبر النظام]
            </span>
          </div>

          <!-- Footer preview -->
          <div class="hf-fp-label d-flex align-center justify-space-between">
            <div class="d-flex align-center">
              <v-icon icon="mdi-page-layout-footer" size="12" class="me-1" />
              <span>معاينة الفوتر (Footer)</span>
            </div>
            <span v-if="interactive" class="hf-preview-hint"
              >انقر على أي عمود لتحديده وتعديله ↖</span
            >
          </div>

          <div
            v-html="liveHtml.footer"
            class="hf-fp-render"
            :class="{ 'hf-clickable-preview': interactive }"
            :title="interactive ? 'انقر على أي عمود لتحديده وتعديله' : ''"
            @click="onPreviewClick($event, 'footer')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  liveHtml: {
    type: Object,
    default: () => ({ header: "", footer: "" }),
  },
  activeTemplate: {
    type: Object,
    default: null,
  },
  interactive: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(["select-cell"]);

const onPreviewClick = (e, defaultSection) => {
  if (!props.interactive) return;

  // Check if clicked directly inside one of the rendered column spans
  const container = e.currentTarget;
  const spans = container
    ? Array.from(container.querySelectorAll(":scope > div > span"))
    : [];
  if (spans.length > 0) {
    const clickedIdx = spans.findIndex((s) => s === e.target || s.contains(e.target));
    if (clickedIdx >= 0) {
      emit("select-cell", { section: defaultSection, idx: clickedIdx });
      return;
    }
  }

  // Fallback: calculate column index by click X position
  if (container) {
    const rect = container.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const width = rect.width;
    const totalCols =
      spans.length ||
      (defaultSection === "header"
        ? props.activeTemplate?.header?.cells?.length
        : props.activeTemplate?.footer?.cells?.length) ||
      3;
    const colWidth = width / totalCols;
    // In RTL, column 0 is on the right
    const colIdx = Math.min(
      totalCols - 1,
      Math.max(0, Math.floor((width - clickX) / colWidth))
    );
    emit("select-cell", { section: defaultSection, idx: colIdx });
  }
};
</script>
