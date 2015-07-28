# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.Historicos.models import Registro
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

@login_required(login_url="/")
def historicos(request):
    if request.session['rol'] >= 2:
        registros = Registro.objects.all().order_by("fechaModificacion").order_by("-horaModificacion")
        paginator = Paginator(registros, 50)
        pagina = request.GET.get('pagina')
        try:
            registros = paginator.page(pagina)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            registros = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            registros = paginator.page(paginator.num_pages)
        return render(request, 'historicos.html', locals())
    else:
        return redirect('error403', origen=request.path)

@login_required(login_url="/")
def historicosFiltrados(request):
    if request.session['rol'] >= 2:
        if request.method == 'POST':
            fecha = request.POST.get('fecha','')
            fecha_expr = re.compile('[\d]{4}-[\d]{2}-[\d]{2}')
            res = fecha_expr.match(fecha)
            if res:
                registros = Registro.objects.filter(fechaModificacion=fecha).order_by("-horaModificacion")
                return render(request, 'historicos.html', locals())
            else:
                registros = Registro.objects.all().order_by("fechaModificacion").order_by("-horaModificacion")
                errors = "Ingresa una fecha válida"
                return render(request, 'historicos.html', locals())
        else:
            return redirect('/historicos/')
    else:
        return redirect('error403', origen=request.path)