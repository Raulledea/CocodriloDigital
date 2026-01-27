"""URLs de la aplicación 'cart'.

Define las rutas para gestionar el carrito de compras y recibos.
"""
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # ===== CARRITO =====
    path('carrito/', views.carrito_view, name='carrito'),
    path('carrito/add/<int:product_id>/', views.add_to_carrito, name='add_to_carrito'),
    path('carrito/update/<int:product_id>/', views.update_carrito, name='update_carrito'),
    path('carrito/remove/<int:product_id>/', views.remove_from_carrito, name='remove_from_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    
    # ===== API ENDPOINTS =====
    path('api/count/', views.cart_count, name='cart_count'),
    path('api/add/<int:product_id>/', views.ajax_add_to_carrito, name='ajax_add_to_carrito'),
    path('api/remove/<int:product_id>/', views.ajax_remove_from_carrito, name='ajax_remove_from_carrito'),
    
    # ===== RECIBOS =====
    path('recibos/', views.receipt_list, name='receipt_list'),
    path('recibos/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
]
