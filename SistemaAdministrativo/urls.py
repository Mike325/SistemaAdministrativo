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

from Secretaria.url_secretaria import *
from Jefe_Dpto.url_jefedep import *
from Admin.url_admin import *

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
]

urlpatterns += url_secretaria + url_jefedep + url_admin