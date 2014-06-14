from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from PMS import settings
from fases.models import Fase
from items.viewsItems import es_miembro
from lineasBase.viewsLineasBase import es_lider
from proyectos.models import Proyecto
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from fases.formsFases import FaseForm, ModificarFaseForm, CrearFaseForm, RolesForm
from datetime import datetime


@login_required
@permission_required('fase')
def registrar_fase(request,id_proyecto):
    '''
        Vista para registrar una nueva fase dentro de un proyecto. Asigna automaticamente el orden,
        realiza las comprobaciones necesarias con respecto a la fecha de inicio y comprueba tambien que los roles
        asociados no pertenezcan a otra fase.
    '''
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    if proyecto.estado!='PEN':
        return HttpResponseRedirect ('/denegado')
    if request.method=='POST':

        formulario = CrearFaseForm(request.POST)
        if formulario.is_valid():
            if len(str(request.POST["fInicio"])) != 10 : #Comprobacion de formato de fecha
                messages.add_message(request, settings.DELETE_MESSAGE, "Error: El formato de Fecha es: DD/MM/AAAA")
            else:
                fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
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
                if aux>0:#comprobacion de pertenencia de roles
                    messages.add_message(request, settings.DELETE_MESSAGE, "Error: El Rol ya ha sido asignado a otra fase")
                else:
                    proyecto=Proyecto.objects.get(id=id_proyecto)
                    cantidad = orden.count()
                    if cantidad>0:#comprobaciones de fecha
                       anterior = Fase.objects.get(orden=cantidad, proyecto_id=id_proyecto)
                       if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase anterior")
                       else:
                            if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                            else:
                                roles = request.POST.getlist("roles")
                                newFase.orden=orden.count()+1 #Calculo del orden de la fase a crear
                                newFase.save()
                                for rol in roles:
                                    newFase.roles.add(rol)
                                    newFase.save()
                                return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                    else:
                        roles = request.POST.getlist("roles")
                        newFase.orden=1
                        newFase.save()
                        for rol in roles:
                            newFase.roles.add(rol)
                            newFase.save()
                        return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearFaseForm()
    return render_to_response('fases/registrarFase.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def listar_fases(request,id_proyecto):
    '''
    vista para listar las fases pertenecientes a un proyecto
    '''

    fases = Fase.objects.filter(proyecto_id=id_proyecto).order_by('orden')
    proyecto = Proyecto.objects.get(id=id_proyecto)

    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    else:
        return render_to_response('fases/listar_fases.html', {'datos': fases, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def fases_sistema(request,id_proyecto):
    '''
    vista para listar las fases del sistema
    '''
    fases = Fase.objects.all()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if proyecto.estado!='PEN':
        return HttpResponseRedirect ('/denegado')
    return render_to_response('fases/fases_sistema.html', {'datos': fases, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def detalle_fase(request, id_fase):

    '''
    vista para ver los detalles del usuario <id_user> del sistema
    '''

    dato = get_object_or_404(Fase, pk=id_fase)
    proyecto = Proyecto.objects.get(id=dato.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    return render_to_response('fases/detalle_fase.html', {'datos': dato}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def editar_fase(request,id_fase):
    '''
        Vista para modificar la descripcion, cantidad maxima de items y fecha de Inicio de una fase.
        Realiza las comprobaciones necesarias con respecto a la fecha de inicio.
    '''
    fase= get_object_or_404(Fase,id=id_fase)
    if fase.estado!='PEN':
        return HttpResponseRedirect ('/denegado')
    id_proyecto= fase.proyecto_id
    proyecto = get_object_or_404(Proyecto,id=id_proyecto)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    if request.method == 'POST':
        # formulario enviado
        fase_form = ModificarFaseForm(request.POST, instance=fase)

        if fase_form.is_valid():
            if len(str(request.POST["fInicio"])) != 10 : #comprobacion de formato de fecha
                messages.add_message(request, settings.DELETE_MESSAGE, "Error: El formato de Fecha es: DD/MM/AAAA")
            else:
                fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
                fecha=fecha.strftime('%Y-%m-%d')
                fecha1=datetime.strptime(fecha,'%Y-%m-%d')
                proyecto=Proyecto.objects.get(id=fase.proyecto_id)
                orden=Fase.objects.filter(proyecto_id=proyecto.id)
                cantidad = orden.count()
                if cantidad>1 and fase.orden != cantidad and fase.orden >1: #comprobaciones de fechas
                       anterior = Fase.objects.get(orden=(fase.orden)-1, proyecto_id=id_proyecto)
                       siguiente = Fase.objects.get(orden=(fase.orden)+1, proyecto_id=id_proyecto)
                       if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase anterior")
                       else:
                           if fecha1>datetime.strptime(str(siguiente.fInicio),'%Y-%m-%d'):
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase siguiente")
                           else:
                                if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                    messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                                else:
                                    fase_form.save()
                                    return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                elif cantidad>1 and fase.orden != cantidad and fase.orden==1:
                   siguiente = Fase.objects.get(orden=(fase.orden)+1, proyecto_id=id_proyecto)
                   if fecha1>datetime.strptime(str(siguiente.fInicio),'%Y-%m-%d'):
                        messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase siguiente")
                   else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                        else:
                            fase_form.save()
                            return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                elif cantidad>1 and fase.orden == cantidad:
                    anterior = Fase.objects.get(orden=(fase.orden)-1, proyecto_id=id_proyecto)
                    if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                        messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase anterior")
                    else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                        else:
                            fase_form.save()
                            return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                else:
                    if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                        messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                    else:
                        fase_form.save()
                        return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        # formulario inicial
        fase_form = ModificarFaseForm(instance=fase)
    return render_to_response('fases/editar_fase.html', { 'form': fase_form, 'fase': fase}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def importar_fase(request, id_fase,id_proyecto):

    '''
        Vista para importar los datos de una fase existente para su utilizacion en la creacion de una nueva.
        Realiza las comprobaciones necesarias con respecto a la fecha de inicio y orden de fase.
    '''
    proyecto = get_object_or_404(id=id_proyecto)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    fase= Fase.objects.get(id=id_fase)
    if request.method=='POST':

        formulario = CrearFaseForm(request.POST)
        if formulario.is_valid():
            if len(str(request.POST["fInicio"])) != 10 :
                messages.add_message(request, settings.DELETE_MESSAGE, "Error: El formato de Fecha es: DD/MM/AAAA")
            else:
                fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
                fecha=fecha.strftime('%Y-%m-%d')
                fecha1=datetime.strptime(fecha,'%Y-%m-%d')
                newFase = Fase(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],maxItems = request.POST["maxItems"],fInicio = fecha, estado = "PEN", proyecto_id = id_proyecto)
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
                       anterior = Fase.objects.get(orden=cantidad, proyecto_id=id_proyecto)
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
                                roles = request.POST.getlist("roles")
                                newFase.orden=1
                                newFase.save()
                                for rol in roles:
                                    newFase.roles.add(rol)
                                    newFase.save()
                                return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearFaseForm(initial={'descripcion':fase.descripcion, 'maxItems':fase.maxItems, 'fInicio':fase.fInicio, 'orden':fase.orden}) #'fInicio':datetime.strptime(str(fase.fInicio),'%Y-%m-%d').strftime('%d/%m/%y')
    return render_to_response('fases/registrarFase.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def asignar_usuario(request,id_fase):
    '''
    vista auxiliar para obtener un listado de usuarios para asociar a la fase, verificando que el usuario
    ya no tenga un rol en esa fase
    '''

    usuarios=User.objects.filter(is_active=True)
    fase=get_object_or_404(Fase,id=id_fase)
    if fase.estado!='PEN':
        return HttpResponseRedirect ('/denegado')
    users=[]
    for usuario in usuarios:
        if es_miembro(usuario.id,id_fase,'') and not es_lider(usuario.id, fase.proyecto.id):
            users.append(usuario)

    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    return render_to_response('fases/lista_usuarios.html', {'datos': users, 'fase' : fase}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def asignar_rol(request,id_usuario, id_fase):
    '''
    vista auxiliar para obtener el listado de roles asociados a una fase para asociarlos a un usuario
    '''
    fase=get_object_or_404(Fase,id=id_fase)
    if fase.estado!='PEN':
        return HttpResponseRedirect ('/denegado')
    usuario=User.objects.get(id=id_usuario)
    roles=Group.objects.filter(fase__id=id_fase)
    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    return render_to_response('fases/listar_roles.html', {'roles': roles, 'usuario':usuario, 'fase':id_fase}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def asociar(request,id_rol,id_usuario,id_fase):
    '''
    vista para asociar un rol perteneciente a una face a un usuario, asociandolo de esta manera a la fase, y al proyecto
    '''
    fase=Fase.objects.get(id=id_fase)
    if fase.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    usuario=User.objects.get(id=id_usuario)
    rol = Group.objects.get(id=id_rol)
    usuario.groups.add(rol)
    usuario.save()
    return HttpResponseRedirect('/fases/proyecto/'+str(fase.proyecto_id))


@login_required
@permission_required('fase')
def des(request,id_fase):
    '''
    vista para listar a los usuario de una fase, para poder desasociarlos
    '''
    fase=get_object_or_404(Fase,id=id_fase)
    if fase.estado!='PEN':
        return HttpResponseRedirect ('/denegado')
    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    roles=Group.objects.filter(fase__id=id_fase)
    usuarios=[]
    for rol in roles:
        p=User.objects.filter(groups__id=rol.id)
        for pp in p:
            usuarios.append(pp)
    return render_to_response('fases/lista_usuarios_d.html', {'datos': usuarios,"fase":id_fase}, context_instance=RequestContext(request))

@login_required
@permission_required('fase')
def desasociar(request,id_usuario, id_fase):
    '''
    vista para remover un rol al usuario, desasociandolo asi de una fase
    '''
    fase=get_object_or_404(Fase,id=id_fase)
    if fase.estado!='PEN':
        return HttpResponseRedirect ('/denegado')
    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    usuario=User.objects.get(id=id_usuario)
    roles=Group.objects.filter(fase__id=id_fase)
    for rol in roles:
        usuario.groups.remove(rol)
        usuario.save()

    return HttpResponseRedirect('/fases/proyecto/'+str(fase.proyecto_id))