from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome da Empresa')
    cnpj = models.CharField(max_length=20, unique=True, verbose_name='CNPJ')
    endereco = models.CharField(max_length=255, verbose_name='Endereço')
    email = models.EmailField(unique=True, verbose_name='Email')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    esta_ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
   

    def __str__(self):
        return self.nome
    

    