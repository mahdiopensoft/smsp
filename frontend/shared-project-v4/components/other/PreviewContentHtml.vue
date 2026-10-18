<template>
  <VSheet width="100%" elevation="0" class="pa-3">
    <v-row no-gutters>
      <v-col
        v-for="(html, index) in props.items"
        :key="index"
        :cols="headerFooter.colSize(props.items?.length)"
      >
        <div
          class="preview-content"
          v-html="headerFooter.highlightVariables(html, variables)"
        />
      </v-col>
    </v-row>
  </VSheet>
</template>
<script setup>
import useHeaderFooter from "../../src/composables/useHeaderFooter";
import { useHeaderFooterStore } from "../../src/stores/headerFooterStore";

const headerFooter = useHeaderFooter();
const headerFooterStore = useHeaderFooterStore();
const props = defineProps({
  items: { type: Array, default: () => [] },

  isHeader: { type: Boolean, default: false },
});
</script>

<style scop>
.preview-content {
  line-height: 1.6;
  color: #333;
}

/* محاذاة نصوص Quill */
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
    /* height: 100px !important; */
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
