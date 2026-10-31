from rest_framework import permissions

class IsControlOfficer(permissions.BasePermission):
    """
    Enforces that the user is authenticated and authorized to view/dispatch/cancel
    grades in the Exam Gradebook and Control Management screens.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_staff or request.user.is_superuser:
            return True
        user_type = getattr(request.user, 'fk_user_type', None)
        if user_type and user_type.name_ar in ['موظف', 'مدرس', 'كنترول', 'إدارة', 'أكاديمي']:
            return True
        if request.user.groups.filter(name__icontains='control').exists():
            return True
        return False
