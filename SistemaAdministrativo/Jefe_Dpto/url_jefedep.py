# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

from views_jefedep import *
from apps.Departamentos.urls import *

url_jefedep = [
    url(r'^inicio-jefedep/$', inicio_jefedep, name='inicio_jefedep'),
	url(r'^nueva_secretaria/$', nueva_secretaria, name='nueva_secretaria'),

]

url_jefedep += app_dep_urls
# añade las urls de la app del Departamento