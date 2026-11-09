"""
Compatibility stub for Subject model.
Redirects to UniversitySubject for backward compatibility.
"""
from academic.models.universities.UniversitySubject import UniversitySubject as Subject

__all__ = ['Subject']
