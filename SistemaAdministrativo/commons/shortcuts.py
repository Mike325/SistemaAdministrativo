# Similar a django.shortcuts, pretende proveer de metodos y clases
# utiles y/o automatizar procesos largos que tienden a repetirse
# a lo largo de todo el codigo.

from django.shortcuts import render, redirect

def panelInicio(request):
    if request.user.is_authenticated():
        if request.session['rol'] == 1:
            return redirect('inicio_secretaria')
        elif request.session['rol'] == 2:
            return redirect('inicio_jefedep')
        else:
            return redirect('inicio_admin')
    else:
        return redirect('/')