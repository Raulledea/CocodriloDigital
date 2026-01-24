"""Vistas de la aplicación 'products'.

Contiene la lógica para gestionar productos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .forms import ProductForm, PromotionForm
from category.models import Category
from .models import Product, Promotion


def list_products(request):
    """Muestra todos los productos agrupados por categoría.

    Recupera las categorías que tienen productos y prefetches los productos
    para reducir consultas. Renderiza la plantilla `products/list_by_category.html`.
    """
    # Obtener categorías que tienen al menos un producto
    categories = Category.objects.prefetch_related('products').filter(products__isnull=False).distinct()

    context = {
        'categories': categories,
    }
    return render(request, 'products/list_products.html', context)


def product_detail(request, product_id):
    """Muestra la información detallada de un producto específico.
    
    Obtiene el producto por su ID y renderiza una plantilla con toda
    su información, incluyendo botones para modificar, eliminar y volver.
    
    Args:
        request: La solicitud HTTP.
        product_id (int): El ID del producto a mostrar.
        
    Returns:
        HttpResponse: La plantilla renderizada con los detalles del producto.
        
    Raises:
        Http404: Si el producto no existe.
    """
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)



def add_product(request):
    """Vista para añadir un nuevo producto.
    
    GET: Muestra formulario vacío de creación de producto.
    POST: Procesa el formulario y guarda el producto si es válido.
    
    Redirige a 'home' después de crear el producto.
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirige a la página principal después de guardar
            return redirect('list_products')
    else:
        form = ProductForm()
    return render(request, 'products/add_products.html', {'form': form})


def edit_product(request, product_id):
    """Vista para editar un producto existente.
    
    GET: Muestra el formulario rellenado con los datos del producto.
    POST: Procesa el formulario y actualiza el producto si es válido.
    
    Args:
        request: La solicitud HTTP.
        product_id (int): El ID del producto a editar.
        
    Returns:
        HttpResponse: El formulario renderizado o redirección tras guardar.
    """
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # Redirige al detalle del producto después de guardar
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'edit': True,
    }
    return render(request, 'products/add_products.html', context)


def delete_product(request, product_id):
    """Vista para eliminar un producto.
    
    GET: Muestra una página de confirmación.
    POST: Elimina el producto y redirige a la lista de productos.
    
    Args:
        request: La solicitud HTTP.
        product_id (int): El ID del producto a eliminar.
        
    Returns:
        HttpResponse: Página de confirmación o redirección tras eliminar.
    """
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == "POST":
        product.delete()
        return redirect('list_products')
    
    context = {
        'product': product,
    }
    return render(request, 'products/delete_product.html', context)


def create_promotion(request, product_id):
    """Vista para crear una nueva promoción para un producto.
    
    GET: Muestra el formulario de creación de promoción.
    POST: Procesa el formulario y guarda la promoción si es válido.
    
    Args:
        request: La solicitud HTTP.
        product_id (int): El ID del producto para el que crear la promoción.
        
    Returns:
        HttpResponse: El formulario renderizado o redirección tras guardar.
    """
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == "POST":
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.product = product
            promotion.save()
            return redirect('promotion_detail', product_id=product.id, promotion_id=promotion.id)
    else:
        form = PromotionForm()
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/create_promotion.html', context)


def promotion_detail(request, product_id, promotion_id):
    """Vista para ver los detalles de una promoción.
    
    Muestra la información completa de una promoción incluyendo
    el período activo, porcentaje de descuento, y botones para
    modificar o eliminar.
    
    Args:
        request: La solicitud HTTP.
        product_id (int): El ID del producto.
        promotion_id (int): El ID de la promoción.
        
    Returns:
        HttpResponse: La plantilla renderizada con los detalles de la promoción.
    """
    product = get_object_or_404(Product, pk=product_id)
    promotion = get_object_or_404(Promotion, pk=promotion_id, product=product)
    
    # Calcular precios
    from decimal import Decimal
    discount_amount = product.price * Decimal(promotion.discount_percent) / Decimal(100)
    discounted_price = product.price - discount_amount
    
    context = {
        'product': product,
        'promotion': promotion,
        'discount_amount': discount_amount,
        'discounted_price': discounted_price,
    }
    return render(request, 'products/promotion_detail.html', context)


def edit_promotion(request, product_id, promotion_id):
    """Vista para editar una promoción existente.
    
    GET: Muestra el formulario rellenado con los datos de la promoción.
    POST: Procesa el formulario y actualiza la promoción si es válido.
    
    Args:
        request: La solicitud HTTP.
        product_id (int): El ID del producto.
        promotion_id (int): El ID de la promoción a editar.
        
    Returns:
        HttpResponse: El formulario renderizado o redirección tras guardar.
    """
    product = get_object_or_404(Product, pk=product_id)
    promotion = get_object_or_404(Promotion, pk=promotion_id, product=product)
    
    if request.method == "POST":
        form = PromotionForm(request.POST, instance=promotion)
        if form.is_valid():
            form.save()
            return redirect('promotion_detail', product_id=product.id, promotion_id=promotion.id)
    else:
        form = PromotionForm(instance=promotion)
    
    context = {
        'form': form,
        'product': product,
        'promotion': promotion,
        'edit': True,
    }
    return render(request, 'products/create_promotion.html', context)


def delete_promotion(request, product_id, promotion_id):
    """Vista para eliminar una promoción.
    
    GET: Muestra una página de confirmación.
    POST: Elimina la promoción y redirige al detalle del producto.
    
    Args:
        request: La solicitud HTTP.
        product_id (int): El ID del producto.
        promotion_id (int): El ID de la promoción a eliminar.
        
    Returns:
        HttpResponse: Página de confirmación o redirección tras eliminar.
    """
    product = get_object_or_404(Product, pk=product_id)
    promotion = get_object_or_404(Promotion, pk=promotion_id, product=product)
    
    if request.method == "POST":
        promotion.delete()
        return redirect('product_detail', product_id=product.id)
    
    context = {
        'product': product,
        'promotion': promotion,
    }
    return render(request, 'products/delete_promotion.html', context)


from django.shortcuts import render
from django.db.models import Q
from .models import Product

def search_results(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        products = Product.objects.none()

    # Calculamos el porcentaje de descuento por producto
    products_with_discount = []
    for p in products:
        if p.final_price < p.price and p.price > 0:
            discount_percent = int((p.price - p.final_price) / p.price * 100)
        else:
            discount_percent = 0
        products_with_discount.append((p, discount_percent))

    return render(request, 'products/search_results.html', {
        'query': query,
        'products_with_discount': products_with_discount
    })
