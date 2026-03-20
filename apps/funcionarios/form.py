from django import forms
from .models import Funcionario
import re
from django.core.exceptions import ValidationError


class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['nome', 'cargo', 'cpf', 'telefone', 'cep', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'id': 'cpf'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefone'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cep', 'placeholder': '00000-000'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_endereco', 'placeholder': 'Endereco completo'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11:
            raise ValidationError('CPF deve conter 11 digitos.')
        return cpf

    def clean_cep(self):
        cep = self.cleaned_data.get('cep', '')
        return re.sub(r'\D', '', cep)
