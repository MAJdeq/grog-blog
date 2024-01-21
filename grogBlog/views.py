
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from blogs.forms import CustomRegistrationForm, CustomLoginForm  # Import your custom form here
from django.contrib.auth import authenticate, login

User = get_user_model()

def register_view(request):
    form = CustomRegistrationForm()
    success_message = None

    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirmPassword')
            if password != confirm_password:
                form.add_error('confirmPassword', 'Passwords do not match')
            else:
                print("Form data:", form.cleaned_data)
                User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                success_message = 'Registration successful!'
                return redirect('home')

        # Debugging: Print form errors
        print("Form errors:", form.errors)

    return render(request, 'registration/registration.html', {'form': form, 'success_message': success_message})


def login_view(request):
    form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})