import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import Group, User
from items.models import Item


class PMSTestCase(TestCase):

    fixtures = ["lineaBase_testmaker"]
    def test_listar_proyectos(self):
        '''
        test para comprobar que se listan los pryectos de un usuario especifico
        '''
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/gestionDeCambios/lineasBase/proyectos/')
        a=self.assertEqual(resp.status_code, 200)

        print 'Test listar proyectos en gestion de cambios'
        c.login(username='admin', password='admin')
        resp = c.get('/gestionDeCambios/lineasBase/proyectos/')
        a=self.assertEqual(resp.status_code, 302)

        print 'Test listar proyectos en gestion de cambios, sin permisos'

    def test_listar_fases(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/gestionDeCambios/lineasBase/proyectos/fases/2')
        a=self.assertEqual(resp.status_code, 200)

        print 'Test listar fases de proyectos en gestion de cambios'
        resp = c.get('/gestionDeCambios/lineasBase/proyectos/fases/1')
        a=self.assertEqual(resp.status_code, 302)

        print 'Test listar fases de proyectos en gestion de cambios, sin permisos'

    def listar_lb(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/gestionDeCambios/lineasBase/listar/2')
        a=self.assertEqual(resp.status_code, 200)

        print 'Test lineas base'
        resp = c.get('/gestionDeCambios/lineasBase/listar/1')
        a=self.assertEqual(resp.status_code, 302)

        print 'Test listar lineas base de proyectos en gestion de cambios,sin permiso'

    def crear_lb(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/gestionDeCambios/lineasBase/crear/2')


        resp = c.post('/gestionDeCambios/lineasBase/crear/2', dict(nombre='lb', items=''))
        a=self.assertEqual(resp.status_code, 200)

        print 'Test crear lineas base'

    def detalle_lb(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/gestionDeCambios/lineasBase/detalle/1')
        a=self.assertEqual(resp.status_code, 200)
        #self.assertEqual(resp.context['datos'].pk, 2)
        print 'Test detalle lineas base'

    def test_finalizar_fase(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/gestionDeCambios/lineasBase/finalizar/fase/1')
        a=self.assertEqual(resp.status_code, 200)
        #self.assertEqual(resp.context['datos'].pk, 2)
        print 'Test finalizar fase'

    def test_reporte_lb(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/gestionDeCambios/lineasBase/reporte/1')
        a=self.assertEqual(resp.status_code,302)
        print 'Test reporte Linea Base sin permiso'

        resp = c.get('/gestionDeCambios/lineasBase/reporte/2')
        a=self.assertEqual(resp.status_code,200)
        print 'Test reporte Linea Base'

    def test_finalizar_proyecto(self):
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/gestionDeCambios/lineasBase/proyecto/finalizar/1')
        a=self.assertEqual(resp.status_code,302)
        print 'Test finalizar proyecto sin permiso'

        resp = c.get('/gestionDeCambios/lineasBase/proyecto/finalizar/2')
        a=self.assertEqual(resp.status_code,200)
        self.assertEqual([resp.context['proyecto'].nombre], ['Proyecto Beta'])
        print 'Test finalizar proyecto que no puede ser finalizado'



