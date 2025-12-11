from django.db import models
from ckeditor.fields import RichTextField


class Viajes(models.Model):
    destino = models.CharField(max_length=100)
    lugar = models.CharField(max_length=100)
    descripcion = RichTextField()
    fecha_salida = models.DateField()
    fecha_regreso = models.DateField()
    costo = models.DecimalField(max_digits=8, decimal_places=2)

    imagen = models.ImageField(null=True, upload_to="fotos", verbose_name="Fotografía")

    # Campos opcionales para mapa y video
    latitud = models.DecimalField(
        "Latitud (opcional)",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    longitud = models.DecimalField(
        "Longitud (opcional)",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    video_url = models.URLField(
        "URL de video (YouTube opcional)",
        max_length=200,
        null=True,
        blank=True,
    )

    cancelado = models.BooleanField(
        default=False,
        verbose_name="Viaje cancelado",
        help_text="Si está marcado, el viaje se mostrará como cancelado en el sitio público.",
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ["-created"]

    def __str__(self):
        return self.destino


class Inscripcion(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
    ]

    viaje = models.ForeignKey(
        Viajes,
        on_delete=models.CASCADE,
        related_name="inscripciones",
    )

    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)

    ciudad = models.CharField(max_length=120)
    estado_texto = models.CharField("Estado", max_length=120)

    personas = models.PositiveIntegerField(default=1)
    mensaje = models.TextField(blank=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="pendiente",
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.nombre} – {self.viaje.destino}"
