from django.conf.urls import include, url
from django.contrib import admin

from apps.Usuarios.views import *
from apps.Historicos.views import *

url_admin = [
    url(r'^$', login, name='login'),
    url(r'^login/$', login),
    url(r'^logout/$', logout, name='logout'),
	url(r'^inicio-administrador/$', inicio_admin, name='inicio_admin'),
    url(r'^sistema/modificar/jefe-departamento', form_sistema_modificar_jefedep),
    url(r'^enviar/modificar/jefe-departamento', sistema_modificar_jefedep),
    url(r'^nuevo_departamento',nuevo_departamento),
    url(r'^activar_usuarios',activar_usuarios),
    url(r'^nuevo_jefe',nuevo_jefe),
    url(r'^nueva_secretaria/$', nueva_secretaria),
    url(r'^historicos/$', historicos),
    url(r'^historicos/filtro/$', historicosFiltrados),
]