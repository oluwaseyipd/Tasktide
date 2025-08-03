from django.urls import path
from .views import home, register, login, overview, all_tasks, create_tasks , completed_tasks, incomplete_tasks

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('dashboard/', overview, name='overview'),
    path('dashboard/all-tasks/', all_tasks, name='all_tasks'),
    path('dashboard/create-task/', create_tasks, name='create_tasks'),
    path('dashboard/completed-tasks/', completed_tasks, name='completed_tasks'),
    path('dashboard/incomplete-tasks/', incomplete_tasks, name='incomplete_tasks'),
]