[1mdiff --git a/templates/home.html b/templates/home.html[m
[1mdeleted file mode 100644[m
[1mindex 08bdd69..0000000[m
[1m--- a/templates/home.html[m
[1m+++ /dev/null[m
[36m@@ -1,130 +0,0 @@[m
[31m-{% extends 'base.html' %}[m
[31m-[m
[31m-{% block title %}[m
[31m-    Home[m
[31m-{% endblock %}[m
[31m-[m
[31m-{% block usuario %}[m
[31m-    Administrador[m
[31m-{% endblock %}[m
[31m-[m
[31m-{% block navegacion %}[m
[31m-    <li><a href="#">Secretaria</a></li>[m
[31m-    <li><a href="#">Jefe de departamento</a></li>[m
[31m-    <li><a href="#">Administrador</a></li>[m
[31m-{% endblock %}[m
[31m-[m
[31m-{% block content %}[m
[31m-    <div class="row">[m
[31m-        <div class="large-4 medium-6 small-12 columns">[m
[31m-            <div class="division-banner">[m
[31m-                <img src="/static/img/logos_carreras/computacion.png">[m
[31m-            </div>[m
[31m-            <div class="large-12 colums panel">[m
[31m-                <h3 class="text-center">Computación<h3>[m
[31m-                <div class="row">[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                </div>[m
[31m-            </div>[m
[31m-        </div>[m
[31m-        <div class="large-4 medium-6 small-12 columns">[m
[31m-            <div class="division-banner">[m
[31m-                <img src="/static/img/logos_carreras/electronica.png">[m
[31m-            </div>[m
[31m-            <div class="large-12 colums panel">[m
[31m-                <h3 class="text-center">Electrónica<h3>[m
[31m-                <div class="row">[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                </div>[m
[31m-            </div>[m
[31m-        </div>[m
[31m-        <div class="large-4 medium-6 small-12 columns">[m
[31m-            <div class="division-banner">[m
[31m-                <img src="/static/img/logos_carreras/informatica.png">[m
[31m-            </div>[m
[31m-            <div class="large-12 colums panel">[m
[31m-                <h3 class="text-center">Informática<h3>[m
[31m-                <div class="row">[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                </div>[m
[31m-            </div>[m
[31m-        </div>[m
[31m-        <div class="large-4 medium-6 small-12 columns">[m
[31m-            <div class="division-banner">[m
[31m-                <img src="/static/img/logos_carreras/biomedica.png">[m
[31m-            </div>[m
[31m-            <div class="large-12 colums panel">[m
[31m-                <h3 class="text-center">Biomédica<h3>[m
[31m-                <div class="row">[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                </div>[m
[31m-            </div>[m
[31m-        </div>[m
[31m-        <div class="large-4 medium-6 small-12 columns">[m
[31m-            <div class="division-banner">[m
[31m-                <img src="/static/img/logos_carreras/robotica.png">[m
[31m-            </div>[m
[31m-            <div class="large-12 colums panel">[m
[31m-                <h3 class="text-center">Robótica<h3>[m
[31m-                <div class="row">[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                    <div class="large-6 columns">[m
[31m-                        <button class="button expand">Función</button>[m
[31m-                    </div>[m
[31m-                </div>[m
[31m-            </div>[m
[31m-        </div>[m
[31m-    </div>[m
[31m-{% endblock %}[m
\ No newline at end of file[m
