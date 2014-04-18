from django.test import TestCase

from proyectos.models import Proyecto
from usuarios.tests import PMSTestCase
# Create your tests here.
class PMSTestCase(TestCase):
    def test_crear_proyecto(self):
        proyecto= Proyecto.objects.create(id=1, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        self.assertEqual(proyecto.nombre,'pruebaProyecto')
    def test_buscar_usuarios(self):
      self.test_crear_proyecto()
      resp = self.client.get('/proyectos/search/?q=pruebaProyecto')
      self.assertEqual(resp.status_code, 200)
      self.assertEqual([proyecto.nombre for proyecto in resp.context['datos']], ['pruebaProyecto'])
    def test_detalle_proyectos(self):
        '''
        Test para visualizar los detalles de un usuario
        '''
        proyecto= Proyecto.objects.create(id=1, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        resp = self.client.get('/proyectos/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['proyecto'].pk, 1)
        self.assertEqual(resp.context['proyecto'].nombre, 'pruebaProyecto')

