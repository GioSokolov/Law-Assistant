from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def contact_view(request):
    return render(request, 'contact.html')

def password_reset_view(request):
    return render(request, 'password-reset.html')

def error_404_view(request, exception=None):
    return render(request, '404.html')

