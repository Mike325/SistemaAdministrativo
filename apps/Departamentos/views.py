from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def inicio_jefedep(request):
	if request.session['rol'] >= 2:
		return render(request, 'inicio-jefedep.html', { 'banner': True });
	else:
	   	return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def computacion_sistema_subircsv(request):
	if request.session['rol'] >= 2:
		return render(request, 'form-subircsv.html');
	else:
	   	return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def computacion_sistema_consulta_modifica(request):
	if request.session['rol'] >= 2:
		return HttpResponse('<strong>En construccion o no aplicable por el momento</strong>');
	else:
	    return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def computacion_form_asistencias(request):
	if request.session['rol'] >= 2:
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
	else:
	    return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def usuarios_gestionar(request):
	if request.session['rol'] >= 2:
		return HttpResponse('<strong>En construccion o no aplicable por el momento</strong>');
	else:
	    return render(request, 'PermisoDenegado.html')