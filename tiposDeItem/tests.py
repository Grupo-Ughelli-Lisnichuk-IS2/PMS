import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import Group, User


class PMSTestCase(TestCase):

    fixtures = ["tipoItem_testmaker"]

    def test_crear_tipoItem(self):
        '''
        Test para la creacion de un tipo de item
        '''
        c = Client()
        c.login(username='admin', password='admin1')

        #creacion correcta del Tipo de item, ya puede visualizarse sus detalles
        resp = c.post('/tiposDeItem/registrar/1',{'nombre':"Tipo 1", 'descripcion':"prueba de crear_tipoItem"},follow=True)
        self.assertEqual(resp.status_code,200)
        resp = c.get('/tiposDeItem/7')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['datos'].nombre, "Tipo 1")



    def test_listar_tiposItem(self):
        '''
         Test para ver si lista correctamente los tipos de Item de una fase
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/tiposDeItem/fase/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([tipoItem.pk for tipoItem in resp.context['datos']], [3, 4, 5])



    def test_detalle(self):
        '''
         Test para comprobar que se despliega correctamente la lista de tipos de item de una fase
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_tipoItem()
        #ver detalle de un tipo de item existente
        resp = c.get('/tiposDeItem/7')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['datos'].pk, 7)
        self.assertEqual(resp.context['datos'].nombre, 'Tipo 1')
        #ver detalle de un tipo de Item inexistente
        resp = c.get('/tiposDeItem/100')
        self.assertEqual(resp.status_code, 404)





    def test_crear_atributo(self):
        '''
        Test de la creacion un atributo dentro de un tipo de item
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_tipoItem()

        #creacion correcta del Tipo de item, ya puede visualizarse sus detalles
        resp = c.post('/tiposDeItem/7/crear_atributo',{'nombre':"atributo 1", 'tipo':"TEX", 'valorDefecto':"1"},follow=True)
        self.assertEqual(resp.status_code,200)
        resp = c.get('/tiposDeItem/7')
        self.assertEqual([atributo.nombre for atributo in resp.context['atributos']], ["atributo 1"])


    def test_eliminar_atributo(self):
        '''
         Test para eliminar un tipo de atributo
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_atributo()
        #eliminacion de un rol existente
        resp = c.get('/tiposDeItem/eliminar/tipo_atributo/6-7')
        self.assertEqual(resp.status_code, 302)

        #eliminacion de un atributo inexistente,
        resp = c.get('/tiposDeItem/eliminar/tipo_atributo/7-6')
        self.assertEqual(resp.status_code, 404)



    def test_editar_tipoItem(self):
        '''
        Test para la modificacion de un tipo de item
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_atributo()

        #modificacion correcta del tipo de item

        resp = c.post('/tiposDeItem/modificar/7',{'nombre':"Tipo nuevo"},follow=True)
        self.assertEqual(resp.status_code, 200)

        #modificacion incorrecta, no redirige, ya que el nombre del tipo de item ya existe
        resp = c.post('/tiposDeItem/registrar/1',{'nombre':"Tipo 1", 'descripcion':"prueba de crear_tipoItem"},follow=True)
        resp = c.post('/tiposDeItem/modificar/7',{'name':"Tipo 1"})
        self.assertEqual(resp.status_code, 200)


    def test_importar(self):
        '''
         Test para ver si se importa correctamente un tipo de item dentro de una fase
        '''

        c = Client()
        c.login(username='admin', password='admin1')

        #prueba importar un tipo de item y asignarle como nombre un nombre ya existente. Retorna un mensaje de nivel 20,
        #informando que ya existe un tipo de item con ese nombre
        resp = c.post('/tiposDeItem/importar/3-3',{'nombre':'tipo 1'})

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['messages'].level, 20)





    def test_eliminar(self):
        '''
         Test para eliminar un tipo de item.
        '''

        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_tipoItem()

        #eliminacion de un rol existente
        resp = c.get('/tiposDeItem/eliminar/7')
        self.assertEqual(resp.status_code, 200)

        #eliminacion de un rol inexistente, (ya se borro)
        resp = c.get('/tiposDeItem/eliminar/20')
        self.assertEqual(resp.status_code, 404)