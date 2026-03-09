from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 #will
from .models import Cliente
from .form import ClienteForm

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista.html', {'clientes': clientes})


def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes:listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/criar.html', {'form': form})


def editar_cliente(request, id):#will:

    cliente = get_object_or_404(Cliente, id=id)#will:

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)#will:

        if form.is_valid():
            form.save()
            return redirect("clientes:listar_clientes")#will:

    else:
        form = ClienteForm(instance=cliente)#will:

    return render(request, "clientes/editar.html", {
        "form": form#will:
    })

def excluir_cliente(request, id): #Incrementando botão de excluir
    cliente = get_object_or_404(Cliente, id = id)
    cliente.delete()
    return redirect('clientes:listar_clientes')