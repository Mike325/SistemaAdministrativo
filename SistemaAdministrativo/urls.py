"""SistemaAdministrativo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from views import *
from views_jefedep import *
from views_admin import *

"""
TODO:
    + Convertir los enlaces a dinamicos
        (que con poner 'computacion' como una variable, el sistema haga 
         la gestion necesaria automaticamente para llegar a la vista indicada
         y asi para los demas departamentos)
    + Mandar las urls a archivos separados (?)
        (estilo lo que se hacia con las apps para importar sus propias urls)
"""

urlpatterns = [
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^ejemplo/$', ejemplo),

    url(r'^inicio-secretaria/$', inicio_secretaria),
    url(r'^computacion/listas/tCompleto$', computacion_listas_tCompleto),
    url(r'^computacion/listas/tMedio$', computacion_listas_tMedio),
    url(r'^computacion/form-incidencias$', form_incidencias),
    url(r'^computacion/reporte-incidencias$', incidencias),

    url(r'^inicio-jefedep/$', inicio_jefedep),
    url(r'^computacion/sistema/csv$', computacion_sistema_subircsv),
    url(r'^computacion/sistema/consulta$', computacion_sistema_consulta_modifica),
    url(r'^computacion/formatos/form-asistencias$', computacion_form_asistencias),
    url(r'^usuarios/gestionar$', usuarios_gestionar),

    url(r'^inicio-administrador/$', inicio_admin),
    url(r'^sistema/modificar/jefe-departamento', sistema_modificar_jefedep),
    url(r'^nuevo_departamento',nuevo_departamento),
    
]
