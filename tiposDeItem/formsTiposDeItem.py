from django.forms import ModelForm
from django import forms
from tiposDeItem.models import TipoItem, Atributo

class TipoItemForm(forms.ModelForm):
    class Meta:
        model = TipoItem
        exclude = ('fase',)

class AtributoForm(forms.ModelForm):
    class Meta:
        model = Atributo
        exclude = ('tipoItem',)

