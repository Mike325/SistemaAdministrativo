from django.db import models
from django.contrib.auth.models import User

'''
FIX:
    + Mejor relacion:
        Jefe de departamento es una propiedad del departamento
        mismo, por lo que se movio a apps.Departamentos.Departamento

        La relacion fue establecida como 1-a-1, por lo que se puede
        accesar tanto desde el Departamento como desde el Usuario.
'''

# from apps.Departamentos.models import Departamento

# Create your models here.
class Rol(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=15)

    def __unicode__(self):
        return self.tipo
        pass


class Usuario(models.Model):
    user = models.OneToOneField(User)
    codigo = models.CharField(max_length=9)
    rol = models.ForeignKey(Rol)
    # jefeDep = models.ForeignKey(Departamento, blank=True, null=True)

    def __unicode__(self):
        return self.user.username
        pass