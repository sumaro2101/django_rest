from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (UpdateDestroyUser,
                         PaymentsListAPIView,
                         UserViewCreate,
                         ViewUserAPI
                         )
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('api/user/create/', UserViewCreate.as_view(), name='user_create'),
    path('api/user/view/<int:pk>/', ViewUserAPI.as_view(), name='user_view'),
    path('api/user/update-delete/<int:pk>/', UpdateDestroyUser.as_view(), name='user_update_delete'),
    path('api/payments', PaymentsListAPIView.as_view(), name='payments_list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
