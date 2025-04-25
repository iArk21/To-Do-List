
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ApyForm
from .models import Apy
import json
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Create your views here.

def home(request):
    return  render(request, 'home.html')



def signup(request):

    if request.method == 'GET':
        return  render(request, 'signup.html',{
           'form': CustomUserCreationForm()
        })
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('apy')
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Revisa los datos ingresados.'
            })
@login_required       
def apy(request):
    apys = Apy.objects.filter(user = request.user)


    return render(request, 'apy.html', {'Tareas': apys})
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

