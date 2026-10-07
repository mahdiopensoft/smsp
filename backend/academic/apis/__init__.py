"""
نظام واجهات برمجة التطبيقات الأكاديمية المقسم والممنهج (Modular Academic APIs):
1. common: واجهات المشتركات والعامة والتقارير
2. schools: واجهات المدارس والتعليم العام (School*)
3. universities: واجهات الجامعات والكليات (University*)
4. institutes: واجهات المعاهد (مجهزة للمستقبل)
"""

# 1. المشتركات (Common)
from .common.OrganizationMVS import OrganizationMVS
from .common.AcademicYearMVS import AcademicYearMVS
from .common.ExamPeriodMVS import ExamPeriodMVS
from .common.StudentMVS import StudentMVS
from .common.SubjectMVS import SubjectMVS
from .common.UnitMVS import UnitMVS
from .common.LessonMVS import LessonMVS
from .common.LearningOutcomeMVS import LearningOutcomeMVS
from .common.CurriculumReportMVS import CurriculumReportMVS
from .common.AlignmentMatrixReportMVS import AlignmentMatrixReportMVS

# 2. المدارس (Schools)
from .schools.SchoolStageMVS import SchoolStageMVS
from .schools.SchoolLevelMVS import SchoolLevelMVS
from .schools.SchoolTrackMVS import SchoolTrackMVS
from .schools.SchoolClassTrackMVS import SchoolClassTrackMVS
from .schools.SchoolSubjectMVS import SchoolSubjectMVS
from .schools.SchoolClassSubjectMVS import SchoolClassSubjectMVS
from .schools.SchoolUnitMVS import SchoolUnitMVS
from .schools.SchoolLessonMVS import SchoolLessonMVS
from .schools.SchoolLearningOutcomeMVS import SchoolLearningOutcomeMVS
from .schools.SchoolSectionMVS import SchoolSectionMVS

# Schools Aliases
EducationalStageMVS = SchoolStageMVS
LevelMVS = SchoolLevelMVS
TrackMVS = SchoolTrackMVS
ClassTrackMVS = SchoolClassTrackMVS
ClassSubjectMVS = SchoolClassSubjectMVS

# 3. الجامعات (Universities)
from .universities.UniversityCollegeMVS import UniversityCollegeMVS
from .universities.UniversityCollegeBranchMVS import UniversityCollegeBranchMVS
from .universities.UniversityCollegeSettingsMVS import UniversityCollegeSettingsMVS
from .universities.UniversityDepartmentMVS import UniversityDepartmentMVS
from .universities.UniversitySpecializationMVS import UniversitySpecializationMVS
from .universities.UniversitySpecializationBranchMVS import UniversitySpecializationBranchMVS
from .universities.UniversityLevelMVS import UniversityLevelMVS
from .universities.UniversityCourseMVS import UniversityCourseMVS
from .universities.UniversityCourseTopicMVS import UniversityCourseTopicMVS
from .universities.UniversityCourseCLOMVS import UniversityCourseCLOMVS
from .universities.UniversitySemesterMVS import UniversitySemesterMVS
from .universities.UniversitySemesterSubjectMVS import UniversitySemesterSubjectMVS
from .universities.UniversityStudySystemMVS import UniversityStudySystemMVS
from .universities.UniversityGradingSystemMVS import UniversityGradingSystemMVS
from .universities.UniversityGradeDistributionMVS import UniversityGradeDistributionMVS
from .universities.UniversityTypeOfGradeMVS import UniversityTypeOfGradeMVS

# Universities Aliases
CollegeMVS = UniversityCollegeMVS
CollegeBranchMVS = UniversityCollegeBranchMVS
CollegeSettingsMVS = UniversityCollegeSettingsMVS
DepartmentMVS = UniversityDepartmentMVS
SpecializationMVS = UniversitySpecializationMVS
SpecializationBranchMVS = UniversitySpecializationBranchMVS
EducationalLevelsMVS = UniversityLevelMVS
CourseTopicMVS = UniversityCourseTopicMVS
CourseCLOMVS = UniversityCourseCLOMVS
SemesterMVS = UniversitySemesterMVS
SemesterSubjectMVS = UniversitySemesterSubjectMVS
StudeySystemMVS = UniversityStudySystemMVS
StudySystemMVS = UniversityStudySystemMVS
GradingSystemMVS = UniversityGradingSystemMVS
GradeDistributionMVS = UniversityGradeDistributionMVS
TypeOfGradeMVS = UniversityTypeOfGradeMVS

# 4. المعاهد (Institutes)
from .institutes import *

__all__ = [
    # Common
    'OrganizationMVS',
    'AcademicYearMVS',
    'ExamPeriodMVS',
    'StudentMVS',
    'SubjectMVS',
    'UnitMVS',
    'LessonMVS',
    'LearningOutcomeMVS',
    'CurriculumReportMVS',
    'AlignmentMatrixReportMVS',

    # Schools (New Standard)
    'SchoolStageMVS',
    'SchoolLevelMVS',
    'SchoolTrackMVS',
    'SchoolClassTrackMVS',
    'SchoolSubjectMVS',
    'SchoolClassSubjectMVS',
    'SchoolUnitMVS',
    'SchoolLessonMVS',
    'SchoolLearningOutcomeMVS',
    'SchoolSectionMVS',
    # Schools (Aliases)
    'EducationalStageMVS',
    'LevelMVS',
    'TrackMVS',
    'ClassTrackMVS',
    'ClassSubjectMVS',

    # Universities (New Standard)
    'UniversityCollegeMVS',
    'UniversityCollegeBranchMVS',
    'UniversityCollegeSettingsMVS',
    'UniversityDepartmentMVS',
    'UniversitySpecializationMVS',
    'UniversitySpecializationBranchMVS',
    'UniversityLevelMVS',
    'UniversityCourseMVS',
    'UniversityCourseTopicMVS',
    'UniversityCourseCLOMVS',
    'UniversitySemesterMVS',
    'UniversitySemesterSubjectMVS',
    'UniversityStudySystemMVS',
    'UniversityGradingSystemMVS',
    'UniversityGradeDistributionMVS',
    'UniversityTypeOfGradeMVS',
    # Universities (Aliases)
    'CollegeMVS',
    'CollegeBranchMVS',
    'CollegeSettingsMVS',
    'DepartmentMVS',
    'SpecializationMVS',
    'SpecializationBranchMVS',
    'EducationalLevelsMVS',
    'CourseTopicMVS',
    'CourseCLOMVS',
    'SemesterMVS',
    'SemesterSubjectMVS',
    'StudeySystemMVS',
    'GradingSystemMVS',
    'GradeDistributionMVS',
    'TypeOfGradeMVS',

    # Institutes
    'InstituteFieldMVS',
    'InstituteEducationSystemMVS',
    'InstituteSpecializationMVS',
    'InstituteLevelMVS',
    'InstituteSemesterMVS',
    'InstituteCurriculumMVS',
    'InstituteBatchMVS',
    'InstituteSubjectMVS',
    'InstituteCurriculumSubjectMVS',
    'InstituteShortCourseMVS',
    'InstituteAdmissionRequirementMVS',
    'InstituteSpecialTrackMVS',
]
