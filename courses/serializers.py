from rest_framework import serializers

from django.db.models import Q

from courses.models import Course, Lesson, Subscribe
from courses.validators import ValidateOnlyYoutubeLink


class LessonSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Lesson
        fields = ('pk',
                  'course',
                  'lesson_name',
                  'description',
                  'lesson_preview',
                  'video_link',
                  )
        validators = [ValidateOnlyYoutubeLink(link='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    
    lessons_detail = LessonSerializer(read_only=True, many=True, source='lessons')
    lessons = serializers.SerializerMethodField(read_only=True)
    subscribe_of_the_course = serializers.SerializerMethodField(read_only=True, source='subscribe')
    
    
    class Meta:
        model = Course
        fields = ('pk',
                  'course_name',
                  'course_preview',
                  'description',
                  'subscribe_of_the_course',
                  'lessons',
                  'lessons_detail',
                  )
        
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
        