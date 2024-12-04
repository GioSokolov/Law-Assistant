from django import forms
from .models import Law, Code, InterpretationDecision, Article


class LawForm(forms.ModelForm):
    class Meta:
        model = Law
        fields = ['title', 'description', 'publication_date', 'document']


class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['title', 'description', 'document']


class InterpretationDecisionForm(forms.ModelForm):
    class Meta:
        model = InterpretationDecision
        fields = ['title', 'category', 'summary', 'document']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'document']