"""
نظام المحولات الأكاديمية المقسم والممنهج (Modular Academic Serializers):
1. common: محولات المشتركات والعامة
2. schools: محولات المدارس والتعليم العام (School*)
3. universities: محولات الجامعات والكليات (University*)
4. institutes: محولات المعاهد (مجهزة للمستقبل)
"""

# 1. المشتركات (Common)
from .common.Organization import OrganizationSerializer
from .common.AcademicYear import AcademicYearSerializer
from .common.ExamPeriod import ExamPeriodSerializer
from .common.Student import StudentSerializer
from .common.Subject import SubjectSerializer
from .common.Unit import UnitSerializer
from .common.Lesson import LessonSerializer
from .common.LearningOutcome import LearningOutcomeSerializer

# 2. المدارس (Schools)
from .schools.SchoolStage import SchoolStageSerializer
from .schools.SchoolLevel import SchoolLevelSerializer
from .schools.SchoolTrack import SchoolTrackSerializer
from .schools.SchoolClassTrack import SchoolClassTrackSerializer
from .schools.SchoolSubject import SchoolSubjectSerializer
from .schools.SchoolClassSubject import SchoolClassSubjectSerializer
from .schools.SchoolUnit import SchoolUnitSerializer
from .schools.SchoolLesson import SchoolLessonSerializer
from .schools.SchoolLearningOutcome import SchoolLearningOutcomeSerializer
from .schools.SchoolSection import SchoolSectionSerializer

# Schools Aliases
EducationalStageSerializer = SchoolStageSerializer
LevelSerializer = SchoolLevelSerializer
TrackSerializer = SchoolTrackSerializer
ClassTrackSerializer = SchoolClassTrackSerializer
ClassSubjectSerializer = SchoolClassSubjectSerializer

# 3. الجامعات (Universities)
from .universities.UniversityCollege import UniversityCollegeSerializer
from .universities.UniversityCollegeBranch import UniversityCollegeBranchSerializer
from .universities.UniversityCollegeSettings import UniversityCollegeSettingsSerializer
from .universities.UniversityDepartment import UniversityDepartmentSerializer
from .universities.UniversitySpecialization import UniversitySpecializationSerializer
from .universities.UniversitySpecializationBranch import UniversitySpecializationBranchSerializer
from .universities.UniversityLevel import UniversityLevelSerializer
from .universities.UniversityCourse import UniversityCourseSerializer
from .universities.UniversityCourseTopic import UniversityCourseTopicSerializer
from .universities.UniversityCourseCLO import UniversityCourseCLOSerializer
from .universities.UniversitySemester import UniversitySemesterSerializer
from .universities.UniversitySemesterSubject import UniversitySemesterSubjectSerializer
from .universities.UniversityStudySystem import UniversityStudySystemSerializer
from .universities.UniversityGradingSystem import UniversityGradingSystemSerializer
from .universities.UniversityGradeDistribution import UniversityGradeDistributionSerializer
from .universities.UniversityTypeOfGrade import UniversityTypeOfGradeSerializer

# Universities Aliases
CollegeSerializer = UniversityCollegeSerializer
CollegeBranchSerializer = UniversityCollegeBranchSerializer
CollegeSettingsSerializer = UniversityCollegeSettingsSerializer
DepartmentSerializer = UniversityDepartmentSerializer
SpecializationSerializer = UniversitySpecializationSerializer
SpecializationBranchSerializer = UniversitySpecializationBranchSerializer
EducationalLevelsSerializer = UniversityLevelSerializer
CourseTopicSerializer = UniversityCourseTopicSerializer
CourseCLOSerializer = UniversityCourseCLOSerializer
SemesterSerializer = UniversitySemesterSerializer
SemesterSubjectSerializer = UniversitySemesterSubjectSerializer
StudeySystemSerializer = UniversityStudySystemSerializer
StudySystemSerializer = UniversityStudySystemSerializer
GradingSystemSerializer = UniversityGradingSystemSerializer
GradeDistributionSerializer = UniversityGradeDistributionSerializer
TypeOfGradeSerializer = UniversityTypeOfGradeSerializer

# 4. المعاهد (Institutes)
from .institutes import *

__all__ = [
    # Common
    'OrganizationSerializer',
    'AcademicYearSerializer',
    'ExamPeriodSerializer',
    'StudentSerializer',
    'SubjectSerializer',
    'UnitSerializer',
    'LessonSerializer',
    'LearningOutcomeSerializer',

    # Schools (New Standard)
    'SchoolStageSerializer',
    'SchoolLevelSerializer',
    'SchoolTrackSerializer',
    'SchoolClassTrackSerializer',
    'SchoolSubjectSerializer',
    'SchoolClassSubjectSerializer',
    'SchoolUnitSerializer',
    'SchoolLessonSerializer',
    'SchoolLearningOutcomeSerializer',
    'SchoolSectionSerializer',
    # Schools (Aliases)
    'EducationalStageSerializer',
    'LevelSerializer',
    'TrackSerializer',
    'ClassTrackSerializer',
    'ClassSubjectSerializer',

    # Universities (New Standard)
    'UniversityCollegeSerializer',
    'UniversityCollegeBranchSerializer',
    'UniversityCollegeSettingsSerializer',
    'UniversityDepartmentSerializer',
    'UniversitySpecializationSerializer',
    'UniversitySpecializationBranchSerializer',
    'UniversityLevelSerializer',
    'UniversityCourseSerializer',
    'UniversityCourseTopicSerializer',
    'UniversityCourseCLOSerializer',
    'UniversitySemesterSerializer',
    'UniversitySemesterSubjectSerializer',
    'UniversityStudySystemSerializer',
    'UniversityGradingSystemSerializer',
    'UniversityGradeDistributionSerializer',
    'UniversityTypeOfGradeSerializer',
    # Universities (Aliases)
    'CollegeSerializer',
    'CollegeBranchSerializer',
    'CollegeSettingsSerializer',
    'DepartmentSerializer',
    'SpecializationSerializer',
    'SpecializationBranchSerializer',
    'EducationalLevelsSerializer',
    'CourseTopicSerializer',
    'CourseCLOSerializer',
    'SemesterSerializer',
    'SemesterSubjectSerializer',
    'StudeySystemSerializer',
    'StudySystemSerializer',
    'GradingSystemSerializer',
    'GradeDistributionSerializer',
    'TypeOfGradeSerializer',

    # Institutes
    'InstituteFieldSerializer',
    'InstituteEducationSystemSerializer',
    'InstituteSpecializationSerializer',
    'InstituteLevelSerializer',
    'InstituteSemesterSerializer',
    'InstituteCurriculumSerializer',
    'InstituteBatchSerializer',
    'InstituteSubjectSerializer',
    'InstituteCurriculumSubjectSerializer',
    'InstituteShortCourseSerializer',
    'InstituteAdmissionRequirementSerializer',
    'InstituteSpecialTrackSerializer',
]
