from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render


# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def signup(request):
    if request.method != 'POST':
        return render(request, 'accounts/signup.html')

    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    user = request.POST.get('user')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if not name or not last_name or not user or not email or not password or \
            not password2:
        messages.error(request, 'You must fill in all fields')
        return render(request, 'accounts/signup.html')

    if len(user) < 6:
        messages.error(request, 'Create a user with more than 6 characters')
        return render(request, 'accounts/signup.html')

    if len(password) < 8:
        messages.error(request,
                       'Your password must have more than 8 characters')
        return render(request, 'accounts/signup.html')

    if password != password2:
        messages.error(request, 'Passwords do not match')
        return render(request, 'accounts/signup.html')

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Invalid email')
        return render(request, 'accounts/signup.html')

    if User.objects.filter(username=user).exists():
        messages.error(request, 'This user already exists, try another one')
        return render(request, 'accounts/signup.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'This email already exists, try another one')
        return render(request, 'accounts/signup.html')

    user_model = User.objects.create_user(
        username=user, email=email, password=password, first_name=name,
        last_name=last_name)
    user_model.save()

    messages.success(
        request, 'Registration completed successfully. Now, you must log in with your credentials.')  # noqa:E501

    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
