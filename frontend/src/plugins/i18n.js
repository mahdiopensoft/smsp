// <!-- added by samer -->

import {
  createI18n
} from "vue-i18n";
import shared from "external-components";
import arMessages from "@/locales/ar.json";
import enMessages from "@/locales/en.json";


import arDServices from "@/locales/d_services/ar.json";
import enDServices from "@/locales/d_services/en.json";




const messages = {
  ar: {

    ...arMessages,
    ...arDServices,
  }, // Use the messages from ar.js for Arabic
  en: {

    ...enMessages,
    ...enDServices,
  }, // Use the messages from en.js for English
}

const i18n = createI18n({
  locale: 'ar', // Default locale
  fallbackLocale: 'en', // Fallback locale
  messages
});

export default i18n;
