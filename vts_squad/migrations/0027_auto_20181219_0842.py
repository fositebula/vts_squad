# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-19 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vts_squad', '0026_job_vts_module'),
    ]

    operations = [
        migrations.CreateModel(
            name='GongGao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=32)),
                ('content', models.CharField(default='', max_length=512)),
            ],
        ),
        migrations.RemoveField(
            model_name='lavadevicetype',
            name='templates',
        ),
        migrations.AddField(
            model_name='lavadevicetype',
            name='template',
            field=models.TextField(default='', max_length=10240),
        ),
    ]
