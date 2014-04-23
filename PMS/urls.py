from django.conf.urls import patterns, url, include
from django.contrib import admin
from usuarios import viewsUsuarios
from roles import viewsRoles
from django.views.generic import edit, TemplateView
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()
from fases import viewsFases


urlpatterns = patterns('',
    # Examples:
     url(r'^$',TemplateView.as_view(template_name='inicio.html')),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^usuarios/',include('usuarios.urls')),
    url(r'^roles/',include('roles.urls')),
    url(r'^fases/',include('fases.urls')),
    url(r'^tiposDeItem/',include('tiposDeItem.urls')),
    url(r'^proyectos/',include('proyectos.urls')),
    url(r'^principal/$',TemplateView.as_view(template_name='principal.html')),
   # url(r'^login/$', viewsUsuarios.LoginView.as_view(), name='login'),
    url(r'^logout/$', viewsUsuarios.LogoutView.as_view(), name='logout'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    # register
    )

