from rest_framework import permissions


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
    Allows access only to employees with a position.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Check if the user has permission to access the object.

        Args:
            request (Request): The request made by the user.
            view (View): The view that handles the request.
            obj (Object): The object being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        # Check if the user has a position
        return bool(request.user.position)
