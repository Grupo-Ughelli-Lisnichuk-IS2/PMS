from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
        url(r'^proyectos/$','lineasBase.viewsLineasBase.gestionar_proyectos'),

        )