from rest_framework.routers import DefaultRouter

from academic.apis.institutes.InstituteFieldMVS import InstituteFieldMVS
from academic.apis.institutes.InstituteEducationSystemMVS import InstituteEducationSystemMVS
from academic.apis.institutes.InstituteSpecializationMVS import InstituteSpecializationMVS
from academic.apis.institutes.InstituteLevelMVS import InstituteLevelMVS
from academic.apis.institutes.InstituteSemesterMVS import InstituteSemesterMVS
from academic.apis.institutes.InstituteCurriculumMVS import InstituteCurriculumMVS
from academic.apis.institutes.InstituteSubjectMVS import InstituteSubjectMVS
from academic.apis.institutes.InstituteCurriculumSubjectMVS import InstituteCurriculumSubjectMVS
from academic.apis.institutes.InstituteUnitMVS import InstituteUnitMVS
from academic.apis.institutes.InstituteLessonMVS import InstituteLessonMVS
from academic.apis.institutes.InstituteExamPeriodMVS import InstituteExamPeriodMVS

"""
Institute URL Routes
Configured for vocational/technical institutes, education systems, curricula, and subjects.
"""

router_institutes = DefaultRouter()

# 1. المجالات وأنظمة التعليم والتخصصات
router_institutes.register(r'institutes/fields', InstituteFieldMVS, basename='institute-field')
router_institutes.register(r'institutes/education-systems', InstituteEducationSystemMVS, basename='institute-education-system')
router_institutes.register(r'institutes/specializations', InstituteSpecializationMVS, basename='institute-specialization')

# 2. الهيكل الأكاديمي: المستويات والفصول
router_institutes.register(r'institutes/levels', InstituteLevelMVS, basename='institute-level')
router_institutes.register(r'institutes/semesters', InstituteSemesterMVS, basename='institute-semester')

# 3. المواد والخطط الدراسية
router_institutes.register(r'institutes/subjects', InstituteSubjectMVS, basename='institute-subject')
router_institutes.register(r'institutes/curricula', InstituteCurriculumMVS, basename='institute-curriculum')
router_institutes.register(r'institutes/curriculum-subjects', InstituteCurriculumSubjectMVS, basename='institute-curriculum-subject')

# 4. الوحدات والدروس والامتحانات المهنية للمعاهد
router_institutes.register(r'institute-units', InstituteUnitMVS, basename='institute-unit')
router_institutes.register(r'institutes/units', InstituteUnitMVS, basename='institute-unit-slash')
router_institutes.register(r'institute-lessons', InstituteLessonMVS, basename='institute-lesson')
router_institutes.register(r'institutes/lessons', InstituteLessonMVS, basename='institute-lesson-slash')
router_institutes.register(r'institute-exam-periods', InstituteExamPeriodMVS, basename='institute-exam-period')
router_institutes.register(r'institutes/exam-periods', InstituteExamPeriodMVS, basename='institute-exam-period-slash')

