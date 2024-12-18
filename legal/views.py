from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, DetailView
from .forms import ArticleForm
from .models import Law, Code, InterpretationDecision, Article, ArticleComment, ArticleLike
from PyPDF2 import PdfReader
from django.contrib.auth.mixins import LoginRequiredMixin


class CodesListView(LoginRequiredMixin, ListView):
    model = Code
    template_name = 'codes.html'
    context_object_name = 'codes'


class LawsListView(LoginRequiredMixin, ListView):
    model = Law
    template_name = 'laws.html'
    context_object_name = 'laws'


class InterpretationsCategoriesView(LoginRequiredMixin, TemplateView):
    template_name = 'interpretations.html'


class InterpretationsListView(LoginRequiredMixin, ListView):
    model = InterpretationDecision
    template_name = 'interpretations_list.html'
    context_object_name = 'decisions'

    def get_queryset(self):
        category = self.kwargs.get('category')
        return InterpretationDecision.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_map = {
            'labor': 'Трудови',
            'family': 'Семейни'
        }
        context['category'] = category_map.get(self.kwargs.get('category'), 'Неизвестна категория')
        return context


class LawDetailView(LoginRequiredMixin, DetailView):
    model = Law
    template_name = 'law_detail.html'
    context_object_name = 'law'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        law = self.object
        document_content = None

        if law.document.name.endswith('.txt'):
            try:
                with law.document.open('r') as file:
                    document_content = file.read()
            except Exception:
                document_content = "Грешка при зареждането на документа."
        elif law.document.name.endswith('.pdf'):
            try:
                pdf_reader = PdfReader(law.document)
                document_content = "\n".join(page.extract_text() for page in pdf_reader.pages)
            except Exception:
                document_content = "Грешка при зареждането на PDF документа."

        context['document_content'] = document_content
        return context


class CodeDetailView(LoginRequiredMixin, DetailView):
    model = Code
    template_name = 'code_detail.html'
    context_object_name = 'code'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.object
        document_content = None

        if code.document.name.endswith('.txt'):
            try:
                with code.document.open('r') as file:
                    document_content = file.read()
            except Exception:
                document_content = "Грешка при зареждането на документа."
        elif code.document.name.endswith('.pdf'):
            try:
                pdf_reader = PdfReader(code.document)
                document_content = "\n".join(page.extract_text() for page in pdf_reader.pages)
            except Exception:
                document_content = "Грешка при зареждането на PDF документа."

        context['document_content'] = document_content
        return context


class InterpretationDetailView(LoginRequiredMixin, DetailView):
    model = InterpretationDecision
    template_name = 'interpretation_detail.html'
    context_object_name = 'interpretation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interpretation = self.object
        document_content = None

        if interpretation.document.name.endswith('.txt'):
            try:
                with interpretation.document.open('r') as file:
                    document_content = file.read()
            except Exception:
                document_content = "Грешка при зареждането на документа."
        elif interpretation.document.name.endswith('.pdf'):
            try:
                pdf_reader = PdfReader(interpretation.document)
                document_content = "\n".join(page.extract_text() for page in pdf_reader.pages)
            except Exception:
                document_content = "Грешка при зареждането на PDF документа."

        context['document_content'] = document_content
        return context


def articles_list(request):
    # Показваме само одобрените статии, подредени по дата на публикуване
    articles = Article.objects.filter(is_approved=True).order_by('-published_date')
    return render(request, 'articles.html', {'articles': articles})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        # Разрешаваме достъп само до одобрени статии
        obj = super().get_object(queryset)
        if not obj.is_approved:
            raise Http404("Статията не е одобрена.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        # Проверка дали потребителят е харесал статията
        liked = False
        if self.request.user.is_authenticated:
            liked = ArticleLike.objects.filter(article=article, user=self.request.user).exists()

        # Извличане на съдържание на документа
        document_content = None
        if article.document:
            if article.document.name.endswith('.txt'):
                try:
                    with article.document.open('r') as file:
                        document_content = file.read()
                except Exception as e:
                    document_content = f"Грешка при зареждането на документа: {str(e)}"
            elif article.document.name.endswith('.pdf'):
                try:
                    with article.document.open('rb') as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        document_content = "\n".join(page.extract_text() for page in pdf_reader.pages)
                except Exception as e:
                    document_content = f"Грешка при зареждането на PDF документа: {str(e)}"

        # Коментари и статус за харесване
        comments = ArticleComment.objects.filter(article=article).order_by('-created_at')
        context['document_content'] = document_content
        context['comments'] = comments
        context['liked'] = liked
        return context


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Вашата статия беше изпратена за одобрение.")
            return redirect('articles_list')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})


@login_required
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)

    # Увери се, че само авторът може да изтрие статията
    if article.author != request.user:
        return HttpResponseForbidden("Нямате право да изтривате тази статия.")

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Статията беше успешно изтрита.")
        return redirect('articles_list')

    return render(request, 'articles.html', {'article': article})


@login_required
def add_comment(request, slug):
    if request.method == 'POST':
        article = get_object_or_404(Article, slug=slug)
        content = request.POST.get('content')
        if content:
            ArticleComment.objects.create(article=article, author=request.user, content=content)
    return redirect('article_detail', slug=slug)


@login_required
def toggle_like(request, slug):
    article = get_object_or_404(Article, slug=slug)
    like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)

    if not created:
        like.delete()

    likes_count = ArticleLike.objects.filter(article=article).count()
    return JsonResponse({'liked': created, 'likes_count': likes_count})