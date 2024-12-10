from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'document']
        labels = {
            'title': 'Заглавие',
            'image': 'Снимка',
            'document': 'Документ',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control custom-field',
                'placeholder': 'Въведете заглавие',
            }),
            'document': forms.ClearableFileInput(attrs={
                'class': 'form-control custom-field',
            }),
        }