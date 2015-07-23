from django.db import models

'''
TODO:
    + Revisar relaciones.
    + Revisar claves primarias de todos los modelos.
    + Considerar models.AutoField() para algunos modelos.
'''

class Departamento(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=120)

    def __unicode__(self):
        return self.nombre
        pass

class Area(models.Model):
    id = models.IntegerField(primary_key=True)
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
        return clave
        pass

class Seccion(models.Model):
    id = models.CharField(max_length=5, primary_key=True)

    def __unicode__(self):
        return id
        pass    

class Profesor(models.Model):
    codigo_udg = models.CharField(max_length=9, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s, %s" %(self.apellido, self.nombre)
        pass

class Edificio(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.id
        pass

class Aula(models.Model):
    nombre = models.CharField(max_length=5)
    fk_edif = models.ForeignKey(Edificio)

    def __unicode__(self):
        return self.id
        pass

class Ciclo(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    fecha_ini = models.DateField()
    fecha_fin = models.DateField()

    def __unicode__(self):
        return id
        pass
    
class Curso(models.Model):
    NRC = models.CharField(max_length=5, primary_key=True)
    fk_profesor = models.ForeignKey(Profesor)
    fk_materia = models.ForeignKey(Materia)
    fk_area = models.ForeignKey(Area)
    fk_edif = models.ForeignKey(Edificio)
    fk_aula = models.ForeignKey(Aula)
    fk_secc = models.ForeignKey(Seccion)
    fk_ciclo = models.ForeignKey(Ciclo)

    def __unicode__(self):
        return self.NRC
        pass