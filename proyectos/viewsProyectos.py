from django.contrib.auth.decorators import login_required, permission_required
from proyectos.formsProyectos import ProyectoForm, CambiarEstadoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from proyectos.models import Proyecto
from fases.models import Fase
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib import messages
from PMS import settings

__author__ = 'Grupo R13'
__date__ = '10-04-2014'
__version__ = '1.0'
__text__ = 'Este modulo contiene funciones que permiten el control de proyectos'




@login_required
@permission_required('proyecto')
def registrar_proyecto(request):
    '''
    Vista para registrar un nuevo proyecto con su lider y miembros de su comite de cambios
    '''

    if request.method=='POST':
        formulario = ProyectoForm(request.POST)

        if formulario.is_valid():
            if formulario.cleaned_data['fecha_ini']>formulario.cleaned_data['fecha_fin']:
                messages.add_message(request, settings.DELETE_MESSAGE, "Fecha de inicio debe ser menor a la fecha de finalizacion")
            else:
                lider=formulario.cleaned_data['lider']
                #asigna el rol lider al usuario seleccionado
                roles = Group.objects.get(name='Lider')
                lider.groups.add(roles)
                formulario.save()
                return HttpResponseRedirect('/proyectos/register/success')
    else:
        formulario = ProyectoForm()
    return render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request))



@login_required
def importar_proyecto(request, id_proyecto):
    '''
    Vista para importar un proyecto, dado en <id_proyecto>  con su lider y miembros del comite
    '''
    proyecto=Proyecto.objects.get(id=id_proyecto)
    if request.method=='POST':
        formulario = ProyectoForm(request.POST, initial={'nombre':proyecto.nombre,'observaciones':proyecto.observaciones, 'descripcion':proyecto.descripcion, 'fecha_ini':proyecto.fecha_ini, 'fecha_fin':proyecto.fecha_fin} )

        #verifica que la fecha de inicio sea menor a la de fin
        if formulario.is_valid():
            if formulario.cleaned_data['fecha_ini']>formulario.cleaned_data['fecha_fin']:
                messages.add_message(request, settings.DELETE_MESSAGE, "Fecha de inicio debe ser menor a la fecha de finalizacion")
            else:
                lider=formulario.cleaned_data['lider']
                roles = Group.objects.get(name='Lider')
                lider.groups.add(roles)
                formulario.save()
                return HttpResponseRedirect('/proyectos/register/success')
    else:
        formulario = ProyectoForm(initial={'nombre':proyecto.nombre,'observaciones':proyecto.observaciones, 'descripcion':proyecto.descripcion, 'fecha_ini':proyecto.fecha_ini, 'fecha_fin':proyecto.fecha_fin} )
    return render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request))



@login_required
def RegisterSuccessView(request):
    '''
    Vista llamada en caso de creacion correcta de un proyecto, redirige a un template de exito
    '''
    return HttpResponseRedirect ('/proyectos/register/success/')


@login_required
def RegisterFailedView(request, id_proyecto):
    '''
    Vista que retorna a un template de fracaso en caso de que el proyecto no pueda cambiar de estado
    '''
    return render_to_response('proyectos/cambio_estado_fallido.html', {'dato': id_proyecto}, context_instance=RequestContext(request))


@login_required
def detalle_proyecto(request, id_proyecto):

    '''
    vista para ver los detalles del proyecto <id_proyecto> del sistema, junto con su lider y los miembros del comite
    '''

    dato = get_object_or_404(Proyecto, pk=id_proyecto)
    comite = User.objects.filter(comite__id=id_proyecto)
    lider = get_object_or_404(User, pk=dato.lider_id)
    return render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato, 'comite': comite, 'lider':lider}, context_instance=RequestContext(request))


@login_required
def listar_proyectos(request):

    '''
    vista para listar los proyectos del sistema del sistema junto con el nombre de su lider
    '''

    proyectos = Proyecto.objects.all().exclude(estado='ACT')


    return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos}, context_instance=RequestContext(request))


@login_required
def buscar_proyecto(request):
    '''
    vista para buscar los proyectos del sistema
    '''
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nombre=query)
        )
        results = Proyecto.objects.filter(qset).distinct()

    else:
        results = []


    return render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))



@login_required
def editar_proyecto(request,id_proyecto):
    '''
    Vista para editar un proyecto,o su lider o los miembros de su comite
    '''
    proyecto= Proyecto.objects.get(id=id_proyecto)
    nombre= proyecto.nombre
    if request.method == 'POST':
        # formulario enviado
        proyecto_form = ProyectoForm(request.POST, instance=proyecto)
        if proyecto_form.is_valid():
            if proyecto_form.cleaned_data['fecha_ini']>proyecto_form.cleaned_data['fecha_fin']:
                messages.add_message(request, settings.DELETE_MESSAGE, "Fecha de inicio debe ser menor a la fecha de finalizacion")
            else:
                lider=proyecto_form.cleaned_data['lider']
                roles = Group.objects.get(name='Lider')
                lider.groups.add(roles)
            # formulario validado correctamente
                proyecto_form.save()
                return HttpResponseRedirect('/proyectos/register/success/')
    else:
        # formulario inicial
        proyecto_form = ProyectoForm(instance=proyecto)
    return render_to_response('proyectos/editar_proyecto.html', { 'proyecto': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))


@login_required
def cambiar_estado_proyecto(request,id_proyecto):
    '''
    Vista para cambiar el estado de un proyecto, verificando que esto sea posible: para estar activo debe tener la cantidad
    necesaria de miembros del comite (cantidad impar)
    Si cambia a activo todas sus fases pasan al estado activo
    '''

    proyecto= Proyecto.objects.get(id=id_proyecto)
    nombre= proyecto.nombre
    comite = User.objects.filter(comite__id=id_proyecto)


    if request.method == 'POST':
        proyecto_form = CambiarEstadoForm(request.POST, instance=proyecto)
        if proyecto_form.is_valid():
                    if proyecto_form.cleaned_data['estado']=='ACT':
                        cantidad = 0
                        for miembros in comite:
                            cantidad+=1
                        if cantidad%2==0:
                            return render_to_response('proyectos/cambio_estado_fallido.html', { 'dato': id_proyecto}, context_instance=RequestContext(request))
                        if cantidad<3:
                            return render_to_response('proyectos/cambio_estado_fallido.html', { 'dato': id_proyecto}, context_instance=RequestContext(request))
                        fases=Fase.objects.filter(proyecto_id=id_proyecto)
                        for fase in fases:
                            fase.estado='EJE'
                            fase.save()
                        # formulario validado correctamente
                        proyecto_form.save()
                        return HttpResponseRedirect('/proyectos/register/success/')
                    else:
                            if proyecto_form.cleaned_data['estado']=='ANU':
                                proyecto_form.save()
                                return HttpResponseRedirect('/proyectos/register/success/')

    else:
        # formulario inicial
        proyecto_form = CambiarEstadoForm(instance=proyecto)
        return render_to_response('proyectos/cambiar_estado_proyecto.html', { 'proyecto': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))

@login_required
def ver_equipo(request,id_proyecto):
    '''
    vista para ver todos los usuarios que forman parte de un proyecto
    '''
    dato=get_object_or_404(Proyecto,pk=id_proyecto)
    comite = User.objects.filter(comite__id=id_proyecto)
    lider = get_object_or_404(User, pk=dato.lider_id)
    fases=Fase.objects.filter(proyecto_id=id_proyecto)
    nombre_roles=[]
    usuarios=[]
    for fase in fases:
        roles=Group.objects.filter(fase__id=fase.id)
        for rol in roles:
            nombre_roles.append(rol)
    #for nombre in nombre_roles:
            u=User.objects.filter(groups__id=rol.id)

            for user in u:
                uu=user.first_name + " " + user.last_name  +  "  -  " + rol.name  +" en la fase   " + fase.nombre +"\n"
                usuarios.append(uu)
    return render_to_response('proyectos/ver_equipo.html', {'proyecto':dato,'lider': lider, 'comite':comite, 'usuarios':usuarios}, context_instance=RequestContext(request))