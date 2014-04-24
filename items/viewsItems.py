from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from fases.models import Fase
from proyectos.models import Proyecto


@login_required
def listar_proyectos(request):

    '''
    vista para listar los proyectos asignados a un usuario expecifico
    '''
    usuario = request.user
    proyectosLider = Proyecto.objects.filter(lider_id=usuario.id, estado='ACT')

    roles=Group.objects.filter(user__id=usuario.id)
    fases=[]
    proyectos=[]
    for rol in roles:
        fase=Fase.objects.get(roles=rol.id)
        fases.append(fase)
    for fase in fases:
        proyecto=Proyecto.objects.get(id=fase.proyecto_id)
        if proyecto.estado=='ACT':
            proyectos.append(proyecto)
    for p in proyectosLider:
        proyectos.append(p)
    return render_to_response('items/abrir_proyecto.html', {'datos': proyectos}, context_instance=RequestContext(request))