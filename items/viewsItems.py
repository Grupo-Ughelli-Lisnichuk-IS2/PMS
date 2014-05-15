from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User, Permission
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from datetime import datetime
# Create your views here.
from django.template import RequestContext
import pydot
from PMS import settings
from fases.models import Fase
from items.models import Item, Archivo, AtributoItem, VersionItem
from proyectos.models import Proyecto
from tiposDeItem.models import TipoItem, Atributo
from items.formsItems import EstadoItemForm
from items.formsItems import PrimeraFaseForm
from tiposDeItem.viewsTiposDeItem import validarAtributo

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
    setproyectos=set(proyectos)
    return render_to_response('items/abrir_proyecto.html', {'datos': setproyectos}, context_instance=RequestContext(request))

@login_required
def listar_fases(request, id_proyecto):

    '''
    vista para listar las fases asignadas a un usuario de un proyecto especifico
    '''
    #busca todas las fases del proyecto
    fasesProyecto=Fase.objects.filter(Q(proyecto_id=id_proyecto) & (Q(estado='EJE') | Q(estado='FIN')))
    usuario = request.user
    proyecto=get_object_or_404(Proyecto,id=id_proyecto)
    fases=[]
    flag=0
    #si es lider pertenece a todas las fases
    if usuario.id==proyecto.lider_id:
        fases=fasesProyecto
        flag=1
    #si no, busca todas las fases en las que tiene algun rol asignado
    else:
        roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
        for rol in roles:
            for f in fasesProyecto:
                ff=Fase.objects.filter(id=f.id,roles__id=rol.id)
                for fff in ff:
                    fases.append(fff)
    #si no encuentra ninguna fase, significa que alguien que no tiene permisos esta tratando de ver
    #fases que no le correponden, se redirige al template de prohibido
    if len(fases)==0 and flag==0:
        return render_to_response('403.html')
    nivel = 1

    return render_to_response('items/abrir_fase.html', {'datos': fases, 'nivel':nivel}, context_instance=RequestContext(request))


def es_miembro(id_usuario, id_fase,permiso):
    '''
    funcion que recibe el id de un usuario y de una fase y devuelve true si el usuario tiene alguna fase asignada
    o false si no tiene ningun rol en esa fase
    Ademas verifica que el estado de la fase se EJE
    '''

    fase=get_object_or_404(Fase,id=id_fase)
    usuario=User.objects.get(id=id_usuario)
    proyecto=get_object_or_404(Proyecto,id=fase.proyecto_id)
    if fase.estado!='EJE':
        return False
    if usuario.id==proyecto.lider_id:
        return True
    rol_usuario=None
    roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
    roles_fase=Group.objects.filter(fase__id=fase.id)
    for rol in roles:
        for r in roles_fase:
            if rol.id==r.id:
                rol_usuario=rol
    if permiso=='' and rol_usuario!=None:
        return True
    if rol_usuario!=None:
        perm=Permission.objects.get(codename=permiso)
        permisos=Permission.objects.filter(group__id=rol_usuario.id)
        for p in permisos:
            if p==perm:
                return True

    return False


@login_required
def listar_tiposDeItem(request, id_fase):

    '''
    vista para listar los tipos de item de las fases asignadas a un usuario de un proyecto especifico
    '''
    #se comprueba que el usuario sea miembro de esa fase, si no es alguien sin permisos
    flag=es_miembro(request.user.id, id_fase,'')

    fase=Fase.objects.get(id=id_fase)
    if flag==True:
        tiposItem = TipoItem.objects.filter(fase_id=id_fase).order_by('nombre')
    else:
        return render_to_response('403.html')

    nivel = 2
    return render_to_response('items/listar_tipoDeItem.html', {'datos': tiposItem, 'fase':fase, 'nivel':nivel}, context_instance=RequestContext(request))


def cantidad_items(id_tipoItem):
    '''
    funcion para contar la cantidad de items ya creados en una fase
    Si aun no se alcanzo el limite devuelve True,
    Ademas verifica que la fase a agregar items no tenga estado FIN
    '''
    titem=get_object_or_404(TipoItem,id=id_tipoItem)
    fase=Fase.objects.get(id=titem.fase_id)
    if fase.estado=='FIN':
        return False
    item=Item.objects.filter(tipo_item_id=id_tipoItem)
    contador=0
    for i in item:
        if i.estado!='ANU':
            contador+=1
    if contador<fase.maxItems:
        return True
    else:
        return False

@login_required

def crear_item(request,id_tipoItem):
    '''
    Vista para crear un item y asignarlo a un tipo de item. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    '''
    atri=1
    hijo=False
    if cantidad_items(id_tipoItem):
        id_fase=TipoItem.objects.get(id=id_tipoItem).fase_id
        flag=es_miembro(request.user.id,id_fase,'agregar_item')
        atributos=Atributo.objects.filter(tipoItem=id_tipoItem)
        if len(atributos)==0:
            atri=0
        fase=Fase.objects.get(id=id_fase)
        proyecto=fase.proyecto_id
        items=[]
        tipoitem=[]
        fase_anterior=Fase.objects.filter(proyecto_id=proyecto, orden=((fase.orden)-1))
        if len(fase_anterior)==0:
            items=[]
        else:
            for fase in fase_anterior:
                titem=TipoItem.objects.filter(fase_id=fase.id)
                for i in titem:
                    it=Item.objects.filter(tipo_item_id=i.id, estado='FIN')
                    for ii in it:
                        items.append(ii)

        if flag==True:
            if request.method=='POST':
                #formset = ItemFormSet(request.POST)
                formulario = PrimeraFaseForm(request.POST)

                if formulario.is_valid():
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                    #obtener item con el cual relacionar
                    item_nombre=request.POST.get('entradalista')
                    if item_nombre!=None:
                        item=''
                        itemss=Item.objects.filter(nombre=item_nombre)
                        for i in itemss:
                            item=i
                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1, relacion_id=item.id, tipo='Sucesor',tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat)
                        newItem.save()
                    else:
                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1,tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat)
                        newItem.save()
                #guardar archivo
                    if request.FILES.get('file')!=None:
                        archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=cod.id)
                        archivo.save()
                #guardar atributos

                    for atributo in atributos:

                        a=request.POST.get(atributo.nombre)
                        if a!=None:
                            #validar atributos antes de guardarlos
                            if validarAtributo(request,atributo.tipo,a):
                                aa=AtributoItem(id_item_id=cod.id, id_atributo=atributo,valor=a,version=1)
                                aa.save()
                    return render_to_response('items/creacion_correcta.html',{'id_tipo_item':id_tipoItem}, context_instance=RequestContext(request))
            else:

                formulario = PrimeraFaseForm()
                hijo=False
            return render_to_response('items/crear_item.html', { 'formulario': formulario, 'atributos':atributos, 'items':items, 'hijo':hijo,'atri':atri,'titem':id_tipoItem}, context_instance=RequestContext(request))
        else:
            return render_to_response('403.html')
    else:
        return render_to_response('items/creacion_incorrecta.html',{'id_tipo_item':id_tipoItem}, context_instance=RequestContext(request))


def puede_add_items(id_fase):
    '''
    Funcion que verifica que ya se pueden agregar items a una fase. Si es la primera fase, se puede
    Si no, se verifica que la fase anterior tenga items en una linea base para poder agregar items a la
    fase siguiente.
    '''
    fase=Fase.objects.get(id=id_fase)
    if fase.orden==1:
        return True
    else:
        fase_anterior=Fase.objects.get(orden=fase.orden-1,proyecto=fase.proyecto)
        tipoitem=TipoItem.objects.filter(fase_id=fase_anterior.id)

        for ti in tipoitem:
            item=Item.objects.filter(tipo_item_id=ti.id)
            for i in item:
                if i.estado=='FIN':
                    return True
    return False

@login_required

def listar_items(request,id_tipo_item):
    '''
    vista para listar los items pertenecientes a un tipo de item
    '''
    titem=get_object_or_404(TipoItem,id=id_tipo_item)
    fase=titem.fase_id
    if es_miembro(request.user.id,fase,''):
        items=Item.objects.filter(tipo_item_id=id_tipo_item).exclude(estado='ANU')
        if puede_add_items(fase):
            nivel = 3
            id_proyecto=Fase.objects.get(id=fase).proyecto_id
            nombre=dibujarProyecto(id_proyecto)
            return render_to_response('items/listar_items.html', {'datos': items, 'titem':titem, 'nivel':nivel,'proyecto':id_proyecto,'name':nombre}, context_instance=RequestContext(request))
        else:
            return HttpResponse("<h1>No se pueden administrar los Items de esta fase. La fase anterior aun no tiene items finalizados<h1>")

    else:
        return render_to_response('403.html')

@login_required
def listar_versiones(request,id_item):
    '''
    vista para listar todas las versiones existentes de un item dado
    '''
    item=get_object_or_404(Item,id=id_item)
    if item.estado!='PEN':
        return HttpResponse("<h1> No se puede modificar un item cuyo estado no sea pendiente")
    titem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=titem.fase_id
    if es_miembro(request.user.id,fase,'cambiar_versionitem'):
        items=VersionItem.objects.filter(id_item_id=id_item).order_by('version')
        return render_to_response('items/listar_versiones.html', {'datos': items, 'titem':titem,'item':item}, context_instance=RequestContext(request))


    else:
        return render_to_response('403.html')

def volver_item(version,rel):
    '''
    funcion que vuelve a  una version anterior de un item dado
    '''
    today = datetime.now() #fecha actual
    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
    item=get_object_or_404(Item,id=version.id_item_id)
    item.version=item.version+1
    item.nombre=version.nombre
    item.descripcion=version.descripcion
    item.costo=version.costo
    item.tiempo=version.tiempo
    item.tipo=version.tipo
    if rel==0:
        item.relacion=version.relacion
    else:
        item.relacion=rel
    item.fecha_mod=dateFormat
    item.save()


def comprobar_relacion(version):
    '''
    comprueba que el item a reversionar este relacionado con un item que aun esta activo (true)
    de lo contrario (false)
    Ademas comprueba que no se formen ciclos al modificar una relacion del tipo padre-hijo
    '''
    if version.relacion==version.id_item.relacion:
        return True
    if version.relacion==None:
        return True
    if version.tipo=='Sucesor':
        return True
    relacion=get_object_or_404(Item,id=version.relacion_id)

    item=version.id_item
    if validar_hijos(relacion, item)!=True:
        return False
  #  a=Item.objects.filter((Q(tipo='Hijo') & Q(relacion=item) & Q(id=relacion.id)) & (Q (estado='PEN') | Q(estado='FIN')  | Q(estado='VAL')))
   # if a!=None:
    #    return False
    items=Item.objects.filter(estado='ANU')
    for i in items:
        if i==relacion:
            return False
    return True

def generar_version(item,usuario):
    '''
    funcion para generar y guardar una nueva version de un item a modificar
    '''
    today = datetime.now() #fecha actual
    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
    item_viejo=VersionItem(id_item=item, nombre=item.nombre, descripcion=item.descripcion, fecha_mod=dateFormat, version=item.version, costo=item.costo, tiempo=item.tiempo, tipo_item=item.tipo_item, relacion=item.relacion, tipo=item.tipo, estado=item.estado, usuario=usuario, lineaBase=item.lineaBase )
    item_viejo.save()


@login_required

def reversionar_item(request, id_version):
    '''
    vista para volver a una version anterior de un item
    '''
    version=get_object_or_404(VersionItem,id=id_version)
    item=get_object_or_404(Item,id=version.id_item_id)
    if item.estado!='PEN':
        return HttpResponse("<h1> No se puede modificar un item cuyo estado no sea pendiente")
    titem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=titem.fase_id
    if es_miembro(request.user.id,fase,'cambiar_versionitem'):
        version=get_object_or_404(VersionItem,id=id_version)
        item=get_object_or_404(Item,id=version.id_item_id)
        generar_version(item,request.user)
        #comprueba la relacion
        if comprobar_relacion(version):

            volver_item(version,0)
            return render_to_response('items/creacion_correcta.html',{'id_tipo_item':titem.id}, context_instance=RequestContext(request))
        else:
                volver_item(version,item.relacion)
                return render_to_response('items/creacion_correcta_relacion.html',{'id_tipo_item':titem.id}, context_instance=RequestContext(request))


    else:
        return render_to_response('403.html')


def descargar(idarchivo):
    '''
    Funcion que recibe el id de un archivo y retorna el objeto archivo dado el id recibido
    '''
    archivo=get_object_or_404(Archivo,id=idarchivo)

    return archivo.archivo

@login_required
def des(request, idarchivo):
    '''
    Vista para descargar un archivo de un item especifico
    '''
    archivo=get_object_or_404(Archivo,id=idarchivo)
    item=get_object_or_404(Item, id=archivo.id_item)
    fase=item.tipo_item__fase
    if es_miembro(request.user.id,fase.id,'')!=True:
        return HttpResponseRedirect('/denegado')
    return StreamingHttpResponse(descargar(idarchivo),content_type='application/force-download')

@login_required
def detalle_item(request, id_item):

    '''
    vista para ver los detalles del item <id_item>
    '''
    item=get_object_or_404(Item,id=id_item)
    tipoitem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=tipoitem.fase_id
    if es_miembro(request.user.id, fase,''):
        atributos=AtributoItem.objects.filter(id_item=id_item)
        archivos=Archivo.objects.filter(id_item=id_item)
        dato = get_object_or_404(Item, pk=id_item)

        return render_to_response('items/detalle_item.html', {'datos': dato, 'atributos': atributos, 'archivos':archivos}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')


@login_required
def detalle_version_item(request, id_version):

    '''
    vista para ver los detalles del item <id_item>
    '''
    item=get_object_or_404(VersionItem,id=id_version)
    tipoitem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=tipoitem.fase_id
    if es_miembro(request.user.id, fase,''):
        dato = get_object_or_404(VersionItem, pk=id_version)

        return render_to_response('items/detalle_version.html', {'datos': dato}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')



@login_required

def crear_item_hijo(request,id_item):
    '''
    Vista para crear un item como hijo de uno ya creado y asignarlo a un tipo de item. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    '''
    item=get_object_or_404(Item,id=id_item)
    hijo=True
    if item.estado=='FIN' or item.estado=='VAL' or item.estado=='PEN':
        atri=1
        id_tipoItem=get_object_or_404(Item,id=id_item).tipo_item_id
        if cantidad_items(id_tipoItem):
            id_fase=get_object_or_404(TipoItem,id=id_tipoItem).fase_id
            flag=es_miembro(request.user.id,id_fase,'agregar_item')
            atributos=Atributo.objects.filter(tipoItem=id_tipoItem)
            if len(atributos)==0:
                atri=0
            fase=get_object_or_404(Fase,id=id_fase)
            proyecto=fase.proyecto_id
            if flag==True:
                if request.method=='POST':
                    #formset = ItemFormSet(request.POST)
                    formulario = PrimeraFaseForm(request.POST)

                    if formulario.is_valid():
                        today = datetime.now() #fecha actual
                        dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                        #obtener item con el cual relacionar

                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1, relacion_id=id_item, tipo='Hijo',tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat)

                        newItem.save()
                    #guardar archivo
                        if request.FILES.get('file')!=None:
                            archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=cod.id)
                            archivo.save()
                    #guardar atributos
                        for atributo in atributos:

                            a=request.POST[atributo.nombre]
                            #validar atributos antes de guardarlos
                            if validarAtributo(request,atributo.tipo,a):
                                aa=AtributoItem(id_item_id=cod.id, id_atributo=atributo,valor=a,version=1)
                                aa.save()
                        return render_to_response('items/creacion_correcta.html',{'id_tipo_item':id_tipoItem}, context_instance=RequestContext(request))
                else:

                    formulario = PrimeraFaseForm()
                    hijo=True
                return render_to_response('items/crear_item.html', { 'formulario': formulario, 'atributos':atributos,'hijo':hijo,'atri':atri}, context_instance=RequestContext(request))
            else:
                return render_to_response('403.html')
        else:
            return render_to_response('items/creacion_incorrecta.html',{'id_tipo_item':id_tipoItem}, context_instance=RequestContext(request))
    else:
        return HttpResponse("<h1>No se puede crear un hijo a un item con estado que no sea Finalizado, Pendiente o Validado</h1>")


@login_required

def eliminar_archivo(request, id_archivo):
    '''
    vista que recibe el id de un archivo y lo borra de la base de datos
    '''

    archivo=get_object_or_404(Archivo,id=id_archivo)
    item=archivo.id_item
    if item.estado!='PEN':
        return HttpResponse("<h1> No se puede modificar un item cuyo estado no sea pendiente")
    fase=item.tipo_item__fase
    if es_miembro(request.user.id, fase.id, 'eliminar_archivo')!=True:
        return HttpResponseRedirect('/denegado')
    archivo.delete()
    return HttpResponseRedirect('/desarrollo/item/archivos/'+str(item.id))

def validar_hijos(item_hijo, item):
    if item_hijo!=None:
        while(item_hijo!=item and item_hijo!=None):
            if item_hijo.relacion==item:
                return False
            else:
                item_hijo=item_hijo.relacion
    return True


@login_required

def cambiar_padre(request, id_item):
    item=get_object_or_404(Item,id=id_item)
    if item.estado!='PEN':
        return HttpResponse("<h1> No se puede modificar un item cuyo estado no sea pendiente")
    tipo=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=get_object_or_404(Fase,id=tipo.fase_id)
    if es_miembro(request.user.id,fase.id,'cambiar_item'):
        items=[]
        titem=TipoItem.objects.filter(fase_id=fase.id)
        for i in titem:
            a=Item.objects.filter(Q(tipo_item_id=i.id) & (Q (estado='PEN') | Q(estado='FIN')  | Q(estado='VAL')))
            for aa in a:
                #verifica que el item a relacionar no sea si mismo, su hijo o ya sea su padre
                if aa != item and item.relacion!=aa and item!=aa.relacion:
                    items.append(aa)
        if request.method=='POST':
            item_nombre=request.POST.get('entradalista')
            if item_nombre!=None:

                    item_rel=''
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                    item=get_object_or_404(Item,id=id_item)
                    generar_version(item, request.user)
                    item.fecha_mod=dateFormat
                    item.version=item.version+1
                    itemss=Item.objects.filter(nombre=item_nombre)
                    for i in itemss:
                        item_rel=i
                    if validar_hijos(item_rel,item):

                        item.relacion=item_rel
                        item.tipo='Hijo'
                        item.save()
                        return HttpResponseRedirect('/desarrollo/item/listar/'+str(item.tipo_item_id))
                    else:
                        messages.add_message(request,settings.DELETE_MESSAGE, "Este item genera ciclos. No puede ser su padre")
        if len(items)==0:
            messages.add_message(request,settings.DELETE_MESSAGE, "No hay otros items que pueden ser padres de este")
        return render_to_response('items/listar_padres.html', { 'items':items, 'tipoitem':item}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/denegado')

@login_required

def cambiar_antecesor(request, id_item):
    '''
    vista para cambiar la relacion de un item, del tipo antecesor
    '''

    item=get_object_or_404(Item,id=id_item)
    if item.estado!='PEN':
        return HttpResponse("<h1> No se puede modificar un item cuyo estado no sea pendiente")
    tipo=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fas=get_object_or_404(Fase,id=tipo.fase_id)
    if es_miembro(request.user.id,fas.id,'cambiar_item'):
        proyecto=fas.proyecto_id
        items=[]
        fase_anterior=Fase.objects.filter(proyecto_id=proyecto, orden=fas.orden-1)
        if len(fase_anterior)==0:
            items=[]
        else:
            for fase in fase_anterior:
                titem=TipoItem.objects.filter(fase_id=fase.id)
                for i in titem:
                    ii=Item.objects.filter(tipo_item_id=i.id, estado='FIN')
                    for it in ii:
                        if it!=item.relacion:
                            items.append(it)
        if request.method=='POST':
            item_nombre=request.POST.get('entradalista')
            if item_nombre!=None:
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                    generar_version(item,request.user)
                    item.fecha_mod=dateFormat
                    item.version=item.version+1
                    item_rel=Item.objects.get(nombre=item_nombre)
                    item.relacion=item_rel
                    item.tipo='Sucesor'
                    item.save()
                    return HttpResponseRedirect('/desarrollo/item/listar/'+str(item.tipo_item_id))
        if len(items)==0:
            messages.add_message(request,settings.DELETE_MESSAGE, "No hay otros items que pueden ser antecesores de este")
        return render_to_response('items/listar_antecesores.html', { 'items':items, 'tipoitem':item}, context_instance=RequestContext(request))
    else:
       return HttpResponseRedirect('/denegado')

@login_required

def listar_archivos(request, id_item):
    '''
    vista para gestionar los archivos de un item dado'
    '''
    item=get_object_or_404(Item,id=id_item)
    if item.estado!='FIN':
        return HttpResponse("<h1> No se pueden modificar un item cuyo estado no sea pendiente")
    titem=get_object_or_404(Item,id=id_item).tipo_item
    fase=titem.fase_id
    if es_miembro(request.user.id,fase,'cambiar_item'):
        archivos=Archivo.objects.filter(id_item=id_item)
        if request.method=='POST':
            if request.FILES.get('file')!=None:
                archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=id_item)
                archivo.save()


        return render_to_response('items/listar_archivos.html', { 'archivos': archivos,'titem':titem}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')


@login_required

def listar_atributos(request, id_item):
    '''
    vista para gestionar los atributos de un item dado
    '''
    item=get_object_or_404(Item,id=id_item)
    if item.estado!='PEN':
        return HttpResponse("<h1> No se pueden modificar un item cuyo estado no sea pendiente")
    titem=get_object_or_404(Item,id=id_item).tipo_item
    fase=titem.fase_id
    if es_miembro(request.user.id,fase,'cambiar_item'):
        atributos=AtributoItem.objects.filter(id_item=id_item)
        id_tipoi=titem.id

        if request.method=='POST':
            for atributo in atributos:
                a=request.POST[atributo.id_atributo.nombre]

                #validar atributos antes de guardarlos
                if validarAtributo(request,atributo.id_atributo.tipo,a):
                    aa=AtributoItem.objects.get(id=atributo.id)
                    aa.valor=a
                    aa.save()
                    atributos=AtributoItem.objects.filter(id_item=id_item)
                    return render_to_response('items/creacion_correcta.html',{'id_tipo_item':id_tipoi}, context_instance=RequestContext(request))
        return render_to_response('items/listar_atributos.html', { 'atributos': atributos,'titem':titem}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/denegado')

@login_required

def editar_item(request,id_item):
    '''
    vista para cambiar el nombre y la descripcion del tipo de item, y ademas agregar atributos al mismo
    '''
    id_tipoItem=get_object_or_404(Item,id=id_item).tipo_item_id
    id_fase=get_object_or_404(TipoItem,id=id_tipoItem).fase_id
    flag=es_miembro(request.user.id,id_fase,'cambiar_item')
    item_nuevo=get_object_or_404(Item,id=id_item)
    if item_nuevo.estado=='PEN':
        if flag==True:

                if request.method=='POST':
                    generar_version(item_nuevo,request.user)
                    formulario = PrimeraFaseForm(request.POST, instance=item_nuevo)

                    if formulario.is_valid():
                        today = datetime.now() #fecha actual
                        dateFormat = today.strftime("%Y-%m-%d") # fecha con format

                        formulario.save()
                        item_nuevo.fecha_mod=dateFormat
                        item_nuevo.version=item_nuevo.version+1
                        item_nuevo.save()

                        return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase, 'id_tipo_item':id_tipoItem}, context_instance=RequestContext(request))

                else:

                    formulario = PrimeraFaseForm(instance=item_nuevo)
                    hijo=True
                return render_to_response('items/editar_item.html', { 'formulario': formulario, 'item':item_nuevo,'titem':id_tipoItem}, context_instance=RequestContext(request))

        else:
                return render_to_response('403.html')
    else:
        return HttpResponse('<h1> No se puede modificar el item, ya que su estado no es Pendiente</h1>')



@login_required
def cambiar_estado_item(request,id_item):
    '''
    vista para cambiar el estado de un item, teniendo en cuenta:
    1) Si se quiere pasar de PEN  a VAL, se verifica que el estado de su padre tambien sea VAL
    2) Si se quiere pasar de VAL a PEN se verifica que el estado de sus hijos tambien sea PEN
    '''

    item=get_object_or_404(Item,id=id_item)
    nombre=item.nombre
    titem=item.tipo_item_id
    if item.estado=='FIN':
        return HttpResponse('<h1>No se puede cambiar el estado de un item finalizado<h1>')
    if request.method == 'POST':
        bandera=False
        item_form = EstadoItemForm(request.POST, instance=item)
        if item_form.is_valid():
                    if item_form.cleaned_data['estado']=='VAL':
                        if item.tipo=='Hijo':
                            papa=item.relacion


                            if papa.estado=='PEN':
                                messages.add_message(request,settings.DELETE_MESSAGE,'No se puede cambiar a Validado ya que su padre no ha sido validado o Finalizado')
                                bandera=True
                            if papa.estado=='VAL':
                                bandera=False
                    if item_form.cleaned_data['estado']=='PEN':
                            hijos=Item.objects.filter(relacion=item).exclude(estado='ANU')
                            for hijo in hijos:
                                if hijo.estado!='PEN' and hijo.tipo=='Hijo':
                                    messages.add_message(request,settings.DELETE_MESSAGE, 'No se puede cambiar  a pendiente ya que tiene hijos con estados distintos a Pendiente')
                                    bandera=True
                    if bandera==True:
                        return render_to_response('items/cambiar_estado_item.html', { 'item_form': item_form, 'nombre':nombre, 'titem':titem}, context_instance=RequestContext(request))
                    else:
                        item_form.save()
                        return render_to_response('items/creacion_correcta.html',{'id_tipo_item':titem}, context_instance=RequestContext(request))

    else:
        # formulario inicial
        item_form = EstadoItemForm(instance=item)
    return render_to_response('items/cambiar_estado_item.html', { 'item_form': item_form, 'nombre':nombre,'titem':titem}, context_instance=RequestContext(request))

def itemsProyecto(proyecto):
    '''
    Funcion que recibe como parametro un proyecto y retorna todos los items del mismo
    '''
    fases = Fase.objects.filter(proyecto_id=proyecto)
    items=[]
    for fase in fases:
        titem=TipoItem.objects.filter(fase=fase)
        for t in titem:
            item=Item.objects.filter(tipo_item=t)
            for i in item:
                items.append(i)
    return items


def dibujarProyecto(proyecto):
    '''
    Funcion que grafica los items con sus relaciones de un proyecto dado
    '''
    #inicializar estructuras
    grafo = pydot.Dot(graph_type='digraph',fontname="Verdana",rankdir="LR")
    fases = Fase.objects.filter(proyecto_id=proyecto).order_by('orden')
    clusters = []
    clusters.append(None)
    for fase in fases:
        if(fase.estado=='FIN'):
            cluster = pydot.Cluster(str(fase.orden),
                                    label=str(fase.orden)+") "+fase.nombre,
                                    style="filled",
                                    fillcolor="gray")
        else:
            cluster = pydot.Cluster(str(fase.orden),
                                    label=str(fase.orden)+") "+fase.nombre)
        clusters.append(cluster)

    for cluster in clusters:
        if(cluster!=None):
            grafo.add_subgraph(cluster)


    lista=itemsProyecto(proyecto)
    items=[]
    for item in lista:
        if item.estado!="ANU":
            items.append(item)
    #agregar nodos
    for item in items:

        if item.estado=="PEN":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="gray",
                                                                 fontcolor="black"))
        elif item.estado=="VAL":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="blue",
                                                                 fontcolor="white"))
        elif item.estado=="FIN":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="green",
                                                                 fontcolor="white"))
        elif item.estado=="REV":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="red",
                                                                 fontcolor="white"))
        elif item.estado=="CON":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="yellow",
                                                                 fontcolor="white"))
        elif item.estado=="BLO":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="pink",
                                                                 fontcolor="white"))
    #agregar arcos
    for item in items:
        relaciones = Item.objects.filter(relacion=item).exclude(estado='ANU')
        if relaciones!=None:
            for relacion in relaciones:
                grafo.add_edge(pydot.Edge(str(item.id),str(relacion.id),label='costo='+str(item.costo) ))

    date=datetime.now()

    name=str(date)+'grafico.jpg'
    grafo.write_jpg(str(settings.BASE_DIR)+'/static/img/'+str(name))
    return name



@login_required
def eliminar_item(request, id_item):
    '''
    Vista que permite cambiar el estado del item a anulado, para ello se verifica que el mismo
    no tenga hijos y ademas que su estado sea pendiente
    '''
    item=get_object_or_404(Item, id=id_item)
    fase=item.tipo_item.fase_id
    if es_miembro(request.user.id,fase,'eliminar_item')!=True or item.estado=='ANU':
        return HttpResponseRedirect('/denegado')
    item=get_object_or_404(Item, id=id_item)
    if item.estado=='PEN':
        a=Item.objects.filter((Q(tipo='Hijo') & Q(relacion=item))).exclude(estado='ANU')
        if len(a)!=0:
            messages.add_message(request,settings.DELETE_MESSAGE,"No se puede eliminar un item que tenga hijos")
        else:
            item.estado='ANU'
            item.save()
            messages.add_message(request,settings.DELETE_MESSAGE,"Item eliminado correctamente")
    else:
         messages.add_message(request,settings.DELETE_MESSAGE,"No se puede eliminar un item cuyo estado no sea pendiente")
    fase=item.tipo_item.fase_id
    titem=item.tipo_item
    id_proyecto=Fase.objects.get(id=fase).proyecto_id
    nombre=dibujarProyecto(id_proyecto)
    nivel=3
    items=Item.objects.filter(tipo_item_id=titem.id).exclude(estado='ANU')
    return render_to_response('items/listar_items.html', {'datos': items, 'titem':titem, 'nivel':nivel,'proyecto':id_proyecto,'name':nombre}, context_instance=RequestContext(request))

@login_required
def listar_muertos(request,id_tipo_item):
    '''
    Vista para listar todos los items con estado anulado de un tipo de item especificado
    '''
    titem=get_object_or_404(TipoItem,id=id_tipo_item)
    fase=titem.fase
    if es_miembro(request.user.id,fase.id,'')!=True:
        return HttpResponseRedirect('/denegado')
    else:
        items=Item.objects.filter(estado='ANU',tipo_item=titem)
        return render_to_response('items/listar_muertos.html', {'datos': items,'tipoitem':titem}, context_instance=RequestContext(request))


@login_required
def detalle_muerto(request,id_item):
    '''
    Vista para ver los detalles de un item con estado anulado
    '''

    item=get_object_or_404(Item,id=id_item)
    if item.estado!='ANU':
        return HttpResponse("<h1> No se puede listar el detalle de un item no anulado")
    titem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=titem.fase
    if es_miembro(request.user.id,fase.id,'')!=True:
        return HttpResponseRedirect('/denegado')
    else:
        return render_to_response('items/detalle_version.html', {'datos': item}, context_instance=RequestContext(request))


@login_required
def revivir(request, id_item):
    '''
    Vista para revivir un item seleccionado. Los criterios a seguir para revivir el item son:
    1) Si el item con el que el item a revivir aun existe, lo revive
    2) Si no, revive el item pero lo relaciona con un item de su fase como hijo
    3) Si ya no existen items en su fase, lo relaciona con un item finalizado de la fase anterior
    como sucesor
    4) Si es de la primera fase y ya no tiene items en su fase, revive el item y no le asigna ninguna relacion
    '''
    item=get_object_or_404(Item,id=id_item)
    titem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=titem.fase
    if es_miembro(request.user.id,fase.id,'')!=True or item.estado!='ANU':
        return HttpResponseRedirect('/denegado')

    else:
        #si revive un item y su relacion aun existe, se revive

        if item.relacion==None:

            item.estado='PEN'
            item.save()
            messages.add_message(request,settings.DELETE_MESSAGE,'Item revivido')
        else:
            if item.relacion.estado!='ANU':
                item.estado='PEN'
                item.save()
                messages.add_message(request,settings.DELETE_MESSAGE,'Item revivido')
            else:
                i=[]
                #si no, se buscan items de su fase y se relaciona con el primero de ellos, del tipo padre
                tipos_item=TipoItem.objects.filter(fase=fase)
                for t in tipos_item:
                    items=Item.objects.filter(tipo_item=titem).exclude(estado='ANU')
                    for it in items:
                        i.append(it)
                if len(i)!=0:
                    item.estado='PEN'
                    item.relacion=i[0]
                    item.tipo='Hijo'
                    item.save()
                    messages.add_message(request,settings.DELETE_MESSAGE,'Item revivido. Relacion cambiada')

                else:
                    #primera fase sin items, revive y quita relacion anterior
                    if titem.fase.orden==1:
                        item.estado='PEN'
                        item.relacion=None
                        item.tipo=''
                        item.save()
                        messages.add_message(request,settings.DELETE_MESSAGE,'Item revivido. Relacion eliminada')
                    else:
                        #si no es la primera fase, se busca un antecesor de la fase anterior y se relaciona con el
                        fase_anterior=Fase.objects.get(proyecto=fase.proyecto, orden=fase.orden-1)
                        tipositem=TipoItem.objects.filter(fase=fase_anterior)
                        ite=[]
                        for t in tipositem:
                            itemss=Item.objects.filter(tipo_item=t, estado='FIN')
                            for ii in itemss:
                                ite.append(ii)
                        item.relacion=ite[0]
                        item.tipo='Sucesor'
                        item.estado='PEN'
                        item.save()
                        messages.add_message(request,settings.DELETE_MESSAGE,'Item revivido. Relacionado con item de fase anterior')
        items=Item.objects.filter(estado='ANU',tipo_item=titem)
        return render_to_response('items/listar_muertos.html', {'datos': items, 'tipoitem':titem}, context_instance=RequestContext(request))