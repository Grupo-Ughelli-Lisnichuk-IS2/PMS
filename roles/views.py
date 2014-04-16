from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse, HttpResponseRedirect, request
from django.template import RequestContext
from roles.forms import GroupForm
from django.shortcuts import render_to_response
from django.db.models import Q
# Create your views here.
def crear_rol(request):

    if request.method == 'POST':
        # formulario enviado
        group_form = GroupForm(request.POST)

        if group_form.is_valid():
            # formulario validado correctamente
            group_form.save()
            return HttpResponseRedirect('/register/success/')

    else:
        # formulario inicial
        group_form = GroupForm()
    return render_to_response('roles/crear_rol.html', { 'group_form': group_form}, context_instance=RequestContext(request))


def lista_roles(request):
    '''
    vista para listar los usuarios del sistema
    '''

    grupos = Group.objects.all()
    return render_to_response('roles/listar_roles.html', {'datos': grupos}, context_instance=RequestContext(request))
def buscarRol(request):
    '''
    vista para buscar los usuarios del sistema
    '''
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(name=query)
        )
        results = Group.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('roles/listar_roles.html', {'datos': results}, context_instance=RequestContext(request))

def detalle_rol(request, id_rol):

    '''
    vista para ver los detalles del usuario <id_user> del sistema
    '''

    dato = get_object_or_404(Group, pk=id_rol)
    permisos = Permission.objects.filter(group__id=id_rol)
    return render_to_response('roles/detalle_rol.html', {'rol': dato, 'permisos': permisos}, context_instance=RequestContext(request))


def eliminar_rol(request, id_rol):

    '''
    vista para ver los detalles del usuario <id_user> del sistema
    '''

    dato = get_object_or_404(Group, pk=id_rol)
    #permisos = Permission.objects.filter(group__id=id_rol)

    #permisos.delete()


    #for permiso in permisos:
     #   permiso.d
    dato.delete()
    grupos = Group.objects.all()
    return render_to_response('roles/listar_roles.html', {'datos': grupos}, context_instance=RequestContext(request))

def editar_rol(request,id_rol):
    rol= Group.objects.get(id=id_rol)
    if request.method == 'POST':
        # formulario enviado
        rol_form = GroupForm(request.POST, instance=rol)

        if rol_form.is_valid():
            # formulario validado correctamente
            rol_form.save()
            return HttpResponseRedirect('/register/success/')

    else:
        # formulario inicial
        rol_form = GroupForm(instance=rol)
    return render_to_response('roles/editar_rol.html', { 'rol': rol_form}, context_instance=RequestContext(request))


