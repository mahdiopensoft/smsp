from rest_framework.routers import DefaultRouter

from academic.apis.institutes.InstituteFieldMVS import InstituteFieldMVS
from academic.apis.institutes.InstituteEducationSystemMVS import InstituteEducationSystemMVS
from academic.apis.institutes.InstituteSpecializationMVS import InstituteSpecializationMVS
from academic.apis.institutes.InstituteLevelMVS import InstituteLevelMVS
from academic.apis.institutes.InstituteSemesterMVS import InstituteSemesterMVS
from academic.apis.institutes.InstituteCurriculumMVS import InstituteCurriculumMVS
from academic.apis.institutes.InstituteSubjectMVS import InstituteSubjectMVS
from academic.apis.institutes.InstituteCurriculumSubjectMVS import InstituteCurriculumSubjectMVS

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

