# Generated by Django 5.0 on 2024-01-18 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ventas',
            old_name='serie',
            new_name='factura',
        ),
    ]