# -*- coding: utf-8 -*-
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

    - ¿Como te llamas?
        Agregado 'nombre' y 'apellidos' al modelo de Usuario.

TODO:
    + Agregar un metodo en 'Usuario' para realizar el procedimiento 
      de dar de alta un usuario en el sistema (de django) y enlazarlo 
      aqui.

      ej.
      def Alta(self, codigo, usuario, nombre, apellidos, correo, rol):
            nuevo = User.objects.create_user(/* ... */)
            nuevo.save()

            self.user = nuevo
            self.nombre = nombre
            self.apellidos = apellidos
            /* ...(etc)... */

    + Agregar metodo para cambiar de rol a un determinado usuario.
        (Por si se llega a dar un caso de cambio de roles/posicion/etc)
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

    nombre = models.CharField(max_length=50, blank=True)
    apellidos = models.CharField(max_length=50, blank=True)

    rol = models.ForeignKey(Rol)

    def __unicode__(self):
        return self.user.username
        pass