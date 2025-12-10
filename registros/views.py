from django.shortcuts import render
from .models import Viajes

def inicio(request):
    viajes = Viajes.objects.all()
    return render(request, 'registros/inicio.html', {'viajes': viajes})