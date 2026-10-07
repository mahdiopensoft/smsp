from django.urls import path, include
from rest_framework.routers import DefaultRouter

from exams.apis.ExamGenerationSettingMVS import ExamGenerationSettingMVS
from exams.apis.ExamScheduleMVS import ExamScheduleMVS
from exams.apis.ExamMVS import ExamMVS
from exams.apis.ExamVersionMVS import ExamVersionMVS
from exams.apis.ExamQuestionOrderMVS import ExamQuestionOrderMVS
from exams.apis.StudentExamRegistrationMVS import StudentExamRegistrationMVS

from exams.apis.ExamCreateMVS import ExamCreateMVS
from exams.apis.ExamModelsMVS import ExamModelsMVS
from exams.apis.ExamArchiveMVS import ExamArchiveMVS
from exams.apis.ExamQualityReportMVS import ExamQualityReportMVS
from exams.apis.TableOfSpecificationsMVS import TableOfSpecificationsMVS

router = DefaultRouter()

# Dedicated Screen MVS Endpoints
# 1. شاشة توليد اختبار (Exam Creation Wizard Screen)
router.register(r'exam-create', ExamCreateMVS, basename='exam-create')

# 2. شاشة إدارة النماذج (Exam Models Management Screen)
router.register(r'exam-models', ExamModelsMVS, basename='exam-models')

# 3. شاشة أرشيف الاختبارات (Exam Archive Screen)
router.register(r'exam-archive', ExamArchiveMVS, basename='exam-archive')

# 4. شاشة تقرير جودة وأوراق الاختبار (Exam Quality & Papers Report Screen)
router.register(r'exam-quality-report', ExamQualityReportMVS, basename='exam-quality-report')

# 5. شاشة جدول المواصفات (Table of Specifications Screen)
router.register(r'table-of-specifications', TableOfSpecificationsMVS, basename='table-of-specifications')

# 6. شاشة التقرير الإقليمي والجغرافي (Regional Report Screen)
from exams.apis.RegionalReportMVS import RegionalReportMVS
router.register(r'regional-report', RegionalReportMVS, basename='regional-report')


from exams.apis.ExamDistributionMVS import ExamDistributionMVS

# 7. شاشة وخدمات توزيع وتصدير الاختبارات المجدول (Exam Distribution & Scheduled Export)
router.register(r'distributions', ExamDistributionMVS, basename='exam-distribution')

# 8. شاشة المحذوفات من المنهج والمقررات (Curriculum Exclusions Screen)
from exams.apis.CurriculumExclusionMVS import CurriculumExclusionMVS
router.register(r'curriculum-exclusions', CurriculumExclusionMVS, basename='curriculum-exclusion')

# Standard Tables / Auxiliaries
router.register(r'exams', ExamMVS, basename='exam')
router.register(r'exam-generation-settings', ExamGenerationSettingMVS, basename='exam-generation-setting')
router.register(r'exam-schedules', ExamScheduleMVS, basename='exam-schedule')
router.register(r'exam-versions', ExamVersionMVS, basename='exam-version')
router.register(r'exam-question-orders', ExamQuestionOrderMVS, basename='exam-question-order')
router.register(r'student-exam-registrations', StudentExamRegistrationMVS, basename='student-exam-registration')

from exams.apis.ExamExportPackageAPI import ExamExportPackageAPI, ExamExportPackageAckAPI

urlpatterns = [
    path('export/package/', ExamExportPackageAPI.as_view(), name='exam-export-package'),
    path('export/package/ack/', ExamExportPackageAckAPI.as_view(), name='exam-export-package-ack'),
    path('', include(router.urls)),
]
