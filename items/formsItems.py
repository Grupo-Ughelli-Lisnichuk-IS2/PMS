from django.forms import ModelForm
from django import forms
from PMS import settings
from items.models import Item, Archivo


class PrimeraFaseForm(forms.ModelForm):
    class Meta:
        model=Item
        exclude=('estado', 'version', 'relacion', 'fecha_creacion', 'fecha_mod','tipo', 'tipo_item')

class ArchivoForm(forms.ModelForm):
    class Meta:
        model=Archivo
        exclude=('id_item','nombre')