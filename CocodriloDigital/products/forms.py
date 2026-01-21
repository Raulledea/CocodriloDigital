"""Formularios para la aplicación 'products'.

Contiene formularios de creación y edición de productos.
"""
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Formulario para crear/editar productos.
    
    Campos: nombre, descripción, precio, stock, categoría, imagen.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']
