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
        )