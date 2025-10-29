from rest_framework.permissions import BasePermission

class IsRegisteredDevice(BasePermission):
    def has_permission(self, request, view):
        return bool(request.auth and 'device_id' in request.auth)