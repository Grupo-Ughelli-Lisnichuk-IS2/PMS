from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from proyectos.models import Proyecto
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError

ESTADOS = (

    ('PEN', 'Pendiente'),
    ('ANU','Anulado'),
    ('ACT', 'Activo'),
)


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
class CambiarEstadoForm(forms.ModelForm):
    estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
    class Meta:
        model = Proyecto
        exclude = ['nombre', 'descripcion', 'fecha_ini', 'fecha_fin', 'lider', 'observaciones', 'comite']


