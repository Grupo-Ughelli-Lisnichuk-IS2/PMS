from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
        url(r'^listar/$','solicitudesCambio.viewsSolicitudesCambio.listar_solicitudes'),
        url(r'^votar/(?P<id_solicitud>\d+)$','solicitudesCambio.viewsSolicitudesCambio.votar'),
        url(r'^votacion/(?P<id_solicitud>\d+)$','solicitudesCambio.viewsSolicitudesCambio.detalle_solicitud'),
        )