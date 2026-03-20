from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Empresa
from .form import EmpresaForm


@login_required
def listar_empresas(request):
    empresa = Empresa.objects.all()
    return render(request, 'empresas/lista.html', {'empresas': empresa})    


@login_required
def criar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empresas:listar_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'empresas/criar.html', {'form': form})


@login_required
def editar_empresa(request, id):   

    empresa = get_object_or_404(Empresa, id=id)   

    if request.method == "POST":
        form = EmpresaForm(request.POST, instance=empresa)   

        if form.is_valid():
            form.save()
            return redirect("empresas:listar_empresas")   

    else:
        form = EmpresaForm(instance=empresa)   

    return render(request, "empresas/editar.html", {
        "form": form   
    })



@login_required
def excluir_empresa(request, id): #Incrementação do botão de excluir empresa
    empresa = get_object_or_404(Empresa, id = id)
    empresa.delete()
    return redirect('empresas:listar_empresas')