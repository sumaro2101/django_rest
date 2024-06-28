from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Payments


class PaymentsSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Payments
        fields = ('user',
                  'date_of_pay',
                  'pay_course',
                  'pay_lesson',
                  'payment_amount',
                  'payment_method',
                  )
        

class UserSerializers(serializers.ModelSerializer):
    payments_info = PaymentsSerializers(many=True, read_only=True, source='payments_set')
    
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
                  'payments_info',
                  )
        