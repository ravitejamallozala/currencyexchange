# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-06-26 06:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='default_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exchange_backend.Currency'),
        ),
        migrations.AlterField(
            model_name='user',
            name='wallet',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet', to='exchange_backend.Wallet'),
        ),
    ]