# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-26 04:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import shopping.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, default='static/default_category.png', upload_to=shopping.models.image_upload_location)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50, unique=True)),
                ('rfc', models.CharField(max_length=13, unique=True)),
                ('country', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=25)),
                ('colony', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=5)),
                ('street', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=5)),
                ('phone_number', models.CharField(max_length=17)),
                ('email', models.EmailField(max_length=254)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('aprobado', 'Aprobado'), ('no aprobado', 'No aprobado'), ('entregado', 'Entregado')], max_length=11)),
                ('subtotal_cost', models.DecimalField(decimal_places=2, max_digits=9)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=9)),
                ('details', models.TextField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shopping.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, default='static/default_product.png', upload_to=shopping.models.image_upload_location)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('stock', models.PositiveSmallIntegerField()),
                ('show', models.BooleanField(default=True)),
                ('weight_measurement', models.CharField(blank=True, choices=[('Mass', (('Kg', 'kg'), ('Gr', 'gr'), ('Oz', 'oz'), ('Lbs', 'lbs'))), ('Capacity', (('Ls', 'ls'), ('Mls', 'mls'), ('Gl', 'gl')))], max_length=4, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('quantity', models.PositiveSmallIntegerField(blank=True, default=1)),
                ('category', models.ForeignKey(default=shopping.models.get_default_product, on_delete=django.db.models.deletion.SET_DEFAULT, to='shopping.Category')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='shopping.Product'),
        ),
    ]
