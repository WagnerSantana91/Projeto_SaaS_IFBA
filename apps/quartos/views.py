from django.shortcuts import render, redirect
from .models import Quarto
from .form import QuartoForm

def listar_quartos(request):
    quarto = Quarto.objects.all()
    return render(request, 'quartos/lista.html', {'quartos': quarto})
    
def criar_quarto(request):
    if request.method == 'POST':
        form = QuartoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quartos:listar_quartos')
    else:
        form = QuartoForm()
    return render(request, 'quartos/criar.html', {'form': form})