from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from items import viewsItems

urlpatterns = patterns('',
        url(r'^proyectos/$','items.viewsItems.listar_proyectos'),

        )