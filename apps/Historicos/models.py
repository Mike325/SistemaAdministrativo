# -*- encoding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from apps.Usuarios.models import Usuario

'''
    +Para generar el histórico a la hora de cambiar algo, llamar:
    Registro.creacion(...) o Registro.modificacion(...)
    dependiendo de si se creó o modificó un objeto
'''


class Registro(models.Model):
    usuario = models.ForeignKey(Usuario)
    fechaModificacion = models.DateField(auto_now_add=True)
    horaModificacion = models.TimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=150)
    cambioDe = models.CharField(max_length=30, blank=True)
    cambioA = models.CharField(max_length=30)
    cambioTabla = models.CharField(max_length=30)

    @classmethod
    def creacion(cls, username, descripcion, cambioA, cambioTabla):
        usuario = Usuario.objects.get(user__username=username)
        registro = cls(usuario=usuario, descripcion=descripcion,
                     cambioA=cambioA, cambioTabla=cambioTabla)
        return registro

    @classmethod
    def modificacion(cls, username, descripcion, cambioDe, cambioA, cambioTabla):
        usuario = Usuario.objects.get(user__username=username)
        registro = cls(usuario=usuario, descripcion=descripcion, cambioDe=cambioDe,
                     cambioA=cambioA, cambioTabla=cambioTabla)
        return registro
