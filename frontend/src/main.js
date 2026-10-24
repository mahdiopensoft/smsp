// Plugins
import { registerPlugins } from "@/plugins";
import i18n from "./plugins/i18n";
import tooltip from './directives/tooltip'
import vEsc from "./directives/esc";
// Components
import App from "./App.vue";


import FilterFields from "./components/FilterFields.vue";
import OMRWorkflowBar from "./components/OMRWorkflowBar.vue";

//utils
import shared from "external-components";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createPinia } from "pinia";
import settings from "../settings";

import router from "./router";
import { makeGlobals } from "@/utils/initGloabals";
// import Datetime from 'vue3-datetime-js';

// Composables
import { createApp } from "vue";
// assets
import "@/styles/style.css";
import"@/styles/index.css"
import headers from "headers";
import dataList from "./utils/DataAutoList";
import {
   fix_branch_field,
  fix_image_url,
  getProfile,
} from "./utils/Function";
import { state } from "./store/state";

//global variable
export const base_url = settings.url;
export const sidebar_url = settings.url_sidbar;
let app;
async function bootstarApp() {
  try {
    app = createApp(App);

    app.config.warnHandler = (msg, instance, trace) => {
      if (import.meta.env?.PROD) return;
      if (typeof msg === "string" && msg.includes("Extraneous non-props attributes")) return;
      console.warn(`[Vue warn]: ${msg}`, trace);
    };

    app.config.errorHandler = (err, instance, info) => {
      if (err && typeof err.message === "string" && err.message.includes("$el")) {
        console.warn("Vuetify $el ref captured:", err);
        return;
      }
      console.error("Vue Error:", err, info);
    };
     // =========================
    // Pinia
    // =========================
    const pinia = createPinia();
    pinia.use(piniaPluginPersistedstate);
    app.use(pinia);

    i18n.global.messages.ar = { ...i18n.global?.messages?.ar, ...shared.ar };
    i18n.global.messages.en = { ...i18n.global?.messages?.en, ...shared.en };
     // =========================
    // i18n
    // =========================
    app.use(i18n);
     // =========================
    // Global plugins
    // =========================
    app.use(shared.ValueValidationPlugin);

    app.use(shared.Globals);


    registerPlugins(app);

    //================component
    app.component("filter-fields", FilterFields);
    app.component("omr-workflow-bar", OMRWorkflowBar);

     // =========================
    // Global directives
    // =========================
    app.directive("esc", vEsc);
    app.directive('tooltip', tooltip)
    // =========================
    // Global properties
    // =========================

    app.config.globalProperties.setting = settings;
    app.config.globalProperties.$shared = shared;
    app.config.globalProperties.$headers = headers;
    app.config.globalProperties.$dataList = dataList;
    app.config.globalProperties.$state = state;
    app.config.globalProperties.$axios = shared.api;
    app.config.globalProperties.$fix_image_url = fix_image_url;
    app.config.globalProperties.$fix_branch_field = fix_branch_field;
    makeGlobals(app);
     // =========================
    // BOOTSTRAP AUTH (IMPORTANT)
    // =========================
    const authStore = shared.useAuthStore();

    try {
      // 🔥 Ask backend to restore session using HttpOnly cookie
      await authStore.initAuth?.();


    } catch (e) {
      console.warn("No active session");
    }

    const components = shared.components;
    await addImport(components);

     // =========================
    // Load dynamic routes AFTER auth check
    // =========================

    // =========================
    // Router
    // =========================

    if (authStore.isAuthenticated) {
      const modules = import.meta.glob("./pages/**/*.vue");


      const allRoute = await shared.dynamicRoutes(modules);
      allRoute.forEach((route) => {
        router.addRoute("home", route);
      });
      await startProject(modules);
    }

    app.use(router);



    // =========================
    // Mount app
    // =========================
    app.mount("#app");
  } catch (error) {
    console.error("Boot error:", error);
    const errEl = document.getElementById("error-message");
    if (errEl) errEl.style.display = "block";
    const loader = document.getElementById("loading-wrapper") || document.querySelector(".loader-all");
    if (loader) loader.remove();
  }


  // console.log(`%c QAS system `, "color: white; background-color: #ff4c3b; padding:5px 10px; border-radius: 5px;");
}


export async function startProject(pages) {
  await getProfile();

  const localComponent = import.meta.glob("./components/**/*.vue");


  await addImport(pages);
  await addImport(localComponent);
}
async function addImport(list) {
  try {

    await Promise.all(
    Object.entries(list).map(async ([path, resolver]) => {
      const fileName = path
        .split("/")
        .pop()
        .replace(/\.\w+$/, "");
      const component = await resolver();
      app.component(fileName, component.default);
    }));
  } catch (_) {
    console.error(_);
  }
}


if (typeof window !== "undefined") {
  window.addEventListener("unhandledrejection", (event) => {
    if (
      event?.reason?.message &&
      typeof event.reason.message === "string" &&
      event.reason.message.includes("$el")
    ) {
      event.preventDefault();
      console.warn("Suppressed unhandled $el promise rejection:", event.reason);
    }
  });
}

bootstarApp();
