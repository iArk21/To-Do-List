from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Apy(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creacion = models.DateTimeField(auto_now_add= True)
    fecha = models.DateTimeField(null = True)
    importancia = models.BooleanField(default = False, verbose_name= "¿Es importante?")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)



    def __str__(self):
        return self.titulo + ' - de '+ self.user.username
    
    def dias_restantes(self):
        from datetime import date
        return (self.fecha - date.today()).days
     
class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    identificacion = models.CharField(max_length=50, unique=True)
    rol = models.CharField(max_length=20, choices=[('gerente', 'Gerente'), ('empleado', 'Empleado')])
    
    ROL_CHOICES = (
        ('empleado', 'Empleado'),
        ('gerente', 'Gerente'),
    )

    def __str__(self):
        return self.username
