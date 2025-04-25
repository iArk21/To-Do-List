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


    def __str__(self):
        return self.titulo + ' - de '+ self.user.username
     
class CustomUser(AbstractUser):
    identificacion= models.CharField(max_length=20, unique=True)
    esAdministrador= models.BooleanField(default=False)

    def __str__(self):
        return self.username
