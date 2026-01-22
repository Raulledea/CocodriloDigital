"""Vistas de la aplicación 'products'.

Contiene la lógica para gestionar productos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .forms import ProductForm
from category.models import Category
from .models import Product


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