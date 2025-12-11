from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

from registros.models import Viajes
from registros.forms import InscripcionForm
from .forms import PreinscripcionForm
import datetime


def inicio(request):
    """Página de inicio con sección de viajes destacados."""
    hoy = datetime.date.today()
    viajes_destacados = Viajes.objects.filter(
        fecha_salida__gte=hoy,
        cancelado=False,
    ).order_by("fecha_salida")[:3]

    context = {
        "viajes_destacados": viajes_destacados,
    }
    return render(request, "contenido/inicio.html", context)


def formulario(request):
    """Formulario de preinscripción general que envía un correo (en consola)."""
    if request.method == "POST":
        form = PreinscripcionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cuerpo = (
                f"Nombre: {data['nombre']}\n"
                f"Email: {data['email']}\n"
                f"Teléfono: {data.get('telefono', '')}\n"
                f"Ciudad: {data.get('ciudad', '')}\n"
                f"Estado: {data.get('estado', '')}\n\n"
                f"Mensaje:\n{data['mensaje']}"
            )
            send_mail(
                subject=f"Preinscripción Ecoturismo - {data['nombre']}",
                message=cuerpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
            )
            messages.success(
                request,
                "Tu preinscripción fue enviada correctamente. "
                "Revisa el correo de demostración en la consola del servidor.",
            )
            form = PreinscripcionForm()  # Limpiar formulario
    else:
        form = PreinscripcionForm()

    return render(request, "contenido/formulario.html", {"form": form})


def viajesProximos(request):
    """Lista de viajes cuya fecha de salida es igual o mayor a hoy, con filtros y paginación."""
    hoy = datetime.date.today()
    viajes_qs = Viajes.objects.filter(fecha_salida__gte=hoy, cancelado=False)

    # Ordenamiento
    orden = request.GET.get("orden", "fecha")
    if orden == "precio":
        viajes_qs = viajes_qs.order_by("costo")
    elif orden == "precio_desc":
        viajes_qs = viajes_qs.order_by("-costo")
    else:
        viajes_qs = viajes_qs.order_by("fecha_salida")

    # Filtros
    q = request.GET.get("q", "").strip()
    precio_max = request.GET.get("precio_max", "").strip()

    if q:
        viajes_qs = viajes_qs.filter(destino__icontains=q)

    if precio_max:
        try:
            precio_valor = float(precio_max)
            viajes_qs = viajes_qs.filter(costo__lte=precio_valor)
        except ValueError:
            pass

    paginator = Paginator(viajes_qs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "viajes_lista": page_obj.object_list,
        "page_obj": page_obj,
        "q": q,
        "precio_max": precio_max,
        "orden": orden,
    }
    return render(request, "contenido/viajesP.html", context)


def viajesTerminados(request):
    """Lista de viajes cuya fecha de regreso ya pasó, con buscador y paginación."""
    hoy = datetime.date.today()
    viajes_qs = Viajes.objects.filter(fecha_regreso__lt=hoy)

    q = request.GET.get("q", "").strip()
    if q:
        viajes_qs = viajes_qs.filter(destino__icontains=q)

    viajes_qs = viajes_qs.order_by("-fecha_regreso")

    paginator = Paginator(viajes_qs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "viajes_lista": page_obj.object_list,
        "page_obj": page_obj,
        "q": q,
    }
    return render(request, "contenido/viajesT.html", context)


def viaje_detalle(request, viaje_id: int):
    """Vista de detalle para un viaje específico (incluye video y mapa si están definidos)."""
    viaje = get_object_or_404(Viajes, id=viaje_id)

    embed_url = None
    if viaje.video_url:
        url = viaje.video_url
        if "watch?v=" in url:
            embed_url = url.replace("watch?v=", "embed/")
        elif "youtu.be/" in url:
            embed_url = url.replace("youtu.be/", "youtube.com/embed/")
        else:
            embed_url = url

    context = {
        "viaje": viaje,
        "embed_url": embed_url,
    }
    return render(request, "contenido/viaje_detalle.html", context)


def inscribirse_viaje(request, viaje_id: int):
    """Formulario de inscripción específico para un viaje."""
    viaje = get_object_or_404(Viajes, id=viaje_id, cancelado=False)
    if request.method == "POST":
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.viaje = viaje
            inscripcion.save()
            messages.success(
                request,
                "Tu solicitud de inscripción fue registrada. "
                "El administrador del sitio podrá confirmarla desde el panel.",
            )
            return redirect("viaje_detalle", viaje_id=viaje.id)
    else:
        form = InscripcionForm()

    return render(
        request,
        "contenido/inscribirse_viaje.html",
        {"form": form, "viaje": viaje},
    )
