from django.urls import path
from . import views

app_name = 'incubacao'
from .views import (
    LoteListView, LoteCreateView, LoteDetailView,
    LoteUpdateView, LoteDeleteView
)

urlpatterns = [
    path('', LoteListView.as_view(), name='lote_lista'),
    path('lotes/novo/', LoteCreateView.as_view(), name='lote_criar'),
    path('lotes/<int:pk>/', LoteDetailView.as_view(), name='lote_detalhe'),
     path('lotes/<int:pk>/editar/', LoteUpdateView.as_view(), name='lote_editar'),
    path('lotes/<int:pk>/deletar/', LoteDeleteView.as_view(), name='lote_deletar'),
    
    
]