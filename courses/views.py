from rest_framework import viewsets, generics, permissions

from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer
from courses.permissions import IsSuperUser, IsModerator, IsCurrentUser

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.get_queryset()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [~IsModerator]
        
        if self.action == 'update':
            permission_classes = [IsSuperUser | IsModerator | IsCurrentUser]
            
        if self.action == 'partial_update':
            permission_classes = [IsSuperUser | IsModerator | IsCurrentUser]
            
        if self.action == 'destroy':
            permission_classes = [IsSuperUser | IsCurrentUser]
            
        else:
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]


class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.get_queryset()
    serializer_class = LessonSerializer
    
    def get_permissions(self):
        
        if self.request.method == 'POST':
            permission_classes = [~IsModerator]
        
        else:
            permission_classes = [permissions.IsAuthenticated]
                        
        return [permission() for permission in permission_classes]
    
    
class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.get_queryset()
    serializer_class = LessonSerializer
    
    def get_permissions(self):
        
        if self.request.method == 'POST':
            permission_classes = [IsSuperUser | IsModerator | IsCurrentUser]
            
        if self.request.method == 'DELETE':
            permission_classes = [IsSuperUser | IsCurrentUser]
            
        else:
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    