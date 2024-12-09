from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile, ForumPost, ForumComment


# Форма за регистрация на потребител
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Форма за профил на потребителя
class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Потребителско име"
    )

    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'phone_number']

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if user_instance:
            self.fields['username'].initial = getattr(user_instance, 'username', None)

    def clean_username(self):
        """Проверяваме дали потребителското име е уникално."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError("Потребителското име вече е заето.")
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        user_instance = self.instance.user  # Свързаният User обект
        user_instance.username = self.cleaned_data['username']  # Актуализираме потребителското име
        if commit:
            user_instance.save()  # Запазваме потребителя
            profile.save()  # Запазваме профила
        return profile
