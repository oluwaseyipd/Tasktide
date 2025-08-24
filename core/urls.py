from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views
from tasks.views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, CompleteTaskListView, task_overview
from tasks import views as task_views
from tasks.views import TaskViewSet
from users import views as user_views



router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),

    path("tasks/<int:pk>/toggle/", task_views.toggle_task_complete, name="toggle_task"),
    # Dashboard views
    path('dashboard/settings/', views.settings, name='settings'),
    path('dashboardprofile/', user_views.profile, name='profile'),
    path('dashboard/completed/', CompleteTaskListView.as_view(), name='completed_tasks'),
    path('dashboard/tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
    path('dashboard/tasks/<int:pk>/', TaskDetailView.as_view(), name='single_task'),
    path('dashboard/tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='update_task'),
    path('dashboard/create/', TaskCreateView.as_view(), name='create_tasks'),
    path('dashboard/tasks/', TaskListView.as_view(), name='all_tasks'),
    path('dashboard/', task_views.task_overview, name='overview'),

    # Authentication views
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/home.html'), name='logout'),

    # Home view
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)