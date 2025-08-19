from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from tasks.views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [

    # Dashboard views
    path('dashboard/settings/', views.settings, name='settings'),
    path('dashboard/completed/', views.completed_tasks, name='completed_tasks'),
    path('dashboard/incomplete/', views.incomplete_tasks, name='incomplete_tasks'),
    path('dashboard/tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
    path('dashboard/tasks/<int:pk>/', TaskDetailView.as_view(), name='single_task'),
    path('dashboard/tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='update_task'),
    path('dashboard/create/', TaskCreateView.as_view(), name='create_tasks'),
    path('dashboard/tasks/', TaskListView.as_view(), name='all_tasks'),
    path('dashboard/', views.overview, name='overview'),
    path('profile/', views.profile, name='profile'),

    # Authentication views
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/home.html'), name='logout'),

    # Home view
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)