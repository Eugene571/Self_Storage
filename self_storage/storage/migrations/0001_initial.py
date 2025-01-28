# Generated by Django 5.1.4 on 2025-01-24 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CellTariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=100)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.CharField(max_length=100, unique=True)),
                ('client_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_occupied', models.BooleanField()),
                ('start_storage', models.DateTimeField(blank=True, null=True)),
                ('end_storage', models.DateTimeField(blank=True, null=True)),
                ('cell_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.celltariff')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contacts', models.CharField(max_length=100)),
                ('start_storage', models.DateTimeField()),
                ('end_storage', models.DateTimeField()),
                ('address', models.CharField(max_length=200)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.cell')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.client')),
            ],
        ),
    ]
