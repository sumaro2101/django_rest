from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from users.views import ViewUpdateUser
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('api/user/<int:pk>/', ViewUpdateUser.as_view(), name='user'),
]

urlpatterns = format_suffix_patterns(urlpatterns)