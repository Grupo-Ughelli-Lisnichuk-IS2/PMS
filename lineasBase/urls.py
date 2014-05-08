from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
        url(r'^proyectos/$','lineasBase.viewsLineasBase.gestionar_proyectos'),
        url(r'^proyectos/fases/(?P<id_proyecto>\d+)$','lineasBase.viewsLineasBase.gestionar_fases'),
        url(r'^listar/(?P<id_fase>\d+)$','lineasBase.viewsLineasBase.listar_lineasBase'),
        url(r'^crear/(?P<id_fase>\d+)$','lineasBase.viewsLineasBase.crear_lineaBase'),
        )