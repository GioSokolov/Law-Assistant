"""
URL configuration for law_assistant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from law_assistant import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.index, name='index'),             # Начална страница с видеото
    path('login/', main_views.login_view, name='login'),  # Страница за вход
    path('register/', main_views.register_view, name='register'),  # Регистрация
    path('contact/', main_views.contact_view, name='contact'),  # Контактна форма
    path('password-reset/', main_views.password_reset_view, name='password_reset'),  # Нулиране на парола
    path('404/', main_views.error_404_view, name='404'),   # 404 страница
    path('accounts/', include('accounts.urls')),  # Accounts URL
    path('legal/', include('legal.urls')),  # Включване на URLs за legal приложението
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




