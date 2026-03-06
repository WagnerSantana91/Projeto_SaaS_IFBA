from django.shortcuts import render, redirect, get_object_or_404
from .models import Empresa
from .form import EmpresaForm

def listar_empresas(request):
    empresa = Empresa.objects.all()
    return render(request, 'empresas/lista.html', {'empresas': empresa})    
    
def criar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empresas:listar_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'empresas/criar.html', {'form': form})

def editar_empresa(request, id):#will:

    empresa = get_object_or_404(Empresa, id=id)#will:

    if request.method == "POST":
        form = EmpresaForm(request.POST, instance=empresa)#will:

        if form.is_valid():
            form.save()
            return redirect("empresas:listar_empresas")#will:

    else:
        form = EmpresaForm(instance=empresa)#will:

    return render(request, "empresas/editar.html", {
        "form": form#will:
    })