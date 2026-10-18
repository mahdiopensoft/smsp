<template>
  <!-- added by samer -->
  <!--  بداية التطبيق -->
  <v-app :theme="state?.theme?.name_en">
    <v-locale-provider id="appViewId" :rtl="$i18n.locale === 'ar' ? true : false">
      <div id="appViews">
        <router-view></router-view>
      </div>
      <v-theme-provider
        class="pa-5 theme-container"
        theme="lightTheme"
        style="z-index: 10000"
      >
        <!-- <div class="page-header" :style="`height:${heightHeader}px`">
            <div v-html="previewHtml.header" />

           
          </div>

          <div class="page-body">
            <div id="printView"></div>
          </div>
          <div class="page-footer" :style="`height:${heightFooter}px`">
            <div v-html="previewHtml.footer" />
          </div> -->
        <v-container class="page-container">
          <v-table class="app-layout">
            <thead>
              <div class="header-inner" v-html="previewHtml.header" />
            </thead>
            <v-container class="mt-0 pt-0">
              <div id="printView"></div>
            </v-container>
            <tfoot>
              <div class="footer-inner" v-html="previewHtml.footer" />
            </tfoot>
          </v-table>
        </v-container>
      </v-theme-provider>
    </v-locale-provider>
  </v-app>
  <alert
    v-if="state.alert"
    v-model="state.alert"
    :details="state.alert_details"
    class="text-white"
  />
</template>
<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { state } from "@/../src/store/state";

import { useHeaderFooterStore } from "./stores/headerFooterStore";
import { useCustomHeaderFooter } from "./headerandfooter/composables/useCustomHeaderFooter";

const headerFooterStore = useHeaderFooterStore();
const customHeaderFooter = useCustomHeaderFooter();

const header_page = computed(() => {
  return JSON.parse(headerFooterStore?.headerFooterData?.header || "[]");
});
const footer_page = computed(() => {
  return JSON.parse(headerFooterStore?.headerFooterData?.footer || "[]");
});

const heightHeader = ref(null);
const heightFooter = ref(null);
const previewHtml = computed(() => {
  if (!headerFooterStore?.headerFooterData) return { header: "", footer: "" };

  const header = headerFooterStore?.headerFooterData?.header
    ? JSON.parse(headerFooterStore?.headerFooterData?.header)
    : "";
  const footer = headerFooterStore?.headerFooterData?.footer
    ? JSON.parse(headerFooterStore?.headerFooterData?.footer)
    : "";

  const jsondata = {
    header,
    footer,
  };
  heightHeader.value = jsondata.header;
  heightFooter.value = jsondata.footer;
  return customHeaderFooter.generateHTMLForTemplate(jsondata);
});
</script>

<style>
html {
  overflow: hidden;
}

@media print {
  @page {
    size: auto;
    margin: -2mm !important;
  }

  html,
  body,
  #app,
  .v-application,
  .v-application__wrap,
  .app-layout,
  .print-continer {
    margin: 0;
    padding: 0;
    overflow: visible !important;
  }

  #appViews,
  .v-overlay-container,
  .v-overlay,
  .v-dialog,
  #appViews * {
    display: none !important;
    visibility: hidden !important;
  }

  .page-container {
    padding: 0 !important;
    margin: 0 !important;
  }

  /* main layout */
  /* .app-layout {
    display: block !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 100% !important;
    border-collapse: collapse;

    position: relative;
    display: flex !important;
    flex-direction: column !important;

  } */
  .header-inner {
    margin-bottom: 15px !important;
  }
  .app-layout thead {
    width: 100% !important;
    display: table-header-group;
  }
  .app-layout tfoot {
    display: block;
    /* position: fixed;
    bottom: 0px;
    left: 0;
    right: 0; */
    display: table-footer-group;
  }
  .app-layout tfoot .footer-inner {
    display: block;
    width: 100% !important;
  }
  .app-layout tbody {
    height: 100% !important;
    display: table-row-group;
  }

  .app-layout td {
    padding: 0;
    border: 0;
  }
  .header-inner,
  .footer-inner {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  /* #printView {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    height: 100% !important;
    min-height: 100% !important;
    break-inside: avoid !important;
    page-break-inside: avoid !important;
    overflow: visible !important;
  } */

  tbody tr,
  .prevent-split {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /*   @page {
    size: auto;
    margin: 0mm;
  }

  #appViews,
  .v-overlay-container,
  .v-overlay,
  .v-dialog {
    display: none !important;
    visibility: hidden !important;
  }

  html,
  body {
    height: 99vh;
    margin: 0;
    padding: 0;
    background: black;
  }

  .print-continer {
    display: flex;
    flex-direction: column;
    height: 99vh;
    box-sizing: border-box;
  }

  .page-header {
    flex-shrink: 0;
    background: white;
  }
  .page-body {
    flex-grow: 1;
    overflow: hidden;
  }
  .page-footer {
    flex-shrink: 0;
    background: white;
  } */

  /* .page-report {
    width: 100% !important;
    max-width: 100% !important;
    table-layout: fixed;
    border-collapse: collapse;
  }

  .page-report thead td,
  .page-report tbody td,
  .page-report tfoot td {
    width: 100% !important;
    box-sizing: border-box;
  }
  thead {
    display: table-header-group;
  }
  tfoot {
    display: table-header-group;
  }
  tbody tr,
  .prevent-split {
    page-break-inside: avoid;
    break-inside: avoid;
  } */
}
</style>
