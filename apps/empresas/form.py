from django import forms
from .models import Empresa
import re
from django.core.exceptions import ValidationError

class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj', 'endereco', 'email', 'telefone', 'esta_ativo']
        widgets ={
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'id':'cnpj', 'placeholder':'00.000.000/0000-00'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control','id':'telefone', 'placeholder':'(00) 00000-0000'}),
            'esta_ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        return re.sub(r'\D', '', cnpj)