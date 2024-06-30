from django.forms import ValidationError
from rest_framework import generics, permissions, mixins
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model, password_validation

from users.serializers import UserSerializers, PaymentsSerializers, UserCreateSerializer
from users.models import Payments
from users.permissions import IsCurrentUser, IsSuperUser
# Create your views here.

class ViewUserAPI(generics.RetrieveAPIView):
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserSerializers
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if not instance == request.user:
            list_of_allow_fields = ('username', 'first_name', 'email', 'avatar')
            data = {key: value for key, value in serializer.data.items()
                               if key in list_of_allow_fields}
            return Response(data)
        
        return Response(serializer.data)
    
    
class UpdateDestroyUser(mixins.DestroyModelMixin, generics.UpdateAPIView):
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated & IsSuperUser |
                          permissions.IsAuthenticated & IsCurrentUser]
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])


class UserViewCreate(generics.CreateAPIView):
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class PaymentsListAPIView(generics.ListCreateAPIView):
    queryset = Payments.objects.get_queryset()
    serializer_class = PaymentsSerializers
    filter_backends = (DjangoFilterBackend,
                       OrderingFilter,
                       )
    filterset_fields = ('pay_course', 'pay_lesson', 'payment_method')
    ordering_fields = ('date_of_pay',)
