from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm



# Homepage view
def home(request):
    return render(request, 'core/home.html')

# Login page view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, F'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/auth/register.html', {'form':form})

@login_required
def settings(request):
    return render(request, 'core/dashboard/settings.html')

