from .SchoolStage import SchoolStage
from .SchoolLevel import SchoolLevel
from .SchoolTrack import SchoolTrack
from .SchoolClassTrack import SchoolClassTrack
from .SchoolSubject import SchoolSubject
from .SchoolClassSubject import SchoolClassSubject
from .SchoolUnit import SchoolUnit
from .SchoolLesson import SchoolLesson
from .SchoolLearningOutcome import SchoolLearningOutcome
from .SchoolSection import SchoolSection

# Compatibility aliases
EducationalStage = SchoolStage
Level = SchoolLevel
Track = SchoolTrack
ClassTrack = SchoolClassTrack
ClassSubject = SchoolClassSubject

__all__ = [
    # New School standard names
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
    # Aliases
    'EducationalStage',
    'Level',
    'Track',
    'ClassTrack',
    'ClassSubject',
]
