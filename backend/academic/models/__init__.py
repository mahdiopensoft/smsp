"""
نظام النماذج الأكاديمية المقسم والممنهج (Modular Academic Models):
1. common: النماذج العامة والمشتركة (الطلاب، السنوات، المنظمات، الفترات، المواد والدروس)
2. schools: نماذج المدارس والتعليم العام (School*)
3. universities: نماذج الجامعات والكليات والأقسام (University*)
4. institutes: نماذج المعاهد ومراكز التدريب (مجهزة للمستقبل)
"""

# 1. المشتركات (Common)
from .common.BaseSyncModel import BaseSyncModel
from .common.Organization import Organization
from .common.AcademicYear import AcademicYear
from .common.Student import Student
from .common.LearningOutcome import LearningOutcome

# Models moved to universities (stubs remain in common for backward compat)
from .universities.UniversitySubject import UniversitySubject
from .universities.UniversityUnit import UniversityUnit
from .universities.UniversityLesson import UniversityLesson
from .universities.UniversityExamPeriod import UniversityExamPeriod

# Backward compatibility aliases for old common names
Subject = UniversitySubject
Unit = UniversityUnit
Lesson = UniversityLesson
ExamPeriod = UniversityExamPeriod

# 2. المدارس (Schools)
from .schools.SchoolStage import SchoolStage
from .schools.SchoolLevel import SchoolLevel
from .schools.SchoolTrack import SchoolTrack
from .schools.SchoolClassTrack import SchoolClassTrack
from .schools.SchoolSubject import SchoolSubject
from .schools.SchoolClassSubject import SchoolClassSubject
from .schools.SchoolUnit import SchoolUnit
from .schools.SchoolLesson import SchoolLesson
from .schools.SchoolLearningOutcome import SchoolLearningOutcome
from .schools.SchoolSection import SchoolSection

# Aliases for Schools
EducationalStage = SchoolStage
Level = SchoolLevel
Track = SchoolTrack
ClassTrack = SchoolClassTrack
ClassSubject = SchoolClassSubject

# 3. الجامعات (Universities)
from .universities.UniversityCollege import UniversityCollege
from .universities.UniversityCollegeBranch import UniversityCollegeBranch
from .universities.UniversityCollegeSettings import UniversityCollegeSettings
from .universities.UniversityDepartment import UniversityDepartment
from .universities.UniversitySpecialization import UniversitySpecialization
from .universities.UniversitySpecializationBranch import UniversitySpecializationBranch
from .universities.UniversityLevel import UniversityLevel
from .universities.UniversityCourse import UniversityCourse
from .universities.UniversityCourseTopic import UniversityCourseTopic
from .universities.UniversityCourseCLO import UniversityCourseCLO
from .universities.UniversitySemester import UniversitySemester
from .universities.UniversitySemesterSubject import UniversitySemesterSubject
from .universities.UniversityStudySystem import UniversityStudySystem
from .universities.UniversityGradingSystem import UniversityGradingSystem
from .universities.UniversityGradeDistribution import UniversityGradeDistribution
from .universities.UniversityTypeOfGrade import UniversityTypeOfGrade

# Aliases for Universities
College = UniversityCollege
CollegeBranch = UniversityCollegeBranch
CollegeSettings = UniversityCollegeSettings
Department = UniversityDepartment
Specialization = UniversitySpecialization
SpecializationBranch = UniversitySpecializationBranch
EducationalLevels = UniversityLevel
CourseTopic = UniversityCourseTopic
CourseCLO = UniversityCourseCLO
Semester = UniversitySemester
SemesterSubject = UniversitySemesterSubject
StudeySystem = UniversityStudySystem
StudySystem = UniversityStudySystem
GradingSystem = UniversityGradingSystem
GradeDistribution = UniversityGradeDistribution
TypeOfGrade = UniversityTypeOfGrade

# 4. المعاهد (Institutes)
from .institutes import *

__all__ = [
    # Common
    'BaseSyncModel',
    'Organization',
    'AcademicYear',
    'Student',
    'LearningOutcome',

    # University Models (previously in common)
    'UniversitySubject',
    'UniversityUnit',
    'UniversityLesson',
    'UniversityExamPeriod',
    # Backward compat aliases
    'ExamPeriod',
    'Subject',
    'Unit',
    'Lesson',

    # Schools (New Standard)
    'SchoolStage',
    'SchoolLevel',
    'SchoolTrack',
    'SchoolClassTrack',
    'SchoolSubject',
    'SchoolClassSubject',
    'SchoolUnit',
    'SchoolLesson',
    'SchoolLearningOutcome',
    'SchoolSection',
    # Schools (Aliases)
    'EducationalStage',
    'Level',
    'Track',
    'ClassTrack',
    'ClassSubject',

    # Universities (New Standard)
    'UniversityCollege',
    'UniversityCollegeBranch',
    'UniversityCollegeSettings',
    'UniversityDepartment',
    'UniversitySpecialization',
    'UniversitySpecializationBranch',
    'UniversityLevel',
    'UniversityCourse',
    'UniversityCourseTopic',
    'UniversityCourseCLO',
    'UniversitySemester',
    'UniversitySemesterSubject',
    'UniversityStudySystem',
    'UniversityGradingSystem',
    'UniversityGradeDistribution',
    'UniversityTypeOfGrade',
    # Universities (Aliases)
    'College',
    'CollegeBranch',
    'CollegeSettings',
    'Department',
    'Specialization',
    'SpecializationBranch',
    'EducationalLevels',
    'CourseTopic',
    'CourseCLO',
    'Semester',
    'SemesterSubject',
    'StudeySystem',
    'StudySystem',
    'GradingSystem',
    'GradeDistribution',
    'TypeOfGrade',

    # Institutes
    'InstituteField',
    'InstituteEducationSystem',
    'InstituteSpecialization',
    'InstituteLevel',
    'InstituteSemester',
    'InstituteCurriculum',
    'InstituteSubject',
    'InstituteCurriculumSubject',
]

