import axios from "axios";
import { reactive } from "vue";

const storedTheme = JSON.parse(localStorage.getItem("theme")) || { id: 1, name_en: "lightTheme", name_ar: "فاتح" };
const profile = JSON.parse(localStorage.getItem("profile")) || {};
const is_super_user = JSON.parse(localStorage.getItem("su")) || {};


export const state = reactive({
  url: "",
  theme: storedTheme,
  alert: false,
  snack: false,
  alert_details: {},
  protected_records: false,
  message_protected_records: [],
  page: {},
  is_dropList: false,
  print: false,
  current_year: {},
  permissions: {},
  unread_news: [],
  unread_generalization: [],
  unread_occasion: [],
  profile: profile,
  notifications_count: undefined,

  isAuthenticated: false,
  is_super_user: is_super_user,
  autolist_data: {},
  profile: profile,
  fk_brunch: profile.ip,
  company_level: profile.zi,
  organization_id: undefined,
  year: undefined,
  current_system: null,
  isPlatFormSys: true,

  isSSO: false,


});



export default state


