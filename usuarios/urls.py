from django.conf.urls import patterns, url
from django.contrib import admin
from usuarios import viewsUsuarios
from roles import viewsRoles
from django.views.generic import edit, TemplateView
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()
from fases import viewsFases
urlpatterns = patterns('',
    url(r'^$','usuarios.viewsUsuarios.lista_usuarios'),
    url(r'^(?P<id_user>\d+)$', 'usuarios.viewsUsuarios.detalle_usuario'),
    url(r'^modificar/(?P<id_user>\d+)$', 'usuarios.viewsUsuarios.modificar_usuario'),
    url(r'^configurar/$', 'usuarios.viewsUsuarios.editar_perfil'),
    url(r'^cambiarPass/$', 'usuarios.viewsUsuarios.cambiar_pass'),
    url(r'^search/$',viewsUsuarios.buscarUsuario, name='buscar_usuarios'),
    url(r'^register/$', viewsUsuarios.RegisterView.as_view),
    url(r'^register/success/$',
        viewsUsuarios.RegisterSuccessView.as_view(
        ), name='register-success'),
    )