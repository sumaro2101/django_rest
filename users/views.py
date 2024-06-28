from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from users.serializers import UserSerializers, PaymentsSerializers
from users.models import Payments
# Create your views here.

    
class ViewUpdateUser(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserSerializers


class PaymentsListAPIView(generics.ListCreateAPIView):
    queryset = Payments.objects.get_queryset()
    serializer_class = PaymentsSerializers
    filter_backends = (DjangoFilterBackend,
                       OrderingFilter,
                       )
    filterset_fields = ('pay_course', 'pay_lesson', 'payment_method')
    ordering_fields = ('date_of_pay',)
