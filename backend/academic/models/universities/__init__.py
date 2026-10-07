from .UniversityCollege import UniversityCollege
from .UniversityCollegeBranch import UniversityCollegeBranch
from .UniversityCollegeSettings import UniversityCollegeSettings
from .UniversityDepartment import UniversityDepartment
from .UniversitySpecialization import UniversitySpecialization
from .UniversitySpecializationBranch import UniversitySpecializationBranch
from .UniversityLevel import UniversityLevel
from .UniversityCourse import UniversityCourse
from .UniversityCourseTopic import UniversityCourseTopic
from .UniversityCourseCLO import UniversityCourseCLO
from .UniversitySemester import UniversitySemester
from .UniversitySemesterSubject import UniversitySemesterSubject
from .UniversityStudySystem import UniversityStudySystem
from .UniversityGradingSystem import UniversityGradingSystem
from .UniversityGradeDistribution import UniversityGradeDistribution
from .UniversityTypeOfGrade import UniversityTypeOfGrade

# Compatibility aliases
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

__all__ = [
    # New University standard names
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
    # Aliases
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
]
