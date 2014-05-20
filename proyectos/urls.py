from django.conf.urls import patterns, url
from django.contrib import admin

from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()
from proyectos import viewsProyectos

urlpatterns = patterns('',
        url(r'^registrar/$','proyectos.viewsProyectos.registrar_proyecto'),
        url(r'^$','proyectos.viewsProyectos.listar_proyectos'),
        url(r'^(?P<id_proyecto>\d+)$', 'proyectos.viewsProyectos.detalle_proyecto'),
        url(r'^search/$',viewsProyectos.buscar_proyecto, name='buscar_proyectos'),
        url(r'^modificar/(?P<id_proyecto>\d+)$', 'proyectos.viewsProyectos.editar_proyecto'),
        url(r'^cambiarEstado/(?P<id_proyecto>\d+)$', 'proyectos.viewsProyectos.cambiar_estado_proyecto'),
        url(r'^importar/(?P<id_proyecto>\d+)$', 'proyectos.viewsProyectos.importar_proyecto'),
        url(r'^equipo/(?P<id_proyecto>\d+)$', 'proyectos.viewsProyectos.ver_equipo'),
        url(r'^register/success/$',
        'proyectos.viewsProyectos.RegisterSuccessView'),
        url(r'^register/failed/(?P<id_proyecto>\d+)$','proyectos.viewsProyectos.RegisterFailedView')
        )