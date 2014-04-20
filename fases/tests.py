from django.test import TestCase, Client
from usuarios.tests import PMSTestCase
from fases.models import Fase
from proyectos.models import Proyecto
from django.contrib.auth.models import User


class PMSTestCase(TestCase):

    fixtures = ["fases_testmaker"]

    def test_listar_fases(self):
        '''
         Test para ver si lista correctamente las fases de un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/fases/proyecto/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([fase.pk for fase in resp.context['datos']], [1, 2])


    def test_fases_sistema(self):
        '''
         Test para ver si lista correctamente las fases del sistema
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/fases/sistema/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([fase.pk for fase in resp.context['datos']], [1, 2, 3])

    def test_crear_fase(self):
        proyecto=Proyecto.objects.get(id=1)
        fase= Fase.objects.create(id=16, nombre='pruebaFase',descripcion='prueba', maxItems=1,fInicio='2012-12-01',orden =1, proyecto=proyecto)
        self.assertEqual(fase.nombre,'pruebaFase')


    def test_detalle_fases(self):
        '''
        Test para visualizar los detalles de una fase
        '''

        proyecto=Proyecto.objects.get(id=1)
        fase=Fase.objects.get(id=1)
        resp = self.client.get('/fases/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['datos'].pk, 1)
        self.assertEqual(resp.context['datos'].nombre, 'Fase 1')



    def test_modficar_proyecto(self):
        '''
         Test para ver si modifica correctamente una fase
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        #test para verificar que si no modifica nada, no guarda
        resp = c.post('/fases/modificar/1')
        self.assertEqual(resp.status_code, 200)

        resp = c.post('/fases/modificar/1',{'descripcion':'hola','maxItems':'2','fInicio':'12/12/2000'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['messages'].level, 20)

        resp = c.post('/fases/modificar/1',{'descripcion':'hola','maxItems':'2','fInicio':'02/01/2012'})
        self.assertEqual(resp.status_code, 200)



    def test_importar(self):
        '''
         Test para ver si importa correctamente una fase
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        #prueba importar una fase y asignarle como nombre un nombre ya existente. Retorna un mensaje de nivel 20,
        #informando que ya existe una fase con ese nombre
        resp = c.post('http://127.0.0.1:8000/fases/importar/1-1',{'nombre':'Fase 1'})

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['messages'].level, 20)


    def test_asignar_usuario(self):
        '''
         Test para ver si se listan correctamente los usuarios para asociarlos a una fase
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/fases/asignar/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([usuario.pk for usuario in resp.context['datos']], [2, 3, 1])

    def test_asignar_rol(self):
        '''
         Test para ver si se listan correctamente los roles asociados a una fase
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/fases/asignar/3/3')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([rol.pk for rol in resp.context['roles']], [8])
        self.assertEqual(resp.context['usuario'].first_name, "Yohanna")


    def test_asociar(self):
        '''
         Test para ver si se asocia correctamente un rol perteneciente a una fase a un usuario
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/fases/asociar/8-3-3')
        resp = c.get('/proyectos/equipo/2')
        self.assertEqual(resp.context['usuarios'][1], u'Yohanna Lisnichuk  -  Analista de la Fase 3 en la fase   Fase 1 del proyecto 2\n')


    def test_des(self):
        '''
        Test para comprobar que se lista correctamente a los usuario de una fase, para poder desasociarlos
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/fases/des/3')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([usuario.pk for usuario in resp.context['datos']], [2])


    def test_desasignar(self):
        '''
        Test para comprobar que un rol ha sido removido satisfactoriamente de un usuario
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/fases/desasignar/2/3')
        resp = c.get('/fases/des/3')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([usuario.pk for usuario in resp.context['datos']], [])


