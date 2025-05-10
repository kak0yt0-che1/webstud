from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.utils import timezone

class UserLessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'lesson')  # нельзя пройти один и тот же урок дважды

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'✔' if self.is_completed else '✘'}"

class CustomUser(AbstractUser):
    is_subscribed = models.BooleanField(default=False)
    used_temp_password = models.BooleanField(default=False)  # 🔥 Добавили это поле

    def __str__(self):
        return self.username
    
from django.db import models

class Course(models.Model):
    LANGUAGE_CHOICES = [
        ('HTML', 'HTML'),
        ('Go', 'Go'),
        ('Python', 'Python'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='HTML')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.course.title} — {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    task_type = models.CharField(
        max_length=10,
        choices=[
            ('none', 'Нет задания'),
            ('test', 'Тест'),
            ('html', 'HTML/JS задание'),
        ],
        default='none'
    )
    html_task_description = models.TextField(blank=True, null=True)
    html_expected_code = models.TextField(blank=True, null=True)
    video_url = models.URLField(
        "YouTube-ссылка",
        blank=True,
        null=True,
        help_text="Полная ссылка вида https://www.youtube.com/watch?v=VIDEO_ID"
    )

    def __str__(self):
        return f"{self.module.title} — {self.title}"



    def __str__(self):
        return f"{self.module.title} — {self.title}"

