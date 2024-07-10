from rest_framework import serializers
from rest_framework.validators import ValidationError

from django.db.models import Q
from django.utils import timezone

import datetime

from courses.models import Course, Lesson, Subscribe
from courses.validators import ValidateOnlyYoutubeLink
from courses.tasks import send


class LessonSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Lesson
        fields = ('pk',
                  'owner',
                  'course',
                  'lesson_name',
                  'description',
                  'lesson_preview',
                  'video_link',
                  )
        validators = [ValidateOnlyYoutubeLink(link='video_link')]
        
    def create(self, validated_data):
        course = validated_data.get('course')
        owner_of_lesson = validated_data.get('owner')
        owner_of_course = course.owner
        if not owner_of_course == owner_of_lesson and not owner_of_lesson.is_superuser:
            raise ValidationError('Добавлять уроки может только владелец данного курса')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        time_four_hour_before = timezone.now() - datetime.timedelta(hours=4)
        if not instance.course.time_update > time_four_hour_before:
            course = instance.course
            instance = super().update(instance, validated_data)
            course.time_update = timezone.now()
            course.save(update_fields=['time_update'])
            send(course.id)
            return instance
        else:
            return super().update(instance, validated_data)
    

class CourseSerializer(serializers.ModelSerializer):
    
    lessons_detail = LessonSerializer(read_only=True, many=True, source='lessons', help_text='Список уроков данного курса')
    lessons = serializers.SerializerMethodField(read_only=True, help_text='Количество уроков у курса')
    subscribe_of_the_course = serializers.SerializerMethodField(read_only=True, source='subscribe', help_text='Является ли текущий пользователь подписан')
    
    
    class Meta:
        model = Course
        fields = ('pk',
                  'owner',
                  'course_name',
                  'course_preview',
                  'description',
                  'subscribe_of_the_course',
                  'lessons',
                  'lessons_detail',
                  )
        
    def update(self, instance, validated_data):
        time_four_hour_before = timezone.now() - datetime.timedelta(hours=4)
        if not instance.time_update > time_four_hour_before:
            instance = super().update(instance, validated_data)
            send.delay(instance.id)
            return instance
        else:
            return super().update(instance, validated_data)
        
    def get_lessons(self, instance):
        """Поле которое показывает количество уроков у данного курса
        """        
        return instance.lessons.get_queryset().count()
    
    def get_subscribe_of_the_course(self, instance):
        """Поле которое вычисляет подписан ли пользователь на данный курс
        """        
        return instance.subscribe.filter(Q(course=instance) & Q(user=self.context['request'].user)).exists()
        

class SubscribeSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Subscribe
        fields = ('course',)
        
        
class LinkPaymentSerializer(serializers.Serializer):
    url = serializers.URLField()


class StripeSessionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, help_text='ID сессии StrypeSession')
    amount_total = serializers.DecimalField(max_digits=12, decimal_places=0, read_only=True, help_text='Общая сумма оплаты, сумма считается в копейках например: 50000 -> 500.00 RUB')
    automatic_tax = serializers.BooleanField(read_only=True, help_text='Взымание налога')
    currency = serializers.CharField(read_only=True, help_text='Курс валюты')
    user_email = serializers.EmailField(read_only=True, help_text='Электронный адресс покупателя')
    user_name = serializers.CharField(read_only=True, help_text='Имя покупатебя')
    phone = serializers.CharField(read_only=True, help_text='Телефон покупателя')
    payment_intent = serializers.CharField(read_only=True, help_text='Id оплаты')
    url = serializers.URLField(read_only=True, help_text='Ссылка на оплату')
    status = serializers.CharField(read_only=True, help_text='Статус оплаты')
    