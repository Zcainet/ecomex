from django import forms
from .models import Viajes, Inscripcion


ESTADOS_MEXICO = [
    ("", "Seleccione un estado"),
    ("Aguascalientes", "Aguascalientes"),
    ("Baja California", "Baja California"),
    ("Baja California Sur", "Baja California Sur"),
    ("Campeche", "Campeche"),
    ("Chiapas", "Chiapas"),
    ("Chihuahua", "Chihuahua"),
    ("Ciudad de México", "Ciudad de México"),
    ("Coahuila", "Coahuila"),
    ("Colima", "Colima"),
    ("Durango", "Durango"),
    ("Guanajuato", "Guanajuato"),
    ("Guerrero", "Guerrero"),
    ("Hidalgo", "Hidalgo"),
    ("Jalisco", "Jalisco"),
    ("México", "México"),
    ("Michoacán", "Michoacán"),
    ("Morelos", "Morelos"),
    ("Nayarit", "Nayarit"),
    ("Nuevo León", "Nuevo León"),
    ("Oaxaca", "Oaxaca"),
    ("Puebla", "Puebla"),
    ("Querétaro", "Querétaro"),
    ("Quintana Roo", "Quintana Roo"),
    ("San Luis Potosí", "San Luis Potosí"),
    ("Sinaloa", "Sinaloa"),
    ("Sonora", "Sonora"),
    ("Tabasco", "Tabasco"),
    ("Tamaulipas", "Tamaulipas"),
    ("Tlaxcala", "Tlaxcala"),
    ("Veracruz", "Veracruz"),
    ("Yucatán", "Yucatán"),
    ("Zacatecas", "Zacatecas"),
]


class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viajes
        fields = [
            "destino",
            "lugar",
            "descripcion",
            "fecha_salida",
            "fecha_regreso",
            "costo",
            "imagen",
            "latitud",
            "longitud",
            "video_url",
            "cancelado",
        ]
        widgets = {
            "fecha_salida": forms.DateInput(attrs={"type": "date"}),
            "fecha_regreso": forms.DateInput(attrs={"type": "date"}),
        }


class InscripcionForm(forms.ModelForm):
    # Sobrescribimos el campo para usar un select con estados
    estado_texto = forms.ChoiceField(
        label="Estado",
        choices=ESTADOS_MEXICO,
        widget=forms.Select(
            attrs={
                "class": "block w-full rounded-lg border border-slate-500/70 bg-slate-900/80 "
                         "text-slate-100 text-sm px-3 py-2.5 focus:outline-none "
                         "focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400",
            }
        ),
    )

    class Meta:
        model = Inscripcion
        fields = ["nombre", "email", "telefono", "ciudad", "estado_texto", "personas", "mensaje"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-500/70 bg-slate-900/80 "
                             "text-slate-100 text-sm px-3 py-2.5 focus:outline-none "
                             "focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400 "
                             "placeholder-slate-400",
                    "placeholder": "Ej. Juan Pérez García",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-500/70 bg-slate-900/80 "
                             "text-slate-100 text-sm px-3 py-2.5 focus:outline-none "
                             "focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400 "
                             "placeholder-slate-400",
                    "placeholder": "ejemplo@correo.com",
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-500/70 bg-slate-900/80 "
                             "text-slate-100 text-sm px-3 py-2.5 focus:outline-none "
                             "focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400 "
                             "placeholder-slate-400",
                    "placeholder": "555-123-4567",
                }
            ),
            "ciudad": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-500/70 bg-slate-900/80 "
                             "text-slate-100 text-sm px-3 py-2.5 focus:outline-none "
                             "focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400 "
                             "placeholder-slate-400",
                    "placeholder": "Ej. Monterrey",
                }
            ),
            "personas": forms.NumberInput(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-500/70 bg-slate-900/80 "
                             "text-slate-100 text-sm px-3 py-2.5 focus:outline-none "
                             "focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400",
                    "min": 1,
                }
            ),
            "mensaje": forms.Textarea(
                attrs={
                    "class": "block w-full rounded-lg border border-slate-500/70 bg-slate-900/80 "
                             "text-slate-100 text-sm px-3 py-2.5 focus:outline-none "
                             "focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400 "
                             "placeholder-slate-400 resize-y",
                    "rows": 4,
                    "placeholder": "Escribe aquí cualquier comentario o duda sobre el viaje.",
                }
            ),
        }
