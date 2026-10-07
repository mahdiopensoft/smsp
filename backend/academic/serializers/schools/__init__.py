from .SchoolStage import SchoolStageSerializer
from .SchoolLevel import SchoolLevelSerializer
from .SchoolTrack import SchoolTrackSerializer
from .SchoolClassTrack import SchoolClassTrackSerializer
from .SchoolSubject import SchoolSubjectSerializer
from .SchoolClassSubject import SchoolClassSubjectSerializer
from .SchoolUnit import SchoolUnitSerializer
from .SchoolLesson import SchoolLessonSerializer
from .SchoolLearningOutcome import SchoolLearningOutcomeSerializer
from .SchoolSection import SchoolSectionSerializer

# Compatibility aliases
EducationalStageSerializer = SchoolStageSerializer
LevelSerializer = SchoolLevelSerializer
TrackSerializer = SchoolTrackSerializer
ClassTrackSerializer = SchoolClassTrackSerializer
ClassSubjectSerializer = SchoolClassSubjectSerializer

__all__ = [
    # New School standard names
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
    # Aliases
    'EducationalStageSerializer',
    'LevelSerializer',
    'TrackSerializer',
    'ClassTrackSerializer',
    'ClassSubjectSerializer',
]
