from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Тук импортираме auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Добавяне на път към таблото
    path('password_reset/', views.change_password, name='password_reset'),
    path("contact/", views.contact, name="contact"),
    path('profile/', views.profile_view, name='profile'),
]
