from rest_framework import generics

from django.contrib.auth import get_user_model
from users.serializers import UserSerializers
from users.models import User
# Create your views here.

    
class ViewUpdateUser(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserSerializers
    