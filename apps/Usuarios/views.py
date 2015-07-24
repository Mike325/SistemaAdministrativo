# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib import auth
# Create your views here.


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

            #Se asigna una variable de sesión para poder acceder a ella desde cualquier página
            request.session['usuario'] = usuario
            request.session['rol'] = user.usuario.rol.id
            
            if request.session['rol'] == 1:
                return redirect('/inicio-secretaria/')
            elif request.session['rol'] == 2:
                return redirect('/inicio-jefedep/')
            else:
                return redirect('/inicio-administrador/')
        else:
            return render(request,'login.html', {'errors': "Usuario o contraseña incorrectos"})
    else:
        return render(request,'login.html')

def logout(request):
    try:
        auth.logout(request)
    except KeyError:
        pass
    return redirect('/')
    