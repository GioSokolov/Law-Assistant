from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from legal.models import Article
from .forms import UserRegisterForm, ProfileForm, CustomContactForm


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
            # Проверка за параметър 'next'
            next_url = request.POST.get('next') or request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Некоректно потребителско име или парола")

    # Вземаме параметър 'next' за предаване в шаблона
    next_url = request.GET.get('next', '')
    return render(request, 'login.html', {'next': next_url})


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
        form = CustomContactForm(request.POST)
        if form.is_valid():
            # Извличане на данни от формата
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Изпращане на имейл
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
        else:
            messages.error(request, "Моля, попълнете формуляра коректно.")
    else:
        form = CustomContactForm()

    return render(request, "contact.html", {'form': form})


@login_required
def profile_view(request):
    # Общ брой статии на текущия потребител
    user_articles_count = Article.objects.filter(author=request.user).count()

    # Статии, чакащи одобрение
    pending_articles_count = Article.objects.filter(author=request.user, is_approved=False).count()

    # Публикувани статии
    published_articles_count = user_articles_count - pending_articles_count

    return render(request, 'profile.html', {
        'user_articles_count': user_articles_count,
        'pending_articles_count': pending_articles_count,
        'published_articles_count': published_articles_count,
    })


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Изтриваме потребителя
        messages.success(request, "Вашият профил беше успешно изтрит.")
        return redirect('index')  # Пренасочваме към началната страница

    return render(request, 'delete_profile.html')  # Шаблон за потвърждение

