from django.contrib import admin

from course.models import Course, Category, Question, QuestionOption, UserCourse, QuestionAnswer, Lecture, MultiTest


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name', )


@admin.register(Category)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade')
    search_fields = ('name', )
    autocomplete_fields = ('course', )


@admin.register(Question)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'category')
    list_display = ('id', 'title', 'category')
    autocomplete_fields = ('category', )


@admin.register(QuestionOption)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ('question__title', 'option_text')
    list_display = ('id', 'option_text', 'question', 'value')
    autocomplete_fields = ('question', )


@admin.register(QuestionAnswer)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'option', 'attempt_counter')
    autocomplete_fields = ('user', 'question', 'option')


@admin.register(UserCourse)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category')
    autocomplete_fields = ('user', 'category')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'priority')
    autocomplete_fields = ('category', )


@admin.register(MultiTest)
class MultiTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'result')
    autocomplete_fields = ('user', )
