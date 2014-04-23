from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from fases.models import Fase
from tiposDeItem.formsTiposDeItem import TipoItemForm
from tiposDeItem.models import TipoItem


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
