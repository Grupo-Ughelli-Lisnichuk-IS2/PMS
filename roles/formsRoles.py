from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, Permission


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), widget=FilteredSelectMultiple("Permisos", is_stacked=False))
    class Meta:
        model = Group
        fields=['name']
