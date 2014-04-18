from django.shortcuts import render
from django.contrib.auth.models import User
from fases.models import Fase
from proyectos.models import Proyecto
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from fases.formsFases import FaseForm, ModificarFaseForm, CrearFaseForm, RolesForm
from datetime import datetime


# Create your views here.


#newPost = Post(title = request.POST["title"], url = request.POST["url"], content = request.POST["content"])
            #guardamos el post

#.datetime.strptime('5/10/1955', '%d/%m/%Y')


def registrar_fase(request,id_proyecto):
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearFaseForm(request.POST)
        if formulario.is_valid():

            fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%y')
            fecha=fecha.strftime('%Y-%m-%d')
            newFase = Fase(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],maxItems = request.POST["maxItems"],fInicio = fecha,orden = request.POST["orden"],estado = "PEN", proyecto_id = id_proyecto)

            newFase.save()
            roles = request.POST.getlist("roles")
            for rol in roles:
               newFase.roles.add(rol)
            newFase.save()
            return HttpResponseRedirect('/fases/proyecto/'+str(id_proyecto))
    else:
        formulario = CrearFaseForm()
    return render_to_response('fases/registrarFase.html',{'formulario':formulario}, context_instance=RequestContext(request))


def listar_fases(request,id_proyecto):
    '''
    vista para listar las fases de un proyecto
    '''

    fases = Fase.objects.filter(proyecto_id=id_proyecto)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    return render_to_response('fases/listar_fases.html', {'datos': fases, 'proyecto' : proyecto}, context_instance=RequestContext(request))


def fases_sistema(request,id_proyecto):
    '''
    vista para listar las fases del sistema
    '''
    fases = Fase.objects.all()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    return render_to_response('fases/fases_sistema.html', {'datos': fases, 'proyecto' : proyecto}, context_instance=RequestContext(request))


def detalle_fase(request, id_fase):

    '''
    vista para ver los detalles del usuario <id_user> del sistema
    '''

    dato = get_object_or_404(Fase, pk=id_fase)
    return render_to_response('fases/detalle_fase.html', {'datos': dato}, context_instance=RequestContext(request))


def editar_fase(request,id_fase):
    fase= Fase.objects.get(id=id_fase)
    if request.method == 'POST':
        # formulario enviado
        fase_form = ModificarFaseForm(request.POST, instance=fase)

        if fase_form.is_valid():
            # formulario validado correctamente
            fase_form.save()
            return HttpResponseRedirect('/register/success/')
    else:
        # formulario inicial
        fase_form = ModificarFaseForm(instance=fase)
    return render_to_response('fases/editar_fase.html', { 'form': fase_form, 'fase': fase}, context_instance=RequestContext(request))



def importar_fase(request, id_fase,id_proyecto):
    fase= Fase.objects.get(id=id_fase)
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearFaseForm(request.POST)
        if formulario.is_valid():
            fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%y')
            fecha=fecha.strftime('%Y-%m-%d')
            newFase = Fase(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],maxItems = request.POST["maxItems"],fInicio = fecha,orden = request.POST["orden"],estado = "PEN", proyecto_id = id_proyecto)
            newFase.save()
            roles = request.POST.getlist("roles")
            for rol in roles:
               newFase.roles.add(rol)
            newFase.save()
            return HttpResponseRedirect('/principal')
    else:
        formulario = CrearFaseForm(initial={'descripcion':fase.descripcion, 'maxItems':fase.maxItems, 'fInicio':fase.fInicio, 'orden':fase.orden})

    return render_to_response('fases/registrarFase.html',{'formulario':formulario}, context_instance=RequestContext(request))

def asignar_usuario(request,id_fase):
    '''
    vista para listar las fases de un proyecto
    '''

    usuarios=User.objects.filter(is_active=True)
    fase=Fase.objects.get(id=id_fase)
    return render_to_response('fases/lista_usuarios.html', {'datos': usuarios, 'fase' : fase}, context_instance=RequestContext(request))
def asignar_rol(request,id_usuario, id_fase):
    '''
    vista para listar las fases de un proyecto
    '''
    fase=Fase.objects.get(id=id_fase)
    usuario=User.objects.get(id=id_usuario)
    if request.method=='POST':


        formulario = RolesForm(request.POST, fase=id_fase)
        if formulario.is_valid():
            roles = request.POST.getlist("roles")
            for rol in roles:
               usuario.groups.add(rol)
            usuario.save()
            return HttpResponseRedirect('/fases/proyecto/'+str(fase.proyecto_id))
    else:
        formulario = RolesForm(fase=id_fase)
    return render_to_response('fases/listar_roles.html', {'roles': formulario, 'usuario':usuario}, context_instance=RequestContext(request))