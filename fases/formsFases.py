from django.forms import ModelForm
from django import forms
from fases.models import Fase

class FaseForm(ModelForm):
    class Meta:
        model = Fase