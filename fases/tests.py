from django.test import TestCase, Client
from usuarios.tests import PMSTestCase
from fases.models import Fase
from proyectos.models import Proyecto
from django.contrib.auth.models import User


class PMSTestCase(TestCase):

    fixtures = ["proyectos_testmaker"]

    def test_listar_fases(self):
        '''
         Test para ver si lista correctamente un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        resp = c.get('/fases/proyecto/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([fase.pk for fase in resp.context['datos']], [4, 3, 2, 1])


    def test_fases_sistema(self):
        '''
         Test para ver si lista correctamente un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        resp = c.get('/fases/sistema/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([fase.pk for fase in resp.context['datos']], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

    def test_crear_fase(self):
        proyecto=Proyecto.objects.get(id=1)
        fase= Fase.objects.create(id=16, nombre='pruebaFase',descripcion='prueba', maxItems=1,fInicio='2012-12-01',orden =1, proyecto=proyecto)
        self.assertEqual(fase.nombre,'pruebaFase')


    def test_detalle_fases(self):
        '''
        Test para visualizar los detalles de una fase
        '''

        proyecto=Proyecto.objects.get(id=6)
        fase=Fase.objects.get(id=15)
        resp = self.client.get('/fases/15')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['datos'].pk, 15)
        self.assertEqual(resp.context['datos'].nombre, 'Pruebas')



    def test_modficar_proyecto(self):
        '''
         Test para ver si modifica correctamente una fase
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #test para verificar que si no modifica nada, no guarda
        resp = c.post('/fases/modificar/1')
        self.assertEqual(resp.status_code, 200)

        resp = c.post('/fases/modificar/1',{'descripcion':'hola','maxItems':'2','fInicio':'12/12/2000'})
        self.assertEqual(resp.status_code, 200)


