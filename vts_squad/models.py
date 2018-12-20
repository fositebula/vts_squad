# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

from django.db import models
from django import forms
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings

# Create your models here.

class MyUserManager(BaseUserManager):
    def creat_user(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    object = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_model_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Job(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    verify_url = models.CharField(max_length=256, default='')
    jenkins_job = models.CharField(max_length=32, default='')
    jenkins_build_num = models.CharField(max_length=12, default='')
    jenkins_node = models.CharField(max_length=12, default='')
    jenkins_trigger = models.CharField(max_length=12, default='')
    jenkins_list = models.CharField(max_length=512, default='')
    jenkins_build_type = models.CharField(max_length=8, default='')
    jenkins_lavatest = models.CharField(max_length=8, default='')
    jenkins_changes = models.CharField(max_length=256, default='')

    download_compress_status = models.CharField(max_length=32, default='Download starting')
    download_log = models.TextField(max_length=1024, default='')
    compress_log = models.TextField(max_length=1024, default='')

    lava_job = models.CharField(max_length=32, default='')
    lava_job_status = models.CharField(max_length=8, default='Submitted')
    lava_job_log = models.TextField(max_length=1024*1024, default='')
    lava_job_yaml = models.TextField(max_length=1024*5, default='')
    lava_test_case_result = models.CharField(max_length=1024, default='')

    vts_version = models.ForeignKey('VtsVersion', default=0)
    vts_module = models.CharField(max_length=64, default='')
    device_type = models.ForeignKey('LavaDeviceType', default=0)

    submit_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.jenkins_build_num

    def get_lava_job_id(self):
        if self.lava_job.startswith('http://'):
            return requests.get(self.lava_job).json().get('job_id')
        else:
            return ''

class Comment(models.Model):
    text = models.TextField(max_length=1024, default='')
    date_time = models.DateTimeField(auto_now=True)

    who = models.ForeignKey(settings.AUTH_USER_MODEL)
    parent = models.ForeignKey('Comment')
    job = models.ForeignKey('Job')

    def __unicode__(self):
        return self.job + self.date_time

class VtsVersion(models.Model):
    version = models.CharField(max_length=32, default='')
    tar_url = models.URLField(default='')

    date_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'VTS: '+self.version

class VtsModule(models.Model):
    vtsmodule = models.CharField(max_length=128)
    date_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.vtsmodule

class LavaDeviceTypeForm(forms.ModelForm):
    deploy_imgs = forms.ChoiceField(widget=forms.SelectMultiple)

    class Meta:
        models = 'LavaDeviceType'
        fields = ('deploy_imgs', )

class DelployImgs(models.Model):
    name = models.CharField(max_length=16, default='')
    img = models.CharField(max_length=32, default='')
    url = models.URLField(default='', blank=True)
    description = models.CharField(max_length=32, default='', blank=True)

    def __unicode__(self):
        return self.name


class LavaDeviceType(models.Model):

    name = models.CharField(max_length=8*8)
    date_time = models.DateTimeField(auto_now=True)
    pac_url = models.CharField(max_length=256, default='')
    template = models.TextField(max_length=1024*10, default='')
    deploy_imgs = models.ManyToManyField('DelployImgs')
    description = models.CharField(max_length=512, default='')
    worker05_pac = models.CharField(max_length=256, default='')

    lava_server_host = models.CharField(max_length=32, default='10.0.70.142')

    squad_api = models.ForeignKey('SquadAPI', default=0)

    def __unicode__(self):
        return self.name + ' ' + self.lava_server_host

class SquadAPI(models.Model):
    api = models.CharField(max_length=128, default='')
    desc = models.CharField(max_length=256, default='', blank=True)
    token = models.CharField(max_length=128, default='')
    name = models.CharField(max_length=32, default='')

    # device_type = models.ForeignKey('LavaDeviceType', default=0)

    def __unicode__(self):
        return self.name

class GongGao(models.Model):
    name = models.CharField(max_length=32, default='')
    content = models.CharField(max_length=512, default='')
    fabu_or_not = models.BooleanField(default=False)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name