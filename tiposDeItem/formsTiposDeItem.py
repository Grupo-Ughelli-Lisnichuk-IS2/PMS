from django.forms import ModelForm
from django import forms
from tiposDeItem.models import TipoItem

class TipoItemForm(forms.ModelForm):
    class Meta:
        model = TipoItem
        exclude = ('fase',)