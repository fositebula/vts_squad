# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib import admin

from django.conf import settings

from models import MyUser, Job, VtsModule, Comment,  LavaDeviceType, VtsVersion, DelployImgs, SquadAPI

# Register your models here.

# class UserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(label='PassWord', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='PassWord111 Confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('email', )
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Password don't match")
#         return password2
#
#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=True)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             self.save()
#         return user
#
# class UserChangeForm(forms.ModelForm):
#     passwd = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = MyUser
#         fields = ('email', 'password', 'is_admin', 'is_active')
#
#     def clean_password(self):
#         return self.initial("password")

class MyUserAdmin(UserAdmin):
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
           'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2', )
        }),
    )

    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()

class JobAdmin(admin.ModelAdmin):
    list_display = ('jenkins_build_num', 'user', 'submit_time', 'lava_job', 'lava_job_status')

    search_fields = ('lava_job', 'jenkins_job', 'user', )

class YamlTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'datetime', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('who', 'text', 'job', 'date_time', )

class VtsModuleForm(forms.ModelForm):
    passwd1 = forms.CharField(label='PassWord', widget=forms.PasswordInput)
    passwd2 = forms.CharField(label='PassWord Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('passwd1')
        password2 = self.cleaned_data.get('passwd2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=True)
        user.set_password(self.cleaned_data["passwd1"])
        if commit:
            self.save()
        return user

class VtsModuleAdmin(admin.ModelAdmin):
    list_display = ('vtsmodule', 'date_time', )

class VtsVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'tar_url', 'date_time', )

class LavaDeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'lava_server_host', 'date_time', )

class DelployImgsAdmin(admin.ModelAdmin):
    list_display = ('name', )

class SquadAPIAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', )


class JobAdmin(admin.ModelAdmin):
    list_display = ('jenkins_job', 'jenkins_build_num', 'submit_time')

admin.site.register(VtsModule, VtsModuleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LavaDeviceType, LavaDeviceTypeAdmin)
admin.site.register(VtsVersion, VtsVersionAdmin)
admin.site.register(DelployImgs, DelployImgsAdmin)
admin.site.register(SquadAPI, SquadAPIAdmin)
admin.site.register(Job, JobAdmin)