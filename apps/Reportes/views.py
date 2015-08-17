# -*- encoding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from datetime import date, datetime, timedelta

from apps.Departamentos.models import *
from apps.Reportes.models import *
from apps.Historicos.models import *

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
dias_abrev = ['L', 'M', 'I', 'J', 'V', 'S']
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

TEMPLATE_SUCCESS = 'hecho.html'
TEMPLATE_FORM_INCIDENCIAS = 'Forms/form-incidencias.html'
TEMPLATE_FORM_REPORTE_INC = 'Forms/form-reporte-incidencias.html'

#Carga de la pagina de incio de las secretarias
@login_required(login_url='/')
def inicio_secretaria(request):
	if request.session['rol'] >= 1:
		_departamentos = Departamento.objects.all()

		bienvenida = False

		if request.session['just_logged']:
			bienvenida = True
			request.session['just_logged'] = False

		return render(request, 'inicio-secretaria.html', 
			{
				'banner': True,
				'lista_departamentos': _departamentos,
				'bienvenida': bienvenida
			})
	else:
		return redirect('error403', origen=request.path)

#Carga del formulario de incidencias
@login_required(login_url='/')
def form_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		form_size = 'medium'
		return render(request, TEMPLATE_FORM_INCIDENCIAS, locals())
		pass
	else:
		return redirect('error403', origen=request.path)

#Formulario para la consulta de las incidencias (por fechas)
@login_required(login_url='/')
def ver_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		fechaI = str(request.POST.get('fechaIni'))
		fechaF = str(request.POST.get('fechaFin'))

		errores = []

		try:
			fI = fechaI.split('-')
			fechaInicio = date(int(fI[0]), int(fI[1]), int(fI[2]))
		except:
			errores.append('Inicio')

		try:
			fF = fechaF.split('-')
			fechaFin = date(int(fF[0]), int(fF[1]), int(fF[2]))
		except:
			errores.append('Fin')

		if not errores:
			num_mes = int(fechaInicio.month)	
			mes_ini = meses[(num_mes-1)].upper()

			num_mes = int(fechaFin.month)
			mes_fin = meses[(num_mes-1)].upper()
			
			extender_info = False

			if mes_ini != mes_fin:
				extender_info = True

			listaIncidencias = Reporte.objects.filter(
					fecha__gte = fechaInicio, 
					fecha__lte = fechaFin
				).select_related('fk_contrato')

			if listaIncidencias:
				return render(request, 'Reportes/incidencias.html',
				{
					'fechaI': fechaInicio, 
					'fechaF': fechaFin, 
					'mes_ini': mes_ini, 
					'mes_fin': mes_fin, 
					'extender_info': extender_info,
					'listaIncidencias': listaIncidencias,
					'listaDias': dias_abrev,
				})
			else:
				return render(request, TEMPLATE_SUCCESS, 
				{
					'accion': 'Vaya. No existe ningun reporte en esas fechas.',
				})

		else:
			return render(request, TEMPLATE_FORM_INCIDENCIAS,
				{
					'errores': errores
				})

	else:
		return redirect('error403', origen=request.path)

#Formulario para reportar una incidencia
@login_required(login_url='/')
def form_reporte_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		_departamento = get_object_or_404(Departamento, nick=dpto)
		
		try:
			# curso = Curso.objects.filter(
			# 		curso__fk_area__fk_departamento=_departamento
			# 	)
			cursos = Curso.objects.filter(
					fk_area__fk_departamento=_departamento
				)
			listaProf = Profesor.objects.filter(
					curso__in=cursos
				).distinct().order_by('apellido').select_related()

			return render(request, TEMPLATE_FORM_REPORTE_INC, 
				{
					'form_size': 'large',
					'profesores': listaProf,
					'lista_cursos': cursos,
					'departamento': _departamento
				})
		except Exception, e:
			#print e
			return render(request, TEMPLATE_FORM_REPORTE_INC, 
				{
					'error': True,
					'departamento': _departamento,
					'profesores': listaProf,
					'form_size': 'large'
				})
		pass
	else:
		return redirect('error403', origen=request.path)

#Procesamiento del formulario para aregar el reporte
@login_required(login_url='/')
def reporte_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		_departamento = get_object_or_404(Departamento, nick=dpto)
		listaProf = Profesor.objects.order_by('apellido')
		listaMaterias = Curso.objects.all()
		
		hoy = date.today()
		dia = hoy.isoweekday()

		if dia >= 7: 
		# si es domingo o por alguna extraña 
		# razon salió un día mas alto
			raise Http404 # pues nada

		errores = []

		try:
			curso = str(request.POST.get('curso'))
			contrato = Contrato.objects.get(fk_curso__NRC = curso)
		except:
			errores.append('Curso')

		comentario = str(request.POST.get('comentario'))
		filtro = { dias_abrev[dia-1]: True }

		h = contrato.fk_curso.fk_horarios.get(**filtro)
		hora_ini = datetime.combine(hoy, h.hora_ini)
		hora_fin = datetime.combine(hoy, h.hora_fin)

		horas_clase = (hora_fin - hora_ini) + timedelta(minutes = 5)
		horas_clase = horas_clase.seconds/3600

		if not errores:
			nuevo_reporte = Reporte(
				fk_contrato = contrato, 
				fk_depto = _departamento, 
				horasFalta = horas_clase,
				comentario = comentario
			)

			nuevo_reporte.save()

			registroReporte = Registro.creacion(request.session['usuario']['nick'], 
										'Se creo el reporte de incidencia ['+nuevo_reporte.__unicode__()+
										'('+nuevo_reporte.fk_contrato.fk_curso.fk_profesor.codigo_udg+')]', 
										nuevo_reporte.__unicode__(), 'Reportes', _departamento)
			registroReporte.save()

			return render(request, TEMPLATE_SUCCESS, 
			{
				'accion': 'Hecho. Se ha realizado el reporte.',
			})

		else:
			return render(request, TEMPLATE_FORM_REPORTE_INC, 
				{
					'errores': errores, 
					'departamento': _departamento,
					'profesores': listaProf,
					'materias': listaMaterias,
				})
	else:
		return redirect('error403', origen=request.path)