from django.shortcuts import render
from fases.models import Fase
from proyectos.models import Proyecto
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from fases.formsFases import FaseForm, ModificarFaseForm


# Create your views here.

def registrar_fase(request, id_proyecto):
    if request.method=='POST':
        formulario = FaseForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/principal')
    else:
        formulario = FaseForm(initial={'proyecto_id': id_proyecto})
    return render_to_response('fases/registrarFase.html',{'formulario':formulario}, context_instance=RequestContext(request))


def listar_fases(request, id_proyecto):
    '''
    vista para listar las fases del sistema
    '''
    fases = Fase.objects.filter(proyecto_id=id_proyecto)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    return render_to_response('fases/listar_fases.html', {'datos': fases, 'proyecto':proyecto}, context_instance=RequestContext(request))



def detalle_fase(request, id_fase):

    '''
    vista para ver los detalles del usuario <id_user> del sistema
    '''

    dato = get_object_or_404(Fase, pk=id_fase)
    return render_to_response('fases/detalle_fase.html', {'datos': dato}, context_instance=RequestContext(request))


def editar_fase(request,id_fase):
    fase= Fase.objects.get(id=id_fase)
    if request.method == 'POST':
        # formulario enviado
        fase_form = ModificarFaseForm(request.POST, instance=fase)

        if fase_form.is_valid():
            # formulario validado correctamente
            fase_form.save()
            return HttpResponseRedirect('/register/success/')
    else:
        # formulario inicial
        fase_form = ModificarFaseForm(instance=fase)
    return render_to_response('fases/editar_fase.html', { 'form': fase_form, 'fase': fase}, context_instance=RequestContext(request))


def fases_sistema(request,id_proyecto):
    '''
    vista para listar las fases del sistema
    '''

    fases = Fase.objects.all()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    return render_to_response('fases/fases_sistema.html', {'datos': fases, 'proyecto':proyecto}, context_instance=RequestContext(request))

def importar_fase(request, id_fase):
    fase= Fase.objects.get(id=id_fase)
    if request.method=='POST':
        formulario = FaseForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/principal')
    else:
        formulario = FaseForm(initial={'nombre':fase.nombre, 'descripcion':fase.descripcion, 'maxItems':fase.maxItems, 'fInicio':fase.fInicio})
    return render_to_response('fases/registrarFase.html',{'formulario':formulario}, context_instance=RequestContext(request))
