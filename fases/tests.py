from django.test import TestCase
from usuarios.tests import PMSTestCase
from fases.models import Fase
from proyectos.models import Proyecto

class PMSTestCase(TestCase):
    def test_crear_fase(self):
        proyecto= Proyecto.objects.create(id=1, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        fase= Fase.objects.create(id=1, nombre='pruebaFase',descripcion='prueba', maxItems=1,fInicio='2012-12-01',orden =1, proyecto=proyecto)
        self.assertEqual(fase.nombre,'pruebaFase')


    def test_detalle_fases(self):
        '''
        Test para visualizar los detalles de una fase
        '''
        proyecto= Proyecto.objects.create(id=1, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        fase= Fase.objects.create(id=1, nombre='pruebaFase',descripcion='prueba', maxItems=1,fInicio='2012-12-01',orden =1, proyecto=proyecto)
        resp = self.client.get('/fases/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['datos'].pk, 1)
        self.assertEqual(resp.context['datos'].nombre, 'pruebaFase')


def test_valid_form(self):
    proyecto= Proyecto.objects.create(id=1, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
    fase= Fase.objects.create(id=1, nombre='pruebaFase',descripcion='prueba', maxItems=1,fInicio='2012-12-01',orden =1, proyecto=proyecto)

    data = {'title': w.title, 'body': w.body,}
    form = WhateverForm(data=data)
    self.assertTrue(form.is_valid())

def test_invalid_form(self):
    w = Whatever.objects.create(title='Foo', body='')
    data = {'title': w.title, 'body': w.body,}
    form = WhateverForm(data=data)
    self.assertFalse(form.is_valid())

