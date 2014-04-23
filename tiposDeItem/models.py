from django.db import models
from fases.models import Fase
# Create your models here.
TIPOS = (

    ('NUM', 'Numerico'),
    ('TEX','Texto'),
    ('LOG', 'Logico'),
    ('FEC','Fecha')
)

class TipoItem(models.Model):
    nombre=models.CharField(max_length=100, null=False)
    descripcion=models.TextField(max_length=140, null=True)
    fase=models.ForeignKey(Fase, related_name='fase', null=True)

class Atributo(models.Model):
    nombre=models.CharField(max_length=100, null=Fase)
    tipo=models.CharField(max_length=3,choices=TIPOS, default='TEX' )
    valorDefecto=models.CharField(max_length=140)
    tipoItem=models.ForeignKey(TipoItem, related_name='tipoItem')

#class AtributoItem(models.Model):
#    id_item=models.SmallIntegerField(null=False);
#    id_atributo=models.SmallIntegerField(null=False);
#    valor=models.CharField(max_length=256);
