from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid




class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    invite_code = models.CharField(max_length=10, blank=True, null=True)
    times_taken = models.PositiveIntegerField(default=0)  # 👈 добавили это поле

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Question(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    QUESTION_TYPES = [
        (TEXT, 'Текст'),
        (IMAGE, 'Зображення'),
        (VIDEO, 'Відео'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=TEXT)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    time_limit = models.PositiveIntegerField(help_text="Час (в секундах) на запитання", default=30)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
