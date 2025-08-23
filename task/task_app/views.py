from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from task_app import models
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from task_app.forms import TaskForm, TaskUpdateForm, TaskFilterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from task_app.mixins import  UserIsOwnerMixin
from django.http import HttpResponseRedirect


# home page
# головна сторінка
class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "task_app/task_list.html"
    login_url = reverse_lazy("task_app:login")


    def get_queryset(self):
        queryset = models.Task.objects.all().order_by("-id")  # все задачи
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context


    

# Actions with interference/information/creation/deletion/update
# Працця із заваданням/інформація/створення/видалення/оновлення
class TaskDetailView(LoginRequiredMixin,DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "task_app/task_detail.html"
    login_url = reverse_lazy("task_app:login")

    # def get_queryset(self):
        # return models.Task.objects.filter(creator=self.request.user)
    

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

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin,DeleteView):
    model = models.Task
    template_name = "task_app/task_confirm_delete.html"  
    success_url = reverse_lazy("task_app:task-list")
    login_url = reverse_lazy("task_app:login")


class TaskUpdateView(LoginRequiredMixin,UserIsOwnerMixin,UpdateView):
    model = models.Task
    form_class = TaskUpdateForm
    template_name = "task_app/task_form.html"
    success_url = reverse_lazy("task_app:task-list")
    login_url = reverse_lazy("task_app:login")

class TaskCompleteView(LoginRequiredMixin,UserIsOwnerMixin,View):
    def post(self, request, *args,**kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return  HttpResponseRedirect(reverse_lazy("task_app:task-list"))
    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(models.Task, pk=task_id)

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


