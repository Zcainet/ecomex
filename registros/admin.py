from django.contrib import admin
from django.utils import timezone
from django.http import HttpResponse
import csv

from .models import Viajes, Inscripcion


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    readonly_fields = (
        "nombre",
        "email",
        "telefono",
        "ciudad",
        "estado_texto",
        "personas",
        "mensaje",
        "estado",
        "created",
    )
    can_delete = False


@admin.register(Viajes)
class ViajesAdmin(admin.ModelAdmin):
    list_display = (
        "destino",
        "lugar",
        "fecha_salida",
        "fecha_regreso",
        "costo",
        "estado_viaje",
        "cancelado",
        "created",
    )
    list_display_links = ("destino",)
    search_fields = ("destino", "lugar")
    list_filter = ("lugar", "fecha_salida", "fecha_regreso", "cancelado")
    ordering = ("-created",)
    date_hierarchy = "fecha_salida"
    list_per_page = 20

    fieldsets = (
        ("Información general", {
            "fields": ("destino", "lugar", "descripcion", "imagen"),
        }),
        ("Fechas", {
            "fields": ("fecha_salida", "fecha_regreso"),
        }),
        ("Costo y estado", {
            "fields": ("costo", "cancelado"),
        }),
        ("Mapa y video (opcional)", {
            "fields": ("latitud", "longitud", "video_url"),
            "classes": ("collapse",),
        }),
        ("Metadatos", {
            "fields": ("created", "updated"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("created", "updated")

    inlines = [InscripcionInline]

    actions = ["exportar_csv", "marcar_cancelado", "marcar_activo"]

    def estado_viaje(self, obj):
        hoy = timezone.now().date()
        if obj.cancelado:
            return "Cancelado"
        if obj.fecha_salida > hoy:
            return "Próximo"
        if obj.fecha_salida <= hoy <= obj.fecha_regreso:
            return "En curso"
        return "Terminado"

    estado_viaje.short_description = "Estado"

    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="viajes_seleccionados.csv"'

        writer = csv.writer(response)
        writer.writerow(["Destino", "Lugar", "Salida", "Regreso", "Costo", "Estado"])

        for v in queryset:
            writer.writerow([
                v.destino,
                v.lugar,
                v.fecha_salida,
                v.fecha_regreso,
                v.costo,
                self.estado_viaje(v),
            ])

        return response

    exportar_csv.short_description = "Exportar viajes seleccionados a CSV"

    def marcar_cancelado(self, request, queryset):
        updated = queryset.update(cancelado=True)
        self.message_user(request, f"{updated} viaje(s) marcados como cancelados.")

    marcar_cancelado.short_description = "Marcar como cancelados"

    def marcar_activo(self, request, queryset):
        updated = queryset.update(cancelado=False)
        self.message_user(request, f"{updated} viaje(s) marcados como activos.")

    marcar_activo.short_description = "Marcar como activos"


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ("viaje", "nombre", "email", "ciudad", "estado_texto", "personas", "estado", "created")
    list_filter = ("estado", "created", "viaje", "estado_texto")
    search_fields = ("nombre", "email", "ciudad", "estado_texto", "viaje__destino")
    readonly_fields = ("created",)

    fieldsets = (
        ("Datos de contacto", {
            "fields": ("viaje", "nombre", "email", "telefono", "ciudad", "estado_texto"),
        }),
        ("Detalle de la inscripción", {
            "fields": ("personas", "mensaje", "estado"),
        }),
        ("Metadatos", {
            "fields": ("created",),
            "classes": ("collapse",),
        }),
    )

    actions = ["marcar_confirmada", "marcar_cancelada", "exportar_inscripciones_csv"]

    def marcar_confirmada(self, request, queryset):
        updated = queryset.update(estado="confirmada")
        self.message_user(request, f"{updated} inscripción(es) marcadas como confirmadas.")

    marcar_confirmada.short_description = "Marcar como confirmadas"

    def marcar_cancelada(self, request, queryset):
        updated = queryset.update(estado="cancelada")
        self.message_user(request, f"{updated} inscripción(es) marcadas como canceladas.")

    marcar_cancelada.short_description = "Marcar como canceladas"

    def exportar_inscripciones_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="inscripciones_seleccionadas.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Viaje",
            "Nombre",
            "Email",
            "Teléfono",
            "Ciudad",
            "Estado",
            "Personas",
            "Estado inscripción",
            "Fecha creación",
        ])

        for ins in queryset:
            writer.writerow([
                ins.viaje.destino,
                ins.nombre,
                ins.email,
                ins.telefono,
                ins.ciudad,
                ins.estado_texto,
                ins.personas,
                ins.estado,
                ins.created,
            ])

        return response

    exportar_inscripciones_csv.short_description = "Exportar inscripciones seleccionadas a CSV"
