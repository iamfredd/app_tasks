from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_completada = models.DateTimeField(auto_now_add=True, blank=True)
    importante = models.BooleanField(default=False)
    completada = models.BooleanField(default=False) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.titulo + ' - ' + self.usuario.username