from rest_framework import viewsets
from rest_framework import generics

from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.get_queryset()
    serializer_class = CourseSerializer


class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.get_queryset()
    serializer_class = LessonSerializer
    
    
class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.get_queryset()
    serializer_class = LessonSerializer
    