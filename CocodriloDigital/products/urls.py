"""URLs de la aplicación 'products'.

Define las rutas para gestionar productos.
"""
from django.urls import path

from . import views

urlpatterns = [
    # Listado de productos por categorías en la raíz de 'products/' (ej. /products/)
    path('', views.list_products, name='list_products'),
    # Ruta para ver detalle de un producto (ej. /products/1/)
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    # Ruta para añadir un nuevo producto (GET muestra formulario, POST guarda el producto)
    path('add_products/', views.add_product, name='add_products'),
    # Ruta para editar un producto existente (ej. /products/1/edit/)
    path('<int:product_id>/edit/', views.edit_product, name='edit_product'),
    # Ruta para eliminar un producto (ej. /products/1/delete/)
    path('<int:product_id>/delete/', views.delete_product, name='delete_product'),
]
