from django.db import models
from fases.models import Fase
ESTADOS = (
    ('CERRADA','Cerrada'),
    ('ROTA','Rota'),

)


class LineaBase(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    fase=models.ForeignKey(Fase)
    estado=models.CharField(max_length=7, verbose_name='Estado',choices=ESTADOS)