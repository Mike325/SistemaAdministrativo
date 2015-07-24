# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.Departamentos.models import Departamento
from apps.Usuarios.models import Usuario
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

#Verificar si el usuario está logeado, en caso contrario, redirecciona a página de log in
@login_required(login_url='/')
def inicio_admin(request):
    #revisa que el usuario tenga permisos necesarios para ver el contenido de esta página
    departamentos = Departamento.objects.all()
    if request.session['rol'] == 3:
        banner = True
        return render(request, 'inicio-administrador.html', locals())
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def form_sistema_modificar_jefedep(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            post_nombreDepartamento = request.POST.get('departamento', '')
            departamento = Departamento.objects.get(nombre=post_nombreDepartamento)
            jefeDepartamento_user = User.objects.filter(is_active=True)
            try:
                jefeDepartamento = Usuario.objects.filter(user=jefeDepartamento_user).get(jefeDep=departamento)
                opcionesJefeDepartamento = Usuario.objects.filter(jefeDep = departamento)
            except ObjectDoesNotExist:
                errors = "No existen jefes de este departamento, favor de crear uno"
                return render(request, 'modificar-jefe-departamento.html', locals())
            return render(request, 'modificar-jefe-departamento.html', locals())
        else:
            return redirect('/inicio-administrador/')
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def sistema_modificar_jefedep(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            #Tomar valores del POST
            post_jefeActual = request.POST.get('jefeActual', '')
            post_departamento = request.POST.get('departamento', '')
            post_nuevoJefe = request.POST.get('nuevoJefe', '')
            #Hacer query del objeto del jefe actual y desactivarlo
            jefeActual = User.objects.get(username = post_jefeActual)
            jefeActual.is_active = False
            jefeActual.save()
            #Hacer query del nuevo jefe (user y usuario) y ponerlo como activo
            nuevoJefe_user = User.objects.get(username = post_nuevoJefe)
            nuevoJefe = Usuario.objects.get(user = nuevoJefe_user)
            nuevoJefe_user.is_active = True
            nuevoJefe_user.save()
            nuevoJefe.save()
        return redirect('/inicio-administrador/')
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def nuevo_departamento(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            codigo = request.POST.get('id','')
            nombre = request.POST.get('nombre', '')
            nuevoDepartamento = Departamento(id = codigo, nombre = nombre)
            nuevoDepartamento.save()
            return redirect('/inicio-administrador/')
        else:
            return render(request, 'nuevo_departamento.html')
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def activar_usuarios(request):
    if request.session['rol'] == 3:
        return render(request, 'activar_usuarios.html')
    else:
        return render(request, 'PermisoDenegado.html')
