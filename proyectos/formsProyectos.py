from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from proyectos.models import Proyecto
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError



class ProyectoForm(forms.ModelForm):
        nombre= forms.CharField(max_length=100)
        descripcion= forms.CharField(label='Descripcion', widget=forms.Textarea)
        fecha_ini=forms.DateField(widget = AdminDateWidget, label='Fecha de Inicio')
        fecha_fin=forms.DateField(widget = AdminDateWidget, label='Fecha de finalizacion')
        lider = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
        observaciones = forms.CharField(label='Observaciones', widget=forms.Textarea)
        comite = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True) )
        class Meta:
            model = Proyecto
            exclude = ['estado']

class ProyectoEditable(ModelForm):
    class Meta:
        model= Proyecto
        fields = ('nombre', 'descripcion', 'observaciones', 'fecha_ini', 'fecha_fin', 'lider', 'comite')
