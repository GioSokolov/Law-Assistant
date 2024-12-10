from django.urls import path
from .views import (
    CodesListView, LawsListView, InterpretationsCategoriesView,
    InterpretationsListView, LawDetailView, CodeDetailView, InterpretationDetailView, articles_list,
    add_comment, toggle_like, ArticleDetailView, add_article, delete_article
)

urlpatterns = [
    path('laws/', LawsListView.as_view(), name='laws_list'),
    path('laws/<int:pk>/', LawDetailView.as_view(), name='law_detail'),
    path('codes/', CodesListView.as_view(), name='codes_list'),
    path('codes/<int:pk>/', CodeDetailView.as_view(), name='code_detail'),
    path('interpretations/', InterpretationsCategoriesView.as_view(), name='interpretations_categories'),
    path('interpretations/<int:pk>/', InterpretationDetailView.as_view(), name='interpretation_detail'),
    path('interpretations/<str:category>/', InterpretationsListView.as_view(), name='interpretations_list'),
    path('articles/', articles_list, name='articles_list'),
    path('articles/add/', add_article, name='add_article'),  # Този маршрут трябва да е преди slug маршрута
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('articles/<slug:slug>/like/', toggle_like, name='toggle_like'),
    path('articles/<slug:slug>/delete/', delete_article, name='delete_article'),
]
