"""URLs de la aplicación 'category'.

Define las rutas para gestionar categorías.
"""
from django.urls import path

from .views import add_category

urlpatterns = [
    # Ruta para añadir una nueva categoría
    path('add_category/', add_category, name='add_category'),
]
