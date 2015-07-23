# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

#Verificar si el usuario está logeado, en caso contrario, redirecciona a página de log in
@login_required(login_url='/')
def inicio_admin(request):
    #revisa que el usuario tenga permisos necesarios para vier el contenido de esta página
    if request.session['rol'] == 3:
        banner = True
        return render(request, 'inicio-administrador.html', locals())
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def form_sistema_modificar_jefedep(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            return render(request, 'modificar-jefe-departamento.html')
        else:
            return redirect('/inicio-administrador/')
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def sistema_modificar_jefedep(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            #Aquí se modifica el jefe de departamento
            return redirect('/inicio-administrador/')
        return redirect('/inicio-administrador/')
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def nuevo_departamento(request):
    if request.session['rol'] == 3:
        return render(request, 'nuevo_departamento.html')
    else:
        return render(request, 'PermisoDenegado.html')