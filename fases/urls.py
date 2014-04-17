from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()
from fases import viewsFases


urlpatterns = patterns('',
        url(r'^registrar/$','fases.viewsFases.registrar_fase'),
        url(r'^$',login_required(viewsFases.listar_fases,'/fases','/login')),
        url(r'^/(?P<id_fase>\d+)$', 'fases.viewsFases.detalle_fase'),
        )