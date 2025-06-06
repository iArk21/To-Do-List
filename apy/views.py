
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ApyForm
from .models import Apy
import json
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import EditarUsuarioForm
from .models import CustomUser
from datetime import date

# Create your views here.

def home(request):
    return  render(request, 'home.html')



def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm()
        })
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            login(request, user)  # Inicia sesión automáticamente
            return redirect('apy')  # Redirige a donde quieras
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Revisa los datos ingresados.'
            })
@login_required
def apy(request):
    tareas = Apy.objects.filter(user=request.user, completada=False)

    tareas_proximas = []
    tareas_urgentes = []

    for tarea in tareas:
        dias_restantes = (tarea.fecha.date() - date.today()).days
        tarea.dias_restantes = dias_restantes  # para mostrar en la plantilla

        if 1 < dias_restantes <= 5:
            tareas_proximas.append(tarea)
        elif dias_restantes <= 1:
            tareas_urgentes.append(tarea)

    return render(request, 'apy.html', {
        'Tareas': tareas,
        'tareas_proximas': tareas_proximas,
        'tareas_urgentes': tareas_urgentes
    })

@login_required
def create_apy(reques):

    if reques.method == 'GET':
        return render(reques, 'create_apy.html',{
            'form' : ApyForm
        })
    else:
        try:
            form = ApyForm(reques.POST)
            new_apy = form.save(commit=False)
            new_apy.user = reques.user
            new_apy.save()
            return redirect('apy')
        except ValueError:
            return render(reques, 'create_apy.html',{
                'form' : ApyForm,
                'error': 'Verifique que los datos ingresados esten correctos'
            })


    
@login_required 
def salida(reques):
    logout(reques)
    return redirect('home')

def autenticar(request):
    if request.method == 'GET':
        return render(request, 'autenticar.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'autenticar.html', {
                'form': AuthenticationForm,
                'error': 'Usuario es incorrecto'
            })
        else:
            login(request, user)
            return redirect('apy')

@login_required
def calendario_apy(request):
    apys = Apy.objects.filter(user=request.user)

    eventos = []
    for apy in apys:
        if apy.fecha:  # 👈 validamos que tenga fecha
            eventos.append({
                'title': apy.titulo,
                'start': apy.fecha.isoformat(),
                'color': '#dc3545' if apy.importancia else '#0d6efd'
            })

    return render(request, 'calendario.html', {
        'eventos': json.dumps(eventos)
    })

User = get_user_model()

def es_gerente(user):
    return user.rol == 'gerente'

@login_required
@user_passes_test(es_gerente)
def gestionar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'gerente/gestionar_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_gerente)
def gestionar_tareas(request):
    tareas = Apy.objects.all()
    return render(request, 'gerente/gestionar_tareas.html', {'tareas': tareas})

def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestionar_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'gerente/crear_usuario.html', {'form': form})

@login_required
@user_passes_test(es_gerente)
def editar_usuario(request, pk):
    usuario = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gestionar_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'gerente/editar_usuario.html', {'form': form})

@login_required
@user_passes_test(es_gerente)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('gestionar_usuarios')
    return render(request, 'gerente/eliminar_usuario.html', {'usuario': usuario})

@login_required
def gestionar(request):
    if request.user.rol == 'gerente':
        # Si el usuario es gerente, muestra la vista para gestionar tareas y usuarios
        tareas = Apy.objects.all()  # Obtén todas las tareas, por ejemplo
        usuarios = CustomUser.objects.exclude(pk=request.user.pk)
        return render(request, 'gestionar.html', {
            'tareas': tareas,
            'usuarios': usuarios
        })
    else:
        # Si no es gerente, redirige a otra página o muestra un mensaje de error
        return redirect('home')  # O redirige a donde lo desees
    
@login_required
@user_passes_test(es_gerente)
def gestionar_tareas(request):
    tareas = Apy.objects.all()
    return render(request, 'gerente/gestionar_tareas.html', {'tareas': tareas})

@login_required
@user_passes_test(es_gerente)
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Apy, id=tarea_id)
    form = ApyForm(request.POST or None, instance=tarea)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('gestionar_tareas')
    return render(request, 'gerente/editar_tarea.html', {'form': form})

@login_required
@user_passes_test(es_gerente)
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Apy, id=tarea_id)
    if request.method == 'POST':
        tarea.delete()
        return redirect('gestionar_tareas')
    return render(request, 'gerente/eliminar_tarea.html', {'tarea': tarea})

def tareas_usuario(request):
    tareas = Apy.objects.filter(usuario=request.user, completada = False)

    tareas_proximas = []
    tareas_urgentes = []

    for tarea in tareas:
        dias_restantes = (tarea.fecha.date() - date.today()).days  # <- importante usar .date()
        tarea.dias_restantes = dias_restantes  # para mostrarlo en template

        if 1 < dias_restantes <= 5:
            tareas_proximas.append(tarea)
        elif dias_restantes <= 1:
            tareas_urgentes.append(tarea)

    return render(request, 'tareas/apy.html', {
        'Tareas': tareas,
        'tareas_proximas': tareas_proximas,
        'tareas_urgentes': tareas_urgentes
    })

@login_required
def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Apy, id=tarea_id, user=request.user)
    tarea.completada = True
    tarea.save()
    return redirect('apy')
