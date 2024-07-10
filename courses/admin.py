from django.contrib import admin

from courses.models import Course, Lesson

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_preview', 'description',)
    
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'lesson_name', 'description', 'lesson_preview', 'video_link',)
        