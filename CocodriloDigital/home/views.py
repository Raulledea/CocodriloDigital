"""Vistas de la aplicación 'home' (página principal).

Muestra productos con descuentos activos.
"""
from django.shortcuts import render
from products.models import Product
from django.utils import timezone
from django.views.generic import ListView


def home(request):
    """Vista funcional para la página principal.
    
    Obtiene todos los productos que tienen promociones activas (en rango de fecha)
    y los pasa a la plantilla home/home.html.
    
    Args:
        request: Objeto de solicitud HTTP.
    
    Returns:
        HttpResponse: Plantilla home.html con lista de productos en descuento.
    """
    # Obtiene la fecha/hora actual
    now = timezone.now()
    
    # Filtra productos que tienen al menos una promoción activa
    # Usa .distinct() para evitar duplicados si hay varias promociones
    discounted_products = Product.objects.filter(
        promotions__discount_percent__isnull=False,  # Que tenga descuento registrado
        promotions__start_date__lte=now,  # Que haya comenzado
        promotions__end_date__gte=now  # Que no haya terminado
    ).distinct()
    
    # Prepara el contexto con los datos
    context = {'discounted_products': discounted_products}
    
    return render(request, 'home/home.html', context)


class Home(ListView):
    """Vista basada en clases (CBV) para la página principal.
    
    Alterna a esta vista si prefieres usar Generic Views.
    Hereda de ListView para listar productos.
    """
    model = Product
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        """Construye el contexto añadiendo productos en descuento.
        
        Returns:
            dict: Contexto con productos en descuento para la plantilla.
        """
        # Obtiene la fecha/hora actual
        now = timezone.now()
        
        # Filtra productos con promociones activas (igual que en la vista funcional)
        discounted_products = Product.objects.filter(
            promotions__discount_percent__isnull=False,
            promotions__start_date__lte=now,
            promotions__end_date__gte=now
        ).distinct()
        
        # Obtiene el contexto padre (con la lista de todos los productos)
        context = super().get_context_data(**kwargs)
        # Añade los productos en descuento
        context['discounted_products'] = discounted_products
        return context
    