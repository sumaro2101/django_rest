from django.urls import path, include

from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import (LessonList,
                           LessonDetail,
                           CourseViewSet,
                           SubscribeAPIToggle,
                           LinkPaymentCourseGetView,
                           LinkPaymentLessonGetView,
                           LinkPaymentDoneView,
                           LinkPaymentCancelView,
                           StripeSessionView,
                           )


app_name = CoursesConfig.name


router = DefaultRouter()
router.register(r'api/course', CourseViewSet, basename='api/course')


urlpatterns = [
    path('', include(router.urls)),
    path('api/lesson/',
         LessonList.as_view(),
         name='lesson_list',
         ),
    path('api/lesson/<int:pk>/',
         LessonDetail.as_view(),
         name='lesson_detail',
         ),
    path('api/lesson/payment/<int:pk>/',
         LinkPaymentLessonGetView.as_view(),
         name='payment_lesson',
         ),
    path('api/done/payment/',
         LinkPaymentDoneView.as_view(),
         name='done_payment',
         ),
    path('api/cancel/payment/',
         LinkPaymentCancelView.as_view(),
         name='cancel_payment',
         ),
    path('api/course/payment/<int:pk>/',
         LinkPaymentCourseGetView.as_view(),
         name='payment_course',
         ),
    path('api/course/subscribe/<int:pk>/',
         SubscribeAPIToggle.as_view(),
         name='subscribe',
         ),
    path('api/payment/detail/<int:pk>/',
         StripeSessionView.as_view(),
         name='session_detail',
         ),
]
