from .InstituteField import InstituteFieldSerializer
from .InstituteEducationSystem import InstituteEducationSystemSerializer
from .InstituteSpecialization import InstituteSpecializationSerializer
from .InstituteLevel import InstituteLevelSerializer
from .InstituteSemester import InstituteSemesterSerializer
from .InstituteCurriculum import InstituteCurriculumSerializer
from .InstituteBatch import InstituteBatchSerializer
from .InstituteSubject import InstituteSubjectSerializer
from .InstituteCurriculumSubject import InstituteCurriculumSubjectSerializer
from .InstituteShortCourse import InstituteShortCourseSerializer
from .InstituteAdmissionRequirement import InstituteAdmissionRequirementSerializer
from .InstituteSpecialTrack import InstituteSpecialTrackSerializer

__all__ = [
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
