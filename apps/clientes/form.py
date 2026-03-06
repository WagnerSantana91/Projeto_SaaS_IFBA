from django import forms
from .models import Cliente
import re
from django.core.exceptions import ValidationError


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'id': 'cpf'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos
        if len(cpf) != 11:
            raise ValidationError('CPF deve conter 11 dígitos.')
        return cpf