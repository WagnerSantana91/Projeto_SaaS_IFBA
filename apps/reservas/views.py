from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.clientes.models import Cliente, Veiculo
from apps.quartos.models import Quarto
from apps.pagamentos.models import Entrada        
from .models import Reserva, Pessoa
from apps.core.email_utils import enviar_email_notificacao
from decimal import Decimal


def _normalizar_modo_conducao(raw_value):
    valor = (raw_value or '').strip().lower()

    mapa_reserva = {
        'proprio': 'carro',
        'carro': 'carro',
        'moto': 'moto',
        'ape': 'ape',
        'a_pe': 'ape',
        '2_carros': '2_carros',
        'taxi': 'taxi',
        'uber': 'uber',
        'uber_moto': 'uber_moto',
        'moto-uber': 'uber_moto',
    }

    mapa_veiculo = {
        'proprio': 'proprio',
        'carro': 'proprio',
        'moto': 'proprio',
        '2_carros': 'proprio',
        'taxi': 'taxi',
        'uber': 'uber',
        'uber_moto': 'moto-uber',
        'moto-uber': 'moto-uber',
        'ape': 'a_pe',
        'a_pe': 'a_pe',
    }

    return {
        'reserva': mapa_reserva.get(valor, 'carro'),
        'veiculo': mapa_veiculo.get(valor, 'proprio'),
    }


@login_required
def criar_reserva(request, quarto_id):
    if request.method == "POST":

              
        quarto_obj = Quarto.objects.get(id=quarto_id)
        # Regra de negocio: se ocupacao >= 60%, aumenta 20% no valor da hora
        quartos_ativos = Quarto.objects.filter(esta_ativo=True)
        total_quartos = quartos_ativos.count()
        ocupados = quartos_ativos.filter(status='ocupado').count()

        # Conta esta reserva no calculo projetado
        if quarto_obj.status != 'ocupado':
            ocupados += 1

        taxa_ocupacao = (ocupados / total_quartos) if total_quartos else 0

        valor_entrada = quarto_obj.valor_hora
        if taxa_ocupacao >= 0.60:
            valor_entrada = (valor_entrada * Decimal('1.20')).quantize(Decimal('0.01'))
        

               
        
        placa_normalizada = (request.POST.get('placa') or '').replace('-', '').replace(' ', '').upper()
        modo_conducao = _normalizar_modo_conducao(request.POST.get('modo_conducao'))
        veiculo, veiculo_criado = Veiculo.objects.get_or_create(        
            placa=placa_normalizada,        
            defaults={        
                'cor': request.POST.get('cor') or 'outro',        
                'cor_personalizada': request.POST.get('cor_personalizada'),        
                'modelo': request.POST.get('modelo') or '',        
                'imagem': request.FILES.get('imagem'),        
                'modo_conducao': modo_conducao['veiculo'],        
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
            modo_conducao=modo_conducao['reserva'],
            veiculo_principal=veiculo
        )
        if quarto_obj.status != 'ocupado':
            quarto_obj.status = 'ocupado'
            quarto_obj.save(update_fields=['status'])

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


        entrada = Entrada.objects.create(
            cliente=cliente,
            valor=valor_entrada,
            forma_pagamento=request.POST.get('forma_pagamento', 'dinheiro'),
        )

        enviar_email_notificacao(
            assunto=f'Nova reserva registrada - Quarto {quarto_obj.numero}',
            mensagem=(
                'Uma nova reserva foi criada no sistema.\n\n'
                f'Cliente: {cliente.nome}\n'
                f'Quarto: {quarto_obj.numero}\n'
                f'Veiculo: {veiculo.placa}\n'
                f'Valor da entrada: R$ {entrada.valor}\n'
                f'Forma de pagamento: {entrada.forma_pagamento}\n'
                f'Data: {reserva.data_entrada:%d/%m/%Y %H:%M}'
            ),
        )

        return redirect('quartos:dashboard_quartos')

    return render(request, 'reservas/modal.html')

@login_required
def dashboard_reservas(request):
    quartos = Quarto.objects.all()
    return render(request, 'reservas/dashboard.html', {'quartos': quartos})
