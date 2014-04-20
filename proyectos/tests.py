from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client

from proyectos.models import Proyecto
from usuarios.tests import PMSTestCase
# Create your tests here.
class PMSTestCase(TestCase):

    fixtures = ["proyectos_testmaker"]


    def test_buscar_proyectos(self):
        '''
        Test para buscar un proyecto
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #Test para proyecto buscar existente
        resp = c.get('/proyectos/search/?q=PMS')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([proyecto.nombre for proyecto in resp.context['datos']], ['PMS'])


    def test_detalle_proyectos(self):
        '''
        Test para visualizar los detalles de un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')

        #Test para proyecto existente
        resp = c.get('/proyectos/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['proyecto'].pk, 1)
        self.assertEqual(resp.context['proyecto'].nombre, 'PMS')

        #Test para proyecto inexistente
        resp = c.get('/proyectos/1000')
        self.assertEqual(resp.status_code, 404)

    def test_listar_proyectos(self):
        '''
         Test para ver si lista correctamente un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        #proyecto= Proyecto.objects.create(id=3, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        resp = c.get('/proyectos/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([proyecto.pk for proyecto in resp.context['datos']], [3,4,5,6,7])

    def test_ver_equipo(self):
        '''
         Test para ver si lista correctamente los usuarios asociados a un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')

        resp = c.get('/proyectos/equipo/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([lider.pk for lider in resp.context['comite']], [10,19,1])

    def test_modficar_proyecto(self):
        '''
         Test para ver si modifica correctamente un proyecto
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #test para verificar que si no modifica nada, no guarda
        resp = c.post('/proyectos/modificar/1')
        self.assertEqual(resp.status_code, 200)

    def test_modficar_estado(self):
        '''
         Test para ver si modifica correctamente un proyecto
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #si cambia el estado se redirige a la pagina de confirmacion
        resp = c.post('/proyectos/cambiarEstado/1',{'estado':'ACT'},follow=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, 'http://testserver/proyectos/register/success/')

    def test_importar(self):
        '''
         Test para ver si importa correctamente un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        #prueba importar un proyecto y asignarle como nombre un nombre ya existente. Retorna un mensaje de nivel 20,
        #informando que ya existe un proyecto con ese nombre
        resp = c.post('/proyectos/importar/1',{'nombre':'PMS'})

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['messages'].level, 20)

    def test_registrar(self):
        '''
         Test para ver si crea correctamente un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        #prueba importar un proyecto y asignarle como nombre un nombre ya existente. Retorna un mensaje de nivel 20,
        #informando que ya existe un proyecto con ese nombre
        resp = c.post('/proyectos/registrar/',{'nombre':'PMS'})

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['messages'].level, 20)

        #registra correctamente y redirige a la pagina indicada
        resp = c.post('/proyectos/registrar/',{'nombre':'Proyecto nuevo', 'descripcion':'ds','observaciones':'sdasd','fecha_ini':'20/02/2014','fecha_fin':'20/02/2015','lider':1,'comite':1},follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, 'http://testserver/proyectos/register/success/')

        #no registra correctamente ya que la fecha de inicio es despues de la de fin
        resp = c.post('/proyectos/registrar/',{'nombre':'Proyecto nuevo 2', 'descripcion':'ds','observaciones':'sdasd','fecha_ini':'20/02/2015','fecha_fin':'20/02/2014','lider':1,'comite':1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['messages'].level, 20)
