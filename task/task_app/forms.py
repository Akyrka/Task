from django import forms
from task_app.models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "end_time","priority"]

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "end_time","priority"]

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        help_texts = {
            "username": "",
            "password1": "",
            "password2": "",
        }