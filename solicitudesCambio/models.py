from django.db import models
from proyectos.models import Proyecto
from items.models import Item
from django.contrib.auth.models import User
ESTADOS = (
    ('RECHAZADA','Rechazada'),
    ('APROBADA','Aprobada'),
    ('PENDIENTE','Pendiente'),
    ('EJECUTADA', 'Ejecutada')
)

VOTO = (
    ('APROBAR','A Favor'),
    ('RECHAZAR','En contra'),

)


class SolicitudCambio(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    descripcion=models.TextField(max_length=140, verbose_name='Descripcion')
    proyecto=models.ForeignKey(Proyecto)
    item=models.ForeignKey(Item)
    fecha=models.DateField(verbose_name='Fecha')
    costo=models.PositiveIntegerField(verbose_name='Costo')
    tiempo=models.PositiveIntegerField(verbose_name='Tiempo')
    usuario=models.ForeignKey(User)
    estado=models.CharField(max_length=10, verbose_name='Estado',choices=ESTADOS)

class Voto(models.Model):
    solicitud=models.ForeignKey(SolicitudCambio)
    usuario=models.ForeignKey(User)
    voto=models.CharField(max_length=10, verbose_name='Voto',choices=VOTO, null=False)


class ItemsARevision(models.Model):
    item_bloqueado=models.ForeignKey(Item, unique=False, related_name='item_bloqueado')
    item_revision=models.ForeignKey(Item, related_name='item_revision')
