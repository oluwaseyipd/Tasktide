from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def register(request):
    return render(request, 'core/register.html')

def login(request):
    return render(request, 'core/login.html')

def overview(request):
    return render(request, 'core/dashboard/overview.html')

def all_tasks(request):
    return render(request, 'core/dashboard/all_tasks.html')

def create_tasks(request):
    return render(request, 'core/dashboard/create_task.html')

def completed_tasks(request):
    return render(request, 'core/dashboard/completed_task.html')

def incomplete_tasks(request):
    return render(request, 'core/dashboard/incomplete_task.html')
