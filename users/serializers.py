from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = get_user_model()
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_staff',
                  'is_active',
                  'phone',
                  'city',
                  'avatar',
                  )
        