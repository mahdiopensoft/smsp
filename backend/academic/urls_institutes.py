from rest_framework.routers import DefaultRouter

from academic.apis.institutes.InstituteFieldMVS import InstituteFieldMVS
from academic.apis.institutes.InstituteEducationSystemMVS import InstituteEducationSystemMVS
from academic.apis.institutes.InstituteSpecializationMVS import InstituteSpecializationMVS
from academic.apis.institutes.InstituteLevelMVS import InstituteLevelMVS
from academic.apis.institutes.InstituteSemesterMVS import InstituteSemesterMVS
from academic.apis.institutes.InstituteCurriculumMVS import InstituteCurriculumMVS
from academic.apis.institutes.InstituteBatchMVS import InstituteBatchMVS
from academic.apis.institutes.InstituteSubjectMVS import InstituteSubjectMVS
from academic.apis.institutes.InstituteCurriculumSubjectMVS import InstituteCurriculumSubjectMVS
from academic.apis.institutes.InstituteShortCourseMVS import InstituteShortCourseMVS
from academic.apis.institutes.InstituteAdmissionRequirementMVS import InstituteAdmissionRequirementMVS
from academic.apis.institutes.InstituteSpecialTrackMVS import InstituteSpecialTrackMVS

"""
Institute URL Routes
Configured for vocational/technical institutes, education systems, curricula, and courses.
"""

router_institutes = DefaultRouter()

# 1. المجالات وأنظمة التعليم والتخصصات
router_institutes.register(r'institutes/fields', InstituteFieldMVS, basename='institute-field')
router_institutes.register(r'institutes/education-systems', InstituteEducationSystemMVS, basename='institute-education-system')
router_institutes.register(r'institutes/specializations', InstituteSpecializationMVS, basename='institute-specialization')

# 2. شروط القبول والمسارات الخاصة
router_institutes.register(r'institutes/admission-requirements', InstituteAdmissionRequirementMVS, basename='institute-admission-requirement')
router_institutes.register(r'institutes/special-tracks', InstituteSpecialTrackMVS, basename='institute-special-track')

# 3. الهيكل الأكاديمي: المستويات والفصول والدفعات
router_institutes.register(r'institutes/levels', InstituteLevelMVS, basename='institute-level')
router_institutes.register(r'institutes/semesters', InstituteSemesterMVS, basename='institute-semester')
router_institutes.register(r'institutes/batches', InstituteBatchMVS, basename='institute-batch')

# 4. المواد والخطط الدراسية
router_institutes.register(r'institutes/subjects', InstituteSubjectMVS, basename='institute-subject')
router_institutes.register(r'institutes/curricula', InstituteCurriculumMVS, basename='institute-curriculum')
router_institutes.register(r'institutes/curriculum-subjects', InstituteCurriculumSubjectMVS, basename='institute-curriculum-subject')

# 5. الدورات التدريبية القصيرة
router_institutes.register(r'institutes/short-courses', InstituteShortCourseMVS, basename='institute-short-course')
