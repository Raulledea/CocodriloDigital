"""URLs de la aplicación 'products'.

Define las rutas para gestionar productos.
"""
from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    # ===== PRODUCTOS =====
    path('', views.list_products, name='list_products'),
    path('add/', views.add_product, name='add_products'),  # ruta para agregar productos
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('<int:product_id>/delete/', views.delete_product, name='delete_product'),

    # ===== PROMOCIONES =====
    path('<int:product_id>/promotion/create/', views.create_promotion, name='create_promotion'),
    path('<int:product_id>/promotion/<int:promotion_id>/', views.promotion_detail, name='promotion_detail'),
    path('<int:product_id>/promotion/<int:promotion_id>/edit/', views.edit_promotion, name='edit_promotion'),
    path('<int:product_id>/promotion/<int:promotion_id>/delete/', views.delete_promotion, name='delete_promotion'),
]