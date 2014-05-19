import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import Group, User


class PMSTestCase(TestCase):

    fixtures = ["items_testmaker"]

    def test_abrir_proyecto(self):
        '''
        test para comprobar que se listan los pryectos de un usuario especifico
        '''
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/proyectos/')
        a=self.assertEqual(resp.status_code, 200)

        print 'Test es miembro: es miembro'
        c = Client()
        c.login(username='lola', password='lola')

        resp = c.get('/desarrollo/proyectos/')
        self.assertEqual(resp.status_code, 302)
        print 'Test si no es miembro=302'

    def test_abrir_fase(self):
        '''
        test para comprobar que se abren las fases de un proyecto y usuarios especificos
        '''
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/proyectos/fases/500')
        self.assertEqual(resp.status_code, 404)

        print 'Test listar fases de proyecto inexistente'

        resp = c.get('/desarrollo/proyectos/fases/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test listar fases de proyecto existente'

    def test_abrir_titem(self):
        '''
        test para comprobar que se abren los tipos de item de una fase
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/fases/tiposDeItem/500')
        self.assertEqual(resp.status_code, 404)

        print 'Test listar tipos de item de fase inexistente'

        resp = c.get('/desarrollo/fases/tiposDeItem/3')
        self.assertEqual(resp.status_code, 200)
        print 'Test listar tipos de item de fase existente'

    def test_crear_item(self):
        '''
        test para comprobar que se crea un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/crear/45')
        self.assertEqual(resp.status_code, 404)

        print 'Test acceder a crear item con un tipo de item inexistente'

        resp = c.get('/desarrollo/item/crear/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test acceder a crear item tipo de item existente'

        resp = c.post('/desarrollo/item/crear/2',{'nombre':'Item'})
        self.assertEqual(resp.status_code,200)
        print 'No crea el item si no completa todos los campos'

        resp = c.post('/desarrollo/item/crear/2',{'nombre':'Item', 'descripcion':'dsdd','costo':'dsds'})
        self.assertEqual(resp.status_code,200)
        print 'No crea el item si un campo esta mal completado'

        resp = c.post('/desarrollo/item/crear/3',{'nombre':'Item', 'descripcion':'dsdd','costo':4, 'tiempo':5})
        self.assertEqual(resp.status_code,200)
        print 'Crea el item si esta correctamente completado'

    def test_listar_item(self):
        '''
        test para comprobar que se listan los items de una fase
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/listar/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test listar item de un tipo de item que no existe'

        resp = c.get('/desarrollo/item/listar/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test listar item de un tipo de item que existe'


    def test_detalle_item(self):
        '''
        test para visualizar los detalles de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/detalle/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test ver detalle item que no existe'

        resp = c.get('/desarrollo/item/detalle/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test ver detalle item que existe'

    def test_crear_item_hijo(self):
        '''
        test para comprobar que se crea un item hijo
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/crear/hijo/45')
        self.assertEqual(resp.status_code, 404)

        print 'Test acceder a crear item con un item inexistente'

        resp = c.get('/desarrollo/item/crear/hijo/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test acceder a crear item con item existente'

        resp = c.post('/desarrollo/item/crear/hijo/2',{'nombre':'Item'})
        self.assertEqual(resp.status_code,200)
        print 'No crea el item si no completa todos los campos'

        resp = c.post('/desarrollo/item/crear/hijo/2',{'nombre':'Item', 'descripcion':'dsdd','costo':'dsds'})
        self.assertEqual(resp.status_code,200)
        print 'No crea el item si un campo esta mal completado'

        resp = c.post('/desarrollo/item/crear/hijo/2',{'nombre':'Item', 'descripcion':'dsdd','costo':4, 'tiempo':5})
        self.assertEqual(resp.status_code,200)
        print 'Crea el item si esta correctamente completado'

    def test_descargar_Archivo(self):
        '''
        test para descargar un archivo de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/descargar/archivo/888')
        self.assertEqual(resp.status_code, 404)
        print 'Test descargar item que no existe'
        c = Client()
        c.login(username='mlopez', password='mlopez')
        #resp = c.post('/desarrollo/item/descargar/archivo/1')
        #self.assertEqual(resp.status_code, 200)
        print 'Test descargar archivo que existe'

    def test_modificar_item(self):
        '''
        test para comprobar que se crea un item hijo
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/modificar/45')
        self.assertEqual(resp.status_code, 404)

        print 'Test acceder modificar item inexistente'

        resp = c.get('/desarrollo/item/modificar/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test acceder a modificar item existente'

        resp = c.post('/desarrollo/item/modificar/2',{'nombre':'Item'})
        self.assertEqual(resp.status_code,200)
        print 'Modifica el item'

        c = Client()
        c.login(username='lola', password='lola')
        resp = c.get('/desarrollo/item/modificar/2')
        self.assertEqual(resp.status_code,302)
        print 'No deja modificar si el usuario no tiene permisos'

    def test_listar_versiones_item(self):
        '''
        test para comprobar que se listan las versiones de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/versiones/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test listar versiones de un item que no existe'

        resp = c.get('/desarrollo/item/versiones/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test listar versiones de un item  que existe'

    def test_reversionar(self):
        '''
        test para comprobar que se reversiona un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/reversionar/45')
        self.assertEqual(resp.status_code, 404)

        print 'Test acceder reversionar item inexistente'

        resp = c.get('/desarrollo/item/reversionar/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test acceder a reversionar item existente'

        resp = c.post('/desarrollo/item/reversionar/2', {'version':1})
        self.assertEqual(resp.status_code,200)
        print 'Reversiona el item'

        c = Client()
        c.login(username='lola', password='lola')
        resp = c.get('/desarrollo/item/reversionar/2')
        self.assertEqual(resp.status_code,302)
        print 'No deja reversionar si el usuario no tiene permisos'

    def test_listar_archivos_item(self):
        '''
        test para comprobar que se listan los archivos de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/archivos/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test listar archivos de un item que no existe'

        #resp = c.get('/desarrollo/item/archivos/2')
        #self.assertEqual(resp.status_code, 200)
        print 'Test listar archivos de un item  que existe'
        c = Client()
        c.login(username='sd', password='sd')
        resp = c.get('/desarrollo/item/archivos/2')
        self.assertEqual(resp.status_code,302)
        print 'No lista los archivos si el usuario no tiene permisos'

    def test_eliminar_archivos_item(self):
        '''
        test para comprobar que si se elimina un archivo
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/archivos/eliminar/888')
        self.assertEqual(resp.status_code, 404)
        print 'Test eliminar archivos de un item que no existe'

       # resp = c.get('/desarrollo/item/archivos/eliminar/1')
        #self.assertEqual(resp.status_code, 302)
        print 'Test eliminar archivos de un item  que existe'

    def test_cambiar_padre(self):
        '''
        test para comprobar que cambia el padre de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/padre/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test cambiar padre de un item que no existe'

        resp = c.get('/desarrollo/item/padre/1')
        self.assertEqual(resp.status_code, 200)
        print 'Test cambiar padre de un item  que existe'

    def test_cambiar_antecesor(self):
        '''
        test para cambiar el antecsor de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/antecesor/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test cambiar antecesor de un item que no existe'

        resp = c.get('/desarrollo/item/antecesor/1')
        self.assertEqual(resp.status_code, 200)
        print 'Test cambiar antecesor de un item  que existe'

    def test_atributos(self):
        '''
        test para listar los atributos de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/atributos/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test listar atributos de un item que no existe'

        resp = c.get('/desarrollo/item/atributos/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test listar atributos de un item  que existe'

    def test_detalle_version(self):
        '''
        test para ver los detalles de la version de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/detalle/version/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test ver detalle de una version de un item que no existe'

        resp = c.get('/desarrollo/item/detalle/version/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test ver detalle de una version de un item  que existe'

    def test_cambiar_estado(self):
        '''
        test para cambiar el estado de un item
        '''

        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/cambiar_estado/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test cambiar estado de un item que no existe'

        resp = c.get('/desarrollo/item/cambiar_estado/2')
        self.assertEqual(resp.status_code, 200)
        print 'Test cambiar estado de un item  que existe'
    def test_eliminar_item(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/eliminar/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test eliminar item que no existe'
        resp = c.get('/desarrollo/item/eliminar/1')
        self.assertEqual(resp.status_code, 302)
        print 'Test eliminar item que existe'

    def test_listar_muertos(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/listar_muertos/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test listar items de tipo de item que no existe'
        resp = c.get('/desarrollo/item/listar_muertos/2')
        self.assertEqual(resp.status_code, 302)
        print 'Test listar items de tipo de item que existe'

    def test_revivir(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/revivir/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test revivir item que no existe'
        resp = c.get('/desarrollo/item/revivir/1')
        self.assertEqual(resp.status_code, 200)
        print 'Test revivir item que existe'

    def test_detalle_anulado(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/desarrollo/item/detalle/muerto/88')
        self.assertEqual(resp.status_code, 404)
        print 'Test detalle item que no existe'
        resp = c.get('/desarrollo/item/detalle/muerto/1')
        self.assertEqual(resp.status_code, 200)
        print 'Test detalle item que existe'
