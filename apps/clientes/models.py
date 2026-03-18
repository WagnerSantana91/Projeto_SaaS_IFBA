from django.db import models
from django.utils import timezone

class Veiculo(models.Model):

    CORES_CHOICES = [
        ('preto', 'Preto'),
        ('branco', 'Branco'),
        ('prata', 'Prata'),
        ('vermelho', 'Vermelho'),
        ('azul', 'Azul'),
        ('outro', 'Outro'),
    ]

    MODO_CONDUCAO_CHOICES = [
        ('proprio', 'Veículo Próprio'),
        ('uber', 'Uber'),
        ('moto-uber', 'Moto-Uber'),
        ('taxi', 'Táxi'),
        ('a_pe', 'A pé'),
    ]

    placa = models.CharField(max_length=10, verbose_name='Placa', unique=True)
    cor = models.CharField(max_length=20, choices=CORES_CHOICES, verbose_name='Cor')
    cor_personalizada = models.CharField(max_length=30, blank=True, null=True)
    modo_conducao = models.CharField(max_length=20, default='proprio', choices=MODO_CONDUCAO_CHOICES, verbose_name='Modo de Condução')
    modelo = models.CharField(max_length=50, verbose_name='Modelo')
    imagem = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.placa


class Cliente(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, verbose_name='Veículo', related_name='pessoas', null=True, blank=True)
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    estrangeiro = models.BooleanField(default=False)
    criado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('veiculo', 'cpf')

    def __str__(self):
        return self.nome
    
    def cpf_formatado(self):
        cpf = self.cpf.replace('.', '').replace('-', '')
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"