# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-12 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vts_squad', '0004_lavadevicetype_pac_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='VtsVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='', max_length=32)),
                ('tar_url', models.URLField(default='')),
                ('date_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='lava_test_case_result',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='job',
            name='lava_job_log',
            field=models.TextField(default='', max_length=1048576),
        ),
        migrations.AlterField(
            model_name='job',
            name='lava_job_yaml',
            field=models.TextField(default='', max_length=5120),
        ),
        migrations.AddField(
            model_name='job',
            name='vts_version',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='vts_squad.VtsVersion'),
        ),
    ]
