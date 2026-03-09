from django.urls import path
from . import views

app_name = 'quartos'

urlpatterns = [
    path('lista/', views.listar_quartos, name='listar_quartos'),
    path('cadastro/', views.criar_quarto, name='criar_quarto'),
    path("editar/<int:id>/", views.editar_quarto, name="editar_quarto"),  #Will
    path('excluir/<int:id>/', views.excluir_quarto, name = 'excluir_quarto'), #Incrementando botão de excluir
]