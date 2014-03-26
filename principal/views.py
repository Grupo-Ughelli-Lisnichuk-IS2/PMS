from principal.forms import UserCreateForm, PerfilCreateForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required



# Create your views here.
def inicio(request):
    return render_to_response('inicio.html',context_instance=RequestContext(request))
def ingresar(request):
  #  if not request.user.is_anonymous():
   #     return HttpResponseRedirect('/privado')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)

            if acceso is not None:
                if acceso.is_superuser:
                    login(request, acceso)
                    return HttpResponseRedirect('/admin')
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('privado.html', {'usuario':usuario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def nuevo_usuario(request):
	if request.method=='POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = UserCreateForm()
	return render_to_response('nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def nuevo_perfil(request):
	if request.method=='POST':
		user_form = UserCreateForm(request.POST, instance=request.user)
		perfil_form = PerfilCreateForm(request.POST, instance=request.user)

		if user_form.is_valid() and perfil_form.is_valid():
			user_form.save()
			perfil_form.save()
			return HttpResponseRedirect('/privado')
	else:
		user_form = UserCreateForm(instance=request.user)
		perfil_form = PerfilCreateForm(instance=request.user)
	return render_to_response('nuevoperfil2.html',{'user_form':UserCreateForm, 'perfil_form':perfil_form}, context_instance=RequestContext(request))




