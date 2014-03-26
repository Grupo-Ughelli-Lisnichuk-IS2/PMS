from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$','principal.views.inicio'),
     url(r'^usuario/nuevo$','principal.views.nuevo_usuario'),
     url(r'^perfil/nuevo$','principal.views.nuevo_perfil'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ingresar/$','principal.views.ingresar'),
    url(r'^admin/', include(admin.site.urls)),
)
