from django.shortcuts import render
from registros.models import Viajes
import datetime


def inicio(request):
    """Página de inicio."""
    return render(request, 'contenido/inicio.html')


def formulario(request):
    """Formulario de preinscripción (solo muestra la vista)."""
    return render(request, 'contenido/formulario.html')


def viajesProximos(request):
    """Lista de todos los viajes ordenados por fecha de salida (próximos)."""
    todos_los_viajes = Viajes.objects.all().order_by('fecha_salida')
    context = {
        'viajes_lista': todos_los_viajes
    }
    return render(request, 'contenido/viajesP.html', context)


def viajesTerminados(request):
    """Lista de viajes cuya fecha de regreso ya pasó."""
    hoy = datetime.date.today()
    viajes_terminados = Viajes.objects.filter(
        fecha_regreso__lt=hoy
    ).order_by('-fecha_regreso')

    context = {
        'viajes_lista': viajes_terminados
    }
    return render(request, 'contenido/viajesT.html', context)
