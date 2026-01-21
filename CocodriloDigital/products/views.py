"""Vistas de la aplicación 'products'.

Contiene la lógica para gestionar productos.
"""
from django.shortcuts import render, redirect
from .forms import ProductForm


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
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'products/add_products.html', {'form': form})