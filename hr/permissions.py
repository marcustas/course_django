from rest_framework import permissions
from hr.models import Position


class IsNotRussianEmail(permissions.BasePermission):
    """
    Allows access only to users whose email does not end with .ru
    """

    def has_permission(self, request, view) -> bool:
        if request.user and request.user.email:
            return not request.user.email.endswith('.ru')
        return False


class HasPositionPermission(permissions.BasePermission):
    """
    Allows access only to users who have position.
    """
    def has_permission(self, request, view) -> bool:
        user_position = request.user.position
        positions = Position.objects.all()
        if user_position in positions:
            return True
        return False
