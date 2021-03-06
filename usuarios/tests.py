import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
class PMSTestCase(TestCase):

    fixtures = ["usuarios_testmaker"]

    def test_crear_usuario(self):
        '''
        Test para la creacion de un usuario con contrasenha
        '''
        u = User.objects.create_user('testuser', 'test@example.com', 'testpw')

        self.assertTrue(u.has_usable_password())
        self.assertFalse(u.check_password('bad'))
        self.assertTrue(u.check_password('testpw'))

        # Test para contrasenha incorrecta
        u.set_unusable_password()
        u.save()
        self.assertFalse(u.check_password('testpw'))
        self.assertFalse(u.has_usable_password())
        u.set_password('testpw')
        self.assertTrue(u.check_password('testpw'))
        u.set_password(None)
        self.assertFalse(u.has_usable_password())

        # Test para identificar permisos
        self.assertTrue(u.is_authenticated())
        self.assertFalse(u.is_staff)
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_superuser)

        # Test para creacion sin password
        u2 = User.objects.create_user('testuser2', 'test2@example.com')
        self.assertFalse(u2.has_usable_password())

    def test_inicio(self):
        '''Test para ver si puede entrar a la pagina de inicio'''
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def login(self, password='testpw'):
        '''
        Test para el login
        '''
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': password,
            })
        self.assertTrue(SESSION_KEY in self.client.session)
        return response

    def test_listar_usuarios(self):
        '''
         Test para crear un usuario y ver si lo lista correctamente
        '''

        usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/usuarios/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('datos' in resp.context)
        self.assertEqual([usu.pk for usu in resp.context['datos']], [2,3,4,1])
        usuario1 = resp.context['datos'][2]
        self.assertEqual(usuario1.username, 'testuser')
        self.assertEqual(usuario1.email, 'test@example.com')

    def test_detalle_usuarios(self):
        '''
        Test para visualizar los detalles de un usuario
        '''
        usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/usuarios/1?')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['usuario'].pk, 1)
        self.assertEqual(resp.context['usuario'].username, 'admin')

    def test_modificar_usuarios(self):
        '''
        Test para cambiar el estado de un usuario
        '''
        usuario2 = User.objects.create_user('testuser33', 'test@example.com', 'testpw')

        c = Client()
        c.login(username='testuser33', password='testpw')
        resp = self.client.post('/usuarios/modificar/6?')
        self.assertEqual(resp.status_code, 302)


    def test_buscar_usuarios(self):
      usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
      c = Client()
      c.login(username='admin', password='admin1')
      resp = c.get('/usuarios/search/?q=testuser')
      self.assertEqual(resp.status_code, 200)
      self.assertEqual([usuario.username for user in resp.context['datos']], ['testuser'])

    def logout(self):
        '''
        Test para el logout
        '''
        usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        c = Client()
        c.login(username='tesuser', password='testpw')
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)

