# ADICIONADO RECENTEMENTE
from django.db import migrations, models  # ADICIONADO RECENTEMENTE
import django.db.models.deletion  # ADICIONADO RECENTEMENTE


class Migration(migrations.Migration):  # ADICIONADO RECENTEMENTE

    initial = True  # ADICIONADO RECENTEMENTE

    dependencies = [  # ADICIONADO RECENTEMENTE
        ('clientes', '0005_remove_veiculo_cliente_cliente_veiculo_and_more'),  # ADICIONADO RECENTEMENTE
    ]  # ADICIONADO RECENTEMENTE

    operations = [  # ADICIONADO RECENTEMENTE
        migrations.CreateModel(  # ADICIONADO RECENTEMENTE
            name='Saida',  # ADICIONADO RECENTEMENTE
            fields=[  # ADICIONADO RECENTEMENTE
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # ADICIONADO RECENTEMENTE
                ('descricao', models.CharField(max_length=200, verbose_name='Descrição')),  # ADICIONADO RECENTEMENTE
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),  # ADICIONADO RECENTEMENTE
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),  # ADICIONADO RECENTEMENTE
            ],  # ADICIONADO RECENTEMENTE
        ),  # ADICIONADO RECENTEMENTE
        migrations.CreateModel(  # ADICIONADO RECENTEMENTE
            name='Entrada',  # ADICIONADO RECENTEMENTE
            fields=[  # ADICIONADO RECENTEMENTE
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # ADICIONADO RECENTEMENTE
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),  # ADICIONADO RECENTEMENTE
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),  # ADICIONADO RECENTEMENTE
                ('forma_pagamento', models.CharField(max_length=50, verbose_name='Forma de Pagamento')),  # ADICIONADO RECENTEMENTE
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente', verbose_name='Cliente')),  # ADICIONADO RECENTEMENTE
            ],  # ADICIONADO RECENTEMENTE
        ),  # ADICIONADO RECENTEMENTE
    ]  # ADICIONADO RECENTEMENTE
