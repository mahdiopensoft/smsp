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
      name: "omr",
      component: () => import("../pages/OMRSystem/OMRScannerLabView.vue"),
      meta: { requiresAuth: true, title: "نظام التصحيح الضوئي (OMR)" },
    },
    {
      path: "omr/scanner-lab",
      name: "omr-scanner-lab",
      component: () => import("../pages/OMRSystem/OMRScannerLabView.vue"),
      meta: { requiresAuth: true, title: "مختبر التصحيح الضوئي (OMR)" },
    },
    {
      path: "omr/scanner",
      name: "omr-scanner",
      component: () => import("../pages/OMRSystem/OMRScannerLabView.vue"),
      meta: { requiresAuth: true, title: "مختبر التصحيح والمسح (OMR)" },
    },
    {
      path: "omr-workflow",
      name: "omr-workflow",
      redirect: "/omr/scanner-lab",
    },
    {
      path: "omr/dashboard",
      name: "omr-dashboard",
      component: () => import("../pages/OMRSystem/OMRDashboardView.vue"),
      meta: { requiresAuth: true, title: "لوحة تحكم التصحيح الضوئي (OMR)" },
    },
    {
      path: "omr/exams",
      name: "omr-exams",
      component: () => import("../pages/OMRSystem/OMRExamsView.vue"),
      meta: { requiresAuth: true, title: "ربط الاختبارات والتصحيح الضوئي (OMR)" },
    },
    {
      path: "omr-exams",
      name: "omr-exams-alias",
      redirect: "/omr/exams",
    },
    {
      path: "omr/template-builder",
      name: "omr-template-builder",
      component: () => import("../pages/OMRSystem/OMRTemplateBuilderView.vue"),
      meta: { requiresAuth: true, title: "مصمم قوالب التصحيح (OMR)" },
    },
    {
      path: "omr/templates",
      name: "omr-templates",
      component: () => import("../pages/OMRSystem/OMRTemplatesView.vue"),
      meta: { requiresAuth: true, title: "قوالب ونماذج التصحيح (OMR)" },
    },
    {
      path: "omr/submissions",
      name: "omr-submissions",
      component: () => import("../pages/OMRSystem/OMRSubmissionsView.vue"),
      meta: { requiresAuth: true, title: "سجل أوراق الإجابة المصححة" },
    },
    {
      path: "submissions",
      name: "submissions-alias",
      redirect: "/omr/submissions",
    },
    {
      path: "omr/submissions/:id",
      name: "omr-submission-detail",
      component: () => import("../pages/OMRSystem/OMRSubmissionDetailView.vue"),
      meta: { requiresAuth: true, title: "تفاصيل ورقة الإجابة والتصحيح" },
      props: true,
    },
    {
      path: "submissions/:id",
      name: "submission-detail-alias",
      redirect: (to) => `/omr/submissions/${to.params.id}`,
    },
    {
      path: "omr/bubble-sheets",
      name: "omr-bubble-sheets",
      component: () => import("../pages/OMRSystem/OMRBubbleSheetsView.vue"),
      meta: { requiresAuth: true, title: "توليد وطباعة أوراق البابل شيت" },
    },
    {
      path: "omr/full-extraction",
      name: "omr-full-extraction",
      component: () => import("../pages/OMRSystem/OMRFullExtractionView.vue"),
      meta: { requiresAuth: true, title: "استخراج وتصدير بيانات OMR" },
    },
    {
      path: "omr/extraction",
      name: "omr-extraction",
      component: () => import("../pages/OMRSystem/OMRFullExtractionView.vue"),
      meta: { requiresAuth: true, title: "الاستخراج الكامل (OMR)" },
    },
    {
      path: "omr/human-review",
      name: "omr-human-review",
      component: () => import("../pages/OMRSystem/OMRHumanReviewView.vue"),
      meta: { requiresAuth: true, title: "المراجعة البشرية (OMR)" },
    },
    {
      path: "omr-human-review",
      name: "omr-human-review-alias",
      redirect: "/omr/human-review",
    },
    {
      path: "human-review",
      name: "human-review-direct-alias",
      redirect: "/omr/human-review",
    },
    {
      path: "omr-dashboard",
      name: "omr-dashboard-alias",
      redirect: "/omr/dashboard",
    },
    {
      path: "omr-submissions",
      name: "omr-submissions-alias",
      redirect: "/omr/submissions",
    },
    {
      path: "omr-submissions/:id",
      name: "omr-submissions-id-alias",
      redirect: (to) => `/omr/submissions/${to.params.id}`,
    },
    {
      path: "omr-scanner",
      name: "omr-scanner-alias",
      redirect: "/omr/scanner",
    },
    {
      path: "omr-extraction",
      name: "omr-extraction-alias",
      redirect: "/omr/extraction",
    },
    {
      path: "omr-templates",
      name: "omr-templates-alias",
      redirect: "/omr/templates",
    },
    {
      path: "omr/demo",
      name: "omr-demo",
      component: () => import("../pages/OMRSystem/OMRDemoView.vue"),
      meta: { requiresAuth: true, title: "العرض التجريبي لـ OMR" },
    },
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
