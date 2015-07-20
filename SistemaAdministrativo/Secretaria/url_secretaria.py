from django.conf.urls import include, url
from django.contrib import admin

from views_secretaria import *

url_secretaria = [
	url(r'^inicio-secretaria/$', inicio_secretaria),
	url(r'^(computacion|electronica|biomedica|robotica|informatica)/listas/tCompleto$', listas_tCompleto),
	url(r'^(computacion|electronica|biomedica|robotica|informatica)/listas/tMedio$', listas_tMedio),
	url(r'^(computacion|electronica|biomedica|robotica|informatica)/form-incidencias$', form_incidencias),
	url(r'^(computacion|electronica|biomedica|robotica|informatica)/reporte-incidencias$', incidencias),
]