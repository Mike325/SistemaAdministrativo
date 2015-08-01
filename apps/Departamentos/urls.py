from django.conf.urls import include, url

from .views import *
# Vistas de la app

app_dep_urls = [
	url(r'^(?P<dpto>.+)/sistema/csv/$', procesar_csv),
	url(r'^(?P<dpto>.+)/sistema/csv/subir$', procesar_csv),
	url(r'^(?P<dpto>.+)/ver_cursos/$', ver_cursos),
	url(r'^(?P<dpto>.+)/consulta/(?P<ciclo>.+)$', sistema_consulta),
	url(r'^(?P<dpto>.+)/modifica/(?P<ciclo>.+)/(?P<nrc>)$', sistema_modifica_nrc),
	url(r'^(?P<dpto>.+)/modifica_curso/(?P<nrc>.+)/(?P<ajax>.*)$', modifica_curso)
]