from django.db import models
from apps.empresas.models import Empresa

class Funcionario(models.Model):

    CARGO_CHOICES = (
        ('gerente', 'Gerente'),
        ('recepcionista', 'Recepcionista'),
        ('limpeza', 'Limpeza'),
        ('manutencao', 'Manutenção'),
    )

    nome = models.CharField(max_length=100, verbose_name='Nome')
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, verbose_name='Cargo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    cep = models.CharField(max_length=9, blank=True, default='', verbose_name='CEP')
    endereco = models.CharField(max_length=255, blank=True, default='', verbose_name='Endereco')

    def __str__(self):
        return f"{self.nome}"
