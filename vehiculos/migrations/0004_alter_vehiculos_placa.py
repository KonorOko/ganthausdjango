# Generated by Django 5.0 on 2023-12-27 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0003_remove_vehiculos_marca_alter_vehiculos_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculos',
            name='placa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
