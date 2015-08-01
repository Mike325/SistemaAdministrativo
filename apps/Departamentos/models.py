from django.db import models
from django.core.validators import RegexValidator

from apps.Usuarios.models import Usuario

alfanumerico = RegexValidator(r'^[0-9a-zA-Z]*$', 'Use solo caracteres alfanumericos (a-Z, 0-9).')

'''
FIX:
    - Jefe de departamento:
        Faltaba ese campo. Ahora todo funciona bien.
        Checar las notas en apps.Usuarios.models para mas detalles.

TODO:
    + Revisar relaciones.
    + Revisar claves primarias de todos los modelos.
    + Considerar models.AutoField() para algunos modelos.
'''

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nick = models.CharField(max_length=20, validators=[alfanumerico], unique=True)
    nombre = models.CharField(max_length=120)
    jefeDep = models.OneToOneField(Usuario, blank=True, null=True)

    def __unicode__(self):
        return self.nombre
        pass

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    fk_departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.nombre
        pass

class Materia(models.Model):
    clave = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=200)
    fk_area = models.ManyToManyField(Area)
    fk_departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.clave
        pass

class Seccion(models.Model):
    id = models.CharField(max_length=5, primary_key=True)

    def __unicode__(self):
        return self.id
        pass    

class Profesor(models.Model):
    codigo_udg = models.CharField(max_length=9, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s, %s" %(self.apellido, self.nombre)
        pass

class Edificio(models.Model):
    '''
    REV:
        + 'Edificio' para contener una variable de aulas.
        (y asi ahorrar tantos duplicados en aula?)
        + 'id' para ser una variable de tipo auto.
    '''
    id = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.id
        pass

class Aula(models.Model):
    nombre = models.CharField(max_length=5)
    fk_edif = models.ForeignKey(Edificio)
    '''
    REV:
        + 'fk_edif' para ser una variable de tipo
            models.ManyToManyField().
    '''

    def __unicode__(self):
        return self.nombre
        pass

class Ciclo(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    fecha_ini = models.DateField()
    fecha_fin = models.DateField()

    def __unicode__(self):
        return self.id
        pass

class Horario(models.Model):
    id = models.AutoField(primary_key=True)

    hora_ini = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    L = models.BooleanField(default=False, blank=True)
    M = models.BooleanField(default=False, blank=True)
    I = models.BooleanField(default=False, blank=True)
    J = models.BooleanField(default=False, blank=True)
    V = models.BooleanField(default=False, blank=True)
    S = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return "%s - %s: %s"%(self.hora_ini, self.hora_fin, [x for x in ['L','M','I','J','V','S'] if eval('self.'+x)==True])
        pass
    

class Curso(models.Model):
    NRC = models.CharField(max_length=5, primary_key=True)

    fk_area = models.ForeignKey(Area)
    
    fk_ciclo = models.ForeignKey(Ciclo)
    fk_materia = models.ForeignKey(Materia)
    fk_secc = models.ForeignKey(Seccion)
    
    fk_edif = models.ForeignKey(Edificio)
    fk_aula = models.ForeignKey(Aula)
    fk_horarios = models.ManyToManyField(Horario, blank=True)
    
    fk_profesor = models.ForeignKey(Profesor)
    #fk_horario = models.ForeignKey(Horario, blank=True, null=True, default='')

    def __unicode__(self):
        return self.NRC
        pass