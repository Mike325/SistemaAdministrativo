from django.db import models
from apps.Departamentos.models import *

class Reporte(models.Model):
	
	id = models.AutoField(primary_key = True)
	fecha = models.DateField()
	fk_profesor = models.ForeignKey(Profesor, default = False)
	categoria = models.CharField(max_length = 30, blank = True, default = False)
	fk_depto = models.ForeignKey(Departamento, default = False)
	fk_materia = models.ForeignKey(Materia, default = False)
	fk_seccion = models.ForeignKey(Seccion, default = False)
	fk_horario = models.ManyToManyField(Horario, blank = True)
	horasFalta = models.IntegerField()
	
	def __unicode__(self):
		return '%s -> %s'%(self.fecha, self.fk_profesor.nombre)
		pass