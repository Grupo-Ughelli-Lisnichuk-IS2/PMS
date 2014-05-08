
from django import forms
from items.models import Item

from lineasBase.models import LineaBase


ESTADOS = (

    ('PEN', 'Pendiente'),
    ('VAL', 'Validado'),
)

class LineaBaseForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.none(), widget=forms.CheckboxSelectMultiple(), required=True)
    def __init__(self, fase, *args, **kwargs):
        super(LineaBaseForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = Item.objects.filter(estado='VAL', tipo_item=fase, lineaBase=None)

    class Meta:
            model= LineaBase
            fields=['nombre',]
