
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('clientes/', include('apps.clientes.urls', namespace='clientes')),
    path('quartos/', include('apps.quartos.urls', namespace='quartos')),
    path('empresas/', include('apps.empresas.urls', namespace='empresas')),
    path ('funcinarios/', include('apps.funcionarios.urls', namespace='funcionarios')),
]
