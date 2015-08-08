# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from datetime import date

from apps.Departamentos.models import *
from apps.Reportes.models import *
from apps.Historicos.models import *

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

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

@login_required(login_url='/')
def listas_tCompleto(request, dpto):
	if request.session['rol'] >= 1:
		hoy = date.today()
		dia = hoy.isoweekday()

		disp_dia = dias[dia - 1].upper()
		disp_num_dia = str(hoy.day)
		disp_mes = meses[hoy.month - 1].upper()
		disp_anio = str(hoy.year)

		fechaDia = disp_dia + " " + disp_num_dia + " DE " + disp_mes + " DE " + disp_anio

		return render(request, 'Listas/listas.html',
			{
				'today': fechaDia, 
				'tiempoC': True,
			})
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def listas_tMedio(request, dpto):
	if request.session['rol'] >= 1:
		dpto = get_object_or_404(Departamento, nick=dpto)

		fecha = date.today()
		mesFc = int(fecha.month)
		dia = fecha.isoweekday()

		mes = meses[ mesFc-1 ][:3].upper()

		fechaDia = dias[dia-1].upper()

		return render(request, 'Listas/listas.html', 
			{
				'dayWeek': fechaDia, 
				'day': fecha.day, 
				'month': mes, 
				'year': fecha.year, 
				'tiempoM': True,
				'departamento': dpto,
			})
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def form_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		form_size = 'medium'
		return render(request, 'Forms/form-incidencias.html', locals())
		pass
	else:
		return redirect('error403', origen=request.path)

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

			listaIncidencias = Reporte.objects.filter(fecha__gte = fechaInicio, fecha__lte = fechaFin)

			if listaIncidencias:
				return render(request, 'Reportes/incidencias.html',
				{
					'fechaI': fechaInicio, 
					'fechaF': fechaFin, 
					'mes_ini': mes_ini, 
					'mes_fin': mes_fin, 
					'extender_info': extender_info,
					'listaIncidencias': listaIncidencias,
				})
			else:
				return render(request, 'hecho.html', 
				{
					'accion': 'Vaya. No existe ningun reporte en esas fechas.',
				})

		else:
			return render(request, 'form-incidencias.html',
				{
					'errores': errores
				})

	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def form_reporte_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		_departamento = get_object_or_404(Departamento, nick=dpto)
		
		try:
			print 'op'
			# listaProf = Profesor.objects.order_by('apellido')
			# listaMaterias = Curso.objects.filter(fk_area__fk_departamento_id=2)

			listaProf = Profesor.objects.filter(
					curso__fk_area__fk_departamento=_departamento
				).distinct().order_by('apellido')

			# listaMaterias = {}

			# listaMaterias = Curso.objects.filter(
			# 		fk_area__fk_departamento=_departamento
			# 	)

			# print listaMaterias # DEBUG

			return render(request, 'Forms/form-reporte-incidencias.html', 
				{
					'departamento': _departamento,
					'profesores': listaProf,
					'form_size': 'large'
				})
		except Exception, e:
			print e
			return render(request, 'Forms/form-reporte-incidencias.html', 
				{
					'error': True,
					'departamento': _departamento,
					'profesores': listaProf,
					'form_size': 'large'
				})
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def reporte_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		_departamento = get_object_or_404(Departamento, nick=dpto)
		listaProf = Profesor.objects.order_by('apellido')
		listaMaterias = Curso.objects.all()

		errores = []

		try:
			fechaReporte = str(request.POST.get('fecha'))
			fechaReporte = fechaReporte.split('-')
			fechaReporte = date(int(fechaReporte[0]), int(fechaReporte[1]), int(fechaReporte[2]))
		except:
			errores.append('Fecha')

		try:
			curso = str(request.POST.get('curso'))
			contrato = Contrato.objects.get(fk_curso__NRC = curso)
		except:
			errores.append('Curso')

		try:
			horasF = int(request.POST.get('horasFalta'))
		except:
			errores.append('Hora')

		if not errores:
			nuevo_reporte = Reporte(
				fecha = fechaReporte, 
				fk_contrato = contrato, 
				fk_depto = _departamento, 
				horasFalta = horasF
			)

			nuevo_reporte.save()

			registroReporte = Registro.creacion(request.session['usuario']['nick'], 
										'Se creo el reporte de incidencia ['+nuevo_reporte.__unicode__()+
										'('+nuevo_reporte.fk_contrato.fk_curso.fk_profesor.codigo_udg+')]', 
										nuevo_reporte.__unicode__(), 'Reportes')
			registroReporte.save()

			return render(request, 'hecho.html', 
			{
				'accion': 'Hecho. Se ha realizado el reporte.',
			})

		else:
			return render(request, 'Forms/form-reporte-incidencias.html', 
				{
					'errores': errores, 
					'departamento': _departamento,
					'profesores': listaProf,
					'materias': listaMaterias,
				})
	else:
		return redirect('error403', origen=request.path)

''' SECCION DE LAS ESTADISTICAS '''

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