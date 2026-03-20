from django.urls import path       
from . import views       

app_name = 'pagamentos'       

urlpatterns = [       
    path('financeiro/', views.financeiro_dashboard, name='financeiro_dashboard'),       
    path('financeiro/nova-entrada/', views.nova_entrada, name='nova_entrada'),       
    path('financeiro/nova-saida/', views.nova_saida, name='nova_saida'),       
]       
