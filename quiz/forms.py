from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)

        # Генерируем поля для каждой викторины
        for question in questions:
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                label=question.text,
                choices=[(answer.id, answer.text) for answer in question.answers.all()],
                widget=forms.RadioSelect,
                required=False   # <-- Теперь не обязательно отвечать на все вопросы
            )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
