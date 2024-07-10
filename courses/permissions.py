from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()
    
    
class IsCurrentUser(BasePermission):
    
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        instance = view.queryset.get(pk=pk)
        try:
            return request.user == instance.owner
        except:
            return request.user == instance.user
    

class IsSuperUser(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_superuser
        