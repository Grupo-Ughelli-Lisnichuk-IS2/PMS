from django.shortcuts import render
from django.views.generic import TemplateView
from proyectos.formsProyectos import ProyectoForm, CambiarEstadoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from proyectos.models import Proyecto
from fases.models import Fase
from django.contrib.auth.models import User
from django.db.models import Q
def registrar_proyecto(request):
    '''
    Vista para registrar un nuevo proyecto con su lider
    '''
    if request.method=='POST':
        formulario = ProyectoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/proyecto/register/success')
    else:
        formulario = ProyectoForm()
    return render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request))

class RegisterSuccessView(TemplateView):
    template_name = 'proyectos/creacion_correcta.html'


def RegisterFailedView(request, id_proyecto):
    return render_to_response('proyectos/cambio_estado_fallido.html', {'dato': id_proyecto}, context_instance=RequestContext(request))

def detalle_proyecto(request, id_proyecto):

    '''
    vista para ver los detalles del proyecto <id_proyecto> del sistema, junto con su lider y los miembros del comite
    '''

    dato = get_object_or_404(Proyecto, pk=id_proyecto)
    comite = User.objects.filter(comite__id=id_proyecto)
    lider = get_object_or_404(User, pk=dato.lider_id)
    return render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato, 'comite': comite, 'lider':lider}, context_instance=RequestContext(request))



def listar_proyectos(request):
    '''
    vista para listar los proyectos del sistema del sistema junto con el nombre de su lider
    '''

    proyectos = Proyecto.objects.all()

    return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos}, context_instance=RequestContext(request))

def buscar_proyecto(request):
    '''
    vista para buscar los proyectos del sistema
    '''
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nombre=query)
        )
        results = Proyecto.objects.filter(qset).distinct()

    else:
        results = []


    return render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))

def editar_proyecto(request,id_proyecto):
    proyecto= Proyecto.objects.get(id=id_proyecto)
    nombre= proyecto.nombre
    if request.method == 'POST':
        # formulario enviado
        proyecto_form = ProyectoForm(request.POST, instance=proyecto)
        if proyecto_form.is_valid():
            # formulario validado correctamente
            proyecto_form.save()
            return HttpResponseRedirect('/proyectos/register/success/')
    else:
        # formulario inicial
        proyecto_form = ProyectoForm(instance=proyecto)
    return render_to_response('proyectos/editar_proyecto.html', { 'proyecto': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))

def cambiar_estado_proyecto(request,id_proyecto):
    proyecto= Proyecto.objects.get(id=id_proyecto)
    nombre= proyecto.nombre
    comite = User.objects.filter(comite__id=id_proyecto)


    if request.method == 'POST':
        proyecto_form = CambiarEstadoForm(request.POST, instance=proyecto)
        if proyecto_form.is_valid():
                    if proyecto_form.cleaned_data['estado']=='ACT':
                        cantidad = 0
                        for miembros in comite:
                            cantidad+=1
                        if cantidad%2==0:
                            return render_to_response('proyectos/cambio_estado_fallido.html', { 'dato': id_proyecto}, context_instance=RequestContext(request))
                        if cantidad<3:
                            return render_to_response('proyectos/cambio_estado_fallido.html', { 'dato': id_proyecto}, context_instance=RequestContext(request))
                       # fases=Fase.objects.filter(proyecto_id=id_proyecto)
                        #for fase in fases:
                         #   fase.estado='EJE'
                          #  fase.save()
                        # formulario validado correctamente
                        proyecto_form.save()
                        return HttpResponseRedirect('/proyectos/register/success/')
                    else:
                            if proyecto_form.cleaned_data['estado']=='ANU':
                                proyecto_form.save()
                                return HttpResponseRedirect('/proyectos/register/success/')

    else:
        # formulario inicial
        proyecto_form = CambiarEstadoForm(instance=proyecto)
        return render_to_response('proyectos/cambiar_estado_proyecto.html', { 'proyecto': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))