from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages

# Create your views here.
from django.template import RequestContext
from PMS import settings
from fases.models import Fase
from tiposDeItem.formsTiposDeItem import TipoItemForm, AtributoForm, TipoItemModForm
from tiposDeItem.models import TipoItem, Atributo


@login_required
@permission_required('tipoItem')
def crear_tipoItem(request, id_fase):
    '''
    vista para crear un tipo, que consta de un nombre y una lista de permisos
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


def listar_tiposItem(request,id_fase):
    '''
    vista para listar las fases pertenecientes a un proyecto
    '''

    tiposItem = TipoItem.objects.filter(fase_id=id_fase).order_by('nombre')
    fase = Fase.objects.get(id=id_fase)
    return render_to_response('tiposDeItem/listar_tipoDeItem.html', {'datos': tiposItem, 'fase' : fase}, context_instance=RequestContext(request))



def detalle_tipoItem(request, id_tipoItem):

    '''
    vista para ver los detalles del tipo de item <id_tipoItem>
    '''

    dato = get_object_or_404(TipoItem, pk=id_tipoItem)
    atributos = Atributo.objects.filter(tipoItem__id=id_tipoItem)
    return render_to_response('tiposDeItem/detalle_tipoDeItem.html', {'datos': dato, 'atributos': atributos}, context_instance=RequestContext(request))


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
            atributo= Atributo(nombre = request.POST["nombre"], tipo = request.POST["tipo"], valorDefecto = request.POST["valorDefecto"])
            atributo.save()
            atributo.tipoItem=tipoItem
            atributo.save()
            tipoItem2 = TipoItem.objects.get(id=id_tipoItem)
            id_fase = tipoItem2.fase_id
            return render_to_response('tiposDeItem/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
    else:
        # formulario inicial
        atributo_form = AtributoForm()
    return render_to_response('tiposDeItem/crear_atributo.html', { 'atributo_form': atributo_form}, context_instance=RequestContext(request))


def eliminar_atributo(request, id_atributo, id_tipoItem):

    '''
    vista para eliminar el atributo <id_atributo>.
    '''

    atributo = get_object_or_404(Atributo, pk=id_atributo)
    tipoItem = get_object_or_404(TipoItem, pk=id_tipoItem)
    fase = tipoItem.fase
    tipoItem.atributo_set.remove(atributo)
    if(atributo.tipoItem.count() == 0):
        atributo.delete()

    messages.add_message(request, settings.DELETE_MESSAGE, "Atributo eliminado")
    tiposItem = TipoItem.objects.filter(fase_id=fase.id).order_by('nombre')
    return render_to_response('tiposDeItem/listar_tipoDeItem.html', {'datos': tiposItem, 'fase' : fase}, context_instance=RequestContext(request))



def editar_TipoItem(request,id_tipoItem):
    '''
    vista para cambiar el nombre del rol o su lista de permisos.
    '''
    tipoItem= TipoItem.objects.get(id=id_tipoItem)
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
    return render_to_response('tiposDeItem/editar_tipoItem.html', { 'tipoItem': tipoItem_form, 'dato':tipoItem, 'id_fase':id_fase}, context_instance=RequestContext(request))


def importar_tipoItem(request, id_tipoItem):
    '''
    Vista para importar un tipo de Item, dado en <id_tipoItem>
    '''
    tipoItem=TipoItem.objects.get(id=id_tipoItem)
    if request.method=='POST':
        formulario = TipoItemForm(request.POST, initial={'nombre':tipoItem.nombre,'descripcion':tipoItem.descripcion} )

        if formulario.is_valid():
                tipo = formulario.save()
                tipo.fase_id= tipoItem.fase_id

                for atributo in tipoItem.atributo_set.all():
                    tipo.atributo_set.add(atributo)
                tipo.save()
#                tipo = formulario.save()
 #               for atributo in tipoItem.atributo_set.all():
  #                  tipo.atributo_set.add(atributo)
   #             tipo.id_fase= tipoItem.fase_id
    #            tipo.save()
                return render_to_response('tiposDeItem/creacion_correcta.html',{'id_fase':tipoItem.fase_id}, context_instance=RequestContext(request))
    else:
        formulario = TipoItemForm(initial={'nombre':tipoItem.nombre,'descripcion':tipoItem.descripcion} )
    return render_to_response('tiposDeItem/crear_tipoDeItem.html', { 'tipoItem_form': formulario}, context_instance=RequestContext(request))

