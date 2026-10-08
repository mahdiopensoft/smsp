// <!-- added by samer -->

import { createRouter, createWebHistory } from "vue-router/auto";

import shared from "external-components";
import LogIn from "@/pages/UserManagment/LogIn/LogIn.vue";
import index from "../pages/index.vue";
import DashBoard from "../pages/DashBoard/DashBoard.vue";
import settings from "../../settings";

const routes = [
  {
    path: settings.multiple_company ? "/:company/login" : "/login",
    name: "Login",
    component: LogIn,
    meta: { quest: true, title: "تسجيل الدخول" },
  },
  {
    path: "/sso-login",
    name: "SSOLogin",
    component: shared.SSOLoginPage,
    meta: { quest: true, title: "تسجيل الدخول - المنصة الموحدة" },
  },

  {
    path: "/sso/callback",
    name: "SSOCallback",
    component: shared.SSOCallback,
    meta: { quest: true, title: "جاري المعالجة..." },
  },
  {
    path: "/auth/callback",
    name: "AuthCallback",
    component: shared.AuthCallback,
    meta: { quest: true, title: "جاري التحقق..." },
  },
  {
    path: "/auth/error",
    name: "AuthError",
    component: shared.AuthError,
    meta: { quest: true, title: "خطأ في المصادقة" },
  },
  {
    path: "/logout-success",
    name: "LogoutSuccess",
    component: shared.LogoutSuccess,
    meta: { quest: true, title: "تم تسجيل الخروج" },
  },
  {
    path: "/system-selector",
    name: "SystemSelector",
    component: shared.SystemSelector,
    meta: { requiresAuth: true, title: "اختيار الانظمة", requiresSSO: true },
  },
  {
    path: "/index",
    name: "Index",
    component: shared.SystemInfo,
    meta: { requiresAuth: true, title: "عرض الانظمة" },
  },
];

var routes_paths = {
  path: "/",
  name: "home",
  component: index,
  redirect: { name: "screen" },
  props: {
    name_ar: "الرئيسية",
    name_en: "home",
  },
  children: [
    {
      path: "/",
      name: "dash-board",
      component: DashBoard,
      meta: { requiresAuth: true },
    },
    {
      path: "screen",
      name: "screen",

      component: DashBoard,
      meta: { requiresAuth: true },
    },
    {
      path: "screen-view",
      name: "screen-view",
      component: shared.ScreenView,

      meta: { requiresAuth: true },
    },
    {
      path: "service-details/:id",
      name: "service-details",
      component: () => import("../pages/Services/Service/ServiceDetails.vue"),
      meta: { requiresAuth: true },
      props: true,
    },
    // ── OMR System Routes ─────────────────────────────────────────
    {
      path: "omr",
      name: "omr-redirect",
      redirect: "/omr-dashboard",
    },
    // 0. لوحة التحكم
    {
      path: "omr-dashboard",
      name: "omr-dashboard",
      component: () => import("../pages/OMRSystem/OMRDashboardView.vue"),
      meta: { requiresAuth: true, title: "لوحة تحكم التصحيح الضوئي (OMR)" },
    },
    {
      path: "omr/dashboard",
      redirect: (to) => ({ path: "/omr-dashboard", query: to.query }),
    },

    // 1. استلام الاختبارات
    {
      path: "omr-exams",
      name: "omr-exams",
      component: () => import("../pages/OMRSystem/OMRExamsView.vue"),
      meta: { requiresAuth: true, title: "استلام الاختبارات (OMR)" },
    },
    {
      path: "omr/exams",
      redirect: (to) => ({ path: "/omr-exams", query: to.query }),
    },

    // 2. تصميم القالب ومصمم القوالب
    {
      path: "omr-template-builder",
      name: "omr-template-builder",
      component: () => import("../pages/OMRSystem/OMRTemplateBuilderView.vue"),
      meta: { requiresAuth: true, title: "مصمم قوالب التصحيح (OMR)" },
    },
    {
      path: "omr/template-builder",
      redirect: (to) => ({ path: "/omr-template-builder", query: to.query }),
    },
    {
      path: "omr-templates",
      name: "omr-templates",
      component: () => import("../pages/OMRSystem/OMRTemplatesView.vue"),
      meta: { requiresAuth: true, title: "إدارة القوالب (OMR)" },
    },
    {
      path: "omr/templates",
      redirect: (to) => ({ path: "/omr-templates", query: to.query }),
    },

    // 3. الطباعة وسجل التصدير
    {
      path: "omr-print-registry",
      name: "omr-print-registry",
      component: () => import("../pages/OMRSystem/OMRPrintRegistryView.vue"),
      meta: { requiresAuth: true, title: "سجل الطباعة وتصدير الأوراق (OMR)" },
    },
    {
      path: "omr/print-registry",
      redirect: (to) => ({ path: "/omr-print-registry", query: to.query }),
    },

    // 4. معمل المسح الضوئي
    {
      path: "omr-scanner-lab",
      name: "omr-scanner-lab",
      component: () => import("../pages/OMRSystem/OMRScannerLabView.vue"),
      meta: { requiresAuth: true, title: "مختبر المسح الضوئي (OMR)" },
    },
    {
      path: "omr/scanner-lab",
      redirect: (to) => ({ path: "/omr-scanner-lab", query: to.query }),
    },

    // 5. المطابقة والتحقق (الأوراق المفقودة)
    {
      path: "omr-verification",
      name: "omr-verification",
      component: () => import("../pages/OMRSystem/OMRVerificationView.vue"),
      meta: { requiresAuth: true, title: "المطابقة والتحقق من الأوراق" },
    },
    {
      path: "omr/verification",
      redirect: (to) => ({ path: "/omr-verification", query: to.query }),
    },

    // 6. سجل الأوراق الممسوحة والمراجعة البشرية
    {
      path: "omr-submissions",
      name: "omr-submissions",
      component: () => import("../pages/OMRSystem/OMRSubmissionsView.vue"),
      meta: { requiresAuth: true, title: "سجل الأوراق الممسوحة" },
    },
    {
      path: "omr/submissions",
      redirect: (to) => ({ path: "/omr-submissions", query: to.query }),
    },
    {
      path: "omr-submissions/:id",
      name: "omr-submission-detail",
      component: () => import("../pages/OMRSystem/OMRSubmissionDetailView.vue"),
      meta: { requiresAuth: true, title: "تفاصيل ورقة الإجابة والتصحيح" },
      props: true,
    },
    {
      path: "omr/submissions/:id",
      redirect: (to) => ({ path: `/omr-submissions/${to.params.id}`, query: to.query }),
    },
    {
      path: "omr-human-review",
      name: "omr-human-review",
      component: () => import("../pages/OMRSystem/OMRHumanReviewView.vue"),
      meta: { requiresAuth: true, title: "المراجعة البشرية (OMR)" },
    },
    {
      path: "omr/human-review",
      redirect: (to) => ({ path: "/omr-human-review", query: to.query }),
    },

    // 7. سجل الدرجات والترحيل
    {
      path: "omr-gradebook",
      name: "omr-gradebook",
      component: () => import("../pages/OMRSystem/OMRGradebookView.vue"),
      meta: { requiresAuth: true, title: "سجل درجات الاختبارات والترحيل (OMR)" },
    },
    {
      path: "omr/gradebook",
      redirect: (to) => ({ path: "/omr-gradebook", query: to.query }),
    },

    // أدوات إضافية (Demo & Extraction)
    {
      path: "omr-full-extraction",
      name: "omr-full-extraction",
      component: () => import("../pages/OMRSystem/OMRFullExtractionView.vue"),
      meta: { requiresAuth: true, title: "الاستخراج الكامل (OMR)" },
    },
    {
      path: "omr/full-extraction",
      redirect: (to) => ({ path: "/omr-full-extraction", query: to.query }),
    },
    {
      path: "omr-demo",
      name: "omr-demo",
      component: () => import("../pages/OMRSystem/OMRDemoView.vue"),
      meta: { requiresAuth: true, title: "العرض التجريبي لـ OMR" },
    },
    {
      path: "omr/demo",
      redirect: (to) => ({ path: "/omr-demo", query: to.query }),
    },

    // Aliases to support all old/alternative links
    { path: "omr-workflow", redirect: (to) => ({ path: "/omr-scanner-lab", query: to.query }) },
    { path: "submissions", redirect: (to) => ({ path: "/omr-submissions", query: to.query }) },
    { path: "submissions/:id", redirect: (to) => ({ path: `/omr-submissions/${to.params.id}`, query: to.query }) },
    { path: "gradebook", redirect: (to) => ({ path: "/omr-gradebook", query: to.query }) },
    { path: "human-review", redirect: (to) => ({ path: "/omr-human-review", query: to.query }) },
    { path: "omr-scanner", redirect: (to) => ({ path: "/omr-scanner-lab", query: to.query }) },
    { path: "omr-extraction", redirect: (to) => ({ path: "/omr-full-extraction", query: to.query }) },
    { path: "omr-bubble-sheets", redirect: (to) => ({ path: "/omr-templates", query: to.query }) },
    {
      path: "instructions",
      name: "instructions",
      component: shared.InstructionsView,
      meta: { requiresAuth: true },
    },
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      component: DashBoard,
    },
  ],
};

const router = createRouter({
  history: createWebHistory(),
  routes: [...routes, routes_paths],
});

shared.routers(router);

export default router;
