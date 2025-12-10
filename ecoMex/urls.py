from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from contenido import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('formulario/', views.formulario, name='formulario_preinscripcion'),
    path('viajesP/', views.viajesProximos, name='viajes_proximos'),
    path('viajesT/', views.viajesTerminados, name='viajes_terminados'),
]

# Servir archivos estáticos y media en modo DEBUG (desarrollo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
