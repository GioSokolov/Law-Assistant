from django.urls import path
from .views import (
    CodesListView, LawsListView, InterpretationsCategoriesView,
    InterpretationsListView, LawDetailView, CodeDetailView, InterpretationDetailView
)

urlpatterns = [
    path('laws/', LawsListView.as_view(), name='laws_list'),
    path('laws/<int:pk>/', LawDetailView.as_view(), name='law_detail'),
    path('codes/', CodesListView.as_view(), name='codes_list'),
    path('codes/<int:pk>/', CodeDetailView.as_view(), name='code_detail'),
    path('interpretations/', InterpretationsCategoriesView.as_view(), name='interpretations_categories'),
    path('interpretations/<int:pk>/', InterpretationDetailView.as_view(), name='interpretation_detail'),
    path('interpretations/<str:category>/', InterpretationsListView.as_view(), name='interpretations_list'),
]
