"""Vistas de la aplicación 'category'.

Contiene la lógica para gestionar categorías con optimizaciones.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CategoryForm
from .models import Category
from CocodriloDigital.utils import superuser_required


@superuser_required()
@require_http_methods(["GET", "POST"])
def add_category(request):
    """Vista para añadir una nueva categoría.
    
    GET: Muestra formulario vacío de creación de categoría.
    POST: Procesa el formulario y guarda la categoría si es válido.
    
    Returns:
        HttpResponse: Formulario o redirección a list_products tras crear.
    """
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Categoría "{category.name}" creada exitosamente.')
            return redirect('list_products')
        else:
            messages.error(request, 'Hubo errores en el formulario. Verifica los datos.')
    else:
        form = CategoryForm()
    
    return render(request, 'category/add_category.html', {'form': form})


@require_http_methods(["GET"])
def category_detail(request, category_id):
    """Vista para ver los detalles de una categoría.
    
    Muestra la información completa de la categoría incluyendo
    todos los productos que pertenecen a ella.
    
    Args:
        request: La solicitud HTTP.
        category_id (int): El ID de la categoría.
        
    Returns:
        HttpResponse: La plantilla renderizada con los detalles de la categoría.
    """
    category = get_object_or_404(Category, pk=category_id)
    
    context = {
        'category': category,
    }
    return render(request, 'category/category_detail.html', context)


@superuser_required()
@require_http_methods(["GET", "POST"])
def edit_category(request, category_id):
    """Vista para editar una categoría existente.
    
    GET: Muestra el formulario rellenado con los datos de la categoría.
    POST: Procesa el formulario y actualiza la categoría si es válido.
    
    Args:
        request: La solicitud HTTP.
        category_id (int): El ID de la categoría a editar.
        
    Returns:
        HttpResponse: El formulario renderizado o redirección tras guardar.
    """
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Categoría "{category.name}" actualizada exitosamente.')
            return redirect('category_detail', category_id=category.id)
        else:
            messages.error(request, 'Hubo errores en el formulario. Verifica los datos.')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'edit': True,
    }
    return render(request, 'category/add_category.html', context)


@superuser_required()
@require_http_methods(["GET", "POST"])
def delete_category(request, category_id):
    """Vista para eliminar una categoría.
    
    GET: Muestra una página de confirmación con información sobre productos.
    POST: Elimina la categoría. Los productos asociados quedarán sin categoría.
    
    Args:
        request: La solicitud HTTP.
        category_id (int): El ID de la categoría a eliminar.
        
    Returns:
        HttpResponse: Página de confirmación o redirección tras eliminar.
    """
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == "POST":
        category_name = category.name
        category.delete()
        messages.success(request, f'Categoría "{category_name}" eliminada exitosamente.')
        return redirect('list_products')
    
    context = {
        'category': category,
    }
    return render(request, 'category/delete_category.html', context)
