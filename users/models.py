from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
    avatar = models.ImageField(blank=True,
                               null=True,
                               verbose_name='аватар'
                               )
