from django.conf.urls import patterns, url
from django.contrib import admin
from usuarios import viewsUsuarios
from roles import views
from django.views.generic import edit, TemplateView
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$',TemplateView.as_view(template_name='inicio.html')),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^usuarios/$',login_required(viewsUsuarios.lista_usuarios,'/usuarios','/login')),
    url(r'^usuarios/(?P<id_user>\d+)$', 'usuarios.viewsUsuarios.detalle_usuario'),
    url(r'^modificar/(?P<id_user>\d+)$', 'usuarios.viewsUsuarios.modificar_usuario'),
    url(r'^configurar/$', 'usuarios.viewsUsuarios.editar_perfil'),
    url(r'^cambiarPass/$', 'usuarios.viewsUsuarios.cambiar_pass'),
    url(r'^crearRol/$', 'roles.views.crear_rol'),
    url(r'^roles/$',login_required(views.lista_roles,'/usuarios','/login')),
    url(r'^roles/(?P<id_rol>\d+)$', 'roles.views.detalle_rol'),
    url(r'^eliminarRoles/(?P<id_rol>\d+)$', 'roles.views.eliminar_rol'),
    url(r'^modificarRoles/(?P<id_rol>\d+)$', 'roles.views.editar_rol'),
    url(r'^search/$',viewsUsuarios.buscarUsuario, name='buscar_usuarios'),
    url(r'^searchRoles/$',views.buscarRol, name='buscar_roles'),
    url(r'^principal/$',login_required(TemplateView.as_view(template_name='principal.html'), '/', '/login')),
    url(r'^login/$', viewsUsuarios.LoginView.as_view(), name='login'),
    url(r'^logout/$', viewsUsuarios.LogoutView.as_view(), name='logout'),
    # register
    url(r'^register/$', login_required(viewsUsuarios.RegisterView.as_view(), '/register', '/login')),
    url(r'^register/success/$',
        viewsUsuarios.RegisterSuccessView.as_view(
        ), name='register-success'),

        )

