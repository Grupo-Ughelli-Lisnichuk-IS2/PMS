#encoding:utf-8
from django.forms import ModelForm
from django import forms
from models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2","first_name","last_name")


class PerfilCreateForm(UserCreationForm):
    class Meta:
        model = Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil

