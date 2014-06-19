from django.test import TestCase, Client

class PMSTestCase(TestCase):
    '''
    Clase que implementa las distintas pruebas para los distintos reportes que genera el sistema
    '''

    fixtures = ["items_testmaker"]


    def test_reporte_usuarios(self):
        '''
        Test para descargar el reporte de usuarios del sistema
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #Test para proyecto buscar existente
        resp = c.get('/reporte/usuarios/')
        self.assertEqual(resp.status_code, 200)
        print 'Reporte de usuarios con permisos de administrador'
        c.login(username='mlopez', password='mlopez')
        #Test para proyecto buscar existente
        resp = c.get('/reporte/usuarios/')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de usuarios sin permisos de administrador'

    def test_reporte_roles(self):
        '''
        Test para generar el reporte de roles del sistema
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #Test para proyecto buscar existente
        resp = c.get('/reporte/roles/')
        self.assertEqual(resp.status_code, 200)
        print 'Reporte de roles con permisos de administrador'
        c.login(username='mlopez', password='mlopez')
        #Test para proyecto buscar existente
        resp = c.get('/reporte/roles/')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de roles sin permisos de administrador'

    def test_reporte_proyectos(self):
        '''
        Test para generar el reporte de proyectos del sistema
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #Test para proyecto buscar existente
        resp = c.get('/reporte/proyectos/')
        self.assertEqual(resp.status_code, 200)
        print 'Reporte de proyectos con permisos de administrador'
        c.login(username='mlopez', password='mlopez')
        #Test para proyecto buscar existente
        resp = c.get('/reporte/proyectos/')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de proyectos sin permisos de administrador'

    def test_reporte_proyecto(self):
        '''
        Test para generar el reporte de proyecto del sistema
        '''
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/reporte/proyecto/proyecto/1')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de proyecto sin permisos'
        c.login(username='pgonzalez', password='pgonzalez')
        resp = c.get('/reporte/proyecto/proyecto/1')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de proyecto con permisos'

    def test_reporte_lineasBase(self):
        '''
        Test para generar el reporte de proyecto del sistema
        '''
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/reporte/proyecto/lineasBase/1')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de lineas base sin permisos'
        c.login(username='pgonzalez', password='pgonzalez')
        resp = c.get('/reporte/proyecto/lineasBase/1')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de lineas base con permisos'

    def test_reporte_sc(self):
        '''
        Test para generar el reporte de sc de un proyecto
        '''
        c = Client()
        c.login(username='mlopez', password='mlopez')
        resp = c.get('/reporte/proyecto/solicitudesCambio/1')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de sc sin permisos'
        c.login(username='pgonzalez', password='pgonzalez')
        resp = c.get('/reporte/proyecto/solicitudesCambio/1')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de sc con permisos'

    def test_reporte_item(self):
        '''
        Test para generar el reporte de items de un proyecto
        '''
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/reporte/proyecto/items/1')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de items sin permisos'
        c.login(username='pgonzalez', password='pgonzalez')
        resp = c.get('/reporte/proyecto/items/1')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de items con permisos'

    def test_reporte_vitem(self):
        '''
        Test para generar el reporte de versiones de items de un proyecto
        '''
        c = Client()
        c.login(username='mlopez', password='mlopez')

        resp = c.get('/reporte/proyecto/versionesItems/1')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de versiones de Items sin permisos'
        c.login(username='pgonzalez', password='pgonzalez')
        resp = c.get('/reporte/proyecto/versionesItems/1')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de versiones de Items con permisos'