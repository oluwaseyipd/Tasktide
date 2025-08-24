from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import generics, permissions
from .serializers import TaskSerializer
from .models import Task
from .forms import TaskCreationForm


class TaskListView(ListView):
    model = Task
    template_name = 'core/dashboard/all_tasks.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']
    paginate_by = 8

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, completed=False).order_by('-created_at')

class CompleteTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'core/dashboard/completed_task.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, completed=True)

    

class TaskDetailView(DetailView):
    model = Task
    template_name = 'core/dashboard/single_task.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = 'core/dashboard/create_task.html'
    success_url = reverse_lazy('all_tasks')
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Task created successfully")
        return response

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskCreationForm
    template_name = 'core/dashboard/create_task.html'
    # success_url = reverse_lazy('all_tasks')
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False 


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'core/dashboard/delete_task.html'
    success_url = reverse_lazy('all_tasks')

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False 

@login_required
@require_POST
def toggle_task_complete(request, pk):
    try:
        task = Task.objects.get(pk=pk, user=request.user)
        task.completed = not task.completed   # toggle
        task.save()
        return JsonResponse({"success": True, "completed": task.completed})
    except Task.DoesNotExist:
        return JsonResponse({"success": False}, status=404)


class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)