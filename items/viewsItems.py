from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.forms.models import modelformset_factory
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from datetime import datetime
# Create your views here.
from django.template import RequestContext
from PMS import settings
from fases.models import Fase
from items.models import Item, Archivo, AtributoItem, VersionItem
from proyectos.models import Proyecto
from tiposDeItem.models import TipoItem, Atributo
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

def listar_fases(request, id_proyecto):

    '''
    vista para listar las fases asignadas a un usuario de un proyecto especifico
    '''
    #busca todas las fases del proyecto
    fasesProyecto=Fase.objects.filter(proyecto_id=id_proyecto, estado='EJE')
    usuario = request.user
    proyecto=Proyecto.objects.get(id=id_proyecto)
    fases=[]
    #si es lider pertenece a todas las fases
    if usuario.id==proyecto.lider_id:
        fases=fasesProyecto
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
    if len(fases)==0:
        return render_to_response('403.html')

    return render_to_response('items/abrir_fase.html', {'datos': fases}, context_instance=RequestContext(request))


def es_miembro(id_usuario, id_fase):
    '''
    funcion que recibe el id de un usuario y de una fase y devuelve true si el usuario tiene alguna fase asignada
    o false si no tiene ningun rol en esa fase
    Ademas verifica que el estado de la fase se EJE
    '''
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
    vista para listar los tipos de item de las fases asignadas a un usuario de un proyecto especifico
    '''
    #se comprueba que el usuario sea miembro de esa fase, si no es alguien sin permisos
    flag=es_miembro(request.user.id, id_fase)

    fase=Fase.objects.get(id=id_fase)
    if flag==True:
        tiposItem = TipoItem.objects.filter(fase_id=id_fase).order_by('nombre')
    else:
        return render_to_response('403.html')


    return render_to_response('items/listar_tipoDeItem.html', {'datos': tiposItem, 'fase':fase}, context_instance=RequestContext(request))


def cantidad_items(id_tipoItem):
    titem=TipoItem.objects.get(id=id_tipoItem)
    fase=Fase.objects.get(id=titem.fase_id)
    item=Item.objects.filter(tipo_item_id=id_tipoItem)
    contador=0
    for i in item:
        contador+=1
    if contador<fase.maxItems:
        return True
    else:
        return False

@login_required
#@permission_required('items.agregar_item')
def crear_item(request,id_tipoItem):
    '''
    Vista para crear un item y asignarlo a un tipo de item. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    '''
    atri=1
    if cantidad_items(id_tipoItem):
        id_fase=TipoItem.objects.get(id=id_tipoItem).fase_id
        flag=es_miembro(request.user.id,id_fase)
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
                    items.append(Item.objects.get(tipo_item_id=i.id, estado='FIN'))

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
                        item=Item.objects.get(nombre=item_nombre).id
                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1, relacion_id=item, tipo='Sucesor',tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat)
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

                        a=request.POST[atributo.nombre]
                        #validar atributos antes de guardarlos
                        if validarAtributo(request,atributo.tipo,a):
                            aa=AtributoItem(id_item_id=cod.id, id_atributo=atributo,valor=a,version=1)
                            aa.save()
                    return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
            else:

                formulario = PrimeraFaseForm()
                hijo=False
                return render_to_response('items/crear_item.html', { 'formulario': formulario, 'atributos':atributos, 'items':items, 'hijo':hijo,'atri':atri}, context_instance=RequestContext(request))
        else:
            return render_to_response('403.html')
    else:
        return render_to_response('items/creacion_incorrecta.html', context_instance=RequestContext(request))


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
        print tipoitem
        for ti in tipoitem:
            item=Item.objects.filter(tipo_item_id=ti.id)
            for i in item:
                if i.estado=='FIN':
                    return True
    return False

@login_required
#@permission_required('item')
def listar_items(request,id_tipo_item):
    '''
    vista para listar los items pertenecientes a un tipo de item
    '''
    titem=TipoItem.objects.get(id=id_tipo_item)
    fase=titem.fase_id
    if es_miembro(request.user.id,fase):
        items=Item.objects.filter(tipo_item_id=id_tipo_item)
        if puede_add_items(fase):
            return render_to_response('items/listar_items.html', {'datos': items, 'titem':titem}, context_instance=RequestContext(request))
        else:
            return HttpResponse("<h1>No se pueden administrar los Items de esta fase. La fase anterior aun no tiene items finalizados<h1>")

    else:
        return render_to_response('403.html')


def listar_versiones(request,id_item):
    '''
    vista para listar todas las versiones existentes de un item dado
    '''
    item=Item.objects.get(id=id_item)
    titem=TipoItem.objects.get(id=item.tipo_item_id)
    fase=titem.fase_id
    if es_miembro(request.user.id,fase):
        items=VersionItem.objects.filter(id_item_id=id_item).order_by('version')
        return render_to_response('items/listar_versiones.html', {'datos': items, 'titem':titem}, context_instance=RequestContext(request))


    else:
        return render_to_response('403.html')

def volver_item(version,rel):
    '''
    funcion que vuelve a  una version anterior de un item dado
    '''
    today = datetime.now() #fecha actual
    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
    item=Item.objects.get(id=version.id_item_id)
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
    '''
    relacion=version.relacion
    items=Item.objects.filter(estado='ANU')
    for i in items:
        if i==relacion:
            return False
    return True


def generar_version(item):
    '''
    funcion para generar y guardar una nueva version de un item a modificar
    '''
    today = datetime.now() #fecha actual
    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
    item_viejo=VersionItem(id_item=item, nombre=item.nombre, descripcion=item.descripcion, fecha_mod=dateFormat, version=item.version, costo=item.costo, tiempo=item.tiempo, tipo_item=item.tipo_item, relacion=item.relacion, tipo=item.tipo, estado=item.estado )
    item_viejo.save()



def reversionar_item(request, id_version):
    version=VersionItem.objects.get(id=id_version)
    item=Item.objects.get(id=version.id_item_id)
    titem=TipoItem.objects.get(id=item.tipo_item_id)
    fase=titem.fase_id
    if es_miembro(request.user.id,fase):
        version=VersionItem.objects.get(id=id_version)
        item=Item.objects.get(id=version.id_item_id)
        generar_version(item)
        if comprobar_relacion(version):

            volver_item(version,0)
            return render_to_response('items/creacion_correcta.html',{'id_fase':titem.id}, context_instance=RequestContext(request))
        else:
                volver_item(version,item.relacion)
                return render_to_response('items/creacion_correcta_relacion.html',{'id_fase':titem.id}, context_instance=RequestContext(request))

    else:
        return render_to_response('403.html')


def descargar(idarchivo):
    """Funcion que recibe el id de un archivo y retorna el objeto archivo dado el id recibido"""
    archivo=Archivo.objects.get(id=idarchivo)

    return archivo.archivo

def des(request, idarchivo):
    '''
    Vista para descargar un archivo de un item especifico
    '''
    return StreamingHttpResponse(descargar(idarchivo),content_type='application/force-download')

@login_required
def detalle_item(request, id_item):

    '''
    vista para ver los detalles del item <id_item>
    '''
    item=Item.objects.get(id=id_item)
    tipoitem=TipoItem.objects.get(id=item.tipo_item_id)
    atributos=AtributoItem.objects.filter(id_item=id_item)
    archivos=Archivo.objects.filter(id_item=id_item)
    dato = get_object_or_404(Item, pk=id_item)

    return render_to_response('items/detalle_item.html', {'datos': dato, 'atributos': atributos, 'archivos':archivos}, context_instance=RequestContext(request))

def crear_item_hijo(request,id_item):
    '''
    Vista para crear un item y asignarlo a un tipo de item. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    '''
    atri=1
    id_tipoItem=Item.objects.get(id=id_item).tipo_item_id
    if cantidad_items(id_tipoItem):
        id_fase=TipoItem.objects.get(id=id_tipoItem).fase_id
        flag=es_miembro(request.user.id,id_fase)
        atributos=Atributo.objects.filter(tipoItem=id_tipoItem)
        if len(atributos)==0:
            atri=0
        fase=Fase.objects.get(id=id_fase)
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
                    return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
            else:

                formulario = PrimeraFaseForm()
                hijo=True
                return render_to_response('items/crear_item.html', { 'formulario': formulario, 'atributos':atributos,'hijo':hijo,'atri':atri}, context_instance=RequestContext(request))
        else:
            return render_to_response('403.html')
    else:
        return render_to_response('items/creacion_incorrecta.html', context_instance=RequestContext(request))




def editar_item(request,id_item):
    '''
    vista para cambiar el nombre y la descripcion del tipo de item, y ademas agregar atributos al mismo
    '''
    id_tipoItem=Item.objects.get(id=id_item).tipo_item_id
    id_fase=TipoItem.objects.get(id=id_tipoItem).fase_id
    flag=es_miembro(request.user.id,id_fase)
    item_nuevo=Item.objects.get(id=id_item)
    if item_nuevo.estado=='PEN':
        if flag==True:

                if request.method=='POST':
                    generar_version(item_nuevo)
                    formulario = PrimeraFaseForm(request.POST, instance=item_nuevo)

                    if formulario.is_valid():
                        today = datetime.now() #fecha actual
                        dateFormat = today.strftime("%Y-%m-%d") # fecha con format

                        formulario.save()
                        item_nuevo.fecha_mod=dateFormat
                        item_nuevo.version=item_nuevo.version+1
                        item_nuevo.save()
                        return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))

                else:

                    formulario = PrimeraFaseForm(instance=item_nuevo)
                    hijo=True
                    return render_to_response('items/editar_item.html', { 'formulario': formulario, 'item':item_nuevo}, context_instance=RequestContext(request))

        else:
                return render_to_response('403.html')
    else:
        HttpResponse('<h1> No se puede modificar el item, ya que su estado no es Pendiente</h1>')