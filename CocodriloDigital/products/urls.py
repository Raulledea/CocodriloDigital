from django.urls import path
from . import views

urlpatterns = [
    # Listado de productos
    path('', views.list_products, name='list_products'),
    # Detalle de producto
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    # Añadir producto
    path('add_products/', views.add_product, name='add_products'),
    # Editar producto
    path('<int:product_id>/edit/', views.edit_product, name='edit_product'),
    # Eliminar producto
    path('<int:product_id>/delete/', views.delete_product, name='delete_product'),

    # Promociones
    path('<int:product_id>/promotion/create/', views.create_promotion, name='create_promotion'),
    path('<int:product_id>/promotion/<int:promotion_id>/', views.promotion_detail, name='promotion_detail'),
    path('<int:product_id>/promotion/<int:promotion_id>/edit/', views.edit_promotion, name='edit_promotion'),
    path('<int:product_id>/promotion/<int:promotion_id>/delete/', views.delete_promotion, name='delete_promotion'),

    # Búsqueda de productos
    path('search/', views.search_results, name='search_results'),
]

