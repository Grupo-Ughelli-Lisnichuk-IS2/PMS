from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()
from tiposDeItem import viewsTiposDeItem


urlpatterns = patterns('',
        url(r'^registrar/(?P<id_fase>\d+)$','tiposDeItem.viewsTiposDeItem.crear_tipoItem'),
        url(r'^eliminar/tipo_atributo/(?P<id_atributo>\d+)-(?P<id_tipoItem>\d+)$','tiposDeItem.viewsTiposDeItem.eliminar_atributo'),
        url(r'^fase/(?P<id_fase>\d+)$','tiposDeItem.viewsTiposDeItem.listar_tiposItem'),
        url(r'^(?P<id_tipoItem>\d+)$', 'tiposDeItem.viewsTiposDeItem.detalle_tipoItem'),
        url(r'^(?P<id_tipoItem>\d+)/crear_atributo$', 'tiposDeItem.viewsTiposDeItem.crear_atributo'),
        url(r'^modificar/(?P<id_tipoItem>\d+)$', 'tiposDeItem.viewsTiposDeItem.editar_TipoItem'),
        url(r'^importar/(?P<id_tipoItem>\d+)-(?P<id_fase>\d+)$','tiposDeItem.viewsTiposDeItem.importar_tipoItem'),
        url(r'^eliminar/(?P<id_tipoItem>\d+)$','tiposDeItem.viewsTiposDeItem.eliminar_tipoItem'),
        url(r'^listar/(?P<id_fase>\d+)$','tiposDeItem.viewsTiposDeItem.listar_tiposItemProyecto'),

        )

