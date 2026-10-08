// Plugins
import Components from "unplugin-vue-components/vite";
import Vue from "@vitejs/plugin-vue";
import Vuetify, { transformAssetUrls } from "vite-plugin-vuetify";
import ViteFonts from "unplugin-fonts/vite";
import VueRouter from "unplugin-vue-router/vite";
import path from "path";


// Utilities
import { defineConfig } from "vite";
import { fileURLToPath, URL } from "node:url";
import settings from "./settings";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    VueRouter(),
    Vue({
      template: { transformAssetUrls },
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/master/packages/vite-plugin#readme
    Vuetify({
      autoImport: true,
      styles: {
        configFile: "src/styles/settings.scss",
      },
    }),
    Components(),
    ViteFonts({
      google: {
        families: [
          {
            name: "Roboto",
            styles: "wght@100;300;400;500;700;900",
          },
        ],
      },
    }),
  ],
  define: { "process.env": {} },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "external-components": path.resolve("C:/Users/ibrahim/Desktop/ibrahim/2026/portal/frontend/src/shared-project-v4/index.js"),
      "datalist": path.resolve('./src/utils/DataAutoList'),
      "headers": path.resolve("./src/utils/Headers.js"),
      "crypto-js": path.resolve("./node_modules/crypto-js"),
      "lodash": path.resolve("./node_modules/lodash"),
      "pinia": path.resolve("./node_modules/pinia"),
      "vue": path.resolve("./node_modules/vue"),
    },
    dedupe: ["vue", "vuetify", "crypto-js", "lodash", "axios", "pinia"],
    extensions: [".js", ".json", ".jsx", ".mjs", ".ts", ".tsx", ".vue"],
  },
  server: {
    port: settings.port,
    fs: {
      allow: [
        ".",
        "C:/Users/ibrahim/Desktop/ibrahim/2026/portal/frontend/src/shared-project-v4",
      ],
    },
  },
});
