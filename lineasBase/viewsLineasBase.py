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



def reporte_lineas_base(id_proyecto):
    '''
    Funcion que recibe el id de un proyecto y genera un reporte en formato pdf de todas las lineas
    base que posee cada fase del proyecto, ordenado por fase y lineas bases con sus items
    '''

    fases=Fase.objects.filter(proyecto_id=id_proyecto).order_by('orden')
    proyecto = get_object_or_404(Proyecto,id=id_proyecto)
    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_lineasBase"+proyecto.nombre+".pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/icono.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=10, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    titulo="<b>Lineas Base proyecto "+proyecto.nombre+"<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))


    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    for f in fases:
        Story.append(Spacer(1, 10))
        Story.append(Indenter(4))
        titulo = Paragraph('<b>' 'Fase '+ str(f.orden) + ' : '+ f.nombre + '<\b>', styles['Titulo'])
        Story.append(titulo)
        Story.append(Indenter(-4))

        lineasBase=set(LineaBase.objects.filter(fase=f))
        contador=0

        for lb in lineasBase:
            contador+=1

            ptext = str(contador)+ ". "+ lb.nombre + "/" + lb.estado + " <br/>"

            Story.append(Indenter(15))
            Story.append(Spacer(1, 10))
            Story.append(Paragraph(ptext, styles["Justify"]))

            Story.append(Indenter(-15))
            if lb.estado=='CERRADA':
                items=Item.objects.filter(lineaBase=lb.id)
            else:
                items=VersionItem.objects.filter(lineaBase=lb.id)
            ptext=''

            for item in items:
                text = ''
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="- " + item.nombre  +  ", Version: " + str(item.version)+"<br/"
                Story.append(Paragraph(text, styles["Items"]))
                Story.append(Indenter(-42))
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_lineasBase"+proyecto.nombre+".pdf"

@login_required
def descargar_reporteLB(request, id_proyecto):
    '''
    Vista para descargar el reporte de lineas base de un proyecto especifico
    '''
    if es_lider(request.user.id, id_proyecto)!=True:
        return HttpResponseRedirect('/denegado')
    a=file(reporte_lineas_base(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')


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
        proyecto.save()
        return render_to_response('lineasBase/finalizacion_correcta_proyecto.html', {'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('lineasBase/finalizacion_incorrecta_proyecto.html', {'proyecto':proyecto}, context_instance=RequestContext(request))
