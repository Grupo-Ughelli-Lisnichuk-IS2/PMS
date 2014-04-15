from django.conf.urls import patterns, url
from django.contrib import admin
from principal import viewsUsuarios
from django.views.generic import edit, TemplateView
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$',TemplateView.as_view(template_name='inicio.html')),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^usuarios/$',login_required(viewsUsuarios.lista_usuarios,'/usuarios','/login')),
    url(r'^usuarios/(?P<id_user>\d+)$', 'principal.viewsUsuarios.detalle_usuario'),
    url(r'^modificar/(?P<id_user>\d+)$', 'principal.viewsUsuarios.modificar_usuario'),
    url(r'^search/$',viewsUsuarios.buscarUsuario, name='buscar_usuarios'),
    url(r'^principal/$',login_required(TemplateView.as_view(template_name='principal.html'), '/', '/login')),
    url(r'^login/$', viewsUsuarios.LoginView.as_view(), name='login'),
    url(r'^logout/$', viewsUsuarios.LogoutView.as_view(), name='logout'),
    # register
    url(r'^register/$', login_required(viewsUsuarios.RegisterView.as_view(), '/register', '/login')),
    url(r'^register/success/$',
        viewsUsuarios.RegisterSuccessView.as_view(
        ), name='register-success'),

        )

