# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from apps.Departamentos.models import Departamento
from apps.Usuarios.models import Usuario, Rol
from apps.Historicos.models import Registro
#Verificar si el usuario está logeado, en caso contrario, redirecciona a página de log in
@login_required(login_url='/')
def inicio_admin(request):
    #revisa que el usuario tenga permisos necesarios para ver el contenido de esta página
    departamentos = Departamento.objects.all()
    if request.session['rol'] == 3:
        banner = True
        bienvenida = False

        if request.session['just_logged']:
            bienvenida = True
            request.session['just_logged'] = False
            
        departamentos = Departamento.objects.all()
        return render(request, 'inicio-administrador.html', locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def form_sistema_modificar_jefedep(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            errors = "No existen jefes de este departamento, favor de crear uno."
            post_nombreDepartamento = request.POST.get('departamento', '')
            departamento = Departamento.objects.get(nombre=post_nombreDepartamento)
            try:
                jefeActual = departamento.jefeDep
                opcionesJefeDepartamento = Usuario.objects.filter(user__is_active=True, rol__id__gte=1, departamento=None)
            except ObjectDoesNotExist:
                errors = "No existen jefes de este departamento, favor de crear uno."
            return render(request, 'modificar-jefe-departamento.html', locals())
        else:
            return redirect('/inicio-administrador/')
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def sistema_modificar_jefedep(request):
    if request.session['rol'] == 3:
        if request.method == 'POST':
            #Tomar valores del POST
            post_jefeActual = request.POST.get('jefeActual', '')
            post_departamento = request.POST.get('departamento', '')
            post_nuevoJefe = request.POST.get('nuevoJefe', '')

            #¿Qué hacer con el antiguo jefe de departamento?
            username_jefeActual = post_jefeActual.split(",",1)[0]
            jefeActual = Usuario.objects.get(user__username=username_jefeActual)

            #Query del objeto del nuevo jefe
            nuevoJefe = Usuario.objects.get(user__username = post_nuevoJefe)

            #Query del departamento del jefe actual
            departamento = Departamento.objects.get(nombre = post_departamento)

            #Sustitución del jefe actual por el nuevo
            departamento.jefeDep = nuevoJefe

            #Guardar los cambios en la base de datos
            departamento.save()

            registro = Registro.modificacion(request.session['usuario']['nick'],
                        'Se cambio el jefe del departamento "'+
                        post_departamento+'" de "'+jefeActual.user.get_full_name()+
                        '" a "'+nuevoJefe.user.get_full_name()+'"', jefeActual,
                        nuevoJefe, 'Departamentos')
            registro.save()

        return redirect('/inicio-administrador/')
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url='/')
def nuevo_departamento(request):
    if request.session['rol'] == 3:
        #Revisar si se entra a la página por POST
        if request.method == 'POST':
            #Obtener los campos del nuevo departamento
            post_abreviacion = request.POST.get('abreviacion','')
            post_nombre = request.POST.get('nombre', '')
            post_nuevoJefe = request.POST.get('nuevoJefe', '')
            
            #Hacer query del nuvo jefe
            nuevoJefe = Usuario.objects.get(user__username=post_nuevoJefe)

            #Crear el nuevo departamento
            nuevoDepartamento = Departamento(nick=post_abreviacion, nombre=post_nombre, jefeDep=nuevoJefe)
            
            #Guardar en la base de datos el nuevo departamento
            nuevoDepartamento.save()

            registro = Registro.creacion(request.session['usuario']['nick'],
                        'Se creó el departamento "'+post_nombre+'"'
                        , post_nombre, 'Departamentos')
            registro.save()

            return redirect('/inicio-administrador/')

        #Si no se entra con POST, se regresa el formulario de nuevo departamento
        else:
            errors = 'No hay jefes de departamento disponibles, crear uno antes de seguir con la creación de departamento'
            opcionesJefeDepartamento = Usuario.objects.filter(user__is_active=True, rol__id__gte=1, departamento=None)
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
            correo = request.POST.get('correo', '')
            if User.objects.filter(username = usuario ).exists():
                errors = 'Ya existe registro con ese nombre'
                return render(request,'nuevo_jefeDep.html',locals())
            else:
                nuevo_usuario = Usuario.alta_jefe(usuario, password, nombre, 
                                                    apellido, correo, codigo)
                nuevo_usuario.save()

                registro = Registro.creacion(request.session['usuario']['nick'],
                        'Se creó el jefe de departamento "'+nuevo_usuario.user.get_full_name()+'"'
                        , usuario, 'Usuarios')
                registro.save()

                return redirect('/inicio-administrador/')
        else:
            return render(request, 'nuevo_jefeDep.html')
    else:
        return render(request, 'PermisoDenegado.html')

@login_required(login_url='/')
def activar_usuarios(request):
    if request.session['rol'] == 3:
        usuarios = Usuario.objects.all()
        return render(request, 'activar_usuarios.html', locals())
    else:
        return redirect('error403', origen=request.path)
