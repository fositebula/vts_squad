# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-13 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vts_squad', '0010_auto_20181213_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lavadevicetype',
            name='template',
            field=models.TextField(default='', max_length=10240),
        ),
    ]
