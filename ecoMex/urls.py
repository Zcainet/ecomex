from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from contenido import views
from registros import views as registros_views

urlpatterns = [
    # Área administrativa de Django
    path("admin/", admin.site.urls),

    # Sitio público
    path("", views.inicio, name="inicio"),
    path("formulario/", views.formulario, name="formulario_preinscripcion"),
    path("viajesP/", views.viajesProximos, name="viajes_proximos"),
    path("viajesT/", views.viajesTerminados, name="viajes_terminados"),
    path("viaje/<int:viaje_id>/", views.viaje_detalle, name="viaje_detalle"),
    path("viaje/<int:viaje_id>/inscribirse/", views.inscribirse_viaje, name="inscribirse_viaje"),

    # Panel de gestión de viajes
    path("panel/viajes/", registros_views.panel_viajes, name="panel_viajes"),
    path("panel/viajes/nuevo/", registros_views.crear_viaje, name="crear_viaje"),
    path("panel/viajes/<int:viaje_id>/editar/", registros_views.editar_viaje, name="editar_viaje"),
    path("panel/viajes/<int:viaje_id>/eliminar/", registros_views.eliminar_viaje, name="eliminar_viaje"),
    path("panel/viajes/export/csv/", registros_views.exportar_viajes_csv, name="exportar_viajes_csv"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
