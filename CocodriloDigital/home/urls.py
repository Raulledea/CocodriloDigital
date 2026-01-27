"""URLs de la aplicación 'home'.

Define las rutas principales del sitio.
"""
from django.urls import path

from . import views

urlpatterns = [
    # Ruta principal que muestra la página de inicio con productos en descuento
    # La ruta '' significa que cargará automáticamente en la raíz (/)
    path('', views.home, name="home"),
]
