from django.conf.urls import patterns, url, include
from django.contrib import admin

from roles import viewsRoles

from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^crear/$', 'roles.viewsRoles.crear_rol'),
    url(r'^$',login_required(viewsRoles.lista_roles,'/usuarios','/login')),
    url(r'^(?P<id_rol>\d+)$', 'roles.viewsRoles.detalle_rol'),
    url(r'^eliminar/(?P<id_rol>\d+)$', 'roles.viewsRoles.eliminar_rol'),
    url(r'^modificar/(?P<id_rol>\d+)$', 'roles.viewsRoles.editar_rol'),
    url(r'^search/$',viewsRoles.buscarRol, name='buscar_roles'),
    url(r'^register/success/$',
        viewsRoles.RegisterSuccessView.as_view(
        ), name='register-success'),
    )
