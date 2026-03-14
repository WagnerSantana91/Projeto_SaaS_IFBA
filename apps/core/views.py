from django.shortcuts import render, redirect
from apps.clientes.models import Cliente
from apps.quartos.models import Quarto
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def dashboard(request):
    """View do dashboard com estatísticas"""
    total_clientes = Cliente.objects.count()
    total_quartos_disponiveis = Quarto.objects.filter(status='disponivel').count()

    context = {
        'total_clientes': total_clientes,
        'total_quartos_disponiveis': total_quartos_disponiveis
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    """View responsável pelo login do usuário"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autentica o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login bem-sucedido
            login(request, user)
            return redirect('core:dashboard')
        else:
            # Login falhou
            messages.error(request, 'Usuário ou senha inválidos.')
    
    # Se for GET, mostra a página de login
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    #messages.success(request, 'Logout realizado com sucesso.')
    return redirect('core:login')