from django.urls import path
from . import views
from apps.core.views import login_view


app_name = 'core'
urlpatterns = [
    path('', login_view, name='login'),  # Usa a função
    path('dashboard/', views.dashboard, name='dashboard'),
    path ('logout/', views.logout_view, name='logout'),
    
]