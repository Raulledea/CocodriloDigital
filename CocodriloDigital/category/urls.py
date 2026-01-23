"""URLs de la aplicación 'category'.

Define las rutas para gestionar categorías.
"""
from django.urls import path

from .views import add_category, category_detail, edit_category, delete_category

urlpatterns = [
    # Ruta para añadir una nueva categoría
    path('add_category/', add_category, name='add_category'),
    # Ruta para ver detalle de una categoría (ej. /category/1/)
    path('<int:category_id>/', category_detail, name='category_detail'),
    # Ruta para editar una categoría (ej. /category/1/edit/)
    path('<int:category_id>/edit/', edit_category, name='edit_category'),
    # Ruta para eliminar una categoría (ej. /category/1/delete/)
    path('<int:category_id>/delete/', delete_category, name='delete_category'),
]
