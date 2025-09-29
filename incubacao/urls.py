from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
app_name = 'incubacao'
from .views import (
    LoteListView, LoteCreateView, LoteDetailView,
    LoteUpdateView, LoteDeleteView
)

urlpatterns = [
    path('', LoteListView.as_view(), name='lote_lista'),
    path('index', LoteListView.as_view(), name='lote_lista'),
    path('lotes/novo/', LoteCreateView.as_view(), name='lote_criar'),
    path('lotes/<int:pk>/', LoteDetailView.as_view(), name='lote_detalhe'),
    path('lotes/<int:pk>/editar/', LoteUpdateView.as_view(), name='lote_editar'),
    path('lotes/<int:pk>/deletar/', LoteDeleteView.as_view(), name='lote_deletar'),

    path("lote/<int:lote_id>/anotacao/", views.adicionar_anotacao, name="adicionar_anotacao"),
    path("anotacao/<int:pk>/deletar/", views.anotacao_deletar, name="anotacao_deletar"),
    path('anotacao/<int:pk>/editar/', views.anotacao_editar, name='anotacao_editar'),
    
    path("register/", views.register, name="register"),

    path("listmenu/", views.listmenu, name="listmenu"),
    path("armazenamento/", views.armazenamento, name="armazenamento"),
    path("incubacao/", views.incubacao, name="incubacao"),
    path("momemnto_incubacao/", views.momemnto_incubacao, name="momemnto_incubacao"),
    path("operacao_maquina/", views.operacao_maquina, name="operacao_maquina"),
    path("controle_temperatura/", views.controle_temperatura, name="controle_temperatura"),
    path("umidade/", views.umidade, name="umidade"),
    path("viragem/", views.viragem, name="viragem"),
    path("transferecia_ovos/", views.transferecia_ovos, name="transferecia_ovos"),
    path("retirada_pintinhos/", views.retirada_pintinhos, name="retirada_pintinhos"),
    
    
    
    

   
    # path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),

    path("login/",auth_views.LoginView.as_view(template_name="login.html",authentication_form=CustomLoginForm),name="login"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    
]