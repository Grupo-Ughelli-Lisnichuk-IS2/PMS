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
from items.viewsItems import es_miembro, dibujarProyecto, generar_version, itemsProyecto
from lineasBase.formsLineasBase import LineaBaseForm
from lineasBase.models import LineaBase
from lineasBase.viewsLineasBase import es_lider
from proyectos.models import Proyecto
from solicitudesCambio.models import SolicitudCambio, Voto
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
                titulo = Paragraph('<b>Proyectos Finalizados <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                contador2=1
                contador=1
            if proyecto.estado=='ANU' and contador3==0:
                titulo = Paragraph('<b>Proyectos Anulados <\b>', styles['Titulo'])
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
    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_proyectos.pdf"


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
            if(len(fases)!=0):
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
            else:
                text="<strong>Proyecto: </strong> Ninguno<br>"
                Story.append(Paragraph(text, styles["Items"]))
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
    costos=itemsProyecto(id_proyecto)
    total=0
    for costo in costos:
        total=costo.costo+total

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
    titulo="<b>Proyecto </b>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    titulo="<b>"+ proyecto.nombre+ "</b>"
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
    text ="<strong>Costo Total: </strong>" + str(total) + " GS <br>"
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
    titulo="<b>Lineas Base proyecto </b>"
    Story.append(Paragraph(titulo,styles['Principal']))


    Story.append(Spacer(1, 12))
    titulo="<b>" + proyecto.nombre+"</b>"
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


def reporte_items(id_proyecto):
    '''
    Funcion que genera el reporte de los items de un proyecto
    '''

    fases=Fase.objects.filter(proyecto_id=id_proyecto).order_by('orden')
    proyecto = get_object_or_404(Proyecto,id=id_proyecto)
    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_items"+proyecto.nombre+".pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)


    Story=[]
    logo = str(settings.BASE_DIR)+"/static/icono.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=3))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubsubsubItems',fontName='Helvetica',fontSize=8,spaceAfter=3))
    styles.add(ParagraphStyle(name='SubsubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=12,spaceAfter=10))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=14,spaceAfter=5, spaceBefore=5))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>Items del Proyecto </b>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    titulo="<b>" + proyecto.nombre+"<br/>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))

    titulo = Paragraph('<b>Fases <\b>', styles['Titulo'])
    Story.append(Spacer(1, 12))
    Story.append(titulo)
    Story.append(Indenter(25))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))
    for fase in fases:
            Story.append(Indenter(25))
            text=""+str(fase.orden)+". "+fase.nombre+"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="______________________________________________<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Tipos de item: </strong> <br>"
            Story.append(Paragraph(text, styles["SubItems"]))
            Story.append(Indenter(-25))
            tipoi=TipoItem.objects.filter(fase=fase)
            for ti in tipoi:
                text = ''
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="- " + ti.nombre +"<br>"
                Story.append(Paragraph(text, styles["SubItems"]))
                Story.append(Indenter(-42))
                items=Item.objects.filter(tipo_item=ti.id)
                Story.append(Indenter(50))
#                text ="<strong>Items: </strong> <br>"
 #               Story.append(Paragraph(text, styles["SubsubItems"]))
                Story.append(Indenter(-50))
                for it in items:
                    text = ''
                    Story.append(Indenter(50))

                    text ="<strong>Item: </strong>" + it.nombre +"<br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    Story.append(Indenter(-50))
                    Story.append(Indenter(60))
                    text ="<strong>Codigo: </strong>"+str(it.id)+" <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    text ="<strong>Descripcion: </strong>"+it.descripcion+" <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    text ="<strong>Costo: </strong>"+str(it.costo)+" <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    text ="<strong>Tiempo: </strong>"+str(it.tiempo)+" <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    text ="<strong>Estado: </strong>"+it.estado+" <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    text ="<strong>Version: </strong>"+str(it.version)+" <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    if it.relacion!=None:
                       rel=get_object_or_404(Item,id=it.relacion_id)
                       text ="<strong>Relacion: </strong> "+it.tipo+" de "+rel.nombre+"<br>"
                    else:
                       text ="<strong>Relacion: </strong> No tiene <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    dateFormat = it.fecha_creacion.strftime("%d-%m-%Y")
                    text ="<strong>Fecha de creacion: </strong>"+dateFormat+" <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    dateFormat = it.fecha_mod.strftime("%d-%m-%Y")
                    text ="<strong>Fecha de modificacion: </strong>"+dateFormat+" <br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    if it.lineaBase!=None:
                       lb=get_object_or_404(LineaBase,id=it.lineaBase_id)
                       text ="<strong>Linea Base: </strong>"+lb.nombre+" <br><br><br>"
                    else:
                       text ="<strong>Linea Base: </strong> Ninguna <br><br><br>"
                    Story.append(Paragraph(text, styles["SubsubItems"]))
                    Story.append(Indenter(-60))


    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_items"+proyecto.nombre+".pdf"


def descargar_reporteItems(request, id_proyecto):
    '''
    Vista para descargar el reporte de lineas base de un proyecto especifico
    '''
    if not es_lider(request.user.id, id_proyecto):
        return HttpResponseRedirect('/denegado')
    a=file(reporte_items(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')



def reporte_versiones_items(id_proyecto):
    '''
    Funcion que genera el reporte de las versiones de los items de un proyecto
    '''

    fases=Fase.objects.filter(proyecto_id=id_proyecto).order_by('orden')
    proyecto = get_object_or_404(Proyecto,id=id_proyecto)
    items = itemsProyecto(proyecto.id)

    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_versiones"+proyecto.nombre+".pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=30,bottomMargin=18)


    Story=[]
    logo = str(settings.BASE_DIR)+"/static/icono.png"
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Principal',alignment=1,spaceAfter=20, fontSize=24))
    styles.add(ParagraphStyle(name='Justify',fontName='Courier-Oblique', alignment=TA_JUSTIFY, fontSize=14,spaceAfter=5))
    styles.add(ParagraphStyle(name='Titulo', fontName='Helvetica', fontSize=18, alignment=0, spaceAfter=25, spaceBefore=3))
    styles.add(ParagraphStyle(name='Header',fontName='Helvetica',fontSize=20))
    styles.add(ParagraphStyle(name='SubsubsubItems',fontName='Helvetica',fontSize=8,spaceAfter=3))
    styles.add(ParagraphStyle(name='SubsubItems',fontName='Helvetica',fontSize=10,spaceAfter=3))
    styles.add(ParagraphStyle(name='SubItems',fontName='Helvetica',fontSize=12,spaceAfter=10))
    styles.add(ParagraphStyle(name='Items',fontName='Helvetica',fontSize=14,spaceAfter=5, spaceBefore=5))
    styles.add(ParagraphStyle(name='Subtitulos',fontSize=12,spaceAfter=3))
    styles.add(ParagraphStyle(name='Encabezado',fontSize=10,spaceAfter=10, left=1, bottom=1))
    im = Image(logo, width=100,height=50)
    Story.append(im)
    contador_act=1
    titulo="<b>Versiones de Items del Proyecto "
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    titulo= "<b>" + proyecto.nombre + "</b>"
    Story.append(Paragraph(titulo,styles['Principal']))
    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))

    titulo = Paragraph('<b>Items <\b>', styles['Titulo'])
    Story.append(Spacer(1, 12))
    Story.append(titulo)
    Story.append(Indenter(25))
    Story.append(Spacer(1, 12))
    Story.append(Indenter(-25))
    for it in items:
            Story.append(Indenter(25))
            text=""+it.nombre+"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="______________________________________________<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Versiones: </strong> <br>"
            Story.append(Paragraph(text, styles["SubItems"]))
            Story.append(Indenter(-25))
            versiones=VersionItem.objects.filter(id_item=it.id)
            if len(versiones)==0:
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="<b>El item aun no se ha modificado desde su creacion. </b><br><br>"
                Story.append(Paragraph(text, styles["SubItems"]))
                Story.append(Indenter(-42))
            for ver in versiones:
                text = ''
                Story.append(Indenter(42))
                Story.append(Spacer(1, 10))
                text ="-Version " + str(ver.version) +"<br>"
                Story.append(Paragraph(text, styles["SubItems"]))
                Story.append(Indenter(-42))

                text = ''
                Story.append(Indenter(50))
                text ="<strong>Nombre: </strong>" + ver.nombre +"<br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                Story.append(Indenter(-50))
                Story.append(Indenter(60))
                text ="<strong>Descripcion: </strong>"+ver.descripcion+" <br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                text ="<strong>Costo: </strong>"+str(ver.costo)+" <br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                text ="<strong>Tiempo: </strong>"+str(ver.tiempo)+" <br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                text ="<strong>Estado: </strong>"+ver.estado+" <br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                if ver.relacion!=None:
                   rel=get_object_or_404(Item,id=ver.relacion_id)
                   text ="<strong>Relacion: </strong> "+ver.tipo+" de "+rel.nombre+"<br>"
                else:
                   text ="<strong>Relacion: </strong> No tiene <br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                dateFormat = ver.fecha_mod.strftime("%d-%m-%Y")
                text ="<strong>Fecha de modificacion: </strong>"+dateFormat+" <br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                text ="<strong>Usuario: </strong>"+ ver.usuario.first_name + " " + ver.usuario.last_name +" <br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                if ver.lineaBase!=None:
                   lb=get_object_or_404(LineaBase,id=ver.lineaBase_id)
                   text ="<strong>Linea Base: </strong>"+lb.nombre+" <br><br><br>"
                else:
                   text ="<strong>Linea Base: </strong> Ninguna <br><br><br>"
                Story.append(Paragraph(text, styles["SubsubItems"]))
                Story.append(Indenter(-60))


    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_versiones"+proyecto.nombre+".pdf"


def descargar_reporteVersionesItems(request, id_proyecto):
    '''
    Vista para descargar el reporte de lineas base de un proyecto especifico
    '''
    if not es_lider(request.user.id, id_proyecto):
        return HttpResponseRedirect('/denegado')
    a=file(reporte_versiones_items(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')


def reporte_solicitudes(id_proyecto):
    '''
    Funcion que genera el reporte de roles del sistema
    '''

    proyecto = get_object_or_404(Proyecto,id=id_proyecto)
    doc = SimpleDocTemplate(str(settings.BASE_DIR)+"/reporte_solicitudes"+proyecto.nombre+".pdf",pagesize=letter,
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
    titulo="<b>Solicitudes del proyecto </b>"
    Story.append(Paragraph(titulo,styles['Principal']))


    Story.append(Spacer(1, 12))
    titulo="<b>" +proyecto.nombre+ "</b>"
    Story.append(Paragraph(titulo,styles['Principal']))


    Story.append(Spacer(1, 12))
    date=datetime.now()
    dateFormat = date.strftime("%d-%m-%Y")
    Story.append(Paragraph('Fecha: ' + str(dateFormat),styles['Subtitulos']))
    solicitudes=[]
    solicitudesPen=SolicitudCambio.objects.filter(proyecto=proyecto,estado='PENDIENTE')
    for s in solicitudesPen:
        solicitudes.append(s)
    pen=0
    solicitudesApr=SolicitudCambio.objects.filter(proyecto=proyecto,estado='APROBADA')
    for s in solicitudesApr:
        solicitudes.append(s)
    apr=0
    solicitudesRec=SolicitudCambio.objects.filter(proyecto=proyecto,estado='RECHAZADA')
    for s in solicitudesRec:
        solicitudes.append(s)
    rec=0
    solicitudesEje=SolicitudCambio.objects.filter(proyecto=proyecto,estado='EJECUTADA')
    for s in solicitudesEje:
        solicitudes.append(s)
    eje=0
    contador=0


    for solicitud in solicitudes:

            contador+=1
            if solicitud.estado=='PENDIENTE' and pen==0:
                titulo = Paragraph('<b>Solicitudes Pendientes <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                pen=1
                contador=1
            if solicitud.estado=='APROBADA' and apr==0:
                titulo = Paragraph('<b>Solicitudes Aprobadas <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                apr=1
                contador=1

            if solicitud.estado=='RECHAZADA' and rec==0:
                titulo = Paragraph('<b>Solicitudes Rechazadas <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                rec=1
                contador=1

            if solicitud.estado=='EJECUTADA' and eje==0:
                titulo = Paragraph('<b>Solicitudes Ejecutadas <\b>', styles['Titulo'])
                Story.append(Spacer(1, 12))
                Story.append(titulo)
                text ="__________________________________________________________<br>"
                Story.append(Paragraph(text, styles["Items"]))
                eje=1
                contador=1

            Story.append(Indenter(25))
            text="<strong>"+str(contador)+".</strong>"
            Story.append(Paragraph(text, styles["Subtitulos"]))
            text ="<strong>Nombre: </strong>" + solicitud.nombre +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Descripcion: </strong>" + solicitud.descripcion +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            it=get_object_or_404(Item,id=solicitud.item_id)
            text ="<strong>Item: </strong>" + it.nombre +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Linea Base afectada: </strong>" + it.lineaBase.nombre +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            dateFormat = solicitud.fecha.strftime("%d-%m-%Y")
            text ="<strong>Fecha de creacion: </strong>" + str(dateFormat) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Costo Total: </strong>" + str(solicitud.costo) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Tiempo Total: </strong>" + str(solicitud.tiempo) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Usuario solicitante: </strong>" + solicitud.usuario.first_name +" "+ solicitud.usuario.last_name +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            favor=Voto.objects.filter(solicitud_id=solicitud.id,voto="APROBAR").count()
            contra=Voto.objects.filter(solicitud_id=solicitud.id,voto="RECHAZAR").count()
            votos = Voto.objects.filter(solicitud_id=solicitud.id)
            text ="<strong>Mimbros que ya votaron: </strong> <br>"
            Story.append(Paragraph(text, styles["Items"]))
            if len(votos)==0:
                text = "Ningun miembro del comite a emitido su voto"
                Story.append(Paragraph(text, styles["SubItems"]))
            for voto in votos:
                text = "- " + voto.usuario.first_name + " " +voto.usuario.last_name +"<br>"
                Story.append(Paragraph(text, styles["SubItems"]))
            text ="<strong>Votos a favor: </strong>" + str(favor) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            text ="<strong>Votos en contra: </strong>" + str(contra) +"<br>"
            Story.append(Paragraph(text, styles["Items"]))
            Story.append(Spacer(1, 12))
            text ="__________________________________________________________<br>"
            Story.append(Paragraph(text, styles["Items"]))

            Story.append(Indenter(-25))


    doc.build(Story)
    return str(settings.BASE_DIR)+"/reporte_solicitudes"+proyecto.nombre+".pdf"


def descargar_reporteSolicitudes(request, id_proyecto):
    '''
    Vista para descargar el reporte de solicitudes de un proyecto especifico
    '''
    if not es_lider(request.user.id, id_proyecto):
        return HttpResponseRedirect('/denegado')
    a=file(reporte_solicitudes(id_proyecto))

    return StreamingHttpResponse(a,content_type='application/pdf')