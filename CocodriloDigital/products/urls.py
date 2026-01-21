"""URLs de la aplicación 'products'.

Define las rutas para gestionar productos.
"""
from django.urls import path

from . import views

urlpatterns = [
    # Ruta para añadir un nuevo producto (GET muestra formulario, POST guarda el producto)
    path('add_products/', views.add_product, name='add_products')
]
