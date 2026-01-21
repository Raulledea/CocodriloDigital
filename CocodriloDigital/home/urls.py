"""URLs de la aplicación 'home'.

Define las rutas principales del sitio.
"""
from django.urls import path

from .views import *

urlpatterns = [
    # Ruta principal que muestra la página de inicio con productos en descuento
    path('home/', Home.as_view(), name="home")
]
