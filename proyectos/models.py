from django.db import models
from django.contrib.auth.models import User
# Create your models here.
ESTADOS = (

    ('PEN', 'Pendiente'),
    ('ANU','Anulado'),
    ('ACT', 'Activo'),
    ('FIN','Finalizado')
)


class Proyecto(models.Model):
    nombre= models.CharField(max_length=100, verbose_name='Nombre',unique=True)
    descripcion= models.TextField(verbose_name='Descripcion')
    fecha_ini=models.DateField(null=False)
    fecha_fin=models.DateField(null=False)
    estado=models.CharField(max_length=3,choices= ESTADOS, default='PEN')
    lider = models.ForeignKey(User)
    observaciones = models.TextField(verbose_name='Observaciones')