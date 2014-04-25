from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from items import viewsItems

urlpatterns = patterns('',
        url(r'^proyectos/$','items.viewsItems.listar_proyectos'),
        url(r'^proyectos/fases/(?P<id_proyecto>\d+)$','items.viewsItems.listar_fases'),
        url(r'^fases/tiposDeItem/(?P<id_fase>\d+)$','items.viewsItems.listar_tiposDeItem'),
        )