from django.forms import ModelForm
from django import forms
from fases.models import Fase
from django.contrib.auth.models import Group
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


class RolesForm(forms.Form):
    roles = forms.ModelMultipleChoiceField(queryset=Group.objects.none() )
    def __init__(self, fase, *args, **kwargs):
        super(RolesForm, self).__init__(*args, **kwargs)
        self.fields['roles'].queryset = Group.objects.filter(fase__id=fase)
