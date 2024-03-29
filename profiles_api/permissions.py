from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self,request,view,obj):
        """check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return False

        return obj.id == request.user.id
