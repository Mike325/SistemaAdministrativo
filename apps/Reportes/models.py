from django.db import models
from apps.Departamentos.models import *

class Reporte(models.Model):
	
	id = models.AutoField(primary_key = True)
	fecha = models.DateField()
	fk_contrato = models.ForeignKey(Contrato, default = False)
	fk_depto = models.ForeignKey(Departamento, default = False)
	horasFalta = models.IntegerField()
	
	def __unicode__(self):
		return '%s -> %s'%(self.fecha, self.fk_contrato.fk_curso.fk_profesor)
		pass