from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Viajes(models.Model):
    destino = models.CharField(max_length=100)
    lugar = models.CharField(max_length=100)
    descripcion = RichTextField()
    fecha_salida = models.DateField()
    fecha_regreso = models.DateField()
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    
    imagen = models.ImageField(null=True,upload_to="fotos",verbose_name="Fotografía")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ["-created"]

    def __str__(self):
        return self.destino