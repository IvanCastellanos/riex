# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-07 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0007_auto_20160507_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_unit',
            name='subtotal_cost',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
