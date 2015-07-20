from django.conf.urls import include, url
from django.contrib import admin

from views_admin import *

url_admin = [
	url(r'^inicio-administrador/$', inicio_admin),
    url(r'^sistema/modificar/jefe-departamento', sistema_modificar_jefedep),
    url(r'^nuevo_departamento',nuevo_departamento),
]