from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from principal.formsUsuarios import RegistrationForm, LoginForm
from django.views.generic.edit import FormView
from PMS import settings
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages

__author__ = 'Grupo R13'
__date__ = '04-04-2013'
__version__ = '1.0'
__text__ = 'Este modulo contiene funciones que permiten el control de administracion de usuarios'

class LoginView(FormView):
    '''Vista para realizar el login '''
    template_name = 'registration/login.html'
    form_class = LoginForm
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        try:
            return settings.LOGIN_REDIRECT_URL
        except:
            return "/accounts/profile/"


class LogoutView(View):
    '''Vista para cerrar la sesion'''
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)



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




def lista_usuarios(request):
	usuarios = User.objects.all()
	return render_to_response('lista_usuarios.html',{'datos':usuarios}, context_instance = RequestContext(request))


def detalle_usuario(request, id_user):
	dato = get_object_or_404(User,pk=id_user)
	return render_to_response('detalle_usuario.html',{'usuario':dato}, context_instance=RequestContext(request))


def modificar_usuario(request, id_user):
	dato = get_object_or_404(User,pk=id_user) 
	dato.is_active=not(dato.is_active)
	dato.save()
    	messages.add_message(request, settings.DELETE_MESSAGE,"Estado Cambiado")
	return render_to_response('lista_usuarios.html', {'datos':User.objects.all}, context_instance=RequestContext(request))


def buscarUsuario(request):
    '''
    vista para buscar los usuarios del sistema
    '''
    query = request.GET.get('q', '')
    if query:
            qset = (
                Q(username=query) |
                Q(first_name=query) |
                Q(last_name=query)
            )
            results = User.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('lista_usuarios.html', {'datos':results}, context_instance=RequestContext(request))