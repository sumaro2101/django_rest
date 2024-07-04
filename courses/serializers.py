from rest_framework import serializers

from courses.models import Course, Lesson
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
    
    class Meta:
        model = Course
        fields = ('pk',
                  'course_name',
                  'course_preview',
                  'description',
                  'lessons',
                  'lessons_detail',
                  )
        
    def get_lessons(self, instance):
        return instance.lessons.get_queryset().count()
        