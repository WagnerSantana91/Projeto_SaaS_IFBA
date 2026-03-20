from django.urls import path
from .views import criar_reserva, dashboard_reservas

app_name = 'reservas'

urlpatterns = [
    path('criar/<int:quarto_id>/', criar_reserva, name='criar_reserva'),
    path('', dashboard_reservas, name='dashboard_reservas'),
]