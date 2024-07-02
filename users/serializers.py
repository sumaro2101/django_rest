import traceback
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Payments
from users.validators import ValidatorOneValueInput, ValidatorSetPasswordUser


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
        validators = [ValidatorOneValueInput(['pay_course', 'pay_lesson'])]
    

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

        
class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password_check = serializers.CharField(write_only=True, required=True)
    
    
    class Meta:
        model = get_user_model()
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'city',
                  'password',
                  'password_check',
                  )
        validators = [ValidatorSetPasswordUser(['password', 'password_check'])]
        
    def create(self, validated_data):
        
        ModelClass = self.Meta.model
        password = validated_data.pop('password_check')
                
        try:
            instance = ModelClass._default_manager.create(**validated_data)
            instance.set_password(password)
            instance.save(update_fields=['password'])
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)
            
        return instance
    