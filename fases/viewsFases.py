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

