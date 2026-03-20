import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .form import FuncionarioForm
from .models import Funcionario


@login_required
def lista_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionarios/lista.html', {'funcionarios': funcionarios})


@login_required
def criar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funcionarios:listar_funcionarios')
    else:
        form = FuncionarioForm()
    return render(request, 'funcionarios/criar.html', {'form': form})


@login_required
def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('funcionarios:listar_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'funcionarios/editar.html', {'form': form})


@login_required
def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    funcionario.delete()
    return redirect('funcionarios:listar_funcionarios')


@login_required
def buscar_cep(request):
    cep = (request.GET.get('cep') or '').strip()
    cep = ''.join(ch for ch in cep if ch.isdigit())

    if len(cep) != 8:
        return JsonResponse({'ok': False, 'mensagem': 'CEP invalido.'}, status=400)

    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        with urlopen(url, timeout=8) as response:
            data = json.loads(response.read().decode('utf-8'))
    except (HTTPError, URLError, TimeoutError, ValueError):
        return JsonResponse(
            {'ok': False, 'mensagem': 'Nao foi possivel consultar o CEP agora.'},
            status=502,
        )

    if data.get('erro'):
        return JsonResponse({'ok': False, 'mensagem': 'CEP nao encontrado.'}, status=404)

    endereco_partes = [
        data.get('logradouro', ''),
        data.get('bairro', ''),
        data.get('localidade', ''),
        data.get('uf', ''),
    ]
    endereco = ', '.join(parte for parte in endereco_partes if parte)
    return JsonResponse({'ok': True, 'endereco': endereco})
