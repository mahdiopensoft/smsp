from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bank.apis.ImportSessionMVS import ImportSessionMVS
from bank.apis.QuestionMVS import QuestionMVS
from bank.apis.QuestionNewMVS import QuestionNewMVS
from bank.apis.QuestionFastEntryMVS import QuestionFastEntryMVS
from bank.apis.QuestionImportMVS import QuestionImportMVS
from bank.apis.QuestionBulkCompleteMVS import QuestionBulkCompleteMVS
from bank.apis.QuestionDiffMVS import QuestionDiffMVS
from bank.apis.QuestionReviewMVS import QuestionReviewMVS
from bank.apis.DashboardMVS import DashboardMVS
from bank.apis.AuthorsReportMVS import AuthorsReportMVS
from bank.apis.BankStatusReportMVS import BankStatusReportMVS
from bank.apis.AuditLogMVS import AuditLogMVS
from bank.apis.AnswerMVS import AnswerMVS

router = DefaultRouter()

# 1. شاشة لوحة التحكم الرئيسية (Main Dashboard Screen)
router.register(r'dashboard', DashboardMVS, basename='dashboard')

# 2. شاشة بنك الأسئلة (Question Bank Screen)
router.register(r'questions', QuestionMVS, basename='question')

# 3. شاشة إضافة وتعديل سؤال جديد (Question Create & Edit Screen)
router.register(r'question-new', QuestionNewMVS, basename='question-new')

# 4. شاشة الإدخال السريع للأسئلة (Question Fast Entry Screen)
router.register(r'question-fast-entry', QuestionFastEntryMVS, basename='question-fast-entry')

# 5. شاشة استيراد من إكسل واستكمال البيانات (Excel Import & Bulk Complete)
router.register(r'question-import', QuestionImportMVS, basename='question-import')
router.register(r'bulk-complete', QuestionBulkCompleteMVS, basename='bulk-complete')

# 6. شاشة مقارنة النسخ (Question Diff View)
router.register(r'question-diff', QuestionDiffMVS, basename='question-diff')

# 7. شاشة طابور المراجعة (Question Review Queue Screen)
router.register(r'question-review', QuestionReviewMVS, basename='question-review')

# 8. شاشة تقرير أداء المؤلفين (Authors Performance Report Screen)
router.register(r'authors-report', AuthorsReportMVS, basename='authors-report')

# 9. شاشة تقرير حالة البنك والمستويات (Bank Status Report Screen)
router.register(r'bank-status-report', BankStatusReportMVS, basename='bank-status-report')

# 10. سجل الرقابة والتدقيق (Audit Logs)
router.register(r'audit-logs', AuditLogMVS, basename='audit-log')

# Auxiliaries
router.register(r'answers', AnswerMVS, basename='answer')
router.register(r'import-sessions', ImportSessionMVS, basename='import-session')

urlpatterns = [
    path('', include(router.urls)),
]
