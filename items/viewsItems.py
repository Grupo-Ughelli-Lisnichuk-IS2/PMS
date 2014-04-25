from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from fases.models import Fase
from proyectos.models import Proyecto
from tiposDeItem.models import TipoItem


@login_required
def listar_proyectos(request):

    '''
    vista para listar los proyectos asignados a un usuario expecifico
    '''
    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    proyectosLider = Proyecto.objects.filter(lider_id=usuario.id, estado='ACT')

    roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
    fases=[]
    proyectos=[]
    #las fases de en las cuales el usuario tiene un rol
    for rol in roles:
        fase=Fase.objects.get(roles=rol.id)
        fases.append(fase)
    #los proyectos a los que pertenecen esas fases
    for fase in fases:
        proyecto=Proyecto.objects.get(id=fase.proyecto_id)
        if proyecto.estado=='ACT':
            proyectos.append(proyecto)
    for p in proyectosLider:
        proyectos.append(p)
    return render_to_response('items/abrir_proyecto.html', {'datos': proyectos}, context_instance=RequestContext(request))

def listar_fases(request, id_proyecto):

    '''
    vista para listar las fases asignadas a un usuario de un proyecto especifico
    '''
    fasesProyecto=Fase.objects.filter(proyecto_id=id_proyecto, estado='EJE')
    usuario = request.user
    proyecto=Proyecto.objects.get(id=id_proyecto)
    fases=[]
    if usuario.id==proyecto.lider_id:
        fases=fasesProyecto
    else:
        roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
        for rol in roles:
            for f in fasesProyecto:
                ff=Fase.objects.filter(id=f.id,roles__id=rol.id)
                for fff in ff:
                    fases.append(fff)
    if len(fases)==0:
        return render_to_response('403.html')

    return render_to_response('items/abrir_fase.html', {'datos': fases}, context_instance=RequestContext(request))


def es_miembro(id_usuario, id_fase):
    fase=Fase.objects.get(id=id_fase)
    usuario=User.objects.get(id=id_usuario)
    proyecto=Proyecto.objects.get(id=fase.proyecto_id)
    if fase.estado!='EJE':
        return False
    if usuario.id==proyecto.lider_id:
        return True
    roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
    roles_fase=Group.objects.filter(fase__id=fase.id)
    for rol in roles:
        for r in roles_fase:
            if rol.id==r.id:
                return True
    return False


def listar_tiposDeItem(request, id_fase):

    '''
    vista para listar las fases asignadas a un usuario de un proyecto especifico
    '''
    flag=es_miembro(request.user.id, id_fase)

    fase=Fase.objects.get(id=id_fase)
    if flag==True:
        tiposItem = TipoItem.objects.filter(fase_id=id_fase).order_by('nombre')
    else:
        return render_to_response('403.html')


    return render_to_response('items/listar_tipoDeItem.html', {'datos': tiposItem, 'fase':fase}, context_instance=RequestContext(request))