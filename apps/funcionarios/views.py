from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Funcionario
from .form import FuncionarioForm


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

    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)   

        if form.is_valid():
            form.save()
            return redirect("funcionarios:listar_funcionarios")   

    else:
        form = FuncionarioForm(instance=funcionario)   

    return render(request, "funcionarios/editar.html", {
        "form": form   
    })


@login_required
def excluir_funcionario(request, id): #Incrementação do botão de excluir
    funcionario = get_object_or_404(Funcionario, id = id)
    funcionario.delete()
    return redirect('funcionarios:listar_funcionarios')