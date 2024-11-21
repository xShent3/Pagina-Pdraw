from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)
    descripcion_categoria = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre_categoria


class MisSolicitudesUsuario(models.Model):
    ESTADO_CHOICES = [
        ('en_espera', 'En Espera'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
        ('rechazado', 'Rechazado'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # 
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En Espera')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Relación con Categoria
    referencia = models.ImageField('img/')  # Campo para almacenar la imagen
    descripcion = models.CharField(max_length=500)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.estado

class Dibujos(models.Model):
    nombre_dibujo = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Relación con Categoria
    imagen = models.ImageField(upload_to='img/')  # Campo para almacenar la imagen

    def __str__(self):
        return self.nombre_dibujo