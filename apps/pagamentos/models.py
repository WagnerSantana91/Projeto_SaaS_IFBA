from django.db import models
from apps.clientes.models import Cliente       



class Entrada(models.Model):       
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')       
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')       
    data = models.DateTimeField(auto_now_add=True, verbose_name='Data')       
    forma_pagamento = models.CharField(max_length=50, verbose_name='Forma de Pagamento')       

    def __str__(self):       
        return f"Entrada - {self.cliente} - R$ {self.valor}"       


class Saida(models.Model):       
    descricao = models.CharField(max_length=200, verbose_name='Descrição')       
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')       
    data = models.DateTimeField(auto_now_add=True, verbose_name='Data')       

    def __str__(self):       
        return f"Saída - {self.descricao} - R$ {self.valor}"       
