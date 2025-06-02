from django.urls import path
from . import views
from django.shortcuts import render

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='quiz_home'),
    path('<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
]


def index(request):
    return render(request, 'index.html')