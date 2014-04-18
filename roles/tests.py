import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import Group, User
class PMSTestCase(TestCase):

    def test_crear_rol(self):
        '''
        Test para la creacion de un usuario con contrasenha
        '''
        u = Group.objects.create()

    def test_listar_roles(self):
        '''
         Test para crear un usuario y ver si lo lista correctamente
        '''
        def login(self, password='testpw'):
            response = self.client.post('/login/', {
            'username': 'testuser',
            'password': password,
            })
            self.assertTrue(SESSION_KEY in self.client.session)
            return response
        usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        self.login('testpw')
        resp = self.client.get('/roles/')
        self.assertEqual(resp.status_code, 200)
    def login(self, password='testpw'):
            response = self.client.post('/login/', {
            'username': 'testuser',
            'password': password,
            })
            self.assertTrue(SESSION_KEY in self.client.session)
            return response

