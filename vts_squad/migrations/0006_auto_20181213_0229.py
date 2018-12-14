# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-13 02:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vts_squad', '0005_auto_20181212_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='yamltemplate',
        ),
        migrations.AddField(
            model_name='job',
            name='device_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='vts_squad.LavaDeviceType'),
        ),
        migrations.AddField(
            model_name='lavadevicetype',
            name='deploy_imgs',
            field=models.CharField(choices=[('zs', '\u6307\u793a\u6027\u901a\u77e5'), ('ps', '\u6279\u793a\u6027\u901a\u77e5'), ('zz', '\u5468\u77e5\u6027\u901a\u77e5'), ('hy', '\u4f1a\u8bae\u901a\u77e5'), ('rm', '\u4efb\u514d\u901a\u77e5')], default='zs', max_length=256),
        ),
        migrations.AddField(
            model_name='lavadevicetype',
            name='description',
            field=models.CharField(default='', max_length=512),
        ),
        migrations.AddField(
            model_name='lavadevicetype',
            name='template',
            field=models.TextField(default='', max_length=5120),
        ),
        migrations.DeleteModel(
            name='YamlTemplate',
        ),
    ]
