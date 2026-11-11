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
    // ── OMR Core Direct Routes ──────────────────────────────────────────
    {
      path: "omr-templates",
      name: "omr-templates-direct",
      component: () => import("../pages/OMRSystem/OMRTemplatesView.vue"),
      meta: { requiresAuth: true, title: "مكتبة القوالب وسياسات التصحيح" },
    },
    {
      path: "omr-settings",
      name: "omr-settings-direct",
      component: () => import("../pages/OMRSystem/OMRTemplatesView.vue"),
      meta: { requiresAuth: true, title: "إعدادات وسياسات الذكاء الاصطناعي والتصحيح" },
    },
    {
      path: "omr-template-builder",
      name: "omr-template-builder-direct",
      component: () => import("../pages/OMRSystem/OMRTemplateBuilderView.vue"),
      meta: { requiresAuth: true, title: "مصمم قوالب التصحيح OMR" },
    },
    {
      path: "omr-exams",
      name: "omr-exams-direct",
      component: () => import("../pages/OMRSystem/OMRExamsView.vue"),
      meta: { requiresAuth: true, title: "استلام وتجهيز الاختبارات" },
    },
    {
      path: "omr-print-registry",
      name: "omr-print-registry-direct",
      component: () => import("../pages/OMRSystem/OMRPrintRegistryView.vue"),
      meta: { requiresAuth: true, title: "طباعة أوراق الإجابة" },
    },
    {
      path: "omr-scanner",
      name: "omr-scanner-direct",
      component: () => import("../pages/OMRSystem/OMRScanningView.vue"),
      meta: { requiresAuth: true, title: "المسح والتصحيح الآلي" },
    },
    {
      path: "omr-submissions",
      name: "omr-submissions-direct",
      component: () => import("../pages/OMRSystem/OMRSubmissionsView.vue"),
      meta: { requiresAuth: true, title: "سجل أوراق الإجابة المصححة" },
    },
    {
      path: "omr-gradebook",
      name: "omr-gradebook-direct",
      component: () => import("../pages/OMRSystem/OMRGradebookView.vue"),
      meta: { requiresAuth: true, title: "كشف الدرجات ورصد الكنترول" },
    },
    {
      path: "omr-verification",
      name: "omr-verification-direct",
      component: () => import("../pages/OMRSystem/OMRVerificationView.vue"),
      meta: { requiresAuth: true, title: "التحقق الهندسي والجودة" },
    },
    {
      path: "omr-scanner-lab",
      name: "omr-scanner-lab-direct",
      component: () => import("../pages/OMRSystem/OMRScannerLabView.vue"),
      meta: { requiresAuth: true, title: "مختبر المسح التجريبي" },
    },
    {
      path: "instructions",
      name: "instructions",
      component: shared.InstructionsView,
      meta: { requiresAuth: true },
    },
    {
      path: "exams-create",
      component: () => import("../pages/ExamGenerator/ExamCreateView.vue"),
      meta: { requiresAuth: true, title: "توليد وتعديل الاختبار" },
    },
    {
      path: "ExamGenerator/ExamCreateView",
      component: () => import("../pages/ExamGenerator/ExamCreateView.vue"),
      meta: { requiresAuth: true, title: "توليد وتعديل الاختبار" },
    },
    {
      path: "exams-archive",
      component: () => import("../pages/ExamGenerator/ExamArchiveView.vue"),
      meta: { requiresAuth: true, title: "أرشيف الاختبارات" },
    },
    {
      path: "ExamGenerator/ExamArchiveView",
      component: () => import("../pages/ExamGenerator/ExamArchiveView.vue"),
      meta: { requiresAuth: true, title: "أرشيف الاختبارات" },
    },
    {
      path: "curriculum-exclusions",
      name: "curriculum-exclusions",
      component: () => import("../pages/ExamGenerator/CurriculumExclusionsView.vue"),
      meta: { requiresAuth: true, title: "المحذوفات من المنهج" },
    },
    {
      path: "ExamGenerator/CurriculumExclusionsView",
      component: () => import("../pages/ExamGenerator/CurriculumExclusionsView.vue"),
      meta: { requiresAuth: true, title: "المحذوفات من المنهج" },
    },
    {
      path: "question-bank-import",
      name: "question-bank-import",
      component: () => import("../pages/QuestionBank/QuestionImportView.vue"),
      meta: { requiresAuth: true, title: "استيراد بنك الأسئلة" },
    },
    {
      path: "QuestionBank/QuestionImportView",
      component: () => import("../pages/QuestionBank/QuestionImportView.vue"),
      meta: { requiresAuth: true, title: "استيراد بنك الأسئلة" },
    },
    // تقارير النظام (Reports)
    {
      path: "reports-exam-quality",
      name: "reports-exam-quality",
      component: () => import("../pages/Reports/ExamPapersReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير جودة الاختبار" },
    },
    {
      path: "reports-authors",
      name: "reports-authors",
      component: () => import("../pages/Reports/AuthorsReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير أداء المؤلفين" },
    },
    {
      path: "reports-curriculum",
      name: "reports-curriculum",
      component: () => import("../pages/Reports/CurriculumReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير التغطية الأكاديمية" },
    },
    {
      path: "reports-bank-status",
      name: "reports-bank-status",
      component: () => import("../pages/Reports/BankStatusReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير حالة بنك الأسئلة" },
    },
    {
      path: "reports-alignment-matrix",
      name: "reports-alignment-matrix",
      component: () => import("../pages/Reports/AlignmentMatrixReportView.vue"),
      meta: { requiresAuth: true, title: "مصفوفة المواءمة الأكاديمية" },
    },
    {
      path: "reports-regional",
      name: "reports-regional",
      component: () => import("../pages/Reports/RegionalReportView.vue"),
      meta: { requiresAuth: true, title: "التقرير الإقليمي والجغرافي" },
    },
    {
      path: "reports-questions-detail",
      name: "reports-questions-detail",
      component: () => import("../pages/Reports/QuestionsDetailReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير الأسئلة التفصيلي" },
    },
    {
      path: "reports-rejected-questions",
      name: "reports-rejected-questions",
      component: () => import("../pages/Reports/RejectedQuestionsReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير الأسئلة المرفوضة" },
    },
    {
      path: "reports-exams-generated",
      name: "reports-exams-generated",
      component: () => import("../pages/Reports/ExamsGeneratedReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير الاختبارات المولدة" },
    },
    {
      path: "reports-exam-distribution",
      name: "reports-exam-distribution",
      component: () => import("../pages/Reports/ExamDistributionReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير توزيع وإرسال الاختبارات" },
    },
    {
      path: "reports-curriculum-exclusions",
      name: "reports-curriculum-exclusions",
      component: () => import("../pages/Reports/CurriculumExclusionsReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير المحذوفات من المنهج" },
    },
    {
      path: "reports-student-registrations",
      name: "reports-student-registrations",
      component: () => import("../pages/Reports/StudentRegistrationsReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير تسجيلات الطلاب" },
    },
    {
      path: "reports-students",
      name: "reports-students",
      component: () => import("../pages/Reports/StudentsReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير الطلاب" },
    },
    {
      path: "reports-omr-results",
      name: "reports-omr-results",
      component: () => import("../pages/Reports/OMRResultsReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير نتائج التصحيح الآلي" },
    },
    {
      path: "reports-omr-review",
      name: "reports-omr-review",
      component: () => import("../pages/Reports/OMRReviewQuestionsReportView.vue"),
      meta: { requiresAuth: true, title: "تقرير أسئلة مراجعة التصحيح" },
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
