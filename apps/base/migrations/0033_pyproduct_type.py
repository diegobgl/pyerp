# Generated by Django 2.2.4 on 2019-08-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_auto_20190817_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='pyproduct',
            name='type',
            field=models.CharField(choices=[('product', 'Almacenable'), ('consu', 'Consumible'), ('service', 'Servicio')], default='open', max_length=64),
        ),
    ]
