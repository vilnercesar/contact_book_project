from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import FormContact


# Create your views here.
def login(request):

    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    user_field = request.POST.get('user')
    password_field = request.POST.get('password')

    user = auth.authenticate(
        request, username=user_field, password=password_field)
    if not user:
        messages.error(request, 'Invalid user or password, please try again')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login successfully')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index')


def signup(request):
    if request.method != 'POST':
        return render(request, 'accounts/signup.html')

    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    user_field = request.POST.get('user')
    email = request.POST.get('email')
    password_field = request.POST.get('password')
    password2 = request.POST.get('password2')

    if not name or not last_name or not user_field or not email \
            or not password_field or not password2:
        messages.error(request, 'You must fill in all fields')
        return render(request, 'accounts/signup.html')

    if len(user_field) < 6:
        messages.error(request, 'Create a user with more than 6 characters')
        return render(request, 'accounts/signup.html')

    if len(password_field) < 8:
        messages.error(request,
                       'Your password must have more than 8 characters')
        return render(request, 'accounts/signup.html')

    if password_field != password2:
        messages.error(request, 'Passwords do not match')
        return render(request, 'accounts/signup.html')

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Invalid email')
        return render(request, 'accounts/signup.html')

    if User.objects.filter(username=user_field).exists():
        messages.error(request, 'This user already exists, try another one')
        return render(request, 'accounts/signup.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'This email already exists, try another one')
        return render(request, 'accounts/signup.html')

    messages.success(
        request, 'Registration completed successfully. Now, you must log in with your credentials.')  # noqa:E501

    user = User.objects.create_user(
        username=user_field, email=email, password=password_field, first_name=name,  # noqa: E501
        last_name=last_name)
    user.save()

    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContact(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Error submitting form')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    description = request.POST.get('description')

    if len(description) < 5:
        messages.error(request, 'Short description')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, 'Sucessfully contact created')
    return redirect('dashboard')
