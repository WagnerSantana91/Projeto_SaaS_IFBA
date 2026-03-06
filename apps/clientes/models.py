from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    telefone = models.CharField(max_length=15, verbose_name='Telefone')
    email = models.EmailField(verbose_name='Email')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')


    def __str__(self):
        return self.nome

    def cpf_formatado(self):
        cpf = self.cpf.replace('.', '').replace('-', '')
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"