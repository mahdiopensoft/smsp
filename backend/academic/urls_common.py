from rest_framework.routers import DefaultRouter

from academic.apis.common.CurriculumReportMVS import CurriculumReportMVS
from academic.apis.common.AlignmentMatrixReportMVS import AlignmentMatrixReportMVS
from academic.apis.common.OrganizationMVS import OrganizationMVS
from academic.apis.common.AcademicYearMVS import AcademicYearMVS
from academic.apis.common.SubjectMVS import SubjectMVS
from academic.apis.common.UnitMVS import UnitMVS
from academic.apis.common.LessonMVS import LessonMVS
from academic.apis.common.LearningOutcomeMVS import LearningOutcomeMVS
from academic.apis.common.ExamPeriodMVS import ExamPeriodMVS
from academic.apis.common.StudentMVS import StudentMVS

router_common = DefaultRouter()

# تقارير المناهج والمواءمة المشتركة (Curriculum & Matrix Reports)
router_common.register(r'curriculum-report', CurriculumReportMVS, basename='curriculum-report')
router_common.register(r'alignment-matrix-report', AlignmentMatrixReportMVS, basename='alignment-matrix-report')

# الكيانات الأكاديمية العامة (Core Academics)
router_common.register(r'organizations', OrganizationMVS, basename='organization')
router_common.register(r'academic-years', AcademicYearMVS, basename='academic-year')
router_common.register(r'subjects', SubjectMVS, basename='subject')
router_common.register(r'units', UnitMVS, basename='unit')
router_common.register(r'lessons', LessonMVS, basename='lesson')
router_common.register(r'learning-outcomes', LearningOutcomeMVS, basename='learning-outcome')
router_common.register(r'exam-periods', ExamPeriodMVS, basename='exam-period')

# الطلاب (Students)
router_common.register(r'students', StudentMVS, basename='student')
