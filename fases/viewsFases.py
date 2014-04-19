from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from PMS import settings
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
            fecha1=datetime.strptime(fecha,'%Y-%m-%d')
            newFase = Fase(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],maxItems = request.POST["maxItems"],fInicio = fecha,estado = "PEN", proyecto_id = id_proyecto)
            aux=0
            orden=Fase.objects.filter(proyecto_id=id_proyecto)
            roles = request.POST.getlist("roles")
            for rol in roles:
               fase=Fase.objects.filter(roles__id=rol)
               if(fase.count()>0):
                 aux=1
            if aux>0:
                messages.add_message(request, settings.DELETE_MESSAGE, "Error: El Rol ya ha sido asignado a otra fase")
            else:
                proyecto=Proyecto.objects.get(id=id_proyecto)
                cantidad = orden.count()
                if cantidad>0:
                   anterior = Fase.objects.get(orden=cantidad)
                   if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                        messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase anterior")
                   else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                        else:
                            roles = request.POST.getlist("roles")
                            newFase.orden=orden.count()+1
                            newFase.save()
                            for rol in roles:
                                newFase.roles.add(rol)
                                newFase.save()
                            return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
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
    id_proyecto= fase.proyecto_id
    if request.method == 'POST':
        # formulario enviado
        fase_form = ModificarFaseForm(request.POST, instance=fase)

        if fase_form.is_valid():
            # formulario validado correctamente
            fase_form.save()
            return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
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
            aux=0
            roles = request.POST.getlist("roles")
            for rol in roles:
               fase=Fase.objects.filter(roles__id=rol)
               if(fase.count()>0):
                 aux=1
            if aux>0:
                messages.add_message(request, settings.DELETE_MESSAGE, "Error. El Rol ya ha sido asignado a otra fase")
            else:
                newFase.save()
                roles = request.POST.getlist("roles")
                for rol in roles:
                   newFase.roles.add(rol)
                newFase.save()
                return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
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
    roles=Group.objects.filter(fase__id=id_fase)
    return render_to_response('fases/listar_roles.html', {'roles': roles, 'usuario':usuario}, context_instance=RequestContext(request))

def asociar(request,id_rol,id_usuario):
    usuario=User.objects.get(id=id_usuario)
    rol = Group.objects.get(id=id_rol)
    usuario.groups.add(rol)
    usuario.save()
    return HttpResponseRedirect('/proyectos')

def des(request,id_fase):
    roles=Group.objects.filter(fase__id=id_fase)
    usuarios=[]
    for rol in roles:
        p=User.objects.filter(groups__id=rol.id)
        for pp in p:
            usuarios.append(pp)
    return render_to_response('fases/lista_usuarios_d.html', {'datos': usuarios,"fase":id_fase}, context_instance=RequestContext(request))

def desasociar(request,id_usuario, id_fase):
    '''
    vista para listar las fases de un proyecto
    '''
    usuario=User.objects.get(id=id_usuario)
    roles=Group.objects.filter(fase__id=id_fase)
    for rol in roles:
        usuario.groups.remove(rol)
        usuario.save()
    return HttpResponseRedirect('/proyectos')