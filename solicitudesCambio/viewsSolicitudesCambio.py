from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from PMS import settings
from items.models import Item
from items.viewsItems import getMaxIdItemEnLista, itemsProyecto
from proyectos.models import Proyecto
from solicitudesCambio.formsSolicitudes import VotoForm
from solicitudesCambio.models import SolicitudCambio, Voto
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def listar_solicitudes(request):

    '''
    vista para listar los proyectos asignados a un usuario expecifico
    '''



    lista_proyectos=Proyecto.objects.filter(comite__id=request.user.id)
    lista_solicitudes=[]
    if len(lista_proyectos)==0:
        return HttpResponseRedirect('/denegado')

    for proyecto in lista_proyectos:
        lista=SolicitudCambio.objects.filter(proyecto=proyecto,estado='PENDIENTE')
        for solicitud in lista:
            lista_solicitudes.append(solicitud)




    return render_to_response('solicitudesCambio/listar_solicitudes.html', {'datos': lista_solicitudes}, context_instance=RequestContext(request))




def puede_votar(id_usuario,id_solicitud):
    solicitud=get_object_or_404(SolicitudCambio, id=id_solicitud)
    lista_proyectos=Proyecto.objects.filter(comite__id=id_usuario, id=solicitud.proyecto.id)
    if len(lista_proyectos)==0:
        return HttpResponseRedirect('/denegado')
    voto=Voto.objects.filter(usuario_id=id_usuario, solicitud=solicitud)
    if len(voto)!=0:
        return False
    else:
        return True

@login_required
def votar(request, id_solicitud):
    if puede_votar(request.user.id, id_solicitud)!=True:
        return HttpResponseRedirect('/denegado')
    solicitud=get_object_or_404(SolicitudCambio, id=id_solicitud)
    item=solicitud.item
    if request.method=='POST':
        formulario=VotoForm(request.POST)
        if formulario.is_valid():
            voto=Voto(solicitud=solicitud,usuario=request.user,voto=request.POST['voto'])
            voto.save()
            votacionCerrada(solicitud)
            aprobada=2
            if votacionCerrada(solicitud):
                resultado(solicitud)
                if solicitud.estado=='APROBADA':
                    aprobada=1
                    item.estado='FIN'
                    item.save()
                    listaitems =itemsProyecto(solicitud.proyecto)
                    maxiditem = getMaxIdItemEnLista(listaitems)
                    global nodos_visitados
                    nodos_visitados = [0]*(maxiditem+1)
                    estadoDependientes(item.id)
                    item.estado='CON'
                    item.save()
                    lb=item.lineaBase
                    lb.estado='ROTA'
                    lb.save()
                else:
                    item.estado='FIN'
                    item.save()
                    aprobada=0

            return render_to_response('solicitudesCambio/votacion_satisfactoria.html',{'aprobada':aprobada}, context_instance=RequestContext(request))
    else:
        formulario=VotoForm()
    return render_to_response('solicitudesCambio/votar_solicitud.html',{'formulario':formulario,'solicitud':solicitud}, context_instance=RequestContext(request))

def estadoDependientes(id_item):
    '''
    Funcion para recorrer el grafo de items del proyecto en profundidad
    Sumando el costo y el tiempo de cada uno
    '''
    global nodos_visitados
#    print id_item
    nodos_visitados[id_item]=1
    item=get_object_or_404(Item,id=id_item)
#    print item.estado
#    print(not(item.estado=='CON' or item.estado=='BLO' or item.estado=='PEN'))
    if not(item.estado=='CON' or item.estado=='BLO' or item.estado=='PEN' or item.estado=='ANU'):
        item.estado='REV'
        item.save()
        relaciones = Item.objects.filter(relacion=item.id)
        for relacion in relaciones:
            if(nodos_visitados[relacion.id]==0):
                estadoDependientes(relacion.id)



def votacionCerrada(solicitud):
    comite = User.objects.filter(comite__id=solicitud.proyecto.id)
    voto=[]
    for miembro in comite:
        voto=Voto.objects.filter(usuario_id=miembro.id, solicitud_id=solicitud.id)
        if len(voto)==0:
            return False
    return True


def detalle_solicitud(request,id_solicitud):
    solicitud=get_object_or_404(SolicitudCambio, id=id_solicitud)
    id_usuario=request.user.id
    lista_proyectos=Proyecto.objects.filter(comite__id=id_usuario, id=solicitud.proyecto.id)
    if len(lista_proyectos)==0:
        return HttpResponseRedirect('/denegado')

    votos = Voto.objects.filter(solicitud_id=solicitud.id)
    favor=0
    contra=0
    usuarios=[]
    for voto in votos:
        usuarios.append(voto.usuario)
        if voto.voto=='RECHAZAR':
            contra+=1
        else:
            favor+=1
    return render_to_response('solicitudesCambio/detalle_solicitud.html',{'usuarios':usuarios,'solicitud':solicitud, 'favor':favor, 'contra':contra}, context_instance=RequestContext(request))


def resultado(solicitud):
    votos = Voto.objects.filter(solicitud_id=solicitud.id)
    favor=0
    contra=0
    for voto in votos:
        if voto.voto=='RECHAZAR':
            contra+=1
        else:
            favor+=1

    if contra>favor:
        solicitud.estado='RECHAZADA'
    else:
        solicitud.estado='APROBADA'
    solicitud.save()