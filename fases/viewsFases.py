from django.shortcuts import render
from fases.models import Fase
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from fases.formsFases import FaseForm


# Create your views here.

def registrar_fase(request):
    if request.method=='POST':
        formulario = FaseForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/principal')
    else:
        formulario = FaseForm()
    return render_to_response('fases/registrarFase.html',{'formulario':formulario}, context_instance=RequestContext(request))


def listar_fases(request):
    '''
    vista para listar las fases del sistema
    '''

    fases = Fase.objects.all()
    return render_to_response('fases/listar_fases.html', {'datos': fases}, context_instance=RequestContext(request))



def detalle_fase(request, id_fase):

    '''
    vista para ver los detalles del usuario <id_user> del sistema
    '''

    dato = get_object_or_404(Fase, pk=id_fase)
    return render_to_response('fases/detalle_fase.html', {'datos': dato}, context_instance=RequestContext(request))