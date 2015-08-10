# -*- coding: utf-8 -*-
'''CAMPOS PARA SUPLENTES'''
FieldSet_Suplente = []
FieldSet_Suplente.append({
		'label': 'NRC',
		'id': 'in-nrc',
		'value': 'fk_curso.NRC',
		'send': False,
		'disable': True,
		'size': 2
	})
FieldSet_Suplente.append({
		'label': 'Clave',
		'id': 'in-cvemat',
		'value': 'fk_curso.fk_materia.clave',
		'send': False,
		'disable': True,
		'size': 2
	})
FieldSet_Suplente.append({
		'label': 'Materia',
		'id': 'in-materia',
		'value': 'fk_curso.fk_materia.nombre',
		'send': False,
		'disable': True,
		'size': 8
	})
FieldSet_Suplente.append({
		'label': 'SECC',
		'id': 'in-secc',
		'value': 'fk_curso.fk_secc',
		'send': False,
		'disable': True,
		'max_length': 5,
		'size': 2
	})
FieldSet_Suplente.append({
		'label': 'Profesor',
		'id': 'in-profesor',
		'value': 'fk_curso.fk_profesor',
		'send': False,
		'disable': True,
		'size': 5
	})
FieldSet_Suplente.append({
		'label': 'Suplente',
		'id': 'in-supp',
		'send': False,
		'value': 'fk_profesor',
		'rel': 'in-codigo',
		'size': 5
	})
FieldSet_Suplente.append({
		'id': 'in-codigo',
		'type': 'hidden',
		'value': 'fk_profesor.codigo_udg',
		'set': 'fk_suplente',
		'model': 'Profesor',
		'filter': 'codigo_udg'
	})
FieldSet_Suplente.append({
		'rootclass': 'rango-fecha',

		'label': 'Inicio suplencia',
		'id': 'in-periodo-ini',
		'class': 'date start',
		'value': 'periodo_ini',
		'set': 'periodo_ini',
		'size': 3
	})
FieldSet_Suplente.append({
		'rootclass': 'rango-fecha',

		'label': 'Fin suplencia',
		'id': 'in-periodo-fin',
		'class': 'date end',
		'value': 'periodo_fin',
		'set': 'periodo_fin',
		'size': 3
	})
FieldSet_Suplente.append({
		'rootclass': 'end',
		'rootstyle': 'padding-top: 27px;',

		'checklabel': 'Vigente todo el ciclo.',
		'id': 'in-full-periodo',
		'type': 'checkbox',
		'value': 'periodo_fin==None',
		'rel': 'in-periodo-ini, in-periodo-fin',
		'size': 3
	})

'''CAMPOS PARA CICLOS'''
FieldSet_Ciclo = []
FieldSet_Ciclo.append({
		'label': 'Nombre ciclo',
		'id': 'in-id-ciclo',
		'value': 'id',
		# 'send': False,
		# 'disable': True,
		'max_length': 5,
		'size': 4
	})
FieldSet_Ciclo.append({
		'rootclass': 'rango-fecha',
		
		'label': 'Fecha inicio',
		'id': 'in-ciclo-ini',
		'value': 'fecha_ini',
		'class': 'date start',
		'size': 5
	})
FieldSet_Ciclo.append({
		'rootclass': 'rango-fecha',
		
		'label': 'Fecha fin',
		'id': 'in-ciclo-fin',
		'value': 'fecha_fin',
		'class': 'date end',
		'size': 5
	})

'''CAMPOS PARA PROFESORES'''
FieldSet_Profesor = []
FieldSet_Profesor.append({
		'id': 'in-codigo',
		'value': 'codigo_udg',
		'send': False,
		'disable': True,
		'size': 3
	})
FieldSet_Profesor.append({
		'id': 'in-apellido',
		'value': 'apellido',
		'max_length': 50,
		'size': 4
	})
FieldSet_Profesor.append({
		'id': 'in-nombre',
		'value': 'nombre',
		'max_length': 50,
		'size': 5
	})