from django.shortcuts import render
from django.urls import reverse_lazy
from task_app import models
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from task_app.forms import TaskForm, TaskUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


# home page
# головна сторінка
class TaskListView(LoginRequiredMixin,ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "task_app/task_list.html"
    login_url = reverse_lazy("task_app:login")


    def get_queryset(self):
        return models.Task.objects.filter(creator=self.request.user)

# Actions with interference/information/creation/deletion/update
# Працця із заваданням/інформація/створення/видалення/оновлення
class TaskDetailView(LoginRequiredMixin,DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "task_app/task_detail.html"
    login_url = reverse_lazy("task_app:login")

    def get_queryset(self):
        return models.Task.objects.filter(creator=self.request.user)

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = models.Task
    template_name = "task_app/task_form.html"  
    form_class = TaskForm
    success_url = reverse_lazy("task_app:task-list")  
    login_url = reverse_lazy("task_app:login")

    def form_valid(self, form):
        # Автоматически проставляем создателя
        form.instance.creator = self.request.user  
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Task
    template_name = "task_app/task_confirm_delete.html"  
    success_url = reverse_lazy("task_app:task-list")
    login_url = reverse_lazy("task_app:login")


class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Task
    form_class = TaskUpdateForm
    template_name = "task_app/task_form.html"
    success_url = reverse_lazy("task_app:task-list")
    login_url = reverse_lazy("task_app:login")


# register/login/logout
# регістрація/логін/вийти з акаунту 

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "task_app/register.html"
    success_url = reverse_lazy("task_app:task-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)  # автоматически логиним пользователя
        return response

class UserLoginView(LoginView):
    template_name = "task_app/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("task_app:task-list")



class UserLogoutView(LogoutView):
    next_page = reverse_lazy("task_app:login")


