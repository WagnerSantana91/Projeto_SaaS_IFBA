from django.shortcuts import redirect, render, get_object_or_404
from .models import Funcionario
from .form import FuncionarioForm

def lista_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionarios/lista.html', {'funcionarios': funcionarios})

def criar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funcionarios:listar_funcionarios')
    else:
        form = FuncionarioForm()
    return render(request, 'funcionarios/criar.html', {'form': form})

def editar_funcionario(request, id):#will:

    funcionario = get_object_or_404(Funcionario, id=id)#will:

    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)#will:

        if form.is_valid():
            form.save()
            return redirect("funcionarios:listar_funcionarios")#will:

    else:
        form = FuncionarioForm(instance=funcionario)#will:

    return render(request, "funcionarios/editar.html", {
        "form": form#will:
    })

def excluir_funcionario(request, id): #Incrementação do botão de excluir
    funcionario = get_object_or_404(Funcionario, id = id)
    funcionario.delete()
    return redirect('funcionarios:listar_funcionarios')