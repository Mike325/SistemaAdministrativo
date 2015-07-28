from django.conf.urls import include, url
from django.contrib import admin

from views_secretaria import *

url_secretaria = [
	url(r'^inicio-secretaria/$', inicio_secretaria, name='inicio_secretaria'),
	url(r'^(.+)/listas/tCompleto$', listas_tCompleto),
	url(r'^(.+)/listas/tMedio$', listas_tMedio),
	url(r'^(.+)/form-incidencias$', form_incidencias),
	url(r'^(.+)/reporte-incidencias$', incidencias)
]