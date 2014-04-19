from django.contrib.auth.models import User
from django.test import TestCase, Client

from proyectos.models import Proyecto
from usuarios.tests import PMSTestCase
# Create your tests here.
class PMSTestCase(TestCase):

    fixtures = ["proyectos_testmaker"]


    def test_buscar_usuarios(self):
        #User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        c = Client()
        c.login(username='admin', password='admin')
       # proyecto= Proyecto.objects.create(id=2, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        resp = c.get('/proyectos/search/?q=PMS')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([proyecto.nombre for proyecto in resp.context['datos']], ['PMS'])

    def test_detalle_proyectos(self):
        '''
        Test para visualizar los detalles de un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        #proyecto= Proyecto.objects.create(id=4, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        resp = c.get('/proyectos/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['proyecto'].pk, 1)
        self.assertEqual(resp.context['proyecto'].nombre, 'PMS')
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
