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
                              help_text='Создатель курса'
                              )
    
    course_name = models.CharField(max_length=200,
                                   verbose_name='имя курса',
                                   help_text='Имя курса',
                                   )
    
    course_preview = models.ImageField(upload_to='courses/course/%Y/%m/%d/',
                               blank=True,
                               null=True,
                               help_text='Изображение характерезуещее курс',
                               )
    
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='дата создания',
                                       blank=True,
                                       null=True,
                                       help_text='Дата создания, назначается автоматически',
                                       )
    
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='дата изменения',
                                       blank=True,
                                       null=True,
                                       help_text='Дата изменения, назначается автоматически',
                                       )
    
    description = models.TextField(blank=True,
                                   null=True,
                                   help_text='Описание курса',
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
                              help_text='Создатель урока',
                              )
     
    course = models.ForeignKey("courses.Course",
                               verbose_name="курс",
                               on_delete=models.CASCADE,
                               related_name='lessons',
                               help_text='Курс урока',
                               )
    
    lesson_name = models.CharField(verbose_name="название урока",
                                   max_length=200,
                                   help_text='Название урока, не более 200 символов',
                                   )
    
    description = models.TextField(verbose_name='описание',
                                   blank=True,
                                   null=True,
                                   help_text='Описание урока',
                                   )
    
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='дата создания',
                                       blank=True,
                                       null=True,
                                       help_text='Дата создания, назначается автоматически',
                                       )
    
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='дата изменения',
                                       blank=True,
                                       null=True,
                                       help_text='Дата изменения, назначается автоматически',
                                       )
    
    lesson_preview = models.ImageField(verbose_name='картинка',
                                       blank=True,
                                       null=True,
                                       upload_to='courses/lessons/%Y/%m/%d/',
                                       help_text='Изображение характеризующее урок',
                                    )
    
    video_link = models.CharField(max_length=256,
                                  verbose_name='ссылка на видео урок',
                                  help_text='Ссылка на видео урок',
                                  )
    

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
                               help_text='Курс подписки',
                               )
    
    user = models.ForeignKey(get_user_model(),
                             verbose_name='пользователь',
                             on_delete=models.CASCADE,
                             help_text='Подписчик',
                             )
    
    
    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        