from django.urls import path
from . import views

app_name = 'todolist_app'

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('tasks/', views.create_todo_task, name='create_todo_task'),
    path('tasks/<int:task_id>/', views.update_todo_task, name='update_todo_task'),
    path('tasks/delete/<int:task_id>/', views.delete_todo_task, name='delete_todo_task'),
]
