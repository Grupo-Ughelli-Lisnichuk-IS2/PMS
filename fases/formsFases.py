from django.forms import ModelForm
from django import forms
from fases.models import Fase

class FaseForm(ModelForm):
    class Meta:
        model = Fase

class CrearFaseForm(ModelForm):
    class Meta:
        model = Fase
        fields = ('nombre', 'descripcion', 'maxItems', 'fInicio', 'orden', 'roles')

class ModificarFaseForm(ModelForm):
    class Meta:
        model = Fase
        fields = ('descripcion', 'maxItems', 'fInicio')