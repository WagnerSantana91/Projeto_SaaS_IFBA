from django.urls import path
from . import views

app_name = 'quartos'

urlpatterns = [
    path('lista/', views.listar_quartos, name='listar_quartos'),
    path('cadastro/', views.criar_quarto, name='criar_quarto'),
]