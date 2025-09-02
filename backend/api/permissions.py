from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows full control for owners and read-only for others.
    Use this on TripPlan and SuggestedLocation.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(obj, 'user') and obj.user == request.user