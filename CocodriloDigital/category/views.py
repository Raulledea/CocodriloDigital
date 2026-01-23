"""Vistas de la aplicación 'category'.

Contiene la lógica para gestionar categorías.
"""
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm
from .models import Category


def add_category(request):
    """Vista para añadir una nueva categoría.
    
    GET: Muestra formulario vacío de creación de categoría.
    POST: Procesa el formulario y guarda la categoría si es válido.
    
    Redirige a la lista de productos después de crear la categoría.
    """
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a la lista de productos después de guardar
            return redirect('list_products')
    else:
        form = CategoryForm()
    return render(request, 'category/add_category.html', {'form': form})


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
            form.save()
            return redirect('category_detail', category_id=category.id)
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'edit': True,
    }
    return render(request, 'category/add_category.html', context)


def delete_category(request, category_id):
    """Vista para eliminar una categoría.
    
    GET: Muestra una página de confirmación con información sobre productos.
    POST: Elimina la categoría. Los productos asociados quedarán sin categoría asignada.
    
    Args:
        request: La solicitud HTTP.
        category_id (int): El ID de la categoría a eliminar.
        
    Returns:
        HttpResponse: Página de confirmación o redirección tras eliminar.
    """
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == "POST":
        # Los productos no se eliminarán, solo perderán la categoría (category=NULL)
        category.delete()
        return redirect('list_products')
    
    context = {
        'category': category,
    }
    return render(request, 'category/delete_category.html', context)
