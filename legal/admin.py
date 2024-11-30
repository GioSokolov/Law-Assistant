from django.contrib import admin
from .models import Category, Law, Code, InterpretationDecision, DocumentFile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Law)
class LawAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('published_date', 'category')
    ordering = ('-published_date',)
    actions = ['mark_as_published']

    def mark_as_published(self, request, queryset):
        queryset.update(published_date='2024-01-01')
        self.message_user(request, "Маркираните закони са актуализирани!")
    mark_as_published.short_description = "Маркирай като публикувано"

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('published_date', 'category')
    ordering = ('-published_date',)

@admin.register(InterpretationDecision)
class InterpretativeDecisionAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('published_date', 'category')
    ordering = ('-published_date',)

@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    list_display = ('document', 'file')
    search_fields = ('document__title',)
    list_filter = ('document__category',)
