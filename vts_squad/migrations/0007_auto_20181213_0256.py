# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-13 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vts_squad', '0006_auto_20181213_0229'),
    ]

    operations = [
        migrations.CreateModel(
            name='DelployImgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=16)),
                ('url', models.URLField(default='')),
                ('description', models.CharField(default='', max_length=32)),
            ],
        ),
        migrations.RemoveField(
            model_name='lavadevicetype',
            name='deploy_imgs',
        ),
        migrations.AddField(
            model_name='lavadevicetype',
            name='deploy_imgs',
            field=models.ManyToManyField(to='vts_squad.DelployImgs'),
        ),
    ]
