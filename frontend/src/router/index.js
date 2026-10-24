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
    component: shared.SystemSelector,
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
    {
      path: "omr-submissions/:id",
      name: "omr-submission-detail-path",
      component: () => import("../pages/OMRSystem/OMRSubmissionDetailView.vue"),
      meta: { requiresAuth: true, title: "تفاصيل تصحيح ورقة الإجابة" },
      props: true,
    },
    {
      path: "omr-submission-detail/:id",
      name: "omr-submission-detail-alias",
      component: () => import("../pages/OMRSystem/OMRSubmissionDetailView.vue"),
      meta: { requiresAuth: true, title: "تفاصيل تصحيح ورقة الإجابة" },
      props: true,
    },
    {
      path: "omr-submission-detail",
      name: "omr-submission-detail-query",
      component: () => import("../pages/OMRSystem/OMRSubmissionDetailView.vue"),
      meta: { requiresAuth: true, title: "تفاصيل تصحيح ورقة الإجابة" },
      props: true,
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
