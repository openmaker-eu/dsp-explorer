# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-06 16:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_country_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('code',)},
        ),
    ]
