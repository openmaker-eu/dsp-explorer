# Generated by Django 2.0.5 on 2018-07-19 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0065_tag_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='area',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='technology',
        ),
        migrations.AlterField(
            model_name='tag',
            name='type',
            field=models.CharField(blank=True, default=None, max_length=50),
        ),
    ]
