from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Course(models.Model):
    """Модель курса
    """  
    owner = models.ForeignKey(get_user_model(),
                              verbose_name='владелец',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              )
    
    course_name = models.CharField(max_length=200,
                                   verbose_name='имя курса'
                                   )
    
    course_preview = models.ImageField(upload_to='courses/course/%Y/%m/%d/',
                               blank=True,
                               null=True,
                               )
    
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='дата создания',
                                       blank=True,
                                       null=True,
                                       )
    
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='дата изменения',
                                       blank=True,
                                       null=True,
                                       )
    
    description = models.TextField(blank=True,
                                   null=True,
                                    )
    

    class Meta:
        verbose_name = ("курс")
        verbose_name_plural = ("курсы")
        ordering = ['-time_update']

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    """Модель урока для курса
    """
    owner = models.ForeignKey(get_user_model(),
                              verbose_name='владелец',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              )
     
    course = models.ForeignKey("courses.Course",
                               verbose_name="курс",
                               on_delete=models.CASCADE,
                               related_name='lessons'
                               )
    
    lesson_name = models.CharField("название урока",
                                   max_length=200,
                                   )
    
    description = models.TextField(verbose_name='описание',
                                   blank=True,
                                   null=True,
                                   )
    
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='дата создания',
                                       blank=True,
                                       null=True,
                                       )
    
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='дата изменения',
                                       blank=True,
                                       null=True,
                                       )
    
    lesson_preview = models.ImageField(verbose_name='картинка',
                                       blank=True,
                                       null=True,
                                       upload_to='courses/lessons/%Y/%m/%d/'
                                    )
    
    video_link = models.CharField(max_length=256, verbose_name='ссылка на видео урок')
    

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['-time_update']

    def __str__(self):
        return self.lesson_name


class Subscribe(models.Model):
    """Модель подписки для курсов
    """    
    course = models.ForeignKey("courses.Course",
                               verbose_name='курс',
                               related_name='subscribe',
                               on_delete=models.CASCADE,
                               )
    
    user = models.ForeignKey(get_user_model(),
                             verbose_name='пользователь',
                             on_delete=models.CASCADE,
                             )
    
    
    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        