from django.forms import ModelForm
from django import forms
from PMS import settings
from items.models import Item, Archivo
from tiposDeItem.models import Atributo


class PrimeraFaseForm(forms.ModelForm):
    class Meta:
        model=Item
        exclude=('estado', 'version', 'relacion', 'fecha_creacion', 'fecha_mod','tipo', 'tipo_item')

class ArchivoForm(forms.ModelForm):
    class Meta:
        model=Archivo
        exclude=('id_item','nombre')


class ValorAtributoForm(forms.ModelForm):
    class Meta:
        model=Atributo
        fields = ('valorDefecto','nombre','tipo')
