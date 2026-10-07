from rest_framework.routers import DefaultRouter

from academic.apis.schools.SchoolStageMVS import SchoolStageMVS
from academic.apis.schools.SchoolLevelMVS import SchoolLevelMVS
from academic.apis.schools.SchoolTrackMVS import SchoolTrackMVS
from academic.apis.schools.SchoolClassTrackMVS import SchoolClassTrackMVS
from academic.apis.schools.SchoolClassSubjectMVS import SchoolClassSubjectMVS
from academic.apis.schools.SchoolSubjectMVS import SchoolSubjectMVS
from academic.apis.schools.SchoolUnitMVS import SchoolUnitMVS
from academic.apis.schools.SchoolLessonMVS import SchoolLessonMVS
from academic.apis.schools.SchoolLearningOutcomeMVS import SchoolLearningOutcomeMVS
from academic.apis.schools.SchoolSectionMVS import SchoolSectionMVS

router_schools = DefaultRouter()

# مسارات الهيكل المدرسي (School Hierarchy)
router_schools.register(r'educational-stages', SchoolStageMVS, basename='educational-stage')
router_schools.register(r'levels', SchoolLevelMVS, basename='level')
router_schools.register(r'tracks', SchoolTrackMVS, basename='track')
router_schools.register(r'class-tracks', SchoolClassTrackMVS, basename='class-track')
router_schools.register(r'class-subjects', SchoolClassSubjectMVS, basename='class-subject')

# مسارات المدارس المستقلة (Independent School Content & Sections)
router_schools.register(r'school-subjects', SchoolSubjectMVS, basename='school-subject')
router_schools.register(r'school-units', SchoolUnitMVS, basename='school-unit')
router_schools.register(r'school-lessons', SchoolLessonMVS, basename='school-lesson')
router_schools.register(r'school-learning-outcomes', SchoolLearningOutcomeMVS, basename='school-learning-outcome')
router_schools.register(r'school-sections', SchoolSectionMVS, basename='school-section')
