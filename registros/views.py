from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import csv

from .models import Viajes
from .forms import ViajeForm


def inicio(request):
    viajes = Viajes.objects.all()
    return render(request, "registros/inicio.html", {"viajes": viajes})


@login_required
def panel_viajes(request):
    """Vista principal del panel de gestión de viajes."""
    viajes = Viajes.objects.all().order_by("-created")
    return render(request, "registros/panel_viajes.html", {"viajes": viajes})


@login_required
def crear_viaje(request):
    if request.method == "POST":
        form = ViajeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "El viaje se creó correctamente.")
            return redirect("panel_viajes")
    else:
        form = ViajeForm()
    return render(request, "registros/form_viaje.html", {"form": form, "modo": "crear"})


@login_required
def editar_viaje(request, viaje_id: int):
    viaje = get_object_or_404(Viajes, id=viaje_id)
    if request.method == "POST":
        form = ViajeForm(request.POST, request.FILES, instance=viaje)
        if form.is_valid():
            form.save()
            messages.success(request, "El viaje se actualizó correctamente.")
            return redirect("panel_viajes")
    else:
        form = ViajeForm(instance=viaje)
    return render(request, "registros/form_viaje.html", {"form": form, "modo": "editar", "viaje": viaje})


@login_required
def eliminar_viaje(request, viaje_id: int):
    viaje = get_object_or_404(Viajes, id=viaje_id)
    if request.method == "POST":
        viaje.delete()
        messages.success(request, "El viaje se eliminó correctamente.")
        return redirect("panel_viajes")
    return render(request, "registros/confirmar_eliminar.html", {"viaje": viaje})


@login_required
def exportar_viajes_csv(request):
    """Exporta todos los viajes a un archivo CSV."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="viajes.csv"'

    writer = csv.writer(response)
    writer.writerow(["Destino", "Lugar", "Fecha salida", "Fecha regreso", "Costo"])

    for v in Viajes.objects.all().order_by("fecha_salida"):
        writer.writerow([v.destino, v.lugar, v.fecha_salida, v.fecha_regreso, v.costo])

    return response
