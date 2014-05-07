from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from proyectos.models import Proyecto





def gestionar_proyectos(request):

    '''
    vista para listar los proyectos del lider
    '''

    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    proyectos = Proyecto.objects.filter(lider_id=usuario.id, estado='ACT')
    if len(proyectos)==0:
        return HttpResponseRedirect('/denegado')
    setproyectos=set(proyectos)
    return render_to_response('lineasBase/gestionar_proyecto.html', {'datos': setproyectos, 'user':usuario}, context_instance=RequestContext(request))