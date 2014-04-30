
from django.db import models
from django.contrib.auth.models import Group
from tiposDeItem.models import TipoItem, Atributo

# Create your models here.
ESTADOS = (
    ('PEN','Pendiente'),
    ('CON','En Construccion'),
    ('FIN','Finalizado'),
    ('VAL','Validado'),
    ('REV','Revision'),
    ('ANU','Anulado'),
)
TIPOS = (

    ('Padre', 'Padre'),
    ('Antecesor', 'Padre'),

)
class Item(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    descripcion=models.TextField(max_length=140, verbose_name='Descripcion')
    costo=models.IntegerField(verbose_name='Costo')
    tiempo=models.IntegerField(verbose_name='Tiempo')
    estado=models.CharField(max_length=3,choices=ESTADOS, verbose_name='Estado')
    version=models.PositiveSmallIntegerField(verbose_name='Version')
    relacion=models.OneToOneField('self',null=True, verbose_name='Relacion', related_name='relacionItem')
    tipo=models.CharField(null=True,max_length=10, choices=TIPOS, verbose_name='Tipo')
    fecha_creacion=models.DateField(verbose_name='Fecha de Creacion')
    fecha_mod=models.DateField(verbose_name='Fecha de Modificacion')
    tipo_item=models.ForeignKey(TipoItem)

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

class Archivo(models.Model):
    archivo=models.FileField(upload_to='archivos')
    id_item=models.ForeignKey(Item, null=True)
    nombre=models.CharField(max_length=100, null=True)

class AtributoItem(models.Model):
    id_item=models.ForeignKey(Item, verbose_name='Item')
    id_atributo=models.ForeignKey(Atributo, verbose_name='Atributo')
    valor=models.CharField(max_length=100, verbose_name='Valor')
    version=models.PositiveSmallIntegerField(verbose_name='Version')

class VersionAtributoItem(models.Model):
    id_atributo_item=models.ForeignKey(AtributoItem, verbose_name='Atributo Item')
    id_item=models.ForeignKey(Item, verbose_name='Item')
    id_atributo=models.ForeignKey(Atributo, verbose_name='Atributo')
    valor=models.CharField(max_length=100, verbose_name='Valor')
    version=models.PositiveSmallIntegerField(verbose_name='Version')


