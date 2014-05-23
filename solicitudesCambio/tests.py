from django.test import TestCase, Client


class PMSTestCase(TestCase):

    fixtures = ["solicitudes_testmaker"]


    def test_listar_solicitudes(self):
        '''
        Test para listar solicitudes de cambio pendientes de un usuario
        '''
        c = Client()
        c.login(username='rperez', password='rperez')

        resp = c.get('/gestionDeCambios/solicitudes/listar/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([solicitud.nombre for solicitud in resp.context['datos']], ['modificar', 'modficaciones necesarias'])
        print 'Test para comprobar que lista correctamente las solicitudes de un usuario'
        c.login(username='admin', password='admin')
        resp = c.get('/gestionDeCambios/solicitudes/listar/')
        self.assertEqual(resp.status_code,302 )
        print 'Test para comprobar que no lista si no tiene permisos'


    def test_detalle_solicitud(self):
        '''
        Test para listar solicitudes de cambio pendientes de un usuario
        '''
        c = Client()
        c.login(username='rperez', password='rperez')

        resp = c.get('/gestionDeCambios/solicitudes/votacion/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([resp.context['solicitud'].nombre], ['Quiero modificar'])
        print 'Test para comprobar que muestra correctamente el detalle de nombre de la solicitud'
        self.assertEqual([miembro.username for miembro in resp.context['usuarios']], ['pgonzalez', 'rperez', 'sperez'])
        print 'Test para comprobar que el usuario es mimbro del comite de esa solicitud y que ya voto'

    def test_votar(self):
        '''
        Test para votar una solicitud de cambio
        '''
        c = Client()
        c.login(username='rperez', password='rperez')
        resp = c.get('/gestionDeCambios/solicitudes/votar/1')
        self.assertEqual(resp.status_code, 302)
        print 'Test para probar que un usuario que ya voto no puede volver a votar'
        resp = c.get('/gestionDeCambios/solicitudes/votar/4')
        self.assertEqual(resp.status_code, 200)
        print 'Test que si deja votar si aun no ha votado y es miembro del comite'
        resp = c.get('/gestionDeCambios/solicitudes/votar/4')
        resp = c.post('/gestionDeCambios/solicitudes/votar/4', {'voto':'APROBAR', 'id_solicitud':4})
        self.assertEqual(resp.status_code, 200)
        print 'Test para probar que un usuario con permisos puede emitir su voto'
