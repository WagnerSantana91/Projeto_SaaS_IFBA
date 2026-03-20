from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    path('lista/', views.lista_funcionarios, name='listar_funcionarios'),
    path('criar/', views.criar_funcionario, name='criar_funcionario'),
    path('editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('excluir/<int:id>/', views.excluir_funcionario, name='excluir_funcionario'),
    path('buscar-cep/', views.buscar_cep, name='buscar_cep'),
]
