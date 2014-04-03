from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    #user = models.OneToOneField(User, unique=True, related_name='perfil')
    user = models.ForeignKey(User, unique=True)
    direccion = models.TextField()
    telefono = models.PositiveIntegerField(null=True, blank=True)
    observacion = models.CharField(max_length=250, blank=True)


#def create_perfil(sender, instance, created, **kwargs):
#    if created:
#        Perfil.objects.create(user=instance)

#nuevo_perfil.connect(create_perfil, sender=User)
