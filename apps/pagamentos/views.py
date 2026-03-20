from django.shortcuts import render, redirect     
from django.contrib.auth.decorators import login_required     
from django.db.models import Sum     
from .models import Entrada, Saida     
from .forms import EntradaForm, SaidaForm     
from apps.core.email_utils import enviar_email_notificacao



@login_required     
def financeiro_dashboard(request):     
    entradas = Entrada.objects.all().order_by('-data')     
    saidas = Saida.objects.all().order_by('-data')     

    inicio = request.GET.get('inicio')     
    fim = request.GET.get('fim')     

    if inicio:     
        entradas = entradas.filter(data__date__gte=inicio)     
        saidas = saidas.filter(data__date__gte=inicio)     

    if fim:     
        entradas = entradas.filter(data__date__lte=fim)     
        saidas = saidas.filter(data__date__lte=fim)     

    total_entradas = entradas.aggregate(total=Sum('valor'))['total'] or 0     
    total_saidas = saidas.aggregate(total=Sum('valor'))['total'] or 0     
    lucro = total_entradas - total_saidas     

    return render(request, 'pagamentos/dashboard.html', {     
        'entradas': entradas,     
        'saidas': saidas,     
        'total_entradas': total_entradas,     
        'total_saidas': total_saidas,     
        'lucro': lucro,     
    })     


@login_required     
def nova_entrada(request):     
    form = EntradaForm(request.POST or None)     
    if request.method == 'POST' and form.is_valid():     
        entrada = form.save()
        enviar_email_notificacao(
            assunto='Nova entrada financeira registrada',
            mensagem=(
                'Uma nova entrada foi registrada no sistema.\n\n'
                f'Cliente: {entrada.cliente}\n'
                f'Valor: R$ {entrada.valor}\n'
                f'Forma de pagamento: {entrada.forma_pagamento}\n'
                f'Data: {entrada.data:%d/%m/%Y %H:%M}'
            ),
        )     
        return redirect('pagamentos:financeiro_dashboard')     
    return render(request, 'pagamentos/nova_entrada.html', {'form': form})     


@login_required     
def nova_saida(request):     
    form = SaidaForm(request.POST or None)     
    if request.method == 'POST' and form.is_valid():     
        saida = form.save()
        enviar_email_notificacao(
            assunto='Nova saida financeira registrada',
            mensagem=(
                'Uma nova saida foi registrada no sistema.\n\n'
                f'Descricao: {saida.descricao}\n'
                f'Valor: R$ {saida.valor}\n'
                f'Data: {saida.data:%d/%m/%Y %H:%M}'
            ),
        )     
        return redirect('pagamentos:financeiro_dashboard')     
    return render(request, 'pagamentos/nova_saida.html', {'form': form})     
