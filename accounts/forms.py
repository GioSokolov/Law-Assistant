from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile
from django.contrib.auth.hashers import check_password


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


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Стара парола")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Нова парола")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Потвърдете новата парола")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError("Старата парола е неправилна.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError("Новите пароли не съвпадат.")
        return cleaned_data


class CustomContactForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        label="Име",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Име',
            'id': 'full-name',
        })
    )
    email = forms.EmailField(
        label="Имейл адрес",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имейл адрес',
            'id': 'email',
        })
    )
    message = forms.CharField(
        label="Съобщение",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Съобщение',
            'id': 'message',
        })
    )
