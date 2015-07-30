from django.db import models
from apps.Departamentos.models import *

class Reporte(models.Model):
	
	codigo = models.IntegerField(primary_key = True)
	fecha = models.DateField()
	profesor = models.CharField(max_length = 50)
	codProf = models.ForeignKey(Profesor)
	categoria = models.CharField(max_length = 50)
	depto = models.ForeignKey(Departamento)
	materia = models.ForeignKey(Materia)
	secc = models.ForeignKey(Seccion)
	horario = models.CharField(max_length = 10)
	horasFalta = models.IntegerField()
	
	def __unicode__(self):
		return self.codigo
		pass