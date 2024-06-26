from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import LessonList, LessonDetail, CourseViewSet

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'api/course', CourseViewSet, basename='api/course')

urlpatterns = [
    path('', include(router.urls)),
    path('api/lesson/', LessonList.as_view(), name='lesson_list'),
    path('api/lesson/<int:pk>', LessonDetail.as_view(), name='lesson_detail'),
]

