# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 15:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20170517_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Profile'),
        ),
    ]
