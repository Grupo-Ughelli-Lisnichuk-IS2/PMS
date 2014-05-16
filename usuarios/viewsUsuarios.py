from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View, TemplateView, ListView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from usuarios.formsUsuarios import RegistrationForm, LoginForm, UserForm
from django.views.generic.edit import FormView
from PMS import settings
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from proyectos.models import Proyecto
from django.template.response import TemplateResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
__author__ = 'Grupo R13'
__date__ = '04-04-2014'
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
            last_name=form.cleaned_data['last_name']
        )

        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('register-success')


class RegisterSuccessView(TemplateView):

    template_name = 'registration/success.html'

@login_required
@permission_required('user')
def lista_usuarios(request):
    '''
    vista para listar todos los usuarios del sistema
    '''

    usuarios = User.objects.all().order_by('is_active').reverse()
    return render_to_response('usuarios/lista_usuarios.html', {'datos': usuarios}, context_instance=RequestContext(request))

@login_required
@permission_required('user')
def detalle_usuario(request, id_user):

    '''
    vista para ver los detalles del usuario <id_user>
    '''

    dato = get_object_or_404(User, pk=id_user)
    roles = Group.objects.filter(user__id=id_user)
    nombres=[]
    for rol in roles:
        nombres.append(rol.name)

    return render_to_response('usuarios/detalle_usuario.html', {'usuario': dato, 'roles':nombres}, context_instance=RequestContext(request))


@login_required
@permission_required('user')
def cambiar_pass (request,
                    template_name='registration/editar_perfil.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    '''
    vista para que un usuario pueda cambiar su contrasenha
    '''
    if request.method == 'POST':
        # formulario enviado
        perfil_form = password_change_form(user=request.user, data= request.POST)
        if perfil_form.is_valid():
            # formulario validado correctamente
            perfil_form.save()

            return HttpResponseRedirect('/usuarios/register/success/')
    else:
        # formulario inicial
        perfil_form=password_change_form(user=request.user)
    return render_to_response('usuarios/cambiar_pass.html', { 'perfil_form': perfil_form}, context_instance=RequestContext(request))


@login_required
@permission_required('user')
def editar_perfil(request):

    '''
    Vista para modificar los datos de un usuario
    '''
    if request.method == 'POST':
        # formulario enviado
        user_form = UserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            # formulario validado correctamente
            user_form.save()
            return HttpResponseRedirect('/usuarios/register/success/')

    else:
        # formulario inicial
        user_form = UserForm(instance=request.user)
    return render_to_response('usuarios/editar_perfil.html', { 'user_form': user_form}, context_instance=RequestContext(request))


@login_required
@permission_required('user')
def modificar_usuario(request, id_user):

    '''
    vista para cambiar el estado del usuario id_user
    '''

    dato = get_object_or_404(User, pk=id_user)
    dato.is_active = not (dato.is_active)
    if dato.is_active == False:
        roles=User.objects.filter(groups__id=dato.id)
        comite=Proyecto.objects.filter(comite__id=dato.id)
        if comite.count()==0 and roles.count()==0:
            dato.save()
            messages.add_message(request, settings.DELETE_MESSAGE, "Estado Cambiado")

        else:
            messages.add_message(request, settings.DELETE_MESSAGE, "No se puede cambiar el estado del Usuario. Tiene rol(es) asociado(s)")
    else:
        dato.save()
        messages.add_message(request, settings.DELETE_MESSAGE, "Estado Cambiado")
    usuarios = User.objects.all().order_by('is_active').reverse()
    return render_to_response('usuarios/lista_usuarios.html', {'datos': usuarios}, context_instance=RequestContext(request))


@login_required
@permission_required('user')
def buscarUsuario(request):
    '''
    vista para buscar un usuario dentro del listado de usuarios del sistema
    '''
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(username=query) |
            Q(first_name=query) |
            Q(last_name=query)
        )
        results = User.objects.filter(qset).distinct().order_by('is_active').reverse()
    else:
        results = []
    return render_to_response('usuarios/lista_usuarios.html', {'datos': results}, context_instance=RequestContext(request))
