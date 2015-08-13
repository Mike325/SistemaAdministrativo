from django.conf.urls import include, url

from .views import * # Vistas de la app

app_dep_urls = [
	url(r'^(?P<dpto>.+)/sistema/csv/cursos/$', procesar_csv_cursos),
	url(r'^(?P<dpto>.+)/sistema/csv/cursos/subir$', procesar_csv_cursos),
	url(r'^(?P<dpto>.+)/sistema/csv/contratos/$', procesar_csv_contratos),
	url(r'^(?P<dpto>.+)/sistema/csv/contratos/subir$', procesar_csv_contratos),

	url(r'^(?P<dpto>.+)/ver_cursos/$', ver_cursos),
	url(r'^(?P<dpto>.+)/modifica_curso/(?P<nrc>.+)/(?P<ajax>.*)$', modifica_curso),

	#url(r'^(?P<dpto>.+)/ciclo/nuevo$', nuevo_ciclo),

	url(r'^(?P<dpto>.+)/suplentes/nuevo$', nuevo_suplente),
	url(r'^(?P<dpto>.+)/suplentes/gestionar$', administrar_suplentes),

	url(r'^sistema/profesores/nuevo$', nuevo_profesor),
	url(r'^sistema/profesores/gestionar$', administrar_profesores),

	#url(r'^(?P<dpto>.+)/ciclos/nuevo$', nuevo_ciclo),
	url(r'^(?P<dpto>.+)/ciclos/gestionar$', administrar_ciclos),

	url(r'^(?P<dpto>.+)/sistema/gestionar/(?P<area>.+)/(?P<area_id>.+)/(?P<ajax>.*)$', gestion_sistema),
]