# Generated by Django 5.0.4 on 2024-09-05 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miAplicacion', '0006_alter_venta_numero_comprobante'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movimientostock',
            old_name='observaciones',
            new_name='comprobante',
        ),
    ]
