"""Vistas de la aplicación 'home' (página principal).

Muestra productos con descuentos activos de forma optimizada.
"""
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from products.models import Product


@require_http_methods(["GET"])
def home(request):
    """Vista para la página principal optimizada.
    
    Obtiene todos los productos que tienen promociones activas usando
    el manager optimizado para reducir consultas a la base de datos.
    
    Args:
        request: Objeto de solicitud HTTP.
    
    Returns:
        HttpResponse: Plantilla home.html con productos en descuento.
    """
    # Usa el manager optimizado para obtener productos con descuentos activos
    discounted_products = Product.objects.with_discounts()
    
    context = {'discounted_products': discounted_products}
    
    return render(request, 'home/home.html', context)



    