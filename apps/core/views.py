from django.shortcuts import render
from apps.clientes.models import Cliente
#from apps.reservas.models import Reserva
from apps.quartos.models import Quarto


#Essa função é responsável por exibir o dashboard, onde é possível visualizar o total de clientes
#cadastrados. Ela consulta o banco de dados para contar o número de clientes e passa essa informação
#para o template 'dashboard.html' através do contexto. O template pode então exibir essa informação de forma visual para o usuário.

def dashboard(request):
    total_clientes = Cliente.objects.count()
    #total_reservas_hoje = Reserva.objects.filter (data_reserva__date=timezone.now().date()).count()
    total_quartos_disponiveis = Quarto.objects.filter (status='disponivel').count()

    context = {'total_clientes': total_clientes,
               #'total_reservas_hoje': total_reservas_hoje,
               'total_quartos_disponiveis': total_quartos_disponiveis
               }
    return render (request, 'dashboard.html', context)



#def dashboard(request):
#    return render(request, 'dashboard.html')