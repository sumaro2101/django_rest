from rest_framework.permissions import BasePermission

class IsCurrentUser(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        user = view.queryset.get(pk=pk)
        return request.user == user
    