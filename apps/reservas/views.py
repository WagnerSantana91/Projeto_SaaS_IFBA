from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.clientes.models import Cliente, Veiculo
from apps.quartos.models import Quarto
from apps.pagamentos.models import Entrada        
from .models import Reserva, Pessoa

@login_required
def criar_reserva(request, quarto_id):
    if request.method == "POST":

              
        quarto_obj = Quarto.objects.get(id=quarto_id)        

               
        
        placa_normalizada = (request.POST.get('placa') or '').replace('-', '').replace(' ', '').upper()        
        veiculo, veiculo_criado = Veiculo.objects.get_or_create(        
            placa=placa_normalizada,        
            defaults={        
                'cor': request.POST.get('cor') or 'outro',        
                'cor_personalizada': request.POST.get('cor_personalizada'),        
                'modelo': request.POST.get('modelo') or '',        
                'imagem': request.FILES.get('imagem'),        
                'modo_conducao': request.POST.get('modo_conducao') or 'proprio',        
            }        
        )        

               
        if not veiculo_criado:        
            veiculo.modelo = request.POST.get('modelo') or veiculo.modelo        
            veiculo.cor = request.POST.get('cor') or veiculo.cor        
            veiculo.save()        


        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')

        cliente, created = Cliente.objects.get_or_create(
            cpf=cpf,
            defaults={'nome': nome, 'veiculo': veiculo}
        )
        

        if not created:
            cliente.veiculo = veiculo
            cliente.save()

        # 3. RESERVA
        reserva = Reserva.objects.create(
            cliente=cliente,
            quarto_id=quarto_id,
            modo_conducao=request.POST.get('modo_conducao'),
            veiculo_principal=veiculo
        )

        # 4. PESSOAS (Adicionais da reserva)
        nomes = request.POST.getlist('nome_pessoa[]')
        cpfs = request.POST.getlist('cpf_pessoa[]')
        estrangeiros = request.POST.getlist('estrangeiro[]')

        for i in range(len(nomes)):
            Pessoa.objects.create(
                reserva=reserva,
                nome=nomes[i],
                cpf=cpfs[i],
                estrangeiro=(str(i) in estrangeiros)
            )


        Entrada.objects.create(        
            cliente=cliente,        
            valor=quarto_obj.valor_hora,        
            forma_pagamento=request.POST.get('forma_pagamento', 'dinheiro'),        
        )        

        return redirect('quartos:dashboard')

    return render(request, 'reservas/modal.html')

@login_required
def dashboard_reservas(request):
    quartos = Quarto.objects.all()
    return render(request, 'reservas/dashboard.html', {'quartos': quartos})
