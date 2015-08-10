# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from datetime import date, time, datetime, timedelta

from apps.Departamentos.models import *
from apps.Reportes.models import *
from apps.Historicos.models import *
from apps.Listas.models import *

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
dias_abrev = ['L', 'M', 'I', 'J', 'V', 'S']
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

#Creacion de la lista de asistencias para profesores de tiempo completo
def crear_lista_diaria_TCompleto(request, dpto):
	hoy = date.today()
	dia = hoy.isoweekday()
	dpto = Departamento.objects.get(nick=dpto)
	'''if dia<6:
		args = {
			dias_abrev[dia - 1]: True
		}

		horarios = Horario.objects.filter(**args)
	else:
		horarios = []'''
	horarios = Horario.objects.filter(L=True)

	cursosTCompleto = Asistencia.objects.filter(
		fecha__startswith = hoy,
		fk_contrato__fk_curso__fk_horarios__in = horarios, 
		fk_contrato__tipo = 'T',
		fk_contrato__fk_curso__fk_materia__fk_departamento__nick = dpto.nick
	).order_by('fk_contrato__fk_curso__fk_horarios__hora_ini','fk_contrato__fk_curso__fk_profesor__apellido')

	if not cursosTCompleto:
		cursosTCompleto = Contrato.objects.filter(
			fk_curso__fk_horarios__in = horarios,
			tipo = 'T',
			fk_curso__fk_materia__fk_departamento__nick = dpto.nick
		).order_by('fk_curso__fk_horarios__hora_ini','fk_curso__fk_profesor__apellido')

		for curso in cursosTCompleto:

			'''agrs = {
				dias_abrev[dia - 1]: True
			}'''
			args = {'L':'True'}
			objeto = curso.fk_curso.fk_horarios.get(**args)

			horasClase = ((datetime.combine(date.today(), objeto.hora_fin) - datetime.combine(date.today(), objeto.hora_ini)) + timedelta(minutes = 5)).seconds/3600
			asis = Asistencia(
					horas_clase = horasClase, 
					fk_contrato = curso
				)
			if str(curso.id) in request.POST:
				asis.asistio = True
			else:
				asis.asistio = False
			asis.save()

		historico = Registro.creacion(request.session['usuario']['nick'],
					'Se guardaron las asistencias de Tiempo Completo del "'+ dpto.nombre +'"',
					'Guardadas', 'Asistencias')
		historico.save()
		return redirect("/inicio-secretaria/")
	else:
		pass

def crear_lista_diaria_TMedio(request, dpto):
	hoy = date.today()
	dia = hoy.isoweekday()
	dpto = Departamento.objects.get(nick=dpto)
	'''if dia<6:
		args = {
			dias_abrev[dia - 1]: True
		}

		horarios = Horario.objects.filter(**args)
	else:
		horarios = []'''
	horarios = Horario.objects.filter(L=True)

	cursosTCompleto = Asistencia.objects.filter(
		fecha__startswith = hoy,
		fk_contrato__fk_curso__fk_horarios__in = horarios, 
		fk_contrato__tipo = 'P',
		fk_contrato__fk_curso__fk_materia__fk_departamento__nick = dpto.nick
	).order_by('fk_contrato__fk_curso__fk_horarios__hora_ini','fk_contrato__fk_curso__fk_profesor__apellido')

	if not cursosTCompleto:
		cursosTCompleto = Contrato.objects.filter(
			fk_curso__fk_horarios__in = horarios,
			tipo = 'P',
			fk_curso__fk_materia__fk_departamento__nick = dpto.nick
		).order_by('fk_curso__fk_horarios__hora_ini','fk_curso__fk_profesor__apellido')

		for curso in cursosTCompleto:

			'''agrs = {
				dias_abrev[dia - 1]: True
			}'''
			args = {'L':'True'}
			objeto = curso.fk_curso.fk_horarios.get(**args)

			horasClase = ((datetime.combine(date.today(), objeto.hora_fin) - datetime.combine(date.today(), objeto.hora_ini)) + timedelta(minutes = 5)).seconds/3600
			asis = Asistencia(
					horas_clase = horasClase, 
					fk_contrato = curso
				)
			if str(curso.id) in request.POST:
				asis.asistio = True
			else:
				asis.asistio = False
			asis.save()

		historico = Registro.creacion(request.session['usuario']['nick'],
					'Se guardaron las asistencias de Tiempo Completo del "'+ dpto.nombre +'"',
					'Guardadas', 'Asistencias')
		historico.save()
		return redirect("/inicio-secretaria/")
	else:
		pass

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

			'''if dia<6:
				args = {
					dias_abrev[dia - 1]: True
				}

				horarios = Horario.objects.filter(**args)
			else:
				horarios = []'''
			horarios = Horario.objects.filter(L = True)

			asistencias = Asistencia.objects.filter(
				fecha__startswith = hoy,
				fk_contrato__fk_curso__fk_horarios__in = horarios, 
				fk_contrato__tipo = 'T',
				fk_contrato__fk_curso__fk_materia__fk_departamento__nick = dpto.nick
				)

			yaRegistradas = True if asistencias else False
	
			cursosTCompleto = Contrato.objects.filter(
				fk_curso__fk_horarios__in = horarios,
				tipo = 'T',
				fk_curso__fk_materia__fk_departamento__nick = dpto.nick
			).order_by('fk_curso__fk_horarios__hora_ini','fk_curso__fk_profesor__apellido')


			return render(request, 'Listas/listas.html',
				{
					'today': fechaDia, 
					'tiempoC': True,
					'listaContratos' : cursosTCompleto,
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
			hoy = date.today()
			dpto = get_object_or_404(Departamento, nick=dpto)

			fecha = date.today()
			mesFc = int(fecha.month)
			dia = fecha.isoweekday()

			mes = meses[ mesFc-1 ][:3].upper()

			fechaDia = dias[dia-1].upper()

			'''if dia<6:
				args = {
					dias_abrev[dia - 1]: True
				}

				horarios = Horario.objects.filter(**args)
			else:
				horarios = []'''
			horarios = Horario.objects.filter(L = True)

			asistencias = Asistencia.objects.filter(
				fecha__startswith = hoy,
				fk_contrato__fk_curso__fk_horarios__in = horarios, 
				fk_contrato__tipo = 'P',
				fk_contrato__fk_curso__fk_materia__fk_departamento__nick = dpto.nick
				)

			yaRegistradas = True if asistencias else False

			cursosTMedio = Contrato.objects.filter(
				fk_curso__fk_horarios__in = horarios, 
				tipo = 'P',
				fk_curso__fk_materia__fk_departamento__nick = dpto.nick
			).order_by('fk_curso__fk_horarios__hora_ini','fk_curso__fk_profesor__apellido')

			return render(request, 'Listas/listas.html', 
				{
					'dayWeek': fechaDia, 
					'day': fecha.day, 
					'month': mes, 
					'year': fecha.year, 
					'tiempoM': True,
					'departamento': dpto,
					'listaContratos' : cursosTMedio,
					'horarios' : horarios,
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