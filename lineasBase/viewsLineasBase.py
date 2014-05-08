from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.
from django.template import RequestContext
from PMS import settings

from fases.models import Fase
from items.models import Item
from items.viewsItems import es_miembro, dibujarProyecto
from lineasBase.formsLineasBase import LineaBaseForm
from lineasBase.models import LineaBase
from proyectos.models import Proyecto
from tiposDeItem.models import TipoItem


@login_required
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

@login_required
def gestionar_fases(request, id_proyecto):

    '''
    vista para listar las fases del proyecto
    '''

    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    fases=Fase.objects.filter(proyecto_id=id_proyecto)
    if es_miembro(request.user.id, fases[0].id,'')==False:
        return HttpResponseRedirect('/denegado')
    proyecto=get_object_or_404(Proyecto, id=id_proyecto)
    setfases=set(fases)

    nombre=dibujarProyecto(id_proyecto)
    return render_to_response('lineasBase/gestionar_fase.html', {'datos': setfases, 'proyecto':proyecto,'name':nombre}, context_instance=RequestContext(request))


@login_required
def listar_lineasBase(request, id_fase):

    '''
    vista para listar las lineas base de una fase
    '''

    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    fase=get_object_or_404(Fase,id=id_fase)
    lineasbase=LineaBase.objects.filter(fase_id=id_fase)
    if es_miembro(request.user.id, id_fase,'')==False:
        return HttpResponseRedirect('/denegado')

    return render_to_response('lineasBase/listar_lineasBase.html', {'datos': lineasbase, 'fase':fase}, context_instance=RequestContext(request))

@login_required
def crear_lineaBase(request, id_fase):

    '''
    vista para crear una linea base.
    Una vez que se crea se asigna el id correspondiente a los items seleccionados, y
    se cambia el estado de los mismos a FIN
    '''

    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    fase=get_object_or_404(Fase,id=id_fase)
    if es_miembro(request.user.id, id_fase,'')==False:
        return HttpResponseRedirect('/denegado')
    items=[]
    titem=TipoItem.objects.filter(fase_id=fase.id)
    for i in titem:
        it=Item.objects.filter(tipo_item_id=i.id, estado='VAL', lineaBase=None)
        for ii in it:
            items.append(ii)
    if len(items)==0:
        return HttpResponse('<h1>No se pueden crear lineas base ya que aun no existen items con estado validado</h1>')
    if request.method=='POST':

                formulario = LineaBaseForm(fase,request.POST)
                items=request.POST.get('items')
                if items is None:
                    pass

                else:
                    if request.POST['nombre']=='':
                        pass
                    else:
                        items= request.POST.getlist('items')

                        flag=False
                        nombre=''
                        for item in items:
                            i=Item.objects.get(id=item)
                            if i.relacion!=None:
                                if i.relacion.estado!='FIN':
                                    flag=True
                                    nombre=i.nombre
                        if flag==True:
                            messages.add_message(request,settings.DELETE_MESSAGE,'El item ' + str(nombre)+ ' posee una relacion con un item no Finalizado')
                        else:
                            cod=lineabase=LineaBase(nombre=request.POST['nombre'], fase=fase)
                            lineabase.save()
                            for item in items:
                                i=Item.objects.get(id=item)
                                i.estado='FIN'
                                i.lineaBase=cod
                                i.save()
                            return render_to_response('lineasBase/creacion_correcta.html',{'id_fase':fase.id}, context_instance=RequestContext(request))

    else:
        formulario=LineaBaseForm(fase=fase)


    return render_to_response('lineasBase/crear_lineaBase.html', {'formulario':formulario}, context_instance=RequestContext(request))

@login_required
def detalle_lineabase(request, id_lb):

    '''
    vista para ver los detalles del item <id_item>
    '''
    lineabase=get_object_or_404(LineaBase,id=id_lb)

    fase=lineabase.fase
    if es_miembro(request.user.id, fase.id,''):
        items=Item.objects.filter(lineaBase=lineabase)
        dato=lineabase
        return render_to_response('lineasBase/detalle_lineaBase.html', {'datos': dato, 'items':items}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')


