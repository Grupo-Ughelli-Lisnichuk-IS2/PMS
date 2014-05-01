from django.forms import ModelForm
from django import forms
from PMS import settings
from items.models import Item, Archivo
from tiposDeItem.models import Atributo

ESTADOS = (

    ('PEN', 'Pendiente'),
    ('FIN','Finalizado'),
    ('VAL', 'Validado'),
)

class PrimeraFaseForm(forms.ModelForm):
    class Meta:
        model=Item
        exclude=('estado', 'version', 'relacion', 'fecha_creacion', 'fecha_mod','tipo', 'tipo_item')

class CambiarEstadoForm(forms.ModelForm):
    estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
    class Meta:
        model=Item
        fields=['estado']