from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.
from django.template import RequestContext
from fases.models import Fase
from tiposDeItem.formsTiposDeItem import TipoItemForm, AtributoForm
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
    return render_to_response('tiposDeItem/detalle_tipoDeItem.html', {'datos': dato}, context_instance=RequestContext(request))


def crear_atributo(request, id_tipoItem):
    '''
    vista para crear un tipo de atributo, que consta de un nombre, un tipo, un valor por defecto
    y esta relacionado con un tipo de Item
    '''

    if request.method == 'POST':
        # formulario enviado
        atributo_form = AtributoForm(request.POST)

        if atributo_form.is_valid():
            tipoItem = TipoItem.objects.get(id=id_tipoItem)
            atributo= Atributo(nombre = request.POST["nombre"], tipo = request.POST["tipo"], valorDefecto = request.POST["valorDefecto"], tipoItem = tipoItem)
            atributo.save()
            id_fase = tipoItem.fase_id
            return render_to_response('tiposDeItem/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
    else:
        # formulario inicial
        atributo_form = AtributoForm()
    return render_to_response('tiposDeItem/crear_atributo.html', { 'atributo_form': atributo_form}, context_instance=RequestContext(request))
