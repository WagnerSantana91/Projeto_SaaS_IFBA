from django.db import models
from apps.clientes.models import Cliente, Veiculo


class Reserva(models.Model):

    MODO_CONDUCAO = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('ape', 'A pé'),
        ('2_carros', '2 Carros'),
        ('taxi', 'Taxi'),
        ('uber', 'Uber'),
        ('uber_moto', 'Uber Moto'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    quarto = models.ForeignKey('quartos.Quarto', on_delete=models.CASCADE, verbose_name='Quarto')

    modo_conducao = models.CharField(max_length=20, choices=MODO_CONDUCAO)

    veiculo_principal = models.ForeignKey(Veiculo,on_delete=models.SET_NULL,null=True,related_name='principal',verbose_name='Veículo Principal')

    veiculo_secundario = models.ForeignKey(Veiculo,on_delete=models.SET_NULL,null=True,blank=True,related_name='secundario',verbose_name='Veículo Secundário')

    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.cliente} - {self.quarto}"


class Pessoa(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='pessoas', verbose_name='Reserva')

    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name='CPF')
    estrangeiro = models.BooleanField(default=False, verbose_name='Estrangeiro')

    def __str__(self):
        return self.nome