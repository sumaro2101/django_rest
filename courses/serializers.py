from rest_framework import serializers
from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    
    lessons = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Course
        fields = ('pk',
                  'course_name',
                  'course_preview',
                  'description',
                  'lessons',
                  )
        
    def get_lessons(self, instance):
        return instance.lessons.get_queryset().count()
        

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
        