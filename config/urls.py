
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('quartos/', include('apps.quartos.urls')),
    path('empresas/', include('apps.empresas.urls')),
    path ('funcinarios/', include('apps.funcionarios.urls')),
]
