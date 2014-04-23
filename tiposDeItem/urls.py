from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()
from tiposDeItem import viewsTiposDeItem


urlpatterns = patterns('',
        url(r'^registrar/(?P<id_fase>\d+)$','tiposDeItem.viewsTiposDeItem.crear_tipoItem'),
        url(r'^fase/(?P<id_fase>\d+)$','tiposDeItem.viewsTiposDeItem.listar_tiposItem'),
        )