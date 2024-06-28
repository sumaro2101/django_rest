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
                             )
    
    city = models.CharField(max_length=150,
                            blank=True,
                            null=True,
                            verbose_name='город'
                            )
    
    avatar = models.ImageField(upload_to='users/',
                               blank=True,
                               null=True,
                               verbose_name='аватар'
                               )


class Payments(models.Model):
    """Модель платежей
    """
    user = models.ForeignKey(get_user_model(),
                             verbose_name='пользователь',
                             on_delete=models.DO_NOTHING,
                             related_name='payments'
                             )
    
    date_of_pay = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата платежа',
                                       )
    
    pay_course = models.ForeignKey("courses.Course",
                                   verbose_name='платеж курса',
                                   blank=True,
                                   null=True,
                                   default=None,
                                   on_delete=models.DO_NOTHING,
                                   )
    
    pay_lesson = models.ForeignKey("courses.Lesson",
                                   verbose_name='платеж урока',
                                   blank=True,
                                   null=True,
                                   default=None,
                                   on_delete=models.DO_NOTHING,
                                   )
    
    payment_amount = models.DecimalField(verbose_name='сумма оплаты',
                                        max_digits=10,
                                        decimal_places=2,
                                        )
    
    payment_method = models.CharField(max_length=50,
                                      verbose_name='способ оплаты',
                                      choices=(
                                          ('cash', 'наличные'),
                                          ('money_transfer', 'перевод денег'),
                                      ),
                                      )
    
    class Meta:
        ordering = ('-date_of_pay',)
    