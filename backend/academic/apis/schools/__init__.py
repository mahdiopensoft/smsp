from .SchoolStageMVS import SchoolStageMVS
from .SchoolLevelMVS import SchoolLevelMVS
from .SchoolTrackMVS import SchoolTrackMVS
from .SchoolClassTrackMVS import SchoolClassTrackMVS
from .SchoolSubjectMVS import SchoolSubjectMVS
from .SchoolClassSubjectMVS import SchoolClassSubjectMVS
from .SchoolUnitMVS import SchoolUnitMVS
from .SchoolLessonMVS import SchoolLessonMVS
from .SchoolLearningOutcomeMVS import SchoolLearningOutcomeMVS
from .SchoolSectionMVS import SchoolSectionMVS

# Compatibility aliases
EducationalStageMVS = SchoolStageMVS
LevelMVS = SchoolLevelMVS
TrackMVS = SchoolTrackMVS
ClassTrackMVS = SchoolClassTrackMVS
ClassSubjectMVS = SchoolClassSubjectMVS

__all__ = [
    # New School standard names
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
    # Aliases
    'EducationalStageMVS',
    'LevelMVS',
    'TrackMVS',
    'ClassTrackMVS',
    'ClassSubjectMVS',
]
