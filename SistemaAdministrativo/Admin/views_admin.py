# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.Departamentos.models import Departamento
from apps.Usuarios.models import Usuario, Rol
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
    errors = 'No hay jefes de departamento disponibles, crear uno antes de seguir con la modificación de jefe de departamento'
    if request.session['rol'] == 3:
        if request.method == 'POST':
            post_nombreDepartamento = request.POST.get('departamento', '')
            departamento = Departamento.objects.get(nombre=post_nombreDepartamento)
            try:
                jefeActual = departamento.jefeDep
                opcionesJefeDepartamento = Usuario.objects.filter(rol = 2).filter(departamento = None)
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
            post_jefeActual = post_jefeActual.split(',', 1)
            post_nuevoJefe = post_nuevoJefe.split(',', 1)
            #Hacer query del objeto del jefe actual y desactivarlo (?)
                #jefeActual_user = User.objects.get(username = post_jefeActual)
                #jefeActual = Usuario.objects.get(user = jefeActual_user)
            #Hacer query del nuevo jefe (user y usuario) y ponerlo como activo
            nuevoJefe_user = User.objects.get(last_name = post_nuevoJefe[0])
            nuevoJefe = Usuario.objects.get(user = nuevoJefe_user)
            #Query del departamento del jefe actual
            departamento = Departamento.objects.get(nombre = post_departamento)
            #Sustitución del jefe actual por el nuevo
            departamento.jefeDep = nuevoJefe
            #Desactivar al antiguo jefe de departamento
            #Guardar los cambios en la base de datos
                #jefeActual.save()
            departamento.save()
        return redirect('/inicio-administrador/')
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def nuevo_departamento(request):
    if request.session['rol'] == 3:
        #Revisar si se entra a la página por POST
        if request.method == 'POST':
            #Obtener los campos del nuevo departamento
            post_codigo = request.POST.get('id','')
            post_nombre = request.POST.get('nombre', '')
            post_nuevoJefe = request.POST.get('nuevoJefe', '')
            post_nuevoJefe = post_nuevoJefe.split(',', 1)
            #Crear el nuevo departamento
            nuevoJefe_user = User.objects.get(last_name = post_nuevoJefe[0])
            nuevoJefe = Usuario.objects.get(user = nuevoJefe_user)
            nuevoDepartamento = Departamento(id = post_codigo, nombre = post_nombre, jefeDep = nuevoJefe)
            #Guardar en la base de datos el nuevo departamento
            nuevoDepartamento.save()
            return redirect('/inicio-administrador/')
        #Si no se entra con POST, se regresa el formulario de nuevo departamento
        else:
            errors = 'No hay jefes de departamento disponibles, crear uno antes de seguir con la creación de departamento'
            opcionesJefeDepartamento = Usuario.objects.filter(rol = 2).filter(departamento = None)
            return render(request, 'nuevo_departamento.html', locals())
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def nuevo_jefe(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            usuario = request.POST.get('username','')
            password = request.POST.get('password', '')
            codigo = request.POST.get('codigo','')
            nombre = request.POST.get('nombre','')
            apellido = request.POST.get('apellido','')
            if User.objects.filter(username = usuario ).exists():
                errors = 'Ya existe registro con ese nombre'
                return render(request,'nuevo_jefeDep.html',locals())
            else:
                Jefe_rol = Rol.objects.get(id = 2 )
                usuario_user = User.objects.create_user(username=usuario, first_name=nombre, 
                                                        last_name=apellido, password = password)
                Jefe_usuario = Usuario(user=usuario_user, codigo=codigo, rol=Jefe_rol)
                usuario_user.save()
                Jefe_usuario.save()
                return redirect('/inicio-administrador/')
        else:
            return render(request, 'nuevo_jefeDep.html')
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def activar_usuarios(request):
    if request.session['rol'] == 3:
        usuarios = User.objects.all();
        return render(request, 'activar_usuarios.html', locals())
