# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-08 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccenter', '0005_auto_add_display_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='value',
            name='value_type',
        ),
        migrations.AlterField(
            model_name='value',
            name='integer_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
