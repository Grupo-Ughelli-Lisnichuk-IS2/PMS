from django.conf.urls import patterns, url, include
from django.contrib import admin
from usuarios import viewsUsuarios

from django.views.generic import edit, TemplateView
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
     url(r'^$',TemplateView.as_view(template_name='inicio.html')),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^usuarios/',include('usuarios.urls')),
    url(r'^roles/',include('roles.urls')),
    url(r'^fases/',include('fases.urls')),
    url(r'^tiposDeItem/',include('tiposDeItem.urls')),
    url(r'^desarrollo/',include('items.urls')),
    url(r'^proyectos/',include('proyectos.urls')),
    url(r'^gestionDeCambios/lineasBase/',include('lineasBase.urls')),

     url(r'^gestionDeCambios/solicitudes/',include('solicitudesCambio.urls')),

    url(r'^reporte/listar_proyectos_reporte/$','reportes.reportes.listar_proyectos_reporte'),
    url(r'^reporte/usuarios/$','reportes.reportes.descargar_reporteUsuarios'),
    url(r'^reporte/roles/$','reportes.reportes.descargar_reporteRoles'),
    url(r'^reporte/proyectos/$','reportes.reportes.descargar_reporteProyectos'),
    url(r'^reporte/ReportesProyectos/$','reportes.reportes.descargar_reporteProyectos'),
    url(r'^principal/$',viewsUsuarios.principal),
    url(r'^denegado/$',TemplateView.as_view(template_name='403.html')),
   # url(r'^login/$', viewsUsuarios.LoginView.as_view(), name='login'),
    url(r'^logout/$', viewsUsuarios.LogoutView.as_view(), name='logout'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    # register
    )

