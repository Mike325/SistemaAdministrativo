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

@login_required(login_url='/')
def nueva_secretaria(request):
    if request.session['rol'] >= 2:
        if request.method == 'POST':
            usuario = request.POST.get('username','')
            password = request.POST.get('password', '')
            codigo = request.POST.get('codigo','')
            nombre = request.POST.get('nombre','')
            apellido = request.POST.get('apellido','')
            correo = request.POST.get('correo', '')
            if User.objects.filter(username = usuario ).exists():
                errors = 'Ya existe registro con ese nombre'
                return render(request,'nueva_secretaria.html',locals())
            else:
                nuevo_usuario = Usuario.alta_secretaria(usuario, password, nombre, 
                                                    apellido, correo, codigo)
                nuevo_usuario.save()
                return redirect('/inicio-administrador/')
        else:
            return render(request, 'nueva_secretaria.html')
    else:
        return render(request, 'PermisoDenegado.html')