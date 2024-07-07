from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db.models import Q

from courses.models import Course, Lesson, Subscribe
from courses.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from courses.permissions import IsSuperUser, IsModerator, IsCurrentUser
from courses.paginators import PaginateCourses, PaginateLessons

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    """Создание, изменение, просмотр, удаление курса.
    Если не администратор и не владелец курса тогда
    возможно только просматривать
    """    
    queryset = Course.objects.get_queryset()
    serializer_class = CourseSerializer
    pagination_class = PaginateCourses
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
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
    """Создание и просмотр списка уроков курса
    """    
    queryset = Lesson.objects.get_queryset()
    serializer_class = LessonSerializer
    pagination_class = PaginateLessons
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_permissions(self):
        
        if self.request.method == 'POST':
            permission_classes = [~IsModerator]
        
        else:
            permission_classes = [permissions.IsAuthenticated]
                        
        return [permission() for permission in permission_classes]
    
    
class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение, удаление урока.
    Если не админ и не владелец возможен только просмотр
    """    
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
    

class SubscribeAPIToggle(generics.GenericAPIView):
    """Подписка-отписка курса
    """    
    queryset = Subscribe.objects.get_queryset()
    serializer_class = SubscribeSerializer
    
    def post(self, *args, **kwargs):
        user = self.request.user
        course = get_object_or_404(Course, pk=kwargs['pk'])
        
        subscribe = Subscribe.objects.filter(Q(user=user) & Q(course=course))
        
        if subscribe.exists():
            user_subscribe = subscribe.get()
            user_subscribe.delete()
            message = 'Подписка удалена'
        else:
            Subscribe.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
            
        return Response({'message': message})
