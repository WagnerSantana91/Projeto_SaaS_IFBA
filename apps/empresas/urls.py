from django.urls import path
from .import views

app_name = 'empresas'

urlpatterns = [
    path('', views.listar_empresas, name='listar_empresas'),
    path('criar/', views.criar_empresa, name='criar_empresa'),
    path("editar/<int:id>/", views.editar_empresa, name="editar_empresa"),  #Will
]
