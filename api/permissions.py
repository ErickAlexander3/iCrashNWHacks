from rest_framework import permissions

class EmergencyServicePermission(permissions.BasePermission):
    """
    Check if the current user is an emergency services provider
    """
    message = 'Action only allowed for emergency service providers'

    def has_permission(self, request, view):
        userinfo = request.user.userinfo
        if userinfo is None:
            return False

        return userinfo.emergency_service_provider