# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-13 06:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vts_squad', '0015_squadapi_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='squadapi',
            name='device_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='vts_squad.LavaDeviceType'),
        ),
        migrations.AlterField(
            model_name='squadapi',
            name='desc',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]