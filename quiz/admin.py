from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'quiz', 'question_type', 'time_limit')

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'created_at')
    search_fields = ('title',)

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)