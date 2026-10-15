from rest_framework.permissions import BasePermission


class IsAdvertisementCreator(BasePermission):
    """Разрешает изменять объявление только его автору."""

    def has_object_permission(self, request, view, obj):
        return obj.creator_id == request.user.id