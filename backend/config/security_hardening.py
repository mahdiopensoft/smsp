"""
Security hardening hooks applied at Django startup and URL loading.
Ensures AllMVS and OpenSoftCoreV41 base viewsets do not expose unauthenticated access.
"""
from rest_framework import permissions


def apply_security_hardening():
    """Patch OpenSoftCoreV41 AllMVS so default permission_classes is IsAuthenticated."""
    from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS

    if not getattr(AllMVS, 'permission_classes', None):
        AllMVS.permission_classes = [permissions.IsAuthenticated]
