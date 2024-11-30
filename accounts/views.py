from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Пренасочване към таблото след регистрация
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def edit_profile(request):
    user = request.user  # Получаване на текущия потребител
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        username = request.POST.get('username')  # Получаване на новото потребителско име от формуляра
        if profile_form.is_valid():
            if username:
                user.username = username  # Обновяване на потребителското име
                user.save()
            profile_form.save()
            messages.success(request, "Профилът е актуализиран успешно!")
            return redirect('dashboard')
        else:
            messages.error(request, "Моля, коригирайте грешките във формуляра.")
    else:
        profile_form = ProfileForm(instance=user.profile)
    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'current_username': user.username,  # Добавяне на текущото потребителско име към контекста
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # Replace 'dashboard' with your actual dashboard URL
        else:
            messages.error(request, "Некоректно потребителско име или парола")
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.info(request, "Успешно излязохте от профила си.")
    return redirect('index')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Запазва сесията активна след смяна на парола
            messages.success(request, 'Вашата парола беше успешно променена.')
            return redirect('dashboard')  # Препраща към таблото за навигация
        else:
            messages.error(request, 'Моля, коригирайте грешките по-долу.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'password-reset.html', {'form': form})



def contact(request):
    if request.method == "POST":
        full_name = request.POST.get("full-name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Валидация на полетата
        if not full_name or not email or not message:
            messages.error(request, "Моля, попълнете всички полета.")
            return render(request, "contact.html")

        # Логика за изпращане на имейл
        subject = f"Контактно съобщение от {full_name}"
        try:
            send_mail(
                subject,
                message,
                email,
                ['your_email@gmail.com'],  # Замени с твоя имейл
                fail_silently=False,
            )
            messages.success(request, "Вашето съобщение беше изпратено успешно!")
            return redirect("contact")  # Замени с подходящата страница
        except Exception as e:
            messages.error(request, f"Възникна грешка: {e}")
            return render(request, "contact.html")

    return render(request, "contact.html")


@login_required
def profile_view(request):
    return render(request, 'profile.html')

