from rest_framework import serializers
from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Course
        fields = ('pk',
                  'course_name',
                  'course_preview',
                  'description',
                  )
        

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
        