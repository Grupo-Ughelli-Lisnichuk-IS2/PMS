from django.db import models
from fases.models import Fase



class LineaBase(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    fase=models.ForeignKey(Fase)