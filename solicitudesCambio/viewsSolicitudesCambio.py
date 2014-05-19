from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from PMS import settings
from items.models import Item
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
#        formulario=VotoForm(request.POST)
        voto=Voto(solicitud=solicitud,usuario=request.user,voto=request.POST['voto'])
        voto.save()
        votacionCerrada(solicitud)
        if votacionCerrada(solicitud):
            resultado(solicitud)
            if solicitud.estado=='APROBADA':
                item.estado='CON'
                item.lineaBase.estado='ROTA'
            else:
                item.estado='FIN'
            item.save()
#        item.estado='CON'
#        item.save()
        return render_to_response('solicitudesCambio/votacion_satisfactoria.html', context_instance=RequestContext(request))
    else:
        formulario=VotoForm()
    return render_to_response('solicitudesCambio/votar_solicitud.html',{'formulario':formulario,'solicitud':solicitud}, context_instance=RequestContext(request))

def votacionCerrada(solicitud):
    comite = User.objects.filter(comite__id=solicitud.proyecto.id)
    voto=[]
    for miembro in comite:
        voto=Voto.objects.filter(usuario_id=miembro.id, solicitud_id=solicitud.id)
        if len(voto)==0:
            return False
    return True

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