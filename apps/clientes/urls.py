from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('lista/', views.listar_clientes, name='listar_clientes'),
    path('cadastro/', views.criar_cliente, name='criar_cliente'),
    path("editar/<int:id>/", views.editar_cliente, name="editar_cliente"),  #Will


]