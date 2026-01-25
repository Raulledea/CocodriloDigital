"""Vistas de la aplicación 'products'.

Contiene la lógica para gestionar productos con optimizaciones de queries
y validaciones de permisos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from .forms import ProductForm, PromotionForm
from .models import Product, Promotion
from category.models import Category
from CocodriloDigital.utils import superuser_required


def list_products(request):
    """Muestra todos los productos agrupados por categoría.

    Recupera categorías con productos usando prefetch_related para optimizar.
    
    Returns:
        HttpResponse: Plantilla list_products.html con categorías y productos.
    """
    categories = Category.objects.prefetch_related(
        'products__promotions'
    ).filter(
        products__isnull=False
    ).distinct()

    context = {'categories': categories}
    return render(request, 'products/list_products.html', context)


@require_http_methods(["GET"])
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


@superuser_required()
@require_http_methods(["GET", "POST"])
def add_product(request):
    """Vista para añadir un nuevo producto.
    
    GET: Muestra formulario vacío de creación de producto.
    POST: Procesa el formulario y guarda el producto si es válido.
    
    Returns:
        HttpResponse: Formulario o redirección a list_products tras crear.
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Producto "{product.name}" creado exitosamente.')
            return redirect('list_products')
        else:
            messages.error(request, 'Hubo errores en el formulario. Verifica los datos.')
    else:
        form = ProductForm()
    
    return render(request, 'products/add_products.html', {'form': form})


@superuser_required()
@require_http_methods(["GET", "POST"])
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
            product = form.save()
            messages.success(request, f'Producto "{product.name}" actualizado exitosamente.')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Hubo errores en el formulario. Verifica los datos.')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'edit': True,
    }
    return render(request, 'products/add_products.html', context)


@superuser_required()
@require_http_methods(["GET", "POST"])
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
        product_name = product.name
        product.delete()
        messages.success(request, f'Producto "{product_name}" eliminado exitosamente.')
        return redirect('list_products')
    
    context = {'product': product}
    return render(request, 'products/delete_product.html', context)


@superuser_required()
@require_http_methods(["GET", "POST"])
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
            messages.success(request, f'Promoción creada exitosamente para "{product.name}".')
            return redirect('promotion_detail', product_id=product.id, promotion_id=promotion.id)
        else:
            messages.error(request, 'Hubo errores en el formulario. Verifica los datos.')
    else:
        form = PromotionForm()
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/create_promotion.html', context)


@require_http_methods(["GET"])
def promotion_detail(request, product_id, promotion_id):
    """Vista para ver los detalles de una promoción.
    
    Muestra la información completa de una promoción incluyendo
    el período activo, porcentaje de descuento, y botones para
    modificar o eliminar (si es superusuario).
    
    Args:
        request: La solicitud HTTP.
        product_id (int): El ID del producto.
        promotion_id (int): El ID de la promoción.
        
    Returns:
        HttpResponse: La plantilla renderizada con los detalles de la promoción.
    """
    product = get_object_or_404(Product, pk=product_id)
    promotion = get_object_or_404(Promotion, pk=promotion_id, product=product)
    
    discount_amount = product.price * Decimal(promotion.discount_percent) / Decimal(100)
    discounted_price = product.price - discount_amount
    
    context = {
        'product': product,
        'promotion': promotion,
        'discount_amount': discount_amount,
        'discounted_price': discounted_price,
    }
    return render(request, 'products/promotion_detail.html', context)


@superuser_required()
@require_http_methods(["GET", "POST"])
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
            promotion = form.save()
            messages.success(request, 'Promoción actualizada exitosamente.')
            return redirect('promotion_detail', product_id=product.id, promotion_id=promotion.id)
        else:
            messages.error(request, 'Hubo errores en el formulario. Verifica los datos.')
    else:
        form = PromotionForm(instance=promotion)
    
    context = {
        'form': form,
        'product': product,
        'promotion': promotion,
        'edit': True,
    }
    return render(request, 'products/create_promotion.html', context)


@superuser_required()
@require_http_methods(["GET", "POST"])
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
        messages.success(request, 'Promoción eliminada exitosamente.')
        return redirect('product_detail', product_id=product.id)
    
    context = {
        'product': product,
        'promotion': promotion,
    }
    return render(request, 'products/delete_promotion.html', context)


@require_http_methods(["GET"])
def carrito_view(request):
    """
    Vista para mostrar el carrito de compras.

    GET: Muestra los productos almacenados en la sesión.
    """
    carrito = request.session.get('carrito', {})

    total = 0
    for item in carrito.values():
        total += item['price'] * item['quantity']

    context = {
        'carrito': carrito,
        'total': total,
    }

    return render(request, 'products/carrito.html', context)


@require_http_methods(["POST"])
def add_to_carrito(request, product_id):
    """
    POST: Agrega un producto al carrito usando sesión.
    """
    product = get_object_or_404(Product, pk=product_id)

    carrito = request.session.get('carrito', {})

    product_id_str = str(product.id)

    if product_id_str in carrito:
        carrito[product_id_str]['quantity'] += 1
    else:
        carrito[product_id_str] = {
            'name': product.name,
            'price': float(product.final_price if hasattr(product, 'final_price') else product.price),
            'quantity': 1,
            'image': product.image.url if product.image else '',
        }

    request.session['carrito'] = carrito
    request.session.modified = True

    messages.success(request, 'Producto añadido al carrito.')
    return redirect('carrito')


@require_http_methods(["POST"])
def remove_from_carrito(request, product_id):
    """
    POST: Elimina un producto del carrito.
    """
    carrito = request.session.get('carrito', {})
    product_id_str = str(product_id)

    if product_id_str in carrito:
        del carrito[product_id_str]
        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, 'Producto eliminado del carrito.')

    return redirect('carrito')
