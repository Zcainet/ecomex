from django import forms

# Lista de estados para usar en el formulario de pre-inscripción
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


class PreinscripcionForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label="Nombre completo",
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-lg border border-gray-300 "
                         "px-3 py-2 text-sm text-gray-900 focus:outline-none "
                         "focus:ring-2 focus:ring-green-500 focus:border-green-500",
                "placeholder": "Ej. Juan Pérez García",
            }
        ),
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "block w-full rounded-lg border border-gray-300 "
                         "px-3 py-2 text-sm text-gray-900 focus:outline-none "
                         "focus:ring-2 focus:ring-green-500 focus:border-green-500",
                "placeholder": "ejemplo@correo.com",
            }
        ),
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-lg border border-gray-300 "
                         "px-3 py-2 text-sm text-gray-900 focus:outline-none "
                         "focus:ring-2 focus:ring-green-500 focus:border-green-500",
                "placeholder": "555-123-4567",
            }
        ),
    )

    ciudad = forms.CharField(
        label="Ciudad",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-lg border border-gray-300 "
                         "px-3 py-2 text-sm text-gray-900 focus:outline-none "
                         "focus:ring-2 focus:ring-green-500 focus:border-green-500",
                "placeholder": "Ej. Monterrey",
            }
        ),
    )

    estado = forms.ChoiceField(
        label="Estado",
        choices=ESTADOS_MEXICO,
        widget=forms.Select(
            attrs={
                "class": "block w-full rounded-lg border border-gray-300 "
                         "px-3 py-2 text-sm text-gray-900 bg-white "
                         "focus:outline-none focus:ring-2 focus:ring-green-500 "
                         "focus:border-green-500",
            }
        ),
    )

    mensaje = forms.CharField(
        label="Mensaje o comentario",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "block w-full rounded-lg border border-gray-300 "
                         "px-3 py-2 text-sm text-gray-900 focus:outline-none "
                         "focus:ring-2 focus:ring-green-500 focus:border-green-500 "
                         "resize-y",
                "rows": 4,
                "placeholder": "Escriba aquí sus dudas o comentarios.",
            }
        ),
    )
