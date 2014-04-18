from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()
from fases import viewsFases


urlpatterns = patterns('',
        url(r'^registrar/(?P<id_proyecto>\d+)$','fases.viewsFases.registrar_fase'),
        url(r'^proyecto/(?P<id_proyecto>\d+)$',login_required(viewsFases.listar_fases,'/fases','/login')),
        url(r'^(?P<id_fase>\d+)$', 'fases.viewsFases.detalle_fase'),
        url(r'^modificar/(?P<id_fase>\d+)$', 'fases.viewsFases.editar_fase'),
        url(r'^sistema/(?P<id_proyecto>\d+)$',login_required(viewsFases.fases_sistema,'/fases/sistema','/login')),
        url(r'^importar/(?P<id_fase>\d+)-(?P<id_proyecto>\d+)$', 'fases.viewsFases.importar_fase'),
        url(r'^asignar/(?P<id_fase>\d+)$', 'fases.viewsFases.asignar_usuario'),
        url(r'^asignar/(?P<id_usuario>\d+)/(?P<id_fase>\d+)$', 'fases.viewsFases.asignar_rol'),
        )