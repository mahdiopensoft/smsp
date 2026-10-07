from rest_framework.routers import DefaultRouter

from academic.apis.universities.UniversityCourseMVS import UniversityCourseMVS
from academic.apis.universities.UniversityCourseTopicMVS import UniversityCourseTopicMVS
from academic.apis.universities.UniversityCourseCLOMVS import UniversityCourseCLOMVS
from academic.apis.universities.UniversityCollegeMVS import UniversityCollegeMVS
from academic.apis.universities.UniversityCollegeBranchMVS import UniversityCollegeBranchMVS
from academic.apis.universities.UniversityCollegeSettingsMVS import UniversityCollegeSettingsMVS
from academic.apis.universities.UniversityDepartmentMVS import UniversityDepartmentMVS
from academic.apis.universities.UniversitySpecializationMVS import UniversitySpecializationMVS
from academic.apis.universities.UniversitySpecializationBranchMVS import UniversitySpecializationBranchMVS
from academic.apis.universities.UniversityLevelMVS import UniversityLevelMVS
from academic.apis.universities.UniversitySemesterMVS import UniversitySemesterMVS
from academic.apis.universities.UniversitySemesterSubjectMVS import UniversitySemesterSubjectMVS
from academic.apis.universities.UniversityStudySystemMVS import UniversityStudySystemMVS
from academic.apis.universities.UniversityTypeOfGradeMVS import UniversityTypeOfGradeMVS
from academic.apis.universities.UniversityGradingSystemMVS import UniversityGradingSystemMVS
from academic.apis.universities.UniversityGradeDistributionMVS import UniversityGradeDistributionMVS

router_universities = DefaultRouter()

# المقررات والمخرجات الأكاديمية للجامعات (University Courses & CLOs)
router_universities.register(r'university-courses', UniversityCourseMVS, basename='university-course')
router_universities.register(r'course-topics', UniversityCourseTopicMVS, basename='course-topic')
router_universities.register(r'course-clos', UniversityCourseCLOMVS, basename='course-clo')

# الهيكل الأكاديمي للجامعات (University Structure: Colleges, Depts, Specializations)
router_universities.register(r'colleges', UniversityCollegeMVS, basename='college')
router_universities.register(r'college-branches', UniversityCollegeBranchMVS, basename='college-branch')
router_universities.register(r'college-settings', UniversityCollegeSettingsMVS, basename='college-setting')
router_universities.register(r'departments', UniversityDepartmentMVS, basename='department')
router_universities.register(r'specializations', UniversitySpecializationMVS, basename='specialization')
router_universities.register(r'specialization-branches', UniversitySpecializationBranchMVS, basename='specialization-branch')
router_universities.register(r'educational-levels', UniversityLevelMVS, basename='educational-level')

# النظم الدراسية والفصول والدرجات (Study Systems, Semesters & Grading)
router_universities.register(r'semesters', UniversitySemesterMVS, basename='semester')
router_universities.register(r'semester-subjects', UniversitySemesterSubjectMVS, basename='semester-subject')
router_universities.register(r'study-systems', UniversityStudySystemMVS, basename='study-system')
router_universities.register(r'type-of-grades', UniversityTypeOfGradeMVS, basename='type-of-grade')
router_universities.register(r'grading-systems', UniversityGradingSystemMVS, basename='grading-system')
router_universities.register(r'grade-distributions', UniversityGradeDistributionMVS, basename='grade-distribution')
