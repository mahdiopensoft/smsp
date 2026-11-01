from .UniversitySubject import UniversitySubjectSerializer
from .UniversityUnit import UniversityUnitSerializer
from .UniversityLesson import UniversityLessonSerializer
from .UniversityExamPeriod import UniversityExamPeriodSerializer
from .UniversityCollege import UniversityCollegeSerializer
from .UniversityCollegeBranch import UniversityCollegeBranchSerializer
from .UniversityCollegeSettings import UniversityCollegeSettingsSerializer
from .UniversityDepartment import UniversityDepartmentSerializer
from .UniversitySpecialization import UniversitySpecializationSerializer
from .UniversitySpecializationBranch import UniversitySpecializationBranchSerializer
from .UniversityLevel import UniversityLevelSerializer
from .UniversityCourse import UniversityCourseSerializer
from .UniversityCourseTopic import UniversityCourseTopicSerializer
from .UniversityCourseCLO import UniversityCourseCLOSerializer
from .UniversitySemester import UniversitySemesterSerializer
from .UniversitySemesterSubject import UniversitySemesterSubjectSerializer
from .UniversityStudySystem import UniversityStudySystemSerializer
from .UniversityGradingSystem import UniversityGradingSystemSerializer
from .UniversityGradeDistribution import UniversityGradeDistributionSerializer
from .UniversityTypeOfGrade import UniversityTypeOfGradeSerializer

# Compatibility aliases
SubjectSerializer = UniversitySubjectSerializer
UnitSerializer = UniversityUnitSerializer
LessonSerializer = UniversityLessonSerializer
ExamPeriodSerializer = UniversityExamPeriodSerializer
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

__all__ = [
    # New University standard names
    'UniversitySubjectSerializer',
    'UniversityUnitSerializer',
    'UniversityLessonSerializer',
    'UniversityExamPeriodSerializer',
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
    # Aliases
    'SubjectSerializer',
    'UnitSerializer',
    'LessonSerializer',
    'ExamPeriodSerializer',
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
]
