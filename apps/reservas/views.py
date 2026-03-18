from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.clientes.models import Cliente, Veiculo
from apps.quartos.models import Quarto
from .models import Reserva, Pessoa

@login_required
def criar_reserva(request, quarto_id):
    if request.method == "POST":
        # 1. VEÍCULO PRINCIPAL (Criamos primeiro, sem o campo 'cliente')
        veiculo = Veiculo.objects.create(
            placa=request.POST.get('placa'),
            cor=request.POST.get('cor'),
            cor_personalizada=request.POST.get('cor_personalizada'),
            modelo=request.POST.get('modelo'),
            imagem=request.FILES.get('imagem'),
            modo_conducao=request.POST.get('modo_conducao') # Adicionado se necessário
        )

        # 2. CLIENTE (Agora vinculamos o cliente ao veículo criado)
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')

        cliente, created = Cliente.objects.get_or_create(
            cpf=cpf,
            defaults={'nome': nome, 'veiculo': veiculo}
        )
        
        # Se o cliente já existia, atualizamos o veículo dele para o atual
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

        return redirect('quartos:dashboard')

    return render(request, 'reservas/modal.html')

@login_required
def dashboard_reservas(request):
    quartos = Quarto.objects.all()
    return render(request, 'reservas/dashboard.html', {'quartos': quartos})
