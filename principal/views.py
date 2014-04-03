from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from principal.forms import RegistrationForm, LoginForm, UsuarioChangeStateForm
from django.views.generic.edit import FormView
from PMS import settings
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.shortcuts import render_to_response


__author__ = 'Grupo R13'
__date__ = '04-04-2013'
__version__ = '1.0'
__text__ = 'Este modulo contiene funciones que permiten el control de administracion de usuarios'



class RegisterView(FormView):
    ''' vista para la creacion de un nuevo ususario
    '''
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        #if request.user.is_authenticated():
         #   return HttpResponseRedirect(config.INDEX_REDIRECT_URL)
        #else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name']
        )

        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('register-success')


class RegisterSuccessView(TemplateView):
    template_name = 'registration/success.html'


class UsuariosListView(ListView):
    '''
    vista para listar todos los usuarios registrados en el sistema

    '''
    model = User
    template_name='lista_usuarios.html'
    login_required = True
    def dispatch(self, *args, **kwargs):
        return super(UsuariosListView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(UsuariosListView, self).get_context_data(**kwargs)
        return context

