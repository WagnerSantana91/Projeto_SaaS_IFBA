from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 #will
from django.contrib.auth.decorators import login_required 
from .form import ClienteForm
from .models import Cliente



@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista.html', {'clientes': clientes})

@login_required
def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes:listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/criar.html', {'form': form})

@login_required
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

@login_required
def excluir_cliente(request, id): #Incrementando botão de excluir
    cliente = get_object_or_404(Cliente, id = id)
    cliente.delete()
    return redirect('clientes:listar_clientes')