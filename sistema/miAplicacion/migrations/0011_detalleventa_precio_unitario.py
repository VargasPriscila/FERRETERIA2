# Generated by Django 4.2.16 on 2024-10-04 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miAplicacion', '0010_alter_detalleventa_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleventa',
            name='precio_unitario',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
