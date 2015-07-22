from django.conf.urls import include, url
from django.contrib import admin

from apps.Usuarios.views import *
from views_admin import *

url_admin = [
    url(r'^login/$', login),
    url(r'^logout/$', logout),
	url(r'^inicio-administrador/$', inicio_admin),
    url(r'^sistema/modificar/jefe-departamento', sistema_modificar_jefedep),
    url(r'^nuevo_departamento',nuevo_departamento),
]