from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from courses.apps import CoursesConfig
from courses.views import LessonList, LessonDetail

app_name = CoursesConfig.name

urlpatterns = [
    path('course/', LessonList.as_view(), name='course_list'),
    path('course/<int:pk>', LessonList.as_view(), name='course_detail'),
    path('lesson/', LessonList.as_view(), name='lesson_list'),
    path('lesson/<int:pk>', LessonDetail.as_view(), name='lesson_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
