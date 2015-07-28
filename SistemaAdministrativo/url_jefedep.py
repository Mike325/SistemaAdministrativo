from django.conf.urls import include, url
from django.contrib import admin

from apps.Departamentos.views import *

url_jefedep = [
	url(r'^inicio-jefedep/$', inicio_jefedep),
	url(r'^computacion/sistema/csv$', computacion_sistema_subircsv),
	url(r'^computacion/sistema/consulta$', computacion_sistema_consulta_modifica),
	url(r'^computacion/formatos/form-asistencias$', computacion_form_asistencias),
	url(r'^usuarios/gestionar$', usuarios_gestionar),
]