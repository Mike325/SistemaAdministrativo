# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

from apps.Departamentos.models import *

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

@login_required(login_url='/')
def inicio_secretaria(request):
	if request.session['rol'] >= 1:
		_departamentos = Departamento.objects.all()

		return render(request, 'inicio-secretaria.html', 
			{
				'banner': True,
				'lista_departamentos': _departamentos
			})
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def listas_tCompleto(request, dpto):
	if request.session['rol'] >= 1:
		hoy = datetime.date.today()
		dia = hoy.isoweekday()

		disp_dia = dias[dia - 1].upper()
		disp_num_dia = str(hoy.day)
		disp_mes = meses[hoy.month - 1].upper()
		disp_anio = str(hoy.year)

		fechaDia = disp_dia + " " + disp_num_dia + " DE " + disp_mes + " DE " + disp_anio

		return render(request, 'listas.html',
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

		fecha = datetime.date.today()
		mesFc = int(fecha.month)
		dia = fecha.isoweekday()

		mes = meses[ mesFc-1 ][:3].upper()

		fechaDia = dias[dia-1].upper()

		return render(request, 'listas.html', 
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
		return render(request, 'form-incidencias.html', locals())
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def ver_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		fechaI = str(request.POST.get('fechaIni'))
		fechaF = str(request.POST.get('fechaFin'))

		try:
			fI = fechaI.split('-')
			fF = fechaF.split('-')
			num_mes = int(fI[1])
			mes_ini = meses[(num_mes-1)].upper()

			num_mes = int(fF[1])
			mes_fin = meses[(num_mes-1)].upper()
			
			extender_info = False

			if mes_ini != mes_fin:
				extender_info = True
			pass
		except:
			return render(request, 'form-incidencias.html',
				{
					'error': True,
				})

		return render(request, 'incidencias.html',
			{
				'dia_ini': fI[2], 
				'dia_fin': fF[2], 
				'mes_ini': mes_ini, 
				'mes_fin': mes_fin, 
				'anio_ini': fI[0],
				'anio_fin': fF[0],
				'extender_info': extender_info,
			})
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def form_reporte_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		_departamento = get_object_or_404(Departamento, nick=dpto)
		
		try:
			listaProf = Profesor.objects.order_by('apellido')
			listaMaterias = Curso.objects.all()

			return render(request, 'form-reporte-incidencias.html', 
				{
					'departamento': _departamento,
					'profesores': listaProf,
					'materias': listaMaterias,
				})
		except:
			return render(request, 'form-reporte-incidencias.html', 
				{
					'error': True,
					'departamento': _departamento,
					'profesores': listaProf,
				})
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def reporte_incidencias(request, dpto):
	if request.session['rol'] >= 1:
		return render(request, 'hecho.html', 
			{
				'accion': 'Hecho. Se ha realizado el reporte.',
			})
		try:
			fecha = str(request.POST.get('fecha'))
			fecha = fecha.split('-')
			maestro = str(request.POST.get('maestro'))
			codigo = str(request.POST.get('codigo'))
			categoria = str(request.POST.get('categoria'))
			depto = str(request.POST.get('depto'))
			materia = str(request.POST.get('materia'))
			seccion = str(request.POST.get('seccion'))
			horario = str(request.POST.get('horario'))
			horasFalta = str(request.POST.get('horasFalta'))			
		except:
			return render(request, 'form-reporte-incidencias.html', 
				{
					'error': True, 'departamento': dpto.upper(),
				})
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def estadisticasDepartamento(request, dpto):
	if request.session['rol'] >= 1:
		departamento = get_object_or_404(Departamento, nick=dpto)
		try:
			#Aquí se genera la información que se pasará a la gráfica
			datos = {
				'nombre' : departamento.nombre
			}
			return render(request, 'estadisticas.html', locals())
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
				return render(request, 'estadisticas.html', locals())
				pass
			except:
				return redirect('inicio-secretaria.html')
		else:
			lista_profesores = Profesor.objects.all()
			objetos = "Profesores"
			return render(request, 'estadisticas-listas.html', locals())
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
				return render(request, 'estadisticas.html', locals())
				pass
			except:
				return redirect('inicio-secretaria')
		else:
			objetos = "Materias"
			lista_materias = Materia.objects.all()
			return render(request, 'estadisticas-listas.html', locals())		
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
				return render(request, 'estadisticas.html', locals())
				pass
			except:
				return redirect('inicio-secretaria.html')
		else:
			objetos = "Ciclos"
			lista_ciclos = Ciclo.objects.all()
			return render(request, 'estadisticas-listas.html', locals())
	else:
		return redirect('error403', origen=request.path)