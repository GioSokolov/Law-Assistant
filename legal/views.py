from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from .models import Law, Code, InterpretationDecision
from PyPDF2 import PdfReader


class CodesListView(ListView):
    model = Code
    template_name = 'codes.html'
    context_object_name = 'codes'


class LawsListView(ListView):
    model = Law
    template_name = 'laws.html'
    context_object_name = 'laws'


class InterpretationsCategoriesView(TemplateView):
    template_name = 'interpretations.html'


class InterpretationsListView(ListView):
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


class LawDetailView(DetailView):
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


class CodeDetailView(DetailView):
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


class InterpretationDetailView(DetailView):
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
