import traceback
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm

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
        
    def create(self, validated_data):
        
        password = validated_data.get('password')
        password_check = validated_data.pop('password_check')
        if password and password_check and password != password_check:
            raise ValidationError(
                'Пароли не совпадают'
            )
        else:
            ModelClass = self.Meta.model
            
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                ValidationError(error)
                
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
    