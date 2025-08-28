from django.urls import path
from task_app import views
from django.contrib.auth import views as auth_views

app_name = "task_app"


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),

    path('', views.TaskListView.as_view(), name="task-list"),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task-detail"),
    path('task-create/', views.TaskCreateView.as_view(), name="task-create"),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name="task-delete"),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name="task-update"),
    path('<int:pk>/complete/', views.TaskCompleteView.as_view(), name="task-complete"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    # path("comments/", views.CommentListView.as_view(), name="comments"),
    # path("tasks/<int:task_id>/add-comments/", views.CommentCreateView.as_view(), name="comments-create"),



]
