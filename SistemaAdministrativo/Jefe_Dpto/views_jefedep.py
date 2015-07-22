from django.http import HttpResponse
from django.shortcuts import render

def inicio_jefedep(request):
	return render(request, 'inicio-jefedep.html', { 'banner': True });

def computacion_sistema_subircsv(request):
	return render(request, 'form-subircsv.html');

def computacion_sistema_consulta_modifica(request):
	return HttpResponse('<strong>En construccion o no aplicable por el momento</strong>');

def computacion_form_asistencias(request):
	if request.method == 'POST':

		criterios = ['si', 'si', 'si', 'si', 'si', 'si']

		return render(request, 'reporte-asist.html', {
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

def usuarios_gestionar(request):
	return HttpResponse('<strong>En construccion o no aplicable por el momento</strong>');