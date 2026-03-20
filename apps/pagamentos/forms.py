# ADICIONADO RECENTEMENTE
from django import forms  # ADICIONADO RECENTEMENTE
from .models import Entrada, Saida  # ADICIONADO RECENTEMENTE


class EntradaForm(forms.ModelForm):  # ADICIONADO RECENTEMENTE
    class Meta:  # ADICIONADO RECENTEMENTE
        model = Entrada  # ADICIONADO RECENTEMENTE
        fields = ['cliente', 'valor', 'forma_pagamento']  # ADICIONADO RECENTEMENTE
        widgets = {  # ADICIONADO RECENTEMENTE
            'cliente': forms.Select(attrs={'class': 'form-control'}),  # ADICIONADO RECENTEMENTE
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0,00'}),  # ADICIONADO RECENTEMENTE
            'forma_pagamento': forms.Select(  # ADICIONADO RECENTEMENTE
                attrs={'class': 'form-control'},  # ADICIONADO RECENTEMENTE
                choices=[  # ADICIONADO RECENTEMENTE
                    ('dinheiro', 'Dinheiro'),  # ADICIONADO RECENTEMENTE
                    ('pix', 'Pix'),  # ADICIONADO RECENTEMENTE
                    ('cartao_credito', 'Cartão de Crédito'),  # ADICIONADO RECENTEMENTE
                    ('cartao_debito', 'Cartão de Débito'),  # ADICIONADO RECENTEMENTE
                ]  # ADICIONADO RECENTEMENTE
            ),  # ADICIONADO RECENTEMENTE
        }  # ADICIONADO RECENTEMENTE


class SaidaForm(forms.ModelForm):  # ADICIONADO RECENTEMENTE
    class Meta:  # ADICIONADO RECENTEMENTE
        model = Saida  # ADICIONADO RECENTEMENTE
        fields = ['descricao', 'valor']  # ADICIONADO RECENTEMENTE
        widgets = {  # ADICIONADO RECENTEMENTE
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Conta de luz, Manutenção...'}),  # ADICIONADO RECENTEMENTE
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0,00'}),  # ADICIONADO RECENTEMENTE
        }  # ADICIONADO RECENTEMENTE
