# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

'''
FIX:
    - Mejor relacion:
        Jefe de departamento es una propiedad del departamento
        mismo, por lo que se movio a apps.Departamentos.Departamento

        La relacion fue establecida como 1-a-1, por lo que se puede
        accesar tanto desde el Departamento como desde el Usuario.

    - Codigos unicos:
        Ahora 'codigo' no puede repetirse (lo normal, no?).
'''

class Rol(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=15)

    def __unicode__(self):
        return self.tipo
        pass

class Usuario(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    codigo = models.CharField(max_length=9, unique=True)
    rol = models.ForeignKey(Rol)

    def __unicode__(self):
        return self.user.username
        pass

    @classmethod
    def alta_jefe(cls, username, password, first_name, last_name, email, codigo):
        nuevo_user = User.objects.create_user(username=username, password=password,
                                     first_name=first_name, last_name=last_name, email=email)
        nuevo_user.save()
        usuario = cls(user=nuevo_user, codigo=codigo, rol=Rol.objects.get(id=2))
        return usuario

    @classmethod
    def alta_secretaria(cls, username, password, first_name, last_name, email, codigo):
        nuevo_user = User.objects.create_user(username=username, password=password,
                                     first_name=first_name, last_name=last_name, email=email)
        nuevo_user.save()
        usuario = cls(user=nuevo_user, codigo=codigo, rol=Rol.objects.get(id=1))
        return usuario

    @classmethod
    def hacer_jefe(self, rol):
        self.rol = Rol.objects.get(id=2)
        return self

    @classmethod
    def hacer_secretaria(self, rol):
        self.rol = Rol.objects.get(id=1)
        return self