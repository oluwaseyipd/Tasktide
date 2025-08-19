from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task
from .forms import TaskCreationForm


class TaskListView(ListView):
    model = Task
    template_name = 'core/dashboard/all_tasks.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']
    paginate_by = 2

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
        return super().form_valid(form)

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
