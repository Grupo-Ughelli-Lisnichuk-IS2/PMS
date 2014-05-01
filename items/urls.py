from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from items import viewsItems

urlpatterns = patterns('',
        url(r'^proyectos/$','items.viewsItems.listar_proyectos'),
        url(r'^proyectos/fases/(?P<id_proyecto>\d+)$','items.viewsItems.listar_fases'),
        url(r'^fases/tiposDeItem/(?P<id_fase>\d+)$','items.viewsItems.listar_tiposDeItem'),
        url(r'^item/crear/(?P<id_tipoItem>\d+)$','items.viewsItems.crear_item'),
        url(r'^item/listar/(?P<id_tipo_item>\d+)$','items.viewsItems.listar_items'),
        url(r'^item/detalle/(?P<id_item>\d+)$','items.viewsItems.detalle_item'),
        url(r'^item/crear/hijo/(?P<id_item>\d+)$','items.viewsItems.crear_item_hijo'),
        url(r'^item/descargar/archivo/(?P<idarchivo>\d+)$','items.viewsItems.des'),
        url(r'^item/modificar/(?P<id_item>\d+)$','items.viewsItems.editar_item'),
        url(r'^item/versiones/(?P<id_item>\d+)$','items.viewsItems.listar_versiones'),
        url(r'^item/reversionar/(?P<id_version>\d+)$','items.viewsItems.reversionar_item'),
        url(r'^item/archivos/(?P<id_item>\d+)$','items.viewsItems.listar_archivos'),
        url(r'^item/archivos/eliminar/(?P<id_archivo>\d+)$','items.viewsItems.eliminar_archivo'),
        url(r'^item/padre/(?P<id_item>\d+)$','items.viewsItems.cambiar_padre'),
        url(r'^item/antecesor/(?P<id_item>\d+)$','items.viewsItems.cambiar_antecesor'),
        url(r'^item/atributos/(?P<id_item>\d+)$','items.viewsItems.listar_atributos'),
        url(r'^item/detalle/version/(?P<id_version>\d+)$','items.viewsItems.detalle_version_item'),
        url(r'^item/cambiar_estado/(?P<id_item>\d+)$','items.viewsItems.cambiar_estado_item'),
        )