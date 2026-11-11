import { defineStore } from "pinia";
import api from "../../plugins/axios-plugin";
import { state } from "@/store/state";
 const profile = state?.profile;

export const useHeaderFooterStore = defineStore("headerFooter", {
  state: () => ({
    localVariables: [
      {
        name_ar: "اسم المستخدم",
        name_en: "user name",
        value: profile?.first_name + " " + profile?.last_name,
      },
      {
        name_ar: "اسم المنظمة",
        name_en: "Organization name",
      },
      {
        name_ar: "شعار المنظمة",
        name_en: "Organization logo",
      },
      { name_ar: "البريد الالكتروني", name_en: "email" },
      { name_ar: "التاريخ الحالي", name_en: "Current date" },
      { name_ar: "الوقت الحالي", name_en: "Current time" },
      { name_ar: "التاريخ والوقت الحالي", name_en: "Current date and time" },
      { name_ar: "عنوان الشاشة", name_en: "Screen title" },
    ],
    listVariables: null,
    status: false,
    headerFooterData:{}
  }),

  getters: {
    variables: (state) => state.listVariables,
  },

  actions: {
    async getVariables() {
      try {
        const response = await api.get(
          "common/environment-variables-r/all/",
          {
            skipInterceptor: true,
          }
        );
        let data = {};
        const res = response?.data?.data || response?.data?.results || response?.data || [];
        const items = Array.isArray(res) ? res : (Array.isArray(res?.results) ? res.results : []);

        items.forEach((e) => {
          if (e && e.name) {
            data[e.name] = e;
          }
        });
        this.listVariables = data;
        this.status = true;
      } catch (err) {
        console.warn("Failed to load environment variables:", err);
        this.listVariables = {};
        this.status = true;
      }
    },
    async changeHeaderFooter  (
        data = {
          fk_screen: undefined,
          fk_print_report_setting: undefined,
        }
      ) {
      
       
        const url = data.fk_screen
          ? "screens/screen/get-print-report-setting/?fk_screen=" + data.fk_screen
          : "common/print-report-setting/" + data.fk_print_report_setting + "/";

        const response = await api(url);
        const res = response.data.data || response.data;
        if (res?.id) {
          this.headerFooterData = res;
          state.header_footer = res;
          
        } else {
          this.headerFooterData = null;
          state.header_footer = null;
        }
      }
  },
});
