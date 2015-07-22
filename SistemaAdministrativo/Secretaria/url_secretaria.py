from django.conf.urls import include, url
from django.contrib import admin

from views_secretaria import *

url_secretaria = [
	url(r'^inicio-secretaria/$', inicio_secretaria),
	url(r'^(computacion|electronica)/listas/tCompleto$', listas_tCompleto),
	url(r'^(computacion|electronica)/listas/tMedio$', listas_tMedio),
	url(r'^(computacion|electronica)/form-incidencias$', form_incidencias),
	url(r'^(computacion|electronica)/reporte-incidencias$', incidencias),
]