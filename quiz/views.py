from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Quiz, Question, Answer
from .forms import QuizForm

def index(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/index.html', {'quizzes': quizzes})

from django.shortcuts import render, get_object_or_404
from .models import Quiz
from .forms import QuizForm

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            user_answers = {}
            correct_answers = {}
            score = 0

            for question in questions:
                answer_id = form.cleaned_data.get(f"question_{question.id}")
                user_answers[question] = answer_id

            # Заполняем correct_answers словарём с ключом — строкой id вопроса, значением — id правильного ответа
            for question in questions:
                correct = question.answers.filter(is_correct=True).first()
                if correct:
                    correct_answers[str(question.id)] = correct.id

            # Подсчёт правильных ответов (score)
            for question, answer_id in user_answers.items():
                correct_id = correct_answers.get(str(question.id))
                if correct_id and str(answer_id) == str(correct_id):
                    score += 1

            total_questions = questions.count()

            return render(request, 'quiz/results.html', {
                'quiz': quiz,
                'user_answers': user_answers,
                'correct_answers': correct_answers,
                'score': score,
                'total_questions': total_questions,
                'questions': questions,
            })
    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'form': form,
    })

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/quiz_results.html', {'quiz': quiz})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def quiz_home(request):
    return render(request, 'quiz/home.html')



