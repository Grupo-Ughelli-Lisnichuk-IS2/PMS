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

        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        c = Client()
        c.login(username='john', password='johnpassword')
        resp = c.get('/roles/')
        self.assertEqual(resp.status_code, 200)


