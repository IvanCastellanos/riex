# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-05 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_auto_20160426_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('aprobado', 'Aprobado'), ('no aprobado', 'No aprobado'), ('entregado', 'Entregado'), ('en curso', 'En curso')], max_length=11),
        ),
    ]
