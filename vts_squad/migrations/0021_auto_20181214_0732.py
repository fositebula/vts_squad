# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-14 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vts_squad', '0020_auto_20181214_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='compress_log',
            field=models.TextField(default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='job',
            name='download_log',
            field=models.TextField(default='', max_length=1024),
        ),
    ]
