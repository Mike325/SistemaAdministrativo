# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib import auth

from SistemaAdministrativo.commons.shortcuts import panelInicio
from apps.Usuarios.models import Usuario

def login(request):
    if request.method == 'POST':
        #Tomar los valores mandados al hacer log in
        usuario = request.POST.get('username','')
        password = request.POST.get('pass','')
        
        #Autentificar que el usuario exista
        user = auth.authenticate(username=usuario, password=password)

        #Si el usuario existe  y está activo, se inicia la sesión
        if user is not None and user.is_active:
            auth.login(request, user)

            usuario = Usuario.objects.get(user=user)
            usuario = {
                    'nick': usuario.user.username,
                    'correo': usuario.user.email,
                    'nombre': usuario.user.first_name,
                    'apellidos': usuario.user.last_name,
                    'codigo': usuario.codigo,
                    'rol': usuario.rol.id
                }

            #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
            request.session['usuario'] = usuario
            request.session['rol'] = user.usuario.rol.id
            request.session['just_logged'] = True

            return panelInicio(request)
        else:
            return render(request,'login.html', {'errors': "Usuario o contraseña incorrectos"})
    else:
        if request.user.is_authenticated():
            return panelInicio(request)
        else:
            return render(request,'login.html')

def logout(request):
    try:
        auth.logout(request)
    except KeyError:
        pass
    return redirect('/')
    