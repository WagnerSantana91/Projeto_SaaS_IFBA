from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quarto
from .form import QuartoForm

@login_required
def listar_quartos(request):
    quarto = Quarto.objects.all()
    return render(request, 'quartos/lista.html', {'quartos': quarto})



@login_required
def criar_quarto(request):
    if request.method == 'POST':
        form = QuartoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quartos:listar_quartos')
    else:
        form = QuartoForm()
    return render(request, 'quartos/criar.html', {'form': form})


@login_required
def editar_quarto(request, id):#will:

    cliente = get_object_or_404(Quarto, id=id)#will:

    if request.method == "POST":
        form = QuartoForm(request.POST, instance=cliente)#will:

        if form.is_valid():
            form.save()
            return redirect("quartos:listar_quartos")#will:

    else:
        form = QuartoForm(instance=cliente)#will:

    return render(request, "quartos/editar.html", {
        "form": form#will:
    })



@login_required
def excluir_quarto(request, id):
    quarto = get_object_or_404(Quarto, id = id)
    quarto.delete()
    return redirect('quartos:listar_quartos')




@login_required
def dashboard_quartos(request):
    quartos = Quarto.objects.all()
    return render(request, 'quartos/dashboard.html', {'quartos': quartos})