# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.Departamentos.models import *

import re # libreria de expresiones regulares

@login_required(login_url='/')
def ver_cursos(request, dpto):
	if request.session['rol'] >= 2: # es jefedep o mayor
		lista_cursos = Curso.objects.all()
		paginator = Paginator(lista_cursos, 100)

		pagina = request.GET.get('pagina')

		try:
			lista_cursos = paginator.page(pagina)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			lista_cursos = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			lista_cursos = paginator.page(paginator.num_pages)

		return render(request, 'Departamentos/modifica_curso.html', locals())
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def procesar_csv(request, dpto):
	if request.session['rol'] >= 2: # es jefedep o mayor
		if request.method == 'POST': # se envio a traves del formulario
			try:
				post_departamento = request.POST.get('depto', '')
				_departamento = get_object_or_404(Departamento, nick=post_departamento)

				post_ciclo = request.POST.get('ciclo-esc', '')
				_ciclo = get_object_or_404(Ciclo, id=post_ciclo)
				pass
			except Exception, e:
				raise e

			errores = [] # inicializa errores
			cursos = [] # inicializa el objeto para los cursos

			try:
				nombre_archivo = request.FILES['archivo-csv']
				datos = unicode(nombre_archivo.read()).replace('\r\n', '\n').replace('\n',';;')
				# Compatibilidad tanto para fin de linea de Windows como de Linux
				# (esperemos que nunca ocurra que alguien modifique el archivo en Mac)

				'''
				TODO:
					+ Verificar la extension del archivo y, como medida adicional, comprobar
					  que el archivo efectivamente esta separado por comas desde un inicio.
				'''
				pass
			except Exception, e:
				ciclos = Ciclo.objects.all()
				errores.append(
					{
						'propiedad': 'Archivo',
						'descripcion': 'No se selecciono un archivo.'
					})
				return render(request, 'Departamentos/form_subir_csv.html', 
					{
						'errores': errores,
						'departamento': _departamento,
						'lista_ciclos': ciclos
					})

			datos = re.sub('\s{2,}', '', datos) # Elimina los espacios en blanco en el nombre de la materia.

			datos = datos.replace('"','').replace(', ','-') 
			# Elimina las comillas y cambia las comas de los nombres por otro caracter.

			datos = datos.split(';;')

			datos.pop() # elimina la linea en blanco
			del datos[0] # elimina los cabezales

			for fila in datos:
				fila = fila.split(',') # separa las columnas por la coma

				# Agrega los datos de la fila a los cursos.
				# Estos datos han de utilizarse luego para añadir la 
				# informacion a la base de datos.
				cursos.append({
					'nrc': fila[0],
					'st':  fila[1],
					'departamento': fila[2],
					'area':    fila[3],
					'clave':   fila[4],
					'materia': fila[5],
					'secc':    fila[6],
					'cred':    fila[7],
					'cupo':    fila[8],
					'ocup':    fila[9],
					'disp':    fila[10],
					'ini':     fila[11],
					'fin':     fila[12],
					'dias': 
					{
						# convierte los valores a Verdadero si
						# la longitud de la columna es mayor que 0
						# (hay algo escrito).
						'lun': True if len(fila[13])>0 else False,
						'mar': True if len(fila[14])>0 else False,
						'mie': True if len(fila[15])>0 else False,
						'jue': True if len(fila[16])>0 else False,
						'vie': True if len(fila[17])>0 else False,
						'sab': True if len(fila[18])>0 else False
					},
					'edif':  fila[19],
					'aula':  fila[20],
					'profesor': fila[21].replace('-', ', '),
					'fecha_inicio': fila[22],
					'fecha_fin':    fila[23],
					'nivel': fila[24]
				})
				pass

			for x in cursos:
				#return HttpResponse(_departamento.id) # DEBUG

				_area, created = Area.objects.get_or_create(nombre=x['area'], fk_departamento=_departamento)

				_materia, created = Materia.objects.get_or_create(clave=x['clave'], nombre=x['materia'], fk_departamento = _departamento)

				# Agrega el area al campo m2m
				_materia.fk_area.add(_area)
				_materia.save()

				# return HttpResponse(_materia) # DEBUG

				# Preparaciones para Profesor
				'''
				TODO:
					+ Pasar las preparaciones a una funcion en commons
					  y que retorne un objeto con todos los datos.
				'''
				profesor = x['profesor'].split(', ')
				profesor = {'nombre': profesor[1], 'apellidos': profesor[0]}

				if re.search('\(\d+\)', profesor['nombre']) is not None:
					codigo_prof = profesor['nombre'].split('(')
					codigo_prof = codigo_prof[1].replace(')', '')

					profesor['nombre'] = re.sub('\(\d+\)', '', profesor['nombre'])
				else:
					errores.append(
						{
							'propiedad': 'Profesor',
							'descripcion': '%s, %s no posee un codigo identificable por el sistema.<br/>Por favor, a&ntilde;adalo manualmente.'%(profesor['apellidos'], profesor['nombre'])
						})
					codigo_prof = '-'
					pass
				# FIN PREPARACIONES

				# return HttpResponse(str(profesor) + ' ## ' + codigo_prof) # DEBUG

				_profesor, created = Profesor.objects.get_or_create(codigo_udg=codigo_prof, nombre=profesor['nombre'], apellido=profesor['apellidos'])

				# return HttpResponse(_profesor.nombre) # DEBUG

				_edificio, created = Edificio.objects.get_or_create(id=x['edif'])

				# return HttpResponse(_edificio) # DEBUG

				_aula, created = Aula.objects.get_or_create(nombre=x['aula'], fk_edif=_edificio)

				_seccion, created = Seccion.objects.get_or_create(id=x['secc'])

				# return HttpResponse(_seccion) # DEBUG

				# FINALMENTE!
				_curso = Curso(
						NRC=x['nrc'], 
						fk_profesor=_profesor, 
						fk_materia=_materia, 
						fk_area=_area,
						fk_edif=_edificio,
						fk_aula=_aula,
						fk_secc=_seccion,
						fk_ciclo=_ciclo
					)

				_curso.save();
				# return HttpResponse(_curso) #YOLO
				pass
			return render(request, 'Departamentos/form_subir_csv.html', {'errores': errores, 'success': True})
			# return JsonResponse(cursos, safe=False); # temporal.
			pass
		else:
			dpto = dpto[:20]
			departamento = get_object_or_404(Departamento, nick=dpto)
			#lista_departamentos = Departamento.objects.all()
			lista_ciclos = Ciclo.objects.all()
			return render(request, 'Departamentos/form_subir_csv.html', locals())

	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def sistema_consulta(request, dpto, ciclo):
	if request.session['rol'] >= 2:
		return render(request, 'Departamentos/modifica_curso.html',
			{
				'dpto': dpto,
				'ciclo': ciclo
			})
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def sistema_modifica_nrc(request, dpto, ciclo, nrc):
	if request.session['rol'] >= 2:
		return render(request, 'Departamentos/modifica_curso_individual.html',
			{
				'dpto': dpto,
				'ciclo': ciclo,
				'nrc': nrc
			})
		pass
	else:
		return redirect('error403', origen=request.path)


''' *************** IMPORTACIONES DE jefe_Depto/views_jefedep.py *************** '''

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.Departamentos.models import Departamento

@login_required(login_url='/')
def inicio_jefedep(request):
	if request.session['rol'] >= 2:
		bienvenida = False

		if request.session['just_logged']:
			bienvenida = True
			request.session['just_logged'] = False

		lista_departamentos = Departamento.objects.all()

		return render(request, 'inicio-jefedep.html', 
			{
				'banner': True, 
				'bienvenida': bienvenida,
				'lista_departamentos': lista_departamentos
			});
	else:
	   	return redirect('error403', origen=request.path)

@login_required(login_url='/')
def computacion_form_asistencias(request):
	if request.session['rol'] >= 2:
		if request.method == 'POST':

			criterios = ['si', 'si', 'si', 'si', 'si', 'si']

			return render(request, 'reporte-asist.html', 
				{
					'departamento' : 'Departamento de Ciencias Computacionales',
					'nombre' : 'Juan Perez Rodriguez', 
					'codigo' : request.POST.get('field-codprof'), 
					'calif' : 'excelente',
					'ciclo' : '2015-A',
					'criterios' : criterios, 
					'fecha' : 'HOY', 
					'nombrefirma' : 'Luisa Hermandia Limbo', 
					'puesto' : 'Profesional'
				});
		else:
			return render(request, 'form-reporte-asistencias.html');
	else:
	    return redirect('error403', origen=request.path)