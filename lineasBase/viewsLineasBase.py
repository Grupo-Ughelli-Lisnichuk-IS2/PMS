from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Indenter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404


from django.template import RequestContext
import time
from django.utils.datetime_safe import datetime
from PMS import settings

from fases.models import Fase
from items.models import Item, VersionItem
from items.viewsItems import es_miembro, dibujarProyecto, generar_version
from lineasBase.formsLineasBase import LineaBaseForm
from lineasBase.models import LineaBase
from proyectos.models import Proyecto
from tiposDeItem.models import TipoItem


def es_lider(id_usuario, id_proyecto):
    '''
    Funcion que devuelve si un usuario es o no el lider del proyecto especificado
    '''
    proyecto=get_object_or_404(Proyecto, id=id_proyecto)
    if proyecto.lider.id==id_usuario:
        return True
    else:
        return False

@login_required
def gestionar_proyectos(request):

    '''
    vista para listar los proyectos del lider
    '''

    request.session['nivel'] = 0
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
    if es_lider(request.user.id, id_proyecto)==False:
        return HttpResponseRedirect('/denegado')
    proyecto=get_object_or_404(Proyecto, id=id_proyecto)
    if proyecto.estado!='ACT':
       return HttpResponseRedirect ('/denegado')
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
    if fase.estado!='EJE':
      return  HttpResponseRedirect ('/denegado')
    lineasbase=LineaBase.objects.filter(fase_id=id_fase)
    if es_lider(request.user.id, fase.proyecto_id)==False:
        return HttpResponseRedirect('/denegado')

    return render_to_response('lineasBase/listar_lineasBase.html', {'datos': lineasbase, 'fase':fase}, context_instance=RequestContext(request))

@login_required
def crear_lineaBase(request, id_fase):

    '''
    vista para crear una linea base.
    Una vez que se crea se asigna el id correspondiente a los items seleccionados, y
    se cambia el estado de los mismos a FIN
    y el estado de la linea base creada es CERRADA
    '''

    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    fase=get_object_or_404(Fase,id=id_fase)
    if es_lider(request.user.id, fase.proyecto_id)==False:
        return HttpResponseRedirect('/denegado')
    if fase.estado!='EJE':
        return HttpResponse('<h1>No se pueden crear lineas base ya que la fase ha finalizado</h1>')
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
                            cod=lineabase=LineaBase(nombre=request.POST['nombre'], fase=fase, estado='CERRADA')
                            lineabase.save()
                            items= request.POST.getlist('items')
                            for item in items:
                                i=Item.objects.get(id=item)
                                generar_version(i,request.user)
                            for item in items:
                                i=Item.objects.get(id=item)
                                i.version=i.version+1
                                i.estado='FIN'
                                i.lineaBase=cod
                                i.save()
                            return render_to_response('lineasBase/creacion_correcta.html',{'id_fase':fase.id}, context_instance=RequestContext(request))

    else:
        formulario=LineaBaseForm(fase=fase)


    return render_to_response('lineasBase/crear_lineaBase.html', {'formulario':formulario,'fase':id_fase}, context_instance=RequestContext(request))

@login_required
def detalle_lineabase(request, id_lb):

    '''
    vista para ver los detalles de la linea base especificada junto con sus items asosciados
    '''
    lineabase=get_object_or_404(LineaBase,id=id_lb)

    fase=lineabase.fase
    if es_lider(request.user.id, fase.proyecto_id):
        items=Item.objects.filter(lineaBase=lineabase)
        dato=lineabase
        return render_to_response('lineasBase/detalle_lineaBase.html', {'datos': dato, 'items':items}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')

def comprobar_items_fase(id_fase):
    '''
    Funcion que recibe el id de una fase y retorna verdadero o falso si es que todos los items de la
    misma se encuentran en una linea base
    '''
    items=Item.objects.filter(tipo_item__fase=id_fase).exclude(estado='ANU')
    if len(items)==0:
        return False
    for item in items:
        if item.lineaBase is None or item.estado!='FIN':
            return False
    return True


@login_required
def finalizar_fase(request, id_fase):

    '''
    vista para finalizar una fase. Los criterios que se tienen en cuenta para finalizarla son:
    1) La fase anterior debe estar finalizada
    2) Todos los items de la fase deben estar en una linea base
    '''
    fase=get_object_or_404(Fase,id=id_fase)

    comprobar_fase=False
    if es_lider(request.user.id, fase.proyecto_id):
        if fase.orden==1 and comprobar_items_fase(id_fase):
            comprobar_fase=True
        elif fase.orden!=1:
            fase_anterior=get_object_or_404(Fase, proyecto=fase.proyecto, orden=fase.orden-1)
            if comprobar_items_fase(fase.id) and fase_anterior.estado=='FIN':
                comprobar_fase=True
        if comprobar_fase:
            fase.estado='FIN'
            fase.save()
            return render_to_response('lineasBase/finalizacion_correcta.html', {'fase':fase}, context_instance=RequestContext(request))
        else:
            return render_to_response('lineasBase/finalizacion_incorrecta.html', {'fase':fase}, context_instance=RequestContext(request))

    else:
        return render_to_response('403.html')




@login_required
def finalizar_proyecto(request, id_proyecto):

    '''
    vista para finalizar un Proyecyo. Los criterios que se tienen en cuenta para finalizarlo son:
    1) Todas las fases deben estar finalizadas 

    '''
    puede_finalizar=True
    if not es_lider(request.user.id, id_proyecto):
        return HttpResponseRedirect ('/denegado')
    proyecto=get_object_or_404(Proyecto,id=id_proyecto)
    if proyecto.estado!='ACT':
        return HttpResponseRedirect ('/denegado')
    fases=Fase.objects.filter(proyecto=proyecto)
    for fase in fases:
        if fase.estado!='FIN':
            puede_finalizar=False
            break
    if puede_finalizar:
        proyecto.estado='FIN'
        today = datetime.now() #fecha actual
        dateFormat = today.strftime("%Y-%m-%d") # fecha con format
        proyecto.fecha_fin_real=dateFormat
        dias=today.date()-proyecto.fecha_fin
        dias= int(str(dias.days))
        print dias
        if dias>0:
            adelanto=0
        else:
            if dias<0:
                adelanto=1
                dias=dias*-1
            else:
                adelanto=2

        proyecto.save()
        return render_to_response('lineasBase/finalizacion_correcta_proyecto.html', {'proyecto':proyecto, 'dias':dias, 'adelanto':adelanto}, context_instance=RequestContext(request))
    else:
        return render_to_response('lineasBase/finalizacion_incorrecta_proyecto.html', {'proyecto':proyecto}, context_instance=RequestContext(request))
