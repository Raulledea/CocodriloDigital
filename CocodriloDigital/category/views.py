"""Vistas de la aplicación 'category'.

Contiene la lógica para gestionar categorías.
"""
from django.shortcuts import render, redirect
from .forms import CategoryForm


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
            return redirect('products_by_category')
    else:
        form = CategoryForm()
    return render(request, 'category/add_category.html', {'form': form})
