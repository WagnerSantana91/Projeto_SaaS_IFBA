from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Veiculo


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'estrangeiro']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'estrangeiro': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'cor', 'cor_personalizada', 'modelo', 'imagem', 'modo_conducao']

        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-1234'
            }),
            'cor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cor_personalizada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a cor (se outro)'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo do veículo'
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'modo_conducao': forms.RadioSelect(),
        }

    def clean(self):
        cleaned_data = super().clean()
        cor = cleaned_data.get('cor')
        cor_personalizada = cleaned_data.get('cor_personalizada')

        # Se escolher "outro", obrigar cor personalizada
        if cor == 'outro' and not cor_personalizada:
            self.add_error('cor_personalizada', 'Informe a cor personalizada.')

        return cleaned_data


# Formset para múltiplas pessoas
ClienteFormSet = inlineformset_factory(
    Veiculo,
    Cliente,
    form=ClienteForm,
    extra=1,  # Número de formulários vazios inicialmente
    min_num=1,  # Mínimo de 1 pessoa obrigatória
    validate_min=True,
    can_delete=True
)