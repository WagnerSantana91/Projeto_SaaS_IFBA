from django.db import models
from apps.empresas.models import Empresa

class Funcionario(models.Model):

    CARGO_CHOICES = (
        ('gerente', 'Gerente'),
        ('recepcionista', 'Recepcionista'),
        ('limpeza', 'Limpeza'),
        ('manutencao', 'Manutenção'),
    )

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='funcionarios',verbose_name='Empresa')
    nome = models.CharField(max_length=100, verbose_name='Nome')
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, verbose_name='Cargo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')

    def __str__(self):
        return f"{self.nome}"