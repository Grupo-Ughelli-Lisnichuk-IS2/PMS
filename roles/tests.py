import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import Group, User
class PMSTestCase(TestCase):

    fixtures = ["fases_testmaker"]

    def test_crear_rol(self):
        '''
        Test para la creacion de un rol
        '''
        c = Client()
        c.login(username='admin', password='admin1')

        #creacion correcta del rol, redirige a la pagina correspondiente
        resp = c.post('/roles/crear/',{'name':"Rol 1"},follow=True)
        self.assertEqual(resp.status_code,200)
 #       self.assertRedirects(resp, 'http://testserver/roles/register/success/')

        #creacion incorrecta: nombre repetido, no redirige
        resp = c.post('/roles/crear/',{'name':"Rol 1"})
        self.assertEqual(resp.status_code,200)


    def test_listar_roles(self):
        '''
         Test para crear un rol y ver si lo lista correctamente
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/roles/')
        self.assertEqual(resp.status_code, 200)

    def test_detalle(self):
        '''
         Test para crear un rol y ver si lo lista correctamente
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_rol()
        #ver detalle de un rol existente
        resp = c.get('/roles/3')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['rol'].pk, 3)
        self.assertEqual(resp.context['rol'].name, 'Analista de la Fase 1')
        #ver detalle de un rol inexistente
        resp = c.get('/roles/100')
        self.assertEqual(resp.status_code, 404)

    def test_eliminar(self):
        '''
         Test para crear un rol y ver si lo lista correctamente
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_rol()
        #eliminacion de un rol existente
        resp = c.get('/roles/eliminar/4')
        self.assertEqual(resp.status_code, 200)

        #eliminacion de un rol inexistente, (ya se borro)
        resp = c.get('/roles/eliminar/19')
        self.assertEqual(resp.status_code, 404)


    def test_modificar_rol(self):
        '''
        Test para la modificacion de un rol
        '''
        c = Client()
        c.login(username='admin', password='admin1')

        #modificacion correcta del rol, redirige a la pagina correspondiente
        resp = c.post('/roles/crear/',{'name':"Rol 1"})
        resp = c.post('/roles/modificar/5',{'name':"Rol 4"},follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, 'http://testserver/roles/register/success/')
        #modificacion incorrecta, no redirige, ya que el nombre de la fase ya existe
        resp = c.post('/roles/crear/',{'name':"Rol 1"})
        resp = c.post('/roles/modificar/5',{'name':"Rol 1"})
        self.assertEqual(resp.status_code, 200)


    def test_buscar_roles(self):
        '''
        Test para buscar un rol
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        #Test para  buscar rol existente
        resp = c.post('/roles/crear/',{'name':"Rol1"})
        resp = c.get('/roles/search/?q=Rol1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([proyecto.name for proyecto in resp.context['datos']], ['Rol1'])

        #test para buscar un rol inexistente,no encuentra ningun rol
        resp = c.get('/roles/search/?q=noexiste')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([proyecto.name for proyecto in resp.context['datos']], [])