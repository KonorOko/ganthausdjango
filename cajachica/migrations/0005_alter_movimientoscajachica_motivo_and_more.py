# Generated by Django 5.0 on 2024-01-10 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajachica', '0004_alter_movimientoscajachica_motivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientoscajachica',
            name='motivo',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='notascajachica',
            name='nota',
            field=models.CharField(max_length=500),
        ),
    ]
