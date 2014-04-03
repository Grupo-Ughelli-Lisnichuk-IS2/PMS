from django.conf.urls import patterns, url
from django.contrib import admin

from principal import views

from django.views.generic import edit, TemplateView
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$',TemplateView.as_view(template_name='inicio.html')),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^usuarios/$',login_required(views.UsuariosListView.as_view(), '/usuarios', '/login')),
    url(r'^search/$',views.search, name='buscar_usuarios'),
    url(r'^principal/$',login_required(TemplateView.as_view(template_name='principal.html'), '/', '/login')),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # register
    url(r'^register/$', login_required(views.RegisterView.as_view(), '/register', '/login')),
    url(r'^register/success/$',
        views.RegisterSuccessView.as_view(
        ), name='register-success'),

        )

