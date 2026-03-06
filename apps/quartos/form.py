from django import forms
from .models import Quarto
import re
from django.core.exceptions import ValidationError


class QuartoForm(forms.ModelForm):

    class Meta:
        model = Quarto
        fields = ['empresa', 'numero', 'tipo', 'valor_hora', 'status', 'esta_ativo']
        widgets ={
            'empresa': forms.Select(attrs={'class': 'form-control'}),  
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'valor_hora': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'esta_ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

