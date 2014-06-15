from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Indenter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext

from django.utils.datetime_safe import datetime
from PMS import settings

from fases.models import Fase
from items.models import Item, VersionItem
from items.viewsItems import es_miembro, dibujarProyecto, generar_version
from lineasBase.formsLineasBase import LineaBaseForm
from lineasBase.models import LineaBase
from lineasBase.viewsLineasBase import es_lider
from proyectos.models import Proyecto
from tiposDeItem.models import TipoItem, Atributo


def reporte_usuarios():
    '''
    Funcion que genera el reporte de usuarios del sistema
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_usuarios.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/icono.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>Usuarios del Sistema<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))


    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    usuarios=User.objects.filter().order_by('is_active').reverse()
    usuarios_activos=User.objects.filter(is_active=True)
    cantidad_act=len(usuarios_activos)
    contador=-1
    titulo = Paragraph('<b>Usuarios Activos <\b>', styles['Titulo'])
    Story.append(Spacer(1, 12))
    Story.append(titulo)
    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))
    for usuario in usuarios:
            contador+=1
            if contador==cantidad_act:
                titulo = Paragraph('<b>Usuarios Inactivos <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                contador_act=1
            Story.append(Indenter(25))
            text="<strong>"+str(contador_act)+".</strong>"
            Story.append(Paragraph(text, styles["Subtitulos"]))
            text ="<strong>Usuario: </strong>" + usuario.username +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Nombre: </strong>" + usuario.first_name + " "+ usuario.last_name +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>E-mail: </strong>" + usuario.email +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            dateFormat = usuario.date_joined.strftime("%d-%m-%Y %H:%M:%S")
            text ="<strong>Fecha de creacion: </strong>" + str(dateFormat) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            dateFormat = usuario.last_login.strftime("%d-%m-%Y %H:%M:%S")
            text ="<strong>Ultimo acceso: </strong>" + str(dateFormat) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Roles: </strong> <br>"
            Story.append(Paragraph(text, styles["Items"]))
            Story.append(Indenter(-25))
            roles=Group.objects.filter(user__id=usuario.id)
            for rol in roles:
                text = ''
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="- " + rol.name +"<br>"
                Story.append(Paragraph(text, styles["SubItems"]))
                Story.append(Indenter(-42))
            Story.append(Indenter(25))
            text ="__________________________________________________________<br>"
            Story.append(Paragraph(text, styles["Items"]))
            Story.append(Spacer(1, 12))
            Story.append(Indenter(-25))
            contador_act+=1
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_usuarios.pdf"




def descargar_reporteUsuarios(request):
    '''
    Vista para descargar el reporte de lineas base de un proyecto especifico
    '''
    if request.user.is_superuser!=True:
        return HttpResponseRedirect('/denegado')
    a=file(reporte_usuarios())

    return StreamingHttpResponse(a,content_type='application/pdf')


def reporte_proyectos():
    '''
    Funcion que genera el reporte de proyectos del sistema
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_proyectos.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)


    Story=[]
    logo = str(settings.BASE_DIR)+"/static/icono.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubsubsubItems',fontName='Helvetica',fontSize=8,spaceAfter=3))
    styles.add(ParagraphStyle(name='SubsubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=14,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>Proyectos del Sistema<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    proyectos_activos=Proyecto.objects.filter(estado='ACT')
    proyectos_fin=Proyecto.objects.filter(estado='FIN')
    proyectos_pen=Proyecto.objects.filter(estado='PEN')
    proyectos_anu=Proyecto.objects.filter(estado='ANU')
    proyectos=[]
    for p in proyectos_pen:
        proyectos.append(p)
    for p in proyectos_activos:
        proyectos.append(p)
    for p in proyectos_fin:
        proyectos.append(p)
    for p in proyectos_anu:
        proyectos.append(p)
    cantidad_pen=len(proyectos_pen)
    cantidad_act=len(proyectos_activos)
    cantidad_fin=len(proyectos_fin)
    contador1=0
    contador2=0
    contador3=0
    contador=0
    titulo = Paragraph('<b>Proyectos Pendientes <\b>', styles['Titulo'])
    Story.append(Spacer(1, 12))
    Story.append(titulo)
    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))
    for proyecto in proyectos:
            contador+=1
            if proyecto.estado=='ACT' and contador1==0:
                titulo = Paragraph('<b>Proyectos Activos <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                contador1=1
                contador=1
            if proyecto.estado=='FIN' and contador2==0:
                titulo = Paragraph('<b>Proyectos Activos <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                contador2=1
                contador=1
            if proyecto.estado=='ANU' and contador3==0:
                titulo = Paragraph('<b>Proyectos Activos <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                contador3=1
                contador=1

            Story.append(Indenter(25))
            text="<strong>"+str(contador)+".</strong>"
            Story.append(Paragraph(text, styles["Subtitulos"]))
            text ="<strong>Nombre: </strong>" + proyecto.nombre +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Descripcion: </strong>" + proyecto.descripcion +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            dateFormat = proyecto.fecha_ini.strftime("%d-%m-%Y")
            text ="<strong>Fecha de creacion: </strong>" + str(dateFormat) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            dateFormat = proyecto.fecha_fin.strftime("%d-%m-%Y")
            text ="<strong>Fecha de finalizacion: </strong>" + str(dateFormat) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Observaciones: </strong>" + proyecto.observaciones +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Lider: </strong>" + proyecto.lider.username +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Fases: </strong> <br>"
            Story.append(Paragraph(text, styles["SubItems"]))
            Story.append(Indenter(-25))
            fases=Fase.objects.filter(proyecto=proyecto)
            for fase in fases:
                text = ''
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="- " + fase.nombre +"<br>"
                Story.append(Paragraph(text, styles["SubItems"]))
                Story.append(Indenter(-42))
                tipoi=TipoItem.objects.filter(fase=fase)
                Story.append(Indenter(50))
                text ="<strong>Tipos de Item: </strong> <br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                Story.append(Indenter(-50))
                for ti in tipoi:
                    text = ''
                    Story.append(Indenter(50))

                    text ="- " + ti.nombre +"<br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    Story.append(Indenter(-50))
                    atributos=Atributo.objects.filter(tipoItem__id=ti.id)
                    Story.append(Indenter(60))
                    text ="<strong>Tipos de Atributo: </strong> <br>"
                    Story.append(Paragraph(text, styles["SubsubsubItems"]))
                    Story.append(Indenter(-60))
                    for atributo in atributos:
                        text = ''
                        Story.append(Indenter(70))
                        text ="- " + atributo.nombre + ", Tipo "+ atributo.tipo + "<br>"
                        Story.append(Paragraph(text, styles["SubsubsubItems"]))
                        Story.append(Indenter(-70))



            Story.append(Indenter(25))
            text ="__________________________________________________________<br>"
            Story.append(Paragraph(text, styles["Items"]))
            Story.append(Spacer(1, 12))
            Story.append(Indenter(-25))
            contador_act+=1
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    return str(settings.BASE_DIR)+"/reporte_proyectos.pdf"
def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.rotate(90)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.rotate(90)
    canvas.restoreState()

def descargar_reporteProyectos(request):
    '''
    Vista para descargar el reporte de lineas base de un proyecto especifico
    '''
    if request.user.is_superuser!=True:
        return HttpResponseRedirect('/denegado')
    a=file(reporte_proyectos())

    return StreamingHttpResponse(a,content_type='application/pdf')



def reporte_roles():
    '''
    Funcion que genera el reporte de roles del sistema
    '''


    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_roles.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/icono.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>Roles del Sistema<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))


    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    roles=Group.objects.all().exclude(name='Lider')
    Story.append(Indenter(25))
    text ="__________________________________________________________<br>"
    Story.append(Paragraph(text, styles["Items"]))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))
    for rol in roles:

            Story.append(Indenter(25))
            text="<strong>"+str(contador_act)+".</strong>"
            Story.append(Paragraph(text, styles["Subtitulos"]))
            text ="<strong>Nombre: </strong>" + rol.name +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Permisos <br></strong>"
            Story.append(Paragraph(text, styles["Items"]))
            permisos=Permission.objects.filter(group__id=rol.id)
            for permiso in permisos:
                text = ''
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="- " + permiso.name +"<br>"
                Story.append(Paragraph(text, styles["SubItems"]))
                Story.append(Indenter(-42))
            fases=Fase.objects.filter(roles__id=rol.id)
            text="<strong>Proyecto: </strong>" + fases[0].proyecto.nombre + "<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Fases asociadas: </strong> <br>"
            Story.append(Paragraph(text, styles["Items"]))
            for fase in fases:
                text = ''
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="- " + fase.nombre + "<br>"
                Story.append(Paragraph(text, styles["SubItems"]))
                Story.append(Indenter(-42))
            Story.append(Indenter(-25))
            Story.append(Indenter(25))
            text ="__________________________________________________________<br>"
            Story.append(Paragraph(text, styles["Items"]))
            Story.append(Spacer(1, 12))
            Story.append(Indenter(-25))
            contador_act+=1
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_roles.pdf"


def descargar_reporteRoles(request):
    '''
    Vista para descargar el reporte de lineas base de un proyecto especifico
    '''
    if request.user.is_superuser!=True:
        return HttpResponseRedirect('/denegado')
    a=file(reporte_roles())

    return StreamingHttpResponse(a,content_type='application/pdf')



def reporte_proyectoLider(id_proyecto):
    '''
    Funcion que genera el reporte de roles del sistema
    '''

    proyecto=get_object_or_404(Proyecto, id=id_proyecto)
    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_proyecto"+proyecto.nombre+".pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)

    Story=[]
    logo = str(settings.BASE_DIR)+"/static/icono.png"

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=15))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=12,spaceAfter=10, spaceBefore=10))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>Proyecto " + proyecto.nombre+ "<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    name=dibujarProyecto(id_proyecto)
    grafo = str(settings.BASE_DIR)+'/static/img/'+str(name)
    im = Image(grafo)

    h=im.imageHeight*0.35
    w=im.imageWidth*0.35
    im = Image(grafo,width=w,height=h)

    Story.append(im)
    text ="<strong>Descripcion: </strong>" + proyecto.descripcion+ "<br>"
    Story.append(Paragraph(text, styles["Items"]))
    text ="<strong>Observaciones: </strong>" + proyecto.observaciones+ "<br>"
    Story.append(Paragraph(text, styles["Items"]))
    dato=get_object_or_404(Proyecto,pk=id_proyecto)
    dateFormat = dato.fecha_ini.strftime("%d-%m-%Y")
    text ="<strong>Fecha de inicio: </strong>" + dateFormat+ "<br>"
    Story.append(Paragraph(text, styles["Items"]))
    dateFormat = dato.fecha_fin.strftime("%d-%m-%Y")
    text ="<strong>Fecha de finalizacion planificada: </strong>" + dateFormat+ "<br>"
    Story.append(Paragraph(text, styles["Items"]))
    if proyecto.estado=='FIN':
        dateFormat = dato.fecha_fin_real.strftime("%d-%m-%Y")
        text ="<strong>Fecha de finalizacion real: </strong>" + dateFormat+ "<br>"
        Story.append(Paragraph(text, styles["Items"]))
        today = datetime.now() #fecha actual
        dateFormat = today.strftime("%Y-%m-%d") # fecha con format
        dias=proyecto.fecha_fin_real-proyecto.fecha_fin
        dias= int(str(dias.days))
        if dias>0:
            text ="<strong>Se ha atrasado: </strong>" + "<b style=\"color=red\">" + str(dias) +"</b>"+ " dia(s)" "<br>"
            Story.append(Paragraph(text, styles["Items"]))
        else:
            if dias<0:

                dias=dias*-1
                text ="<strong>Se ha adelantado: </strong>" + '<b style="color=green">' + str(dias) +"</b>"+ " dia(s)" "<br>"
                Story.append(Paragraph(text, styles["Items"]))
            else:
                text ="<strong>Finalizado en el plazo estimado: </strong>"
                Story.append(Paragraph(text, styles["Items"]))

    else:
        today = datetime.now() #fecha actual
        dateFormat = today.strftime("%Y-%m-%d") # fecha con format
        dias=today.date()-proyecto.fecha_fin
        dias= int(str(dias.days))
        if dias>0:
            text ="<strong>Proyecto atrasado: </strong>" + "<b style=\"color=red\">" + str(dias) +"</b>"+ " dia(s)" "<br>"
            Story.append(Paragraph(text, styles["Items"]))
        else:
            if dias<=0:

                dias=dias*-1
                text ="<strong>Quedan: </strong>" + '<b style="color=green">' + str(dias) +"</b>"+ " dia(s) para finalizar el proyecto" "<br>"
                Story.append(Paragraph(text, styles["Items"]))



    comite = User.objects.filter(comite__id=id_proyecto)
    text ="<strong>Miembros del comite: </strong> <br>"
    Story.append(Paragraph(text, styles["Items"]))
    for  miembro in comite:
        Story.append(Indenter(30))
        text ="- " + miembro.first_name + " " + miembro.last_name + "<br>"
        Story.append(Paragraph(text, styles["SubItems"]))
        Story.append(Indenter(-30))
    lider = get_object_or_404(User, pk=dato.lider_id)
    text ="<strong>Lider: </strong>"  + lider.first_name + " " + lider.last_name + "<br>"
    Story.append(Paragraph(text, styles["Items"]))
    fases=Fase.objects.filter(proyecto_id=id_proyecto)
    nombre_roles=[]
    text ="<strong>Equipo: </strong>" "<br>"
    Story.append(Paragraph(text, styles["Items"]))
    for fase in fases:
        roles=Group.objects.filter(fase__id=fase.id)
        for rol in roles:
            nombre_roles.append(rol)
            u=User.objects.filter(groups__id=rol.id)
            for user in u:
                Story.append(Indenter(30))
                uu=user.first_name + " " + user.last_name  +  "  -  " + rol.name  +" en la fase   " + fase.nombre +"\n"
                Story.append(Paragraph(uu, styles["SubItems"]))
                Story.append(Indenter(-30))

    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_proyecto"+proyecto.nombre+".pdf"


def descargar_reporteProyectoLider(request, id_proyecto):
    '''
    Vista para descargar el reporte de lineas base de un proyecto especifico
    '''
    if not es_lider(request.user.id, id_proyecto):
        return HttpResponseRedirect('/denegado')
    a=file(reporte_proyectoLider(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')





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



@login_required
def listar_proyectos_reporte(request):

    '''
    vista para listar los proyectos del lider
    '''

    request.session['nivel'] = 0
    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    proyectos = Proyecto.objects.filter(Q(lider=request.user)&((Q(estado='ACT')|Q(estado='FIN'))))
    if len(proyectos)==0:
        return HttpResponseRedirect('/denegado')
    setproyectos=set(proyectos)
    return render_to_response('listar_proyectos_reporte.html', {'datos': setproyectos, 'user':usuario}, context_instance=RequestContext(request))
