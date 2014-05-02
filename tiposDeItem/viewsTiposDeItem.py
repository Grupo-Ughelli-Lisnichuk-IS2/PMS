from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages

# Create your views here.
from django.template import RequestContext
import time
from PMS import settings
from fases.models import Fase
from tiposDeItem.formsTiposDeItem import TipoItemForm, AtributoForm, TipoItemModForm
from tiposDeItem.models import TipoItem, Atributo


@login_required
@permission_required('tipoItem')
def crear_tipoItem(request, id_fase):
    '''
    vista para crear un tipo de Item, que consta de un nombre y una descripcion
    '''
    if request.method == 'POST':
        # formulario enviado
        tipoItem_form = TipoItemForm(request.POST)

        if tipoItem_form.is_valid():
            tipoItem= tipoItem_form.save()
            tipoItem.fase_id=id_fase
            tipoItem.save()

            return render_to_response('tiposDeItem/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
    else:
        # formulario inicial
        tipoItem_form = TipoItemForm()
    return render_to_response('tiposDeItem/crear_tipoDeItem.html', { 'tipoItem_form': tipoItem_form}, context_instance=RequestContext(request))

@login_required
@permission_required('tipoItem')
def listar_tiposItem(request,id_fase):
    '''
    vista para listar los tipos de Item pertenecientes a una fase dada
    '''

    tiposItem = TipoItem.objects.filter(fase_id=id_fase).order_by('nombre')
    fase = Fase.objects.get(id=id_fase)
    return render_to_response('tiposDeItem/listar_tipoDeItem.html', {'datos': tiposItem, 'fase' : fase}, context_instance=RequestContext(request))


@login_required
@permission_required('tipoItem')
def detalle_tipoItem(request, id_tipoItem):

    '''
    vista para ver los detalles del tipo de item <id_tipoItem>
    '''

    dato = get_object_or_404(TipoItem, pk=id_tipoItem)
    atributos = Atributo.objects.filter(tipoItem__id=id_tipoItem)
    return render_to_response('tiposDeItem/detalle_tipoDeItem.html', {'datos': dato, 'atributos': atributos}, context_instance=RequestContext(request))



def validarAtributo(request, datatype, valor):
    '''
    Funcion para validar que el valor por defecto ingresado para un atributo concuerde con el tipo especificado
    '''
    if datatype=="FEC":
            try:
                fecha=datetime.strptime(str(valor),'%d/%m/%Y')
            except ValueError:
                    messages.add_message(request, settings.DELETE_MESSAGE, "Fecha incorrecta debe ser del tipo DD/MM/AAAA")
                    return False
    else:
                if datatype=="NUM":
                    a= valor.isdigit()
                    if not a:
                        messages.add_message(request, settings.DELETE_MESSAGE, "Valor no es numerico")
                        return False

                else:
                    if datatype=="LOG":
                        if valor!= "Verdadero" and valor!="Falso":
                            messages.add_message(request,settings.DELETE_MESSAGE, "Valor no es booleano. Debe ser Verdadero o Falso")
                            return False

    return True



@login_required
@permission_required('tipoItem')
def crear_atributo(request, id_tipoItem):
    '''
    vista para crear un tipo de atributo, que consta de un nombre, un tipo, un valor por defecto
    y esta relacionado con un tipo de Item
    '''

    if request.method == 'POST':
        # formulario enviado
        atributo_form = AtributoForm(request.POST)

        if atributo_form.is_valid():
            tipoItem = TipoItem.objects.filter(id=id_tipoItem)#uso filter y no get porque atributo.tipoItem=tipoItem requiere que tipoItem sea Iterable

            valor=request.POST["valorDefecto"]
            datatype=request.POST["tipo"]
            if validarAtributo(request,datatype,valor):
                atributo= Atributo(nombre = request.POST["nombre"], tipo = request.POST["tipo"], valorDefecto = request.POST["valorDefecto"])
                atributo.save()
                atributo.tipoItem=tipoItem
                atributo.save()
                tipoItem2 = get_object_or_404(TipoItem,id=id_tipoItem)
                id_fase = tipoItem2.fase_id
                return HttpResponseRedirect('/tiposDeItem/modificar/'+str(id_tipoItem))
    else:
        # formulario inicial
        atributo_form = AtributoForm()
    return render_to_response('tiposDeItem/crear_atributo.html', { 'atributo_form': atributo_form}, context_instance=RequestContext(request))

@login_required
@permission_required('tipoItem')
def eliminar_atributo(request, id_atributo, id_tipoItem):

    '''
    vista para eliminar el atributo <id_atributo>, si ningun otro tipo de Item esta relacionado a este atributo, el mismo
    es eliminado completamente.
    '''

    atributo = get_object_or_404(Atributo, pk=id_atributo)
    tipoItem = get_object_or_404(TipoItem, pk=id_tipoItem)
    fase = tipoItem.fase
    tipoItem.atributo_set.remove(atributo)
    if(atributo.tipoItem.count() == 0):
        atributo.delete()

    messages.add_message(request, settings.DELETE_MESSAGE, "Atributo eliminado")
    tiposItem = TipoItem.objects.filter(fase_id=fase.id).order_by('nombre')

    return HttpResponseRedirect('/tiposDeItem/modificar/'+str(id_tipoItem))


@login_required
@permission_required('tipoItem')
def editar_TipoItem(request,id_tipoItem):
    '''
    vista para cambiar el nombre y la descripcion del tipo de item, y ademas agregar atributos al mismo
    '''
    tipoItem= get_object_or_404(TipoItem,id=id_tipoItem)
    atributos=Atributo.objects.filter(tipoItem__id=id_tipoItem)
    id_fase=tipoItem.fase_id
    if request.method == 'POST':
        # formulario enviado
        tipoItem_form = TipoItemModForm(request.POST, instance=tipoItem)

        if tipoItem_form.is_valid():
            # formulario validado correctamente
            tipoItem_form.save()
            return render_to_response('tiposDeItem/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))

    else:
        # formulario inicial
        tipoItem_form = TipoItemModForm(instance=tipoItem)
    return render_to_response('tiposDeItem/editar_tipoItem.html', { 'atributos': atributos, 'tipoItem': tipoItem_form, 'dato':tipoItem, 'id_fase':id_fase}, context_instance=RequestContext(request))

@login_required
@permission_required('tipoItem')
def importar_tipoItem(request, id_tipoItem,id_fase):
    '''
    Vista para importar un tipo de Item, dado en <id_fase>
    '''
    tipoItem=get_object_or_404(TipoItem,id=id_tipoItem)
    if request.method=='POST':
        formulario = TipoItemForm(request.POST, initial={'nombre':tipoItem.nombre,'descripcion':tipoItem.descripcion} )

        if formulario.is_valid():
                tipo = formulario.save()
                tipo.fase_id= id_fase

                for atributo in tipoItem.atributo_set.all():
                    tipo.atributo_set.add(atributo)
                tipo.save()

                return render_to_response('tiposDeItem/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
    else:
        formulario = TipoItemForm(initial={'nombre':tipoItem.nombre,'descripcion':tipoItem.descripcion} )
    return render_to_response('tiposDeItem/crear_tipoDeItem.html', { 'tipoItem_form': formulario}, context_instance=RequestContext(request))

@login_required
@permission_required('tipoItem')
def eliminar_tipoItem(request, id_tipoItem):
    '''
    Vista para eliminar un tipo de Item. Tambien se encarga de la eliminacion de atributos no referenciados
    '''
    tipoItem = get_object_or_404(TipoItem, pk=id_tipoItem)
    fase = tipoItem.fase
    for atributo in tipoItem.atributo_set.all():
        tipoItem.atributo_set.remove(atributo)
        if(atributo.tipoItem.count() == 0):
            atributo.delete()
    tipoItem.delete()
    messages.add_message(request, settings.DELETE_MESSAGE, "Tipo de item eliminado")
    tiposItem = TipoItem.objects.filter(fase_id=fase.id).order_by('nombre')
    return render_to_response('tiposDeItem/listar_tipoDeItem.html', {'datos': tiposItem}, context_instance=RequestContext(request))

@login_required
@permission_required('tipoItem')
def listar_tiposItemProyecto(request,id_fase):
    '''
    vista para listar las fases pertenecientes a un proyecto
    '''
    fase = get_object_or_404(Fase,id=id_fase)
    proyecto_id = fase.proyecto_id
    fases = Fase.objects.filter(proyecto_id=proyecto_id)
    tiposItem = TipoItem.objects.all()
#    tiposItem = []
#    for f in fases:
#        tiposItem.append(TipoItem.objects.filter(fase=f))

    return render_to_response('tiposDeItem/importar_tipoDeItem.html', {'datos': tiposItem, 'fase' : fase}, context_instance=RequestContext(request))