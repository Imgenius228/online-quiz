from django.urls import path
from . import views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

app_name = 'quiz'

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('quiz_home/', views.quiz_home, name='quiz_home'),
    path('', views.index, name='quiz_home'),
    path('<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('', views.home_redirect, name='home'),
    path('register/', views.register, name='register'),
    path('quiz_home/', views.quiz_home, name='quiz_home'),
    path('', views.home_redirect, name='home'),
    path('join/', views.join_quiz_by_code, name='join_quiz'),
    path('my-results/', views.my_results, name='my_results'),
    path('create/', views.create_quiz, name='create_quiz'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def index(request):
    return render(request, 'index.html')