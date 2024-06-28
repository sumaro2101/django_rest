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
    
    def create(self, validated_data):
        pay_course = validated_data.get('pay_course')
        pay_lesson = validated_data.get('pay_lesson')
        
        if pay_course and pay_lesson:
            raise ValueError('pay_course и pay_lesson не могут быть опеределенны вместе')
        if not pay_course and not pay_lesson:
            raise ValueError('Нужно опередить одно из полей (pay_course, pay_lesson)')
        
        return super().create(validated_data)
    

class UserSerializers(serializers.ModelSerializer):
    payments_info = PaymentsSerializers(many=True, read_only=True, source='payments')
    
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
        