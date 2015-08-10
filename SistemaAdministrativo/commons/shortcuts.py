# Similar a django.shortcuts, pretende proveer de metodos y clases
# utiles y/o automatizar procesos largos que tienden a repetirse
# a lo largo de todo el codigo.

from functools import wraps
from django.shortcuts import render, redirect
from apps.Departamentos.models import Departamento

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

def sidebar_context(request):
    return{
        'lista_departamentos' : Departamento.objects.all(),
    }

def verifica_dpto(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        try:
            dptoObjeto = Departamento.objects.get(jefeDep__user__username=request.session['usuario']['nick'])
            print dptoObjeto.nick
            print kwargs
            if dptoObjeto.nick == kwargs['dpto']:
                return view(request, *args, **kwargs)
            else:
                return redirect('/')
        except:
            if request.session['usuario']['rol']>2:
                return view(request, *args, **kwargs)
            else:
                return redirect('/')
    return wrapper