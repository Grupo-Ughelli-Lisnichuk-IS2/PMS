from django.forms import ModelForm
from django import forms
from proyectos.models import Proyecto

class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto

class ProyectoEditable(ModelForm):
    class Meta:
        model= Proyecto
        fields = ('nombre', 'descripcion', 'observaciones', 'fecha_ini', 'fecha_fin', 'lider', 'comite')
