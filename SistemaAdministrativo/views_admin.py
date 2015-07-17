from django.shortcuts import render

def inicio_admin(request):
	return render(request, 'inicio-administrador.html', { 'banner' : True })

def sistema_modificar_jefedep(request):
	return render(request, 'modificar-jefe-departamento.html')