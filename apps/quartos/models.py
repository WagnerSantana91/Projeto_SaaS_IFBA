from django.db import models
from apps.empresas.models import Empresa


class Quarto(models.Model):

    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('ocupado', 'Ocupado'),
        ('manutencao', 'Em Manutenção'),
    ]

    TIPO_CHOICES = [
        ('standard', 'Standard'),
        ('luxo', 'Luxo'),
        ('super_luxo', 'Super Luxo'),
        ('presidencial', 'Presidencial'),
        ('tematica', 'Temática'),
    ]


    numero = models.CharField(max_length=10, verbose_name='Número do Quarto')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name='Tipo do Quarto')
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor por Hora')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel', verbose_name='Status do Quarto')
    esta_ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    
    def __str__(self):
        return f'Quarto - {self.numero} )'
    

    def cor_status(self):
        cores = {
            'ocupado': '#e74c3c',
            'livre': '#2ecc71',
            'limpeza': '#f1c40f',
            'manutencao': '#7f8c8d',
        }
        return cores.get(self.status, '#34495e')