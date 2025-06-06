"""
URL configuration for ToDoList project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('apy/', views.apy, name='apy'),
    path('apy/create/', views.create_apy, name='create_apy'),
    path('logout/', views.salida, name='logout'),
    path('autenticar/', views.autenticar, name='autenticar'),
    path('apy/calendario/', views.calendario_apy, name='calendario_apy'),
    path('gerente/usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('gerente/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('gerente/usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('gerente/usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('gestionar/', views.gestionar, name='gestionar'),
    path('gerente/tareas/', views.gestionar_tareas, name='gestionar_tareas'),
    path('gerente/tareas/editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('gerente/tareas/eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tarea/<int:tarea_id>/completar/', views.completar_tarea, name='completar_tarea'),



 
]
