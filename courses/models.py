from django.db import models

# Create your models here.

class Course(models.Model):
    """Модель курса
    """    
    course_name = models.CharField(max_length=200,
                                   verbose_name='имя курса'
                                   )
    
    course_preview = models.ImageField(upload_to='courses/course/%Y/%m/%d/',
                               blank=True,
                               null=True,
                               )
    
    description = models.TextField(blank=True,
                                   null=True,
                                    )
    

    class Meta:
        verbose_name = ("курс")
        verbose_name_plural = ("курсы")

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    """Модель урока для курса
    """    
    course = models.ForeignKey("courses.Course",
                               verbose_name="курс",
                               on_delete=models.CASCADE,
                               )
    
    lesson_name = models.CharField("название урока",
                                   max_length=200,
                                   )
    
    descriptons = models.TextField(verbose_name='описание',
                                   blank=True,
                                   null=True,
                                   )
    
    lesson_preview = models.ImageField(verbose_name='картинка',
                                       blank=True,
                                       null=True,
                                       upload_to='courses/lessons/%Y/%m/%d/'
                                    )
    
    video_link = models.FileField(verbose_name='ссылка на видео',
                                         upload_to='courses/videos/%Y/%m/%d/',
                                         max_length=256,
                                         blank=True,
                                         null=True,
                                         )
    

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.lesson_name
