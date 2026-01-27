"""Formularios para la aplicación 'category'.

Contiene formularios de creación y edición de categorías.
"""
from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """Formulario para crear/editar categorías.
    
    Campos: nombre, descripción, categoría padre (opcional).
    """
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
