import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import Group, User


class PMSTestCase(TestCase):

    fixtures = ["tipoItem_testmaker"]

    def test_crear_tipoItem(self):
        '''
        Test para la creacion de un rol
        '''
        c = Client()
        c.login(username='admin', password='admin1')

        #creacion correcta del rol, redirige a la pagina correspondiente
        resp = c.post('/tiposDeItem/registrar/1',{'nombre':"Tipo 1", 'descripcion':"prueba de crear_tipoItem"},follow=True)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.context['nombre'].pk, "Tipo 1")

        #creacion incorrecta: nombre repetido, no redirige
        resp = c.post('/tiposDeItem/registrar/1',{'name':"Tipo 1"})
        self.assertEqual(resp.status_code,200)

