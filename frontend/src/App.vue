
<template>
  <!-- added by samer -->
  <!--  بداية التطبيق -->
  <v-app :theme="state?.theme?.name_en">
    <v-locale-provider :rtl="$i18n.locale === 'ar' ? true : false">
      <div id="appViews">
        <router-view />
      </div>
      <v-theme-provider class="pa-5" theme="lightTheme" style="z-index: 10000">
        <div class="only-print">
          <table class="print-layout-table">
            <thead>
              <tr>
                <td>
                  <header class="report-header">
                    <preview-content-html
                      :items="header_page"
                      :variables="variables"
                    />
                  </header>
                </td>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td>
                  <main class="main-report">
                    <div id="printView"></div>
                  </main>
                </td>
              </tr>
            </tbody>

            <tfoot>
              <tr>
                <td>
                  <div class="footer-spacer-block"></div>
                </td>
              </tr>
            </tfoot>
          </table>
          <footer class="report-footer text-center align-center justify-center">
            <preview-content-html :items="footer_page" :variables="variables" />
          </footer>
        </div>
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
import { ref, computed, onBeforeMount, watch } from "vue";

import { state } from "./store/state";











const variable = ref({});

const header_page = computed(() => {
  return JSON.parse(state?.header_footer?.header || "[]");
});
const footer_page = computed(() => {
  return JSON.parse(state?.header_footer?.footer || "[]");
});
const variables = computed(() => {
  return state.variables || {};
});
</script>

<style>
html {
  overflow: hidden;
}

@media print {
  /* إظهار واجهة الطباعة */
  #printView {
    display: block !important;
    z-index: 999999;
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
    overflow: visible !important;
  }

  .v-table__wrapper {
    height: auto;
  }

  :root {
    --v-theme-background: #ffffff !important;
    --v-theme-surface: #ffffff !important;
    --v-theme-on-background: #000000 !important;
    --v-theme-on-surface: #000000 !important;
  }

  body {
    background: white !important;
    color: black !important;
  }
}
</style>
