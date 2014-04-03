#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm):

    username = forms.RegexField(label=_("Usuario: "),regex=r'^\w+$', widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Username")}))
    password = forms.CharField(label=_("Contraseña: "),widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Password")}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                classes = self.fields[f_name].widget.attrs.get('class', '')
                classes += ' has-error'
                self.fields[f_name].widget.attrs['class'] = classes



class RegistrationForm(forms.Form):

    username = forms.RegexField(label=_("Usuario:  "),regex=r'^\w+$', widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Username")}))
    first_name = forms.CharField(label=_("Nombre:  "),widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Nombre")}))
    last_name = forms.CharField(label=_("Apellido:  "),widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Apellido")}))
    email = forms.EmailField(label=_("Email:  "),widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'form-control', 'placeholder': _("Email Address")}))
    password1 = forms.CharField(label=_("Constraseña:  "),widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Password")}))
    password2 = forms.CharField(label=_("Repita la contraseña:  "), widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Confirm your password")}))


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' has-error'
                    self.fields[f_name].widget.attrs['class'] = classes

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("Account already exists."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Passwords don't match."))
        return self.cleaned_data
