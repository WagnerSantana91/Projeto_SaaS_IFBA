from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required 
from .form import ClienteForm, VeiculoForm, ClienteFormSet
from .models import Cliente, Veiculo


@login_required
def listar_clientes(request):
    # Buscamos os veículos e já trazemos as pessoas juntas para economizar banco de dados
    veiculos = Veiculo.objects.prefetch_related('pessoas').all().order_by('-criado_em')
    return render(request, 'clientes/lista.html', {'veiculos': veiculos})



@login_required
def criar_cliente(request):

    if request.method == 'POST':
        veiculo_form = VeiculoForm(request.POST, request.FILES)
        formset = ClienteFormSet(request.POST, instance=None)

        if veiculo_form.is_valid() and formset.is_valid():
            # Salva o veículo primeiro
            veiculo = veiculo_form.save()

            # Salva o formset com a instância do veículo
            formset.instance = veiculo
            formset.save()

            return redirect('clientes:listar_clientes')

    else:
        veiculo_form = VeiculoForm()
        formset = ClienteFormSet(instance=None)

    return render(request, 'clientes/criar.html', {
        'veiculo_form': veiculo_form,
        'formset': formset
    })


@login_required
def editar_cliente(request, id):

    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == "POST":
        veiculo_form = VeiculoForm(request.POST, request.FILES, instance=veiculo)
        formset = ClienteFormSet(request.POST, instance=veiculo)

        if veiculo_form.is_valid() and formset.is_valid():
            veiculo_form.save()
            formset.save()
            return redirect("clientes:listar_clientes")

    else:
        veiculo_form = VeiculoForm(instance=veiculo)
        formset = ClienteFormSet(instance=veiculo)

    return render(request, "clientes/editar.html", {
        "veiculo_form": veiculo_form,
        "formset": formset
    })


@login_required
def excluir_cliente(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    veiculo.delete()
    return redirect('clientes:listar_clientes')