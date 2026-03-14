from django import forms
from .models import Funcionario
import re
from django.core.exceptions import ValidationError


class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['nome', 'cargo', 'cpf', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'id': 'cpf'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefone'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos
        if len(cpf) != 11:
            raise ValidationError('CPF deve conter 11 dígitos.')
        return cpf