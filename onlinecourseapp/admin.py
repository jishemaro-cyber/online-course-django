from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from courses.models import Course, Lesson, Instructor, Learner, Enrollment
from .models import Question, Choice, Submission


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [LessonInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'course', 'lesson', 'grade')
    list_filter = ('course', 'lesson')
    search_fields = ('question_text',)
    inlines = [ChoiceInline]


class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_time', 'total_learners')


class LearnerAdmin(admin.ModelAdmin):
    list_display = ('user',)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('learner', 'course', 'enrollment_date')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
