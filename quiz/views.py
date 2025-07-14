from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Quiz, Question, Answer
from .forms import QuizForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import Group

def index(request):
    query = request.GET.get('q', '')
    quizzes = Quiz.objects.all()

    if query:
        quizzes = quizzes.filter(title__icontains=query)
        return render(request, 'quiz/index.html', {
            'quizzes': quizzes,
            'query': query,
        })

    new_quizzes = quizzes.order_by('-created_at')[:5]
    popular_quizzes = quizzes.order_by('-times_taken')[:5]

    return render(request, 'quiz/index.html', {
        'new_quizzes': new_quizzes,
        'popular_quizzes': popular_quizzes,
        'query': '',
    })

from django.shortcuts import render, get_object_or_404
from .models import Quiz
from .forms import QuizForm

from django.shortcuts import render, get_object_or_404
from .models import Quiz
from .forms import QuizForm

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            raw_answers = form.cleaned_data

            user_answers = {
                key.replace('question_', ''): str(value)
                for key, value in raw_answers.items()
            }

            correct_answers = {}
            score = 0

            for question in questions:
                correct = question.answers.filter(is_correct=True).first()
                correct_id = str(correct.id) if correct else ''
                qid = str(question.id)
                user_answer = user_answers.get(qid, '')

                correct_answers[qid] = correct_id

                if user_answer == correct_id:
                    score += 1

            quiz.times_taken += 1
            quiz.save()

            return render(request, 'quiz/results.html', {
                'quiz': quiz,
                'user_answers': user_answers,
                'correct_answers': correct_answers,
                'score': score,
                'total_questions': questions.count(),
                'questions': questions,
            })
    else:
        form = QuizForm(questions=questions)
        form_questions = list(zip(form, questions))

    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'form': form,
        'form_questions': form_questions,
    })



def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/quiz_results.html', {'quiz': quiz})

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('quiz:index')
    return redirect('quiz:login')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='Користувач')
            user.groups.add(group)

            login(request, user)
            return redirect('quiz:index')
    else:
        form = RegistrationForm()
    return render(request, 'quiz/register.html', {'form': form})

@login_required(login_url='/register/')
def quiz_home(request):
    return render(request, 'quiz/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('quiz:index')
        else:
            messages.error(request, "Неправильный логин или пароль")
    return render(request, 'quiz/login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('quiz:login')


def join_quiz_by_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            quiz = Quiz.objects.get(invite_code=code)
            return redirect('quiz:take_quiz', quiz_id=quiz.id)
        except Quiz.DoesNotExist:
            messages.error(request, "Код не знайдено 😢")

    return render(request, 'quiz/join_quiz.html')


