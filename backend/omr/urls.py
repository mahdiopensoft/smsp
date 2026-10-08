from django.urls import path, include
from rest_framework.routers import DefaultRouter

from omr.apis.OMRSheetResultMVS import OMRSheetResultMVS
from omr.apis.OMRQuestionResultMVS import OMRQuestionResultMVS
from omr.apis.OMRHumanReviewMVS import OMRHumanReviewMVS
from omr.apis.OMRFullExtractionMVS import OMRFullExtractionMVS
from omr.apis.OMRScannerLabMVS import OMRScannerLabMVS
from omr.apis.OMRBubbleSheetsMVS import OMRBubbleSheetsMVS
from omr.apis.OMRTemplatesMVS import OMRTemplatesMVS
from omr.apis.ExamLinkingMVS import ExamLinkingMVS
from omr.apis.ExamGradebookMVS import ExamGradebookMVS
from omr.apis.OMRPrintRegistryMVS import OMRPrintRegistryMVS
from omr.apis.OMRVerificationMVS import OMRVerificationMVS

from omr.api import grade_sheet, get_result, get_annotated_image, detect_template_api

router = DefaultRouter()

# 0. شاشة سجل درجات الاختبارات والترحيل لنظام الكنترول (Exam Gradebook & Control Dispatch)
router.register(r'gradebook', ExamGradebookMVS, basename='gradebook')

# Dedicated Screen MVS Endpoints
# 1. شاشة المراجعة البشرية والتدقيق (Human Review Screen)
router.register(r'human-review', OMRHumanReviewMVS, basename='human-review')

# 2. شاشة الاستخراج الكامل (OMR Full Extraction Screen)
router.register(r'omr-extraction', OMRFullExtractionMVS, basename='omr-extraction')

# 3. شاشة المختبر والمسح (OMR Scanner Lab Screen)
router.register(r'omr-scanner', OMRScannerLabMVS, basename='omr-scanner')

# 4. شاشة أوراق الإجابة ومكتبة القوالب (OMR Bubble Sheets CAD Screen)
router.register(r'omr-bubble-sheets', OMRBubbleSheetsMVS, basename='omr-bubble-sheets')

# 5. شاشة تصميم القوالب الهندسية (OMR Templates Designer Screen)
router.register(r'omr-templates', OMRTemplatesMVS, basename='omr-templates')

# 6. شاشة ربط الاختبارات والتصحيح الضوئي (Exams OMR Linking Screen)
router.register(r'exam-linking', ExamLinkingMVS, basename='exam-linking')

# 7. شاشة سجل الطباعة (Print Registry Screen)
router.register(r'print-registry', OMRPrintRegistryMVS, basename='print-registry')

# 8. شاشة المطابقة والتحقق (Verification Screen)
router.register(r'verification', OMRVerificationMVS, basename='verification')

# Standard Tables
router.register(r'omr-sheet-results', OMRSheetResultMVS, basename='omr-sheet-result')
router.register(r'omr-question-results', OMRQuestionResultMVS, basename='omr-question-result')

urlpatterns = [
    # ─── Direct OpenCV/SVG OMR Engine Endpoints ──────────────────────────────
    path('detect-template/', detect_template_api, name='omr-detect-template'),
    path('grade/', grade_sheet, name='omr-grade'),
    path('results/<str:result_id>/', get_result, name='omr-result'),
    path('annotated/<str:result_id>/', get_annotated_image, name='omr-annotated'),
    path('', include(router.urls)),
]
