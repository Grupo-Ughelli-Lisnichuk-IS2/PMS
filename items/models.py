
from django.db import models
from django.contrib.auth.models import Group, User
from tiposDeItem.models import TipoItem, Atributo
from lineasBase.models import LineaBase
# Create your models here.
ESTADOS = (
    ('PEN','Pendiente'),
    ('CON','En Construccion'),
    ('FIN','Finalizado'),
    ('VAL','Validado'),
    ('REV','Revision'),
    ('ANU','Anulado'),
    ('BLO','Bloqueado')
)
TIPOS = (

    ('Padre', 'Padre'),
    ('Antecesor', 'Padre'),

)
class Item(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    descripcion=models.TextField(max_length=140, verbose_name='Descripcion')
    costo=models.PositiveIntegerField(verbose_name='Costo')
    tiempo=models.PositiveIntegerField(verbose_name='Tiempo')
    estado=models.CharField(max_length=3,choices=ESTADOS, verbose_name='Estado')
    version=models.PositiveSmallIntegerField(verbose_name='Version')
    relacion=models.ForeignKey('self',null=True, verbose_name='Relacion', related_name='relacionItem')
    tipo=models.CharField(null=True,max_length=10, choices=TIPOS, verbose_name='Tipo')
    fecha_creacion=models.DateField(verbose_name='Fecha de Creacion')
    fecha_mod=models.DateField(verbose_name='Fecha de Modificacion')
    tipo_item=models.ForeignKey(TipoItem)
    lineaBase=models.ForeignKey(LineaBase, null=True)
    def __str__(self):
        return self.nombre

class VersionItem(models.Model):
    id_item=models.ForeignKey(Item, verbose_name='Item', related_name='itemVersion')
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    descripcion=models.TextField(max_length=140, verbose_name='Descripcion')
    costo=models.PositiveIntegerField(verbose_name='Costo')
    tiempo=models.PositiveIntegerField(verbose_name='Tiempo')
    estado=models.CharField(max_length=3,choices=ESTADOS, verbose_name='Estado')
    version=models.PositiveSmallIntegerField(verbose_name='Version')
    relacion=models.ForeignKey(Item,null=True, verbose_name='Relacion',related_name='relacionVersion')
    tipo=models.CharField(null=True,max_length=10, choices=TIPOS, verbose_name='Tipo')
    fecha_mod=models.DateField(verbose_name='Fecha de Modificacion')
    tipo_item=models.ForeignKey(TipoItem)
    usuario=models.ForeignKey(User)
    lineaBase=models.ForeignKey(LineaBase, null=True)

class Archivo(models.Model):
    archivo=models.FileField(upload_to='archivos')
    id_item=models.ForeignKey(Item, null=True)
    nombre=models.CharField(max_length=100, null=True)

class AtributoItem(models.Model):
    id_item=models.ForeignKey(Item, verbose_name='Item')
    id_atributo=models.ForeignKey(Atributo, verbose_name='Atributo')
    valor=models.CharField(max_length=100, verbose_name='Valor')





