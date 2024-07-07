from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class User(AbstractUser):
    """Переопределение стандартной модели пользователя
    """    
    phone = PhoneNumberField(null=True,
                             blank=True,
                             verbose_name='номер телефона',
                             unique=True,
                             help_text='Номер телефона пример "+7(913)0000000"',
                             )
    
    city = models.CharField(max_length=150,
                            blank=True,
                            null=True,
                            verbose_name='город',
                            help_text='Город проживания пользователя',
                            )
    
    avatar = models.ImageField(upload_to='users/',
                               blank=True,
                               null=True,
                               verbose_name='аватар',
                               help_text='Аватар пользователя',
                               )


class Payments(models.Model):
    """Модель платежей
    """
    user = models.ForeignKey(get_user_model(),
                             verbose_name='пользователь',
                             on_delete=models.DO_NOTHING,
                             related_name='payments',
                             help_text='Владелец платежа',
                             )
    
    date_of_pay = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата платежа',
                                       help_text='Дата платежа',
                                       )
    
    pay_course = models.ForeignKey("courses.Course",
                                   verbose_name='платеж курса',
                                   blank=True,
                                   null=True,
                                   default=None,
                                   on_delete=models.DO_NOTHING,
                                   help_text='Платеж за курс, возможно выбрать либо курс либо урок',
                                   )
    
    pay_lesson = models.ForeignKey("courses.Lesson",
                                   verbose_name='платеж урока',
                                   blank=True,
                                   null=True,
                                   default=None,
                                   on_delete=models.DO_NOTHING,
                                   help_text='Платеж за урок, возможно выбрать либо курс либо урок',
                                   )
    
    payment_amount = models.DecimalField(verbose_name='сумма оплаты',
                                        max_digits=10,
                                        decimal_places=2,
                                        help_text='Сумма оплаты, максимум 8 значное число',
                                        )
    
    payment_method = models.CharField(max_length=50,
                                      verbose_name='способ оплаты',
                                      choices=(
                                          ('cash', 'наличные'),
                                          ('money_transfer', 'перевод денег'),
                                      ),
                                      help_text='Способ оплаты, либо наличные либо денежный перевод',
                                      )
    
    class Meta:
        ordering = ('-date_of_pay',)
    