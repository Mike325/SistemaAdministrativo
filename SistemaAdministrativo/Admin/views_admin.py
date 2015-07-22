# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

#Verificar si el usuario tiene permisos para estas vistas, por el momento sólo pide que esté logeado

@login_required(login_url='/login/')
def inicio_admin(request):
	return render(request, 'inicio-administrador.html', { 'banner' : True })

@login_required(login_url='/login/')
def sistema_modificar_jefedep(request):
	return render(request, 'modificar-jefe-departamento.html')

@login_required(login_url='/login/')
def nuevo_departamento(request):
	return render(request, 'nuevo_departamento.html')