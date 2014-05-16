
from django import forms

import items.models


ESTADOS = (

    ('PEN', 'Pendiente'),
    ('VAL', 'Validado'),
)

class PrimeraFaseForm(forms.ModelForm):
    class Meta:
        model=items.models.Item
        exclude=('estado', 'version', 'relacion', 'fecha_creacion', 'fecha_mod','tipo', 'tipo_item', 'lineaBase')

class EstadoItemForm(forms.ModelForm):
    estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
    class Meta:
        model=items.models.Item
        fields=['estado']