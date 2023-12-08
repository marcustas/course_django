from rest_framework import permissions
class IsNotRussianEmail(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user and request.user.email:
            return not request.user.email.endswith('.ru')
        return False


class HasPositionPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        return bool(request.user.position)