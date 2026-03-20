import json
from urllib.parse import urlencode
from urllib.request import urlopen

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.clientes.models import Cliente
from apps.quartos.models import Quarto
from apps.reservas.models import Reserva


def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_quartos_disponiveis = Quarto.objects.filter(status='disponivel').count()
    total_reservas_hoje = Reserva.objects.filter(data_entrada__date=timezone.localdate()).count()

    previsao_tempo = {
        'disponivel': False,
        'resumo': 'Nao foi possivel consultar a previsao agora.',
        'chance_clientes_percentual': None,
        'chance_clientes_texto': 'Indefinida',
        'regra': 'Regra: se a noite tiver chuva forte, chance de mais clientes cai.',
    }

    params = {
        'latitude': -12.9714,
        'longitude': -38.5014,
        'hourly': 'precipitation_probability,weather_code',
        'timezone': 'America/Sao_Paulo',
        'forecast_days': 1,
    }
    url = 'https://api.open-meteo.com/v1/forecast?' + urlencode(params)

    try:
        with urlopen(url, timeout=8) as response:
            data = json.loads(response.read().decode('utf-8'))

        hourly = data.get('hourly', {})
        horarios = hourly.get('time', [])
        chuva_prob = hourly.get('precipitation_probability', [])
        codigos = hourly.get('weather_code', [])
        hoje = timezone.localdate().isoformat()

        dados_noite = []
        for horario, prob, codigo in zip(horarios, chuva_prob, codigos):
            horario = str(horario)
            if not horario.startswith(hoje):
                continue

            hora = int(horario[11:13])
            if 18 <= hora <= 23:
                dados_noite.append(
                    {
                        'prob': int(prob or 0),
                        'codigo': int(codigo or 0),
                    }
                )

        if not dados_noite:
            previsao_tempo['resumo'] = 'Sem dados de previsao para o horario da noite.'
            previsao_tempo['regra'] = 'Regra usada quando tiver dados da noite (18h-23h).'
        else:
            maior_dado = max(dados_noite, key=lambda item: item['prob'])
            maior_chuva = maior_dado['prob']
            codigo_referencia = maior_dado['codigo']

            codigos_de_chuva = {
                51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99
            }
            tem_codigo_chuva = any(
                item['codigo'] in codigos_de_chuva for item in dados_noite
            )
            noite_chuvosa = maior_chuva >= 40 or tem_codigo_chuva

            descricao_por_codigo = {
                0: 'ceu limpo',
                1: 'poucas nuvens',
                2: 'nublado parcial',
                3: 'nublado',
                61: 'chuva fraca',
                63: 'chuva moderada',
                65: 'chuva forte',
                80: 'pancadas de chuva',
                95: 'trovoadas',
            }
            descricao = descricao_por_codigo.get(codigo_referencia, 'condicao variavel')

            if noite_chuvosa:
                chance_percentual = 40
                chance_texto = 'Baixa'
            elif maior_chuva <= 20:
                chance_percentual = 75
                chance_texto = 'Alta'
            else:
                chance_percentual = 60
                chance_texto = 'Media'

            previsao_tempo['disponivel'] = True
            previsao_tempo['chance_clientes_percentual'] = chance_percentual
            previsao_tempo['chance_clientes_texto'] = chance_texto
            previsao_tempo['resumo'] = (
                'Noite com ' + descricao + '; pico de chuva previsto: ' + str(maior_chuva) + '%.'
            )
            previsao_tempo['regra'] = (
                'Regra usada: olhando 18h ate 23h, se chuva >= 40% '
                '(ou codigo de chuva), chance cai. Se nao chover, chance sobe.'
            )

    except Exception:
        pass

    context = {
        'total_clientes': total_clientes,
        'total_quartos_disponiveis': total_quartos_disponiveis,
        'total_reservas_hoje': total_reservas_hoje,
        'previsao_tempo': previsao_tempo,
    }
    return render(request, 'dashboard.html', context)


def login_view(request):
    """View responsavel pelo login do usuario"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:dashboard')

        messages.error(request, 'Usuario ou senha invalidos.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('core:login')
