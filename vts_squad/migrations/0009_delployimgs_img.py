# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-13 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vts_squad', '0008_auto_20181213_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='delployimgs',
            name='img',
            field=models.CharField(default='', max_length=16),
        ),
    ]