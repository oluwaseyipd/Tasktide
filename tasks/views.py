from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django.utils import timezone
from .serializers import TaskSerializer
from .models import Task
from .forms import TaskCreationForm

# Task views
class TaskListView(ListView):
    model = Task
    template_name = 'core/dashboard/all_tasks.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']
    paginate_by = 8

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user, completed=False).order_by('-created_at')
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(title__icontains=search)

        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

# Completed tasks view
class CompleteTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'core/dashboard/completed_task.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, completed=True).order_by('-created_at')


# Task detail view
class TaskDetailView(DetailView):
    model = Task
    template_name = 'core/dashboard/single_task.html'


# Task creation view
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
    

# Task update view
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
    

# Task deletion view
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'core/dashboard/delete_task.html'
    success_url = reverse_lazy('all_tasks')

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False 
    

# Task viewset
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # restrict tasks to logged-in user
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Search fields
    search_fields = ["title", "description"]

    # Filter fields
    filterset_fields = ["completed", "due_date", "created_at"]

    # Ordering
    ordering_fields = ["due_date", "created_at"]
    ordering = ["created_at"]  # default order


# Task overview page 
@login_required
def task_overview(request):
    user = request.user
    tasks = Task.objects.filter(user=user)

    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    overdue = tasks.filter(completed=False, due_date__lt=timezone.now()).count()
    pending = tasks.filter(completed=False, due_date__gte=timezone.now()).count()

      # Pending just for today
    today = timezone.now().date()
    pending_today = tasks.filter(completed=False, due_date__date=today).count()

    context = {
        "total": total,
        "completed": completed,
        "overdue": overdue,
        "pending": pending,
        "pending_today": pending_today, 
    }
    return render(request, 'core/dashboard/overview.html', context)


# Task completion toggle
@login_required
@require_POST
def toggle_task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({
    "success": True,
    "completed": task.completed,
    "stats": {
        "completed": Task.objects.filter(user=request.user, completed=True).count(),
        "pending": Task.objects.filter(user=request.user, completed=False).count(),
    }
})
