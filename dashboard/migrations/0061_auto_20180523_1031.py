# Generated by Django 2.0.5 on 2018-05-23 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0060_auto_20180517_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='place',
            field=models.TextField(default=None, null=True),
        ),
    ]