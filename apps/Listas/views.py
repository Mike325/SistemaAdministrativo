# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from datetime import date, time, datetime, timedelta

from apps.Departamentos.models import *
from apps.Reportes.models import *
from apps.Historicos.models import *
from apps.Listas.models import *

import re, math

# Override del día
DAY_OVR = 2

dias_abrev = ['L', 'M', 'I', 'J', 'V', 'S']
dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

#Creacion de la lista de asistencias para profesores de tiempo completo
def crear_lista_diaria_TCompleto(request, dpto):
	hoy = date.today()
	dia = hoy.isoweekday()
	dpto = Departamento.objects.get(nick=dpto)

	'''
	Override del día para pruebas.
	(COMENTAR O ELIMINAR PARA PRODUCCION)
	'''
	dia = DAY_OVR # DEBUG

	_profesor = None
	filtro = {}

	for clave, valor in request.POST.items():
		if not clave.startswith('csrf'): # no tiene que ver con el key CSRF
			_profesor = Profesor.objects.get(
					codigo_udg=str(clave)
				) ## GG OPT

			filtro = { 'fk_curso__fk_horarios__' + dias_abrev[dia-1]: True }
			contratos = Contrato.objects.filter(
					tipo='T',
					fk_curso__fk_profesor=_profesor,
					**filtro
				) ## GG OPT

			filtro = { dias_abrev[dia-1]: True }

			_asistencia = None
			tipoActual = contratos[0].fk_tipocont
			for contrato in contratos:
				'''
				REV:
					+ La validación del contrato no sería necesaria aqui
					  dado que se almacena la asistencia para cada contrato.
					+ Estadisticas tendría que analizar los distintos tipos 
					  de contrato.
				'''
				# if contrato.fk_tipocont != tipoActual:
				#   print tipoActual, '-', contrato.fk_tipocont
				#   pass

				assist = Asistencia()
				assist.asistio = True if valor=='on' else False
				assist.fk_contrato = contrato

				# PREPARACIONES HORAS DE CLASE >> inicio
				horas_clase = None
				for x in contrato.fk_curso.fk_horarios.filter(**filtro):
					hora_ini = datetime.combine(hoy, x.hora_ini)
					hora_fin = datetime.combine(hoy, x.hora_fin)

					if horas_clase:
						horas_clase = horas_clase + (hora_fin - hora_ini)
					else:
						horas_clase = hora_fin - hora_ini

					#print horas_clase # DEBUG
					pass # for
				# PREPARACIONES HORAS DE CLASE >> fin

				horas = horas_clase.seconds/60
				assist.horas_clase = int(math.ceil(horas/60.0))
				assist.save()

				# print assist # DEBUG
				pass # for 
			pass # if

			historico = Registro.creacion(request.session['usuario']['nick'],
					  'Se guardaron las asistencias de Tiempo Completo del "'+ dpto.nombre +'"',
					  'Guardadas', 'Asistencias', dpto)
			historico.save()
		pass # for

	return redirect("/")
	pass # view

def crear_lista_diaria_TMedio(request, dpto):
	hoy = date.today()
	dia = hoy.isoweekday()
	dpto = Departamento.objects.get(nick=dpto)

	'''
	Override del día para pruebas.
	(COMENTAR O ELIMINAR PARA PRODUCCION)
	'''
	dia = DAY_OVR # DEBUG

	'''
		REV: Horario puede que no se ocupe aqui
	'''

	filtro = { dias_abrev[dia-1]: True }

	for clave, valor in request.POST.items():
		print clave, '\t\t', valor
		if not clave.startswith('csrf'): # no tiene que ver con el key CSRF
			_contrato = Contrato.objects.get(id=clave)
			assist = Asistencia()
			assist.fk_contrato = _contrato
			assist.asistio = True if valor=='on' else False

			# PREPARACIONES HORAS DE CLASE >> inicio
			horas_clase = None
			for x in _contrato.fk_curso.fk_horarios.filter(**filtro):
				hora_ini = datetime.combine(hoy, x.hora_ini)
				hora_fin = datetime.combine(hoy, x.hora_fin)

				if horas_clase:
					horas_clase = horas_clase + (hora_fin - hora_ini)
				else:
					horas_clase = hora_fin - hora_ini

				#print horas_clase # DEBUG
				pass # for
			# PREPARACIONES HORAS DE CLASE >> fin

			horas = horas_clase.seconds/60
			assist.horas_clase = int(math.ceil(horas/60.0))

			assist.save() # GUARDA LOS DATOS
			print assist

			pass # if
		pass # for

	historico = Registro.creacion(request.session['usuario']['nick'],
					'Se guardaron las asistencias de Medio Tiempo del "'+ dpto.nombre +'"',
					'Guardadas', 'Asistencias', dpto)
	historico.save()

	return redirect('/')

#Listas de tiempo completo
@login_required(login_url='/')
def listas_tCompleto(request, dpto):
	if request.session['rol'] >= 1:
		if request.method == 'POST':
			return crear_lista_diaria_TCompleto(request, dpto)
		else:
			dpto = get_object_or_404(Departamento, nick = dpto)
			hoy = date.today()
			dia = hoy.isoweekday()
			
			disp_dia = dias[dia - 1].upper()
			disp_num_dia = str(hoy.day)
			disp_mes = meses[hoy.month - 1].upper()
			disp_anio = str(hoy.year)

			fechaDia = disp_dia + " " + disp_num_dia + " DE " + disp_mes + " DE " + disp_anio

			'''
			Override del día para pruebas.
			(COMENTAR O ELIMINAR PARA PRODUCCION)
			'''
			dia = DAY_OVR # DEBUG

			profesores = Profesor.objects.filter(
					curso__fk_area__fk_departamento=dpto
				).distinct().order_by('apellido')

			filtro = {'fk_horarios__'+dias_abrev[dia-1]: True}

			#cursos = Curso.objects.filter(**filtro)

			listaAsistencia = []

			for x in profesores:
				cursos = x.curso_set.filter(
						fk_profesor=x,
						contrato__isnull=False, # todos los cursos con un contrato
						fk_area__fk_departamento=dpto, # que tengan el departamento
						**filtro # más el filtro extra
					)
				contratos = Contrato.objects.filter(
						tipo='T',
						fk_curso__in=cursos
					).values('fk_tipocont__nombre')
				horarios = Horario.objects.filter(
						curso__in=cursos
					).order_by('hora_ini')#.values()

				cuenta = horarios.count()

				if contratos and cuenta > 0:
					listaAsistencia.append({
							'profesor': x.apellido + ', ' + x.nombre + '(' + x.codigo_udg + ')',
							'hora_ini': horarios[0].hora_ini,
							'hora_fin': horarios[cuenta-1].hora_fin,
							'codigo_prof': x.codigo_udg
						})
					pass
				pass

				'''DESCOMENTAR SI QUIERE ORDENARSE POR HORA DE INICIO'''
				#listaAsistencia = sorted(listaAsistencia, key=lambda d: (d['hora_ini'], d['profesor']))

			# return HttpResponse('') # DEBUG

			yaRegistradas = Asistencia.objects.filter(
					fecha__startswith = hoy,
					fk_contrato__tipo = 'T',
					fk_contrato__fk_curso__fk_materia__fk_departamento__nick = dpto.nick
				).count()
			yaRegistradas = yaRegistradas!=0

			return render(request, 'Listas/listas.html',
				{
					'today': fechaDia, 
					'tiempoC': True,
					'listaAsistencia' : listaAsistencia,
					'horarios' : horarios,
					'yaRegistradas' : yaRegistradas
				})
	else:
		return redirect('error403', origen=request.path)

#Listas de medio tiempo
@login_required(login_url='/')
def listas_tMedio(request, dpto):
	if request.session['rol'] >= 1:
		if request.method == 'POST':
			return crear_lista_diaria_TMedio(request, dpto)
		else:
			dpto = get_object_or_404(Departamento, nick=dpto)
			hoy = date.today()
			dia = hoy.isoweekday()
			mes_num = int(hoy.month)

			disp_dia = dias[dia-1].upper()
			disp_mes = meses[mes_num-1][:3].upper()

			'''
			Override del día para pruebas.
			(COMENTAR O ELIMINAR PARA PRODUCCION)
			'''
			dia = DAY_OVR # DEBUG

			filtro = { dias_abrev[dia-1]: True }

			horarios = Horario.objects.filter(**filtro)

			yaRegistradas = Asistencia.objects.filter(
					fecha__startswith = hoy,
					fk_contrato__tipo = 'P',
					fk_contrato__fk_curso__fk_materia__fk_departamento = dpto
				).count()
			yaRegistradas = yaRegistradas!=0

			cursosTMedio = Contrato.objects.filter(
					tipo = 'P',
					fk_curso__fk_horarios__in = horarios,
					fk_curso__fk_area__fk_departamento = dpto
				).order_by('fk_curso__fk_horarios__hora_ini','fk_curso__fk_profesor__apellido')

			return render(request, 'Listas/listas.html', 
				{
					'tiempoM': True,
					'departamento': dpto,
					'dayWeek': disp_dia, 
					'day': hoy.day, 
					'month': disp_mes, 
					'year': hoy.year, 

					'horarios' : horarios,
					'listaContratos' : cursosTMedio,
					'yaRegistradas' : yaRegistradas
				})
	else:
		return redirect('error403', origen=request.path)


''' Apartado de estaticas sobre asistencias '''

#Estadisticas de asistencia de un depto.
@login_required(login_url='/')
def estadisticasDepartamento(request, dpto):
	if request.session['rol'] >= 1:
		departamento = get_object_or_404(Departamento, nick=dpto)
		try:
			#Aquí se genera la información que se pasará a la gráfica
			datos = {
				'nombre' : departamento.nombre
			}
			form_size = 'small'
			return render(request, 'Listas/estadisticas.html', locals())
			pass
		except:
			return redirect('inicio-secretaria.html')
	else:
		return redirect('error403', origen=request.path)

#Estadisticas de asistencia de un profesor
@login_required(login_url='/')
def estadisticasProfesor(request):
	if request.session['rol'] >= 1:
		if request.GET.get('profesor'):
			profesor = get_object_or_404(Profesor, codigo_udg=request.GET.get('profesor'))
			try:
				#Aquí se genera la información que se pasará a la gráfica
				datos = {
					'nombre' : (profesor.nombre + " " + profesor.apellido +
								 "(" + profesor.codigo_udg + ")")
				}
				form_size = 'small'
				return render(request, 'Listas/estadisticas.html', locals())
				pass
			except:
				return redirect('inicio-secretaria.html')
		else:
			lista_profesores = Profesor.objects.all()
			objetos = "Profesores"
			form_size = 'small'
			return render(request, 'Listas/estadisticas-listas.html', locals())
	else:
		return redirect('error403', origen=request.path)

#Estadisticas de asistencia de una materia
@login_required(login_url='/')
def estadisticasMateria(request):
	if request.session['rol'] >= 1:
		if request.GET.get('materia'):
			materia = get_object_or_404(Materia, clave=request.GET.get('materia'))
			try:
				#Aquí se genera la información que se pasará a la gráfica
				datos = {
					'nombre' : materia.nombre + " (" + materia.clave + ")"
				}
				form_size = 'small'
				return render(request, 'Listas/estadisticas.html', locals())
				pass
			except:
				return redirect('inicio-secretaria')
		else:
			form_size = 'small'
			objetos = "Materias"
			lista_materias = Materia.objects.all()
			return render(request, 'Listas/estadisticas-listas.html', locals())     
	else:
		return redirect('error403', origen=request.path)

#Estadisticas de asistencia por ciclo escolar
@login_required(login_url='/')
def estadisticasCiclo(request):
	if request.session['rol'] >= 1:
		if request.GET.get('ciclo'):
			ciclo = get_object_or_404(Ciclo, id=request.GET.get('ciclo'))
			try:
				#Aquí se genera la información que se pasará a la gráfica
				datos = {
					'nombre' : "Ciclo " + ciclo.id
				}
				form_size = 'small'
				return render(request, 'Listas/estadisticas.html', locals())
				pass
			except:
				return redirect('inicio-secretaria.html')
		else:
			objetos = "Ciclos"
			lista_ciclos = Ciclo.objects.all()
			form_size = 'small'
			return render(request, 'Listas/estadisticas-listas.html', locals())
	else:
		return redirect('error403', origen=request.path)