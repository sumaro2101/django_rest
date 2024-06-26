from rest_framework import serializers
from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Course
        fields = ('course_name',
                  'course_preview',
                  'description',
                  )
        

class LessonSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Lesson
        fields = ('course_id',
                  'lesson_name',
                  'descriptons',
                  'lesson_preview',
                  'video_link',
                  )
        