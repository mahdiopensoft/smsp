<template>
  <VSheet width="100%" elevation="0" :class="['preview-html-root', isHeader ? 'th-root' : '']">
 
    <div :class="isHeader ? 'th-grid' : 'v-row no-gutters'">
      <div
        v-for="(html, index) in items"
        :key="index"
        :class="[
          isHeader ? 'th-col' : '',
          isHeader && index === 0 ? 'th-col--ar' : '',
          isHeader && index === 1 ? 'th-col--center' : '',
          isHeader && index === 2 ? 'th-col--en' : '',
          !isHeader ? `v-col-md-${headerFooter.colSize(props.items?.length)} v-col-12` : ''
        ]"
      >
      
        <div
          :class="[
            'preview-content preview-content-area',
            isHeader ? 'th-content-wrap' : 'preview-card-wrap'
          ]"
          v-html="headerFooter.highlightVariables(html)"
        />
      </div>
    </div>
    
    <!-- Unified Accent Divider just like TableHeader -->
    <div v-if="isHeader" class="th-divider"></div>
  </VSheet>
</template>

<script setup>
import useHeaderFooter from "../../src/composables/useHeaderFooter";
import { useHeaderFooterStore } from "../../src/stores/headerFooterStore";

const headerFooter = useHeaderFooter();
const headerFooterStore = useHeaderFooterStore();
const props = defineProps({
  items: { type: Array, default: () => [] },
  
  isHeader: { type: Boolean, default: false }
});
 
 
</script>

<style>
/* ═══════════════════════════════════════════════════════
   PREVIEW CONTENT HTML — Professional Report Design
   ═══════════════════════════════════════════════════════ */

/* ── TableHeader Parity Styling for Dynamic Print Headers ── */
.th-root {
  width: 100% !important;
  background-color: rgba(var(--v-theme-on-surface), 0.02) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1) !important;
  padding: 20px 24px 12px !important;
  direction: rtl !important;
  border-radius: 0px !important;
}

.th-grid {
  display: grid !important;
  grid-template-columns: 1fr auto 1fr !important;
  align-items: start !important;
  gap: 20px !important;
}

.th-col {
  display: flex !important;
  flex-direction: column !important;
}

.th-col--ar {
  text-align: right !important;
  direction: rtl !important;
  align-items: flex-start !important;
  padding-top: 4px !important;
}

.th-col--center {
  text-align: center !important;
  align-items: center !important;
  justify-content: center !important;
}

.th-col--en {
  text-align: left !important;
  direction: ltr !important;
  align-items: flex-start !important;
  padding-top: 4px !important;
}

.th-divider {
  height: 2px !important;
  margin: 14px 0 10px !important;
  background: linear-gradient(90deg,
      transparent,
      rgba(var(--v-theme-primary), 0.15) 15%,
      rgba(var(--v-theme-primary), 0.15) 85%,
      transparent) !important;
}

/* ── Format Dynamic Content from v-html to match TableHeader Typography exactly ── */
.th-content-wrap p,
.th-content-wrap span {
  margin: 0 !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
  line-height: 1.6 !important;
  color: rgba(var(--v-theme-on-surface), 0.65) !important;
  font-family: 'Tajawal', sans-serif !important;
}

.th-col--ar .th-content-wrap p:first-child,
.th-col--ar .th-content-wrap span:first-child,
.th-col--en .th-content-wrap p:first-child,
.th-col--en .th-content-wrap span:first-child {
  font-weight: 800 !important;
  font-size: 0.85rem !important;
  color: rgba(var(--v-theme-on-surface), 0.87) !important;
  margin-bottom: 1px !important;
}

.th-col--ar .th-content-wrap p:last-child,
.th-col--ar .th-content-wrap span:last-child,
.th-col--en .th-content-wrap p:last-child,
.th-col--en .th-content-wrap span:last-child {
  font-weight: 700 !important;
  font-size: 0.7rem !important;
  margin-top: 2px !important;
  color: rgba(var(--v-theme-on-surface), 0.4) !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
}

.th-col--center .th-content-wrap p,
.th-col--center .th-content-wrap span {
  margin: 0 0 6px !important;
  font-size: 0.9rem !important;
  font-weight: 700 !important;
  color: rgba(var(--v-theme-on-surface), 0.8) !important;
  text-align: center !important;
}

.th-col--center .th-content-wrap img {
  height: 76px !important;
  width: auto !important;
  max-width: 120px !important;
  object-fit: contain !important;
  display: block !important;
  margin: 0 auto !important;
}

.preview-html-root {
  background: transparent !important;
}

/* ── Container Logic ── */
.preview-card-wrap {
  background-color: rgb(var(--v-theme-surface));
  padding: 24px;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  border-radius: 12px;
  margin: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px -3px rgba(0,0,0,0.03);
}

/* ── Typography — Executive Standard ── */
.preview-content-area {
  line-height: 1.8;
  color: rgba(var(--v-theme-on-surface), 0.85);
  font-size: 0.95rem;
  word-break: break-word;
  font-family: 'Tajawal', sans-serif !important;
}

/* Institutional Headings */
.preview-content-area h1 {
  margin: 0 0 0.75rem;
  color: rgba(var(--v-theme-on-surface), 0.95);
  font-weight: 900;
  font-size: 1.6rem;
  letter-spacing: -0.02em;
}

.preview-content-area h2 {
  color: rgba(var(--v-theme-on-surface), 0.8);
  font-weight: 800;
  font-size: 1.3rem;
  margin: 1.5rem 0 0.75rem;
}

/* Specialized Table Rendering */
.preview-content-area table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: white;
}

/* Header-Specific Layout Tables (Transparent) */
.preview-content-area table.layout-table {
  border: none !important;
  background: transparent !important;
}

.preview-content-area table th {
  background: rgba(var(--v-theme-on-surface), 0.04);
  padding: 12px 15px;
  text-align: inherit;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.15);
  font-weight: 800;
}

.preview-content-area table td {
  padding: 10px 15px;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
}

/* Image/Logo Handling */
.preview-content-area img {
  max-width: 100%;
  height: auto;
  object-fit: contain;
  display: inline-block;
  vertical-align: middle;
}

/* ═══════════════════════════════════════════════════════
   PRINT OVERRIDES — Integrated with App.vue Logic
   ═══════════════════════════════════════════════════════ */

@media print {
  .preview-html-root {
    width: 100% !important;
  }

  .preview-card-wrap {
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }

  .preview-content-area {
    color: #000 !important;
    font-size: 11pt !important;
    line-height: 1.5 !important;
  }

  .preview-content-area h1 {
    font-size: 18pt !important;
    margin-bottom: 5mm !important;
  }

  .preview-content-area h2 {
    font-size: 14pt !important;
  }

  /* Optimized Print Tables */
  .preview-content-area table th {
    background-color: #f5f5f5 !important;
    border: 1px solid #666 !important;
    color: #000 !important;
  }

  .preview-content-area table td {
    border: 1px solid #999 !important;
    color: #000 !important;
  }

  /* Clean Dividers */
  .preview-content-area hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 1cm 0;
  }
}

.preview-content .ql-align-center {
  text-align: center !important;
}

.preview-content .ql-align-right {
  text-align: right !important;
}

.preview-content .ql-align-left {
  text-align: left !important;
}

.preview-content .ql-align-justify {
  text-align: justify !important;
}

/* تنسيق الشاشة (Web View) */
.flex-grow-1 {
  flex-grow: 1 !important;
}

.mt-auto {
  margin-top: auto !important;
}

/* التنسيق العادي للشاشة */
.print-layout-table {
  width: 100%;
  border-collapse: collapse;
}

.header-spacer,
.footer-spacer {
  display: none; /* إخفاء المساحات في العرض العادي */
}

.only-print {
  display: none !important;
}
@media print {
  .no-print {
    display: none !important;
  }

  .only-print {
    display: block !important;
  }

  thead {
    display: table-header-group !important;
  }

  tfoot {
    display: table-footer-group !important;
  }

  tr {
    page-break-inside: avoid;
    page-break-after: auto;
  }

  .report-header {
    z-index: 1000;
    /* border: 0.5px solid grey; */
    background-color: white;

    padding: 5px;
    width: calc(100vw - 20px);
  }

  .report-footer {
    z-index: 1000;
    /* border: 0.5px solid grey; */
    background-color: white;

    padding: 5px;
    width: calc(100vw - 20px);
    
    position: fixed;
    bottom: 10px;
  }

  .footer-spacer-block {
    height: 120px;
    visibility: hidden;
  }

  /* تأكد من أن الـ VCard والـ Main لا يملكان خاصية Overflow */
  .v-card,
  .main-report {
    overflow: visible !important;
  }

  /* منع قطع الصفوف في منتصفها */
  .custom-data-table tr {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  html,
  body {
    height: 100px !important;
    background: white !important;
    margin: 5px !important;
  }

  .v-application__wrap {
    background-color: white !important;
    min-height: 100% !important;
    overflow: hidden !important;
  }

  .v-table__wrapper {
    overflow: hidden !important;
  }

  .v-table > .v-table__wrapper > table > tbody > tr > td,
  .v-table > .v-table__wrapper > table > thead > tr > td,
  .v-table > .v-table__wrapper > table > tfoot > tr > td {
    text-wrap: wrap;
  }

  .v-table > .v-table__wrapper > table > thead > tr > td > span {
    font-size: 2px !important;
  }

  * {
    color-adjust: exact !important;
    -webkit-print-color-adjust: exact !important;
  }

  .no_print {
    display: none;
  }

  .print-btn {
    display: none;
  }

  @page {
    margin: 0px !important;
  }

  #footer {
    display: none !important;
  }

  .hide-item {
    display: none;
  }

  .printable {
    display: block !important;
  }

  .show-item {
    display: block;
  }
}
</style>
<style scoped></style>