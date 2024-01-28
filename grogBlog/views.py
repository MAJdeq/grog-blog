from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login
from blogs.forms import CustomRegistrationForm, CustomLoginForm  # Import your custom form here
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings  # Import settings module

User = get_user_model()

def register_view(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    
    return render(request, 'registration/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)  # Use settings.LOGIN_REDIRECT_URL
    else:
        form = CustomLoginForm()

    return render(request, 'registration/login.html', {'form': form})
