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