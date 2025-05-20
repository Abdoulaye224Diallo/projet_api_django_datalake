from rest_framework.permissions import BasePermission
from .models import APIRight

class HasEndpointAccess(BasePermission):
    def has_permission(self, request, view):
        if not request.auth:
            return False
        token = str(request.auth)
        endpoint = view.__class__.__name__
        return APIRight.objects.filter(token=token, endpoint_name=endpoint, can_access=True).exists()
