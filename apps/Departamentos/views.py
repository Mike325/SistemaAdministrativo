# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.Departamentos.models import *
from apps.Historicos.models import *

import re # libreria de expresiones regulares

# from django import template

# register = template.Library()

# @register.assignment_tag
# def query(qs, **kwargs):
#     """ template tag which allows queryset filtering. Usage:
#           {% query books author=author as mybooks %}
#           {% for book in mybooks %}
#             ...
#           {% endfor %}
#     """
#     return qs.filter(**kwargs)

TEMPLATE_FORM_CSV = 'Forms/form_subir_csv.html'

@login_required(login_url='/')
def inicio_jefedep(request):
	if request.session['rol'] >= 2:
		options = {'banner': True} # Opciones por defecto

		bienvenida = False

		if request.session['just_logged']:
			bienvenida = True
			request.session['just_logged'] = False

		lista_departamentos = Departamento.objects.all()

		options.update({'bienvenida': bienvenida})
		options.update({'lista_departamentos': lista_departamentos})

		return render(request, 'inicio-jefedep.html', options)
	else:
	   	return redirect('error403', origen=request.path)

@login_required(login_url='/')
def gestion_sistema(request, dpto, area, area_id, ajax=False):
	_tabla = None
	options = {}
	filtros = {}
	campos = []

	if area == 'suplentes':
		_tabla = Suplente
		filtros.update({'id': area_id})

		campos.append({
				'label': 'NRC',
				'id': 'in-nrc',
				'value': 'fk_curso.NRC',
				'send': False,
				'disable': True,
				'size': 2
			})
		campos.append({
				'label': 'Clave',
				'id': 'in-cvemat',
				'value': 'fk_curso.fk_materia.clave',
				'send': False,
				'disable': True,
				'size': 2
			})
		campos.append({
				'label': 'Materia',
				'id': 'in-materia',
				'value': 'fk_curso.fk_materia.nombre',
				'send': False,
				'disable': True,
				'size': 8
			})
		campos.append({
				'label': 'SECC',
				'id': 'in-secc',
				'value': 'fk_curso.fk_secc',
				'send': False,
				'disable': True,
				'max_length': 5,
				'size': 2
			})
		campos.append({
				'label': 'Profesor',
				'id': 'in-profesor',
				'value': 'fk_curso.fk_profesor',
				'send': False,
				'disable': True,
				'size': 5
			})
		campos.append({
				'label': 'Suplente',
				'id': 'in-supp',
				'send': False,
				'value': 'fk_profesor',
				'rel': 'in-codigo',
				'size': 5
			})
		campos.append({
				'id': 'in-codigo',
				'type': 'hidden',
				'value': 'fk_profesor.codigo_udg'
			})
		pass
	elif area == 'profesores':
		_tabla = Profesor
		filtros.update({'codigo_udg': area_id})
		pass
	elif area == 'ciclos':
		_tabla = Ciclo
		filtros.update({'id': area_id})
		pass

	try:
		_objeto = _tabla.objects.get(**filtros)
		print _objeto
	except:
		_objeto = None
		print 'fack'
		pass

	if _objeto:
		for campo in campos:
			if 'value' in campo:
				campo['value'] = eval('_objeto.' + campo['value'])
				#print eval('_objeto.' + campo['value'])
				pass
			pass
		pass

	options.update({'ajax': ajax})
	options.update({'campos': campos})
	#print campos
	#return HttpResponse(_objeto)
	return render(request, 'Forms/gestion_general.html', options)

@login_required(login_url='/')
def administrar_suplentes(request, dpto):
	if request.session['rol'] >= 2:
		options = {'area':'suplentes', 'titulo': 'Suplentes'}

		suplentes = Suplente.objects.all()
		_departamento = get_object_or_404(Departamento, nick=dpto)

		options.update({'datos': suplentes})
		return render(request, 'Departamentos/gestion_suplentes.html', options)
		pass
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def ver_cursos(request, dpto):
	if request.session['rol'] >= 2: # es jefedep o mayor
		lista_cursos = Curso.objects.filter(fk_area__fk_departamento__nick=dpto).order_by('fk_materia__nombre')
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

		return render(request, 'Departamentos/ver_cursos.html', locals())
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def modifica_curso(request, dpto, nrc, ajax=False):
	if request.session['rol'] >= 2: # es jefedep o mayor
		_nrc = int(nrc)
		curso = get_object_or_404(Curso, NRC=_nrc)

		if request.method == 'POST':
			errores = []
			warns = []

			'''ELIMINACIONES PENDIENTES'''
			in_delete_req = [
					k.replace('delete-horario-','') # valor asignado si...
					for k, v in request.POST.items() # para cada (clave, valor) en los elementos POST
						if k.startswith('delete-horario-') and v == 'true'
						# ^ si la clave inicia con el prefijo 'delete-horario-'
						#   y su valor es igual a "verdadero".
				]

			# print 'A eliminar:', in_delete_req # DEBUG

			for x in in_delete_req: # para cada elemento en la lista de elementos a eliminar... 
				_horario = Horario.objects.get(id=str(x))

				if _horario and _horario.curso_set.all().count() <=1: 
					# si hay solo 1 curso asignado al horario este se elimina de la BD.
					# (tambien por si dada alguna extraña razon hay 0 cursos con ese horario)
					_horario.delete()
					pass
				elif _horario and _horario.curso_set.all().count() > 1:
					# si hay más de un solo curso asignado a ese horario
					# (lo que muy probablemente signifique que en los demas cursos debe de  
					#   quedar totalmente intacto), solo lo removemos del curso actual.
					_curso.fk_horarios.remove(_horario)
					pass
				else:
					pass

				pass

			'''HORARIOS NUEVOS'''
			in_new_req = [
					{ k.replace('in-horarioN-','') : v } # valor a asignar si...
					for k, v in request.POST.items() if k.startswith('in-horarioN-')
				]

			actual = ''
			datos = {}
			_horario = None

			if in_new_req: # Si hay nuevos horarios
				# Ordenamos los nuevos horarios y los pasamos a un arreglo con
				# la clave principal.
				in_new_req = sorted(in_new_req)

				for x in in_new_req:
					for clave, valor in x.items():
						temp = clave.split('-',1)

						if temp[0] != actual:
							actual = temp[0]
							datos[actual] = {}

						datos[actual].update({ temp[1] : valor })
						pass
					pass

				# Procesamos todas las entradas
				for clave, valor in datos.items():
					# PREPARACIONES EDIFICIO >> inicio
					if 'edif' in datos[clave] and datos[clave]['edif'] != '':
						# Tenemos un edificio en la solicitud
						_edificio, created = Edificio.objects.get_or_create( id = datos[clave]['edif'].upper() )

						if created:
							# warns.append(
							# 	{
							# 		'tipo': 'Objeto inexistente',
							# 		'desc': 'Se creo un edificio nuevo.'
							# 	})
							edificioCreadoRegistro = Registro.creacion(
									request.session['usuario']['nick'], 
									'Se creo el edificio "' + _edificio.id + '"',
									_edificio.id, 'Edificios'
								)

							edificioCreadoRegistro.save()
							pass
					else:
						errores.append(
							{
								'tipo': 'Edificio',
								'desc': 'Entrada invalida.'
							})
					# PREPARACIONES EDIFICIO >> fin

					# PREPARACIONES AULA >> inicio
					if 'aula' in datos[clave] and datos[clave]['aula'] != '':
						_aula, created = Aula.objects.get_or_create(
								nombre = datos[clave]['aula'].upper(), 
								fk_edif = _edificio
							)

						if created:
							# warns.append(
							# 	{
							# 		'tipo': 'Objeto inexistente',
							# 		'desc': 'Se creo una aula nueva.'
							# 	})
							aulaCreadaRegistro = Registro.creacion(
									request.session['usuario']['nick'],
									'Se creo el aula "' + _aula.nombre + '"',
									_aula.nombre, 'Aulas'
								)
							aulaCreadaRegistro.save()
							pass
					else:
						errores.append(
							{
								'tipo': 'Aula',
								'desc': 'Entrada invalida.'
							})
					# PREPARACIONES AULA >> fin

					if not errores:
						_horario = Horario()

						_horario.hora_ini = datos[clave]['hora-ini'] if 'hora-ini' in datos[clave] else None
						_horario.hora_fin = datos[clave]['hora-fin'] if 'hora-fin' in datos[clave] else None
						_horario.L = True if 'dias-L' in datos[clave] and datos[clave]['dias-L'] == 'on' else False
						_horario.M = True if 'dias-M' in datos[clave] and datos[clave]['dias-M'] == 'on' else False
						_horario.I = True if 'dias-I' in datos[clave] and datos[clave]['dias-I'] == 'on' else False
						_horario.J = True if 'dias-J' in datos[clave] and datos[clave]['dias-J'] == 'on' else False
						_horario.V = True if 'dias-V' in datos[clave] and datos[clave]['dias-V'] == 'on' else False
						_horario.S = True if 'dias-S' in datos[clave] and datos[clave]['dias-S'] == 'on' else False

						_horario.fk_edif = _edificio
						_horario.fk_aula = _aula

						try:
							_horario.save()
							curso.fk_horarios.add(_horario)
							pass
						except Exception, e:
							errores.append({
									'tipo': 'Nuevo horario # ' + clave,
									'desc': 'Hubo un problema al guardar los datos.<br/><small>Olvidó algun campo?</small>'
								})
						pass
					else:
						errores.append({
								'tipo': 'Datos incompletos',
								'desc': 'Imposible continuar.<br/><b>No se guardaron todos los cambios.</b>'
							})
				pass

				if errores:
					return JsonResponse(errores, safe=False)
					pass

			'''HORARIOS EXISTENTES'''
			if in_delete_req:
				in_horarios = [
						{ k.replace('in-horario-','') : v } # valor a asignar si...
						for k, v in request.POST.items() if k.startswith('in-horario-') and 
							[x not in k for x in in_delete_req]
					]
				pass
			else:
				in_horarios = [
						{ k.replace('in-horario-','') : v } # valor a asignar si...
						for k, v in request.POST.items() if k.startswith('in-horario-')
					]
				pass

			in_horarios = sorted(in_horarios) # ordena los elementos

			print 'Entradas horarios: ', in_horarios # DEBUG

			actual=''
			datos = {}
			_horario = None

			for x in in_horarios:
				for clave, valor in x.items():
					temp = clave.split('-',1)

					if temp[0] != actual:
						actual = temp[0]
						datos[actual] = {}

					datos[actual].update({ temp[1] : valor })
					#datos[actual].append({ temp[1].replace('-','_') : valor })
					pass
				pass

			#print datos

			for clave, valor in datos.items():
				# PREPARACIONES EDIFICIO >> inicio
				if 'edif' in datos[clave]:
					# Tenemos un edificio en la solicitud
					_edificio, created = Edificio.objects.get_or_create( id = datos[clave]['edif'].upper() )

					if created:
						# warns.append(
						# 	{
						# 		'tipo': 'Objeto inexistente',
						# 		'desc': 'Se creo un edificio nuevo.'
						# 	})
						edificioCreadoRegistro = Registro.creacion(request.session['usuario']['nick'], 
														'Se creo el edificio "'+_edificio.nombre+'"',
														_edificio.nombre, 'Edificios')
						edificioCreadoRegistro.save()
						pass
				else:
					errores.append(
						{
							'tipo': 'Edificio',
							'desc': 'Entrada invalida.'
						})
				# PREPARACIONES EDIFICIO >> fin

				# PREPARACIONES AULA >> inicio
				if 'aula' in datos[clave]:
					_aula, created = Aula.objects.get_or_create(
							nombre = datos[clave]['aula'].upper(), 
							fk_edif = _edificio
						)

					if created:
						# warns.append(
						# 	{
						# 		'tipo': 'Objeto inexistente',
						# 		'desc': 'Se creo una aula nueva.'
						# 	})
						aulaCreadaRegistro = Registro.creacion(request.session['usuario']['nick'], 
														'Se creo el aula "'+_aula.nombre+'"',
														_aula.nombre, 'Aulas')
						aulaCreadaRegistro.save()
						pass
				else:
					errores.append(
						{
							'tipo': 'Aula',
							'desc': 'Entrada invalida.'
						})
				# PREPARACIONES AULA >> fin

				if not errores:
					_horario = Horario.objects.get(id=str(clave))
					horarioAnterior = Horario.objects.get(id=str(clave))
					
					_horario.hora_ini = datos[clave]['hora-ini'] if 'hora-ini' in datos[clave] else None
					_horario.hora_fin = datos[clave]['hora-fin'] if 'hora-fin' in datos[clave] else None
					_horario.L = True if 'dias-L' in datos[clave] and datos[clave]['dias-L'] == 'on' else False
					_horario.M = True if 'dias-M' in datos[clave] and datos[clave]['dias-M'] == 'on' else False
					_horario.I = True if 'dias-I' in datos[clave] and datos[clave]['dias-I'] == 'on' else False
					_horario.J = True if 'dias-J' in datos[clave] and datos[clave]['dias-J'] == 'on' else False
					_horario.V = True if 'dias-V' in datos[clave] and datos[clave]['dias-V'] == 'on' else False
					_horario.S = True if 'dias-S' in datos[clave] and datos[clave]['dias-S'] == 'on' else False

					_horario.fk_edif = _edificio
					_horario.fk_aula = _aula

					if _horario.curso_set.all().count() > 1:
						_horario.pk = None

					_horario.save()

					if horarioAnterior.__unicode__() != _horario.__unicode__():
						registroHorario = Registro.modificacion(
								request.session['usuario']['nick'],

								'Se cambio el horario del curso "' + curso.NRC + '" de "'
								+ horarioAnterior.__unicode__() + '" a "' + _horario.__unicode__() + '"',

								horarioAnterior.__unicode__(), 
								_horario.__unicode__(), 
								'Horarios'
							)
						registroHorario.save()

					if horarioAnterior.fk_aula.nombre != _aula.nombre:
						registroAula = Registro.modificacion(
								request.session['usuario']['nick'],

								'Se cambio el aula del curso "' + curso.NRC + '" de "' 
								+ horarioAnterior.fk_aula.nombre+'" a "' + _aula.nombre+'"',

								horarioAnterior.fk_aula.nombre, 
								_aula.nombre,
								'Horarios'
							)
						registroAula.save()
					if horarioAnterior.fk_edif.id != _edificio.id:
						registroEdif = Registro.modificacion(
								request.session['usuario']['nick'],

								'Se cambio el edificio del curso "'+curso.NRC+'" de "'+
								horarioAnterior.fk_edif.id+'" a "'+ _edificio.id+'"',

								horarioAnterior.fk_edif.id, 
								_edificio.id,
								'Horarios'
							)
						registroEdif.save()

					Horario.objects.filter(curso__isnull=True).delete()

					# print '\nGuardado en la BD:', _horario # DEBUG

					'''AHORA HAY QUE PROCESAR LOS DATOS CORRESPONDIENTES AL CURSO'''
					pass
				else:
					return JsonResponse(errores, safe=False)
				pass

			#print datos # DEBUG
			in_secc = request.POST.get('in-secc', '').upper()
			in_codigo_prof = request.POST.get('in-codigo', '')

			if in_codigo_prof:
				profesor_actual = curso.fk_profesor
				_profesor = Profesor.objects.get(codigo_udg=in_codigo_prof)
				if in_codigo_prof != profesor_actual.codigo_udg:
					registroP = Registro.modificacion(
							request.session['usuario']['nick'],
							'Se cambio el profesor "' 
							+ profesor_actual.nombre + " " + profesor_actual.apellido+
		                    '" por "'+_profesor.nombre+" "+_profesor.apellido+'"', 
		                    profesor_actual.codigo_udg,
		                    _profesor.codigo_udg, 'Cursos'
                    	)
					registroP.save()
				curso.fk_profesor = _profesor
				pass

			if in_secc:
				secc_actual = curso.fk_secc
				_seccion = Seccion.objects.get(id=in_secc)
				if in_secc != secc_actual.id:
					registroS = Registro.modificacion(
							request.session['usuario']['nick'],
							'Se cambio la seccion "' +
	                        secc_actual.id+" por "+_seccion.id+'"', 
	                        secc_actual.id,
	                        _seccion.id, 
	                        'Cursos'
                        )
					registroS.save()
				curso.fk_secc = _seccion
				pass

			curso.save()

			return HttpResponse('Se guardaron los cambios correctamente.')
			pass
		else:
			lista_materias = Materia.objects.all()
			lista_profesores = Profesor.objects.all()
			id_nuevo_curso = Horario.objects.last().id + 1

			options = locals()

			return render(request, 'Forms/form_modifica_curso.html', options)
	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def procesar_csv_contratos(request, dpto):
	if request.session['rol'] >= 2: # es jefedep o mayor
		default_options = {'titulo_tipo':'Contratos', 'form_size': 'medium'}
		options = {}

		# Inicializacion de objetos.
		errores = []
		contratos = []

		if request.method == 'POST': # se envio a traves del formulario

			try: # validacion de las variables de departamento.
				post_departamento = request.POST.get('depto', '')
				_departamento = get_object_or_404(Departamento, nick=post_departamento)

				post_ciclo = request.POST.get('ciclo-esc', '')
				_ciclo = get_object_or_404(Ciclo, id=post_ciclo)
				pass
			except Exception, e:
				errores.append({
						'propiedad': 'Departamento/Ciclo',
						'descripcion': 'Hubo un error con alguno de los dos campos.'
					})
				pass

			try: # validacion del archivo csv (existencia y tipo)
				archivo_csv = request.FILES['archivo-csv']

				if not archivo_csv or archivo_csv.content_type != 'text/csv':
					ciclos = Ciclo.objects.all()
					errores.append({
							'propiedad': 'Archivo',
							'descripcion': 'Tipo de archivo no valido.'
						})
					archivo_csv = None

					options.update(default_options)
					options.update({'errores': errores})
					options.update({'departamento': _departamento})
					options.update({'lista_ciclos': ciclos})

					return render(request, TEMPLATE_FORM_CSV, options)
					pass

				datos = archivo_csv.read().replace('\r\n', '\n').replace('\n',';;')
				# Compatibilidad tanto para fin de linea de Windows como de Linux
				# (esperemos que nunca ocurra que alguien modifique el archivo en Mac)
			except Exception, e:
				ciclos = Ciclo.objects.all()
				errores.append(
					{
						'propiedad': 'Archivo',
						'descripcion': 'No se selecciono un archivo.'
					})

				options.update(default_options)
				options.update({'errores': errores})
				options.update({'departamento': _departamento})
				options.update({'lista_ciclos': ciclos})

				return render(request, TEMPLATE_FORM_CSV, options)

			datos = datos.replace('"','').replace(', ','-') 
			datos = datos.split(';;')

			datos.pop() # elimina la linea en blanco
			del datos[0] # elimina los cabezales

			for fila in datos:
				fila = fila.split(',')

				contratos.append({
						'nrc': fila[4],
						'tipo': fila[6],
						'tipoC': fila[11]
					})
				pass

			print 'Contratos:', contratos

			for fila in contratos:
				try:
					_curso = Curso.objects.get(NRC=fila['nrc'])
					pass
				except Exception, e:
					errores.append({
							'propiedad': 'Contrato',
							'descripcion': 'El NRC ' + fila['nrc'] + ' no está registrado propiamente en los cursos.<br/>No se pudo agregar el contrato.'
						})

				if _curso:
					_tipo_cont, created = TipoContrato.objects.get_or_create(
							nombre = fila['tipoC']
						)

					_contrato, created = Contrato.objects.get_or_create(
							fk_curso=_curso,
							tipo=fila['tipo'],
							fk_tipocont=_tipo_cont
						)
					_contrato.save()

					# print _contrato, '\n'
					pass

				pass

			options.update(default_options)
			options.update({'errores': errores, 'success': True})
			return render(request, TEMPLATE_FORM_CSV, options)
			pass
		else: # mostrar el formulario
			dpto = dpto[:20]
			departamento = get_object_or_404(Departamento, nick=dpto)

			if Curso.objects.filter(fk_area__fk_departamento=departamento).count() <= 0:
				# al parecer no hay cursos para ese departamento
				errores.append({
						'propiedad': 'Imposible continuar',
						'descripcion': 'No hay cursos registrados para este departamento.'
					})
				options.update({'errores': errores})
				options.update({'desactivar': True})
				pass

			lista_ciclos = Ciclo.objects.all()

			options.update(default_options)
			options.update({'departamento': departamento})
			options.update({'lista_ciclos': lista_ciclos})

			return render(request, TEMPLATE_FORM_CSV, options)

@login_required(login_url='/')
def procesar_csv_cursos(request, dpto):
	if request.session['rol'] >= 2: # es jefedep o mayor
		default_options = {'titulo_tipo':'Cursos', 'form_size': 'medium'}
		options = {}

		if request.method == 'POST': # se envio a traves del formulario
			try:
				post_departamento = request.POST.get('depto', '')
				_departamento = get_object_or_404(Departamento, nick=post_departamento)

				post_ciclo = request.POST.get('ciclo-esc', '')
				_ciclo = get_object_or_404(Ciclo, id=post_ciclo)
				pass
			except Exception, e:
				errores.append({
						'propiedad': 'Departamento/Ciclo',
						'descripcion': 'Hubo un error con alguno de los campos.'
					})
				pass

			errores = [] # inicializa errores
			cursos = [] # inicializa el objeto para los cursos

			try:
				archivo_csv = request.FILES['archivo-csv']

				if not archivo_csv or archivo_csv.content_type != 'text/csv':
					ciclos = Ciclo.objects.all()
					errores.append({
							'propiedad': 'Archivo',
							'descripcion': 'Tipo de archivo no valido.'
						})
					archivo_csv = None

					options.update(default_options)
					options.update({'errores': errores})
					options.update({'departamento': _departamento})
					options.update({'lista_ciclos': ciclos})

					return render(request, TEMPLATE_FORM_CSV, options)
					pass

				datos = unicode(archivo_csv.read()).replace('\r\n', '\n').replace('\n',';;')
				# Compatibilidad tanto para fin de linea de Windows como de Linux
				# (esperemos que nunca ocurra que alguien modifique el archivo en Mac)

				pass
			except Exception, e:
				ciclos = Ciclo.objects.all()
				errores.append(
					{
						'propiedad': 'Archivo',
						'descripcion': 'No se selecciono un archivo.'
					})

				options.update(default_options)
				options.update({'errores': errores})
				options.update({'departamento': _departamento})
				options.update({'lista_ciclos': ciclos})

				return render(request, TEMPLATE_FORM_CSV, options)

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

				_area, created = Area.objects.get_or_create(
						nombre=x['area'], 
						fk_departamento=_departamento
					)

				_materia, created = Materia.objects.get_or_create(
						clave=x['clave'], 
						nombre=x['materia'], 
						fk_departamento = _departamento
					)

				_materia.fk_area.add(_area) # Agrega el area al campo m2m
				_materia.save()

				# return HttpResponse(_materia) # DEBUG

				# Preparaciones para Profesor
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
					codigo_prof = None
					pass
				# FIN PREPARACIONES

				_profesor, created = Profesor.objects.get_or_create(
						codigo_udg=codigo_prof, 
						nombre=profesor['nombre'], 
						apellido=profesor['apellidos']
					)

				_edificio, created = Edificio.objects.get_or_create(id=x['edif'])

				_aula, created = Aula.objects.get_or_create(
						nombre=x['aula'], 
						fk_edif=_edificio
					)

				_seccion, created = Seccion.objects.get_or_create(id=x['secc'])

				# PREPARACIONES HORA >> INICIO
				if re.search( '\d+', x['ini'] ) is not None:
					temp_hora = re.search('(?P<hora>\d{,2})(?P<min>\d{,2})', x['ini'])
					hora_ini = str(temp_hora.group('hora')) + ':' + str(temp_hora.group('min'))
					pass
				else:
					hora_ini = None

				if re.search( '\d+', x['fin'] ) is not None:
					temp_hora = re.search('(?P<hora>\d{,2})(?P<min>\d{,2})', x['fin'])
					hora_fin = str(temp_hora.group('hora')) + ':' + str(temp_hora.group('min'))
					pass
				else:
					hora_fin = None
				# PREPARACIONES HORA >> FIN

				_horario, created = Horario.objects.get_or_create(
						hora_ini = hora_ini,
						hora_fin = hora_fin,
						L = x['dias']['lun'],
						M = x['dias']['mar'],
						I = x['dias']['mie'],
						J = x['dias']['jue'],
						V = x['dias']['vie'],
						S = x['dias']['sab'],
						fk_edif = _edificio,
						fk_aula = _aula
					)

				# return HttpResponse(_horario) # DEBUG

				# FINALMENTE!
				_curso = Curso(
						NRC=x['nrc'], 
						fk_profesor=_profesor, 
						fk_materia=_materia, 
						fk_area=_area,
						fk_secc=_seccion,
						fk_ciclo=_ciclo
					)

				_curso.fk_horarios.add(_horario)
				_curso.save();
				# return HttpResponse(_curso) #YOLO
				pass

			options.update(default_options)
			options.update({'errores': errores})
			options.update({'success': True})

			return render(request, TEMPLATE_FORM_CSV, options)
			# return JsonResponse(cursos, safe=False); # temporal.
			pass
		else:
			dpto = dpto[:20]
			departamento = get_object_or_404(Departamento, nick=dpto)
			lista_ciclos = Ciclo.objects.all()
			
			options.update(default_options)
			options.update({'departamento': departamento})
			options.update({'lista_ciclos': lista_ciclos})

			return render(request, TEMPLATE_FORM_CSV, options)

	else:
		return redirect('error403', origen=request.path)

@login_required(login_url='/')
def sistema_modifica_nrc(request, dpto, ciclo, nrc):
	if request.session['rol'] >= 2:
		options = {'dpto': dpto, 'ciclo': ciclo, 'nrc': nrc}

		return render(request, 'Departamentos/modifica_curso_individual.html', options)
		pass
	else:
		return redirect('error403', origen=request.path)

# @login_required(login_url='/')
# def computacion_form_asistencias(request):
# 	if request.session['rol'] >= 2:
# 		if request.method == 'POST':

# 			criterios = ['si', 'si', 'si', 'si', 'si', 'si']

# 			return render(request, 'reporte-asist.html', 
# 				{
# 					'departamento' : 'Departamento de Ciencias Computacionales',
# 					'nombre' : 'Juan Perez Rodriguez', 
# 					'codigo' : request.POST.get('field-codprof'), 
# 					'calif' : 'excelente',
# 					'ciclo' : '2015-A',
# 					'criterios' : criterios, 
# 					'fecha' : 'HOY', 
# 					'nombrefirma' : 'Luisa Hermandia Limbo', 
# 					'puesto' : 'Profesional'
# 				})
# 		else:
# 			return render(request, 'form-reporte-asistencias.html');
# 	else:
# 	    return redirect('error403', origen=request.path)