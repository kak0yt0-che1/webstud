from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Course, Module, Lesson, CustomUser

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['course', 'title']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'module',
            'title',
            'content',
            'task_type',
            'html_task_description',
            'html_expected_code',
            'video_url',
        ]

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']