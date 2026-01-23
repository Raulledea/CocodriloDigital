"""Formularios para la aplicación 'products'.

Contiene formularios de creación y edición de productos y promociones.
"""
from django import forms
from .models import Product, Promotion


class ProductForm(forms.ModelForm):
    """Formulario para crear/editar productos.
    
    Campos: nombre, descripción, precio, stock, categoría, imagen.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']


class PromotionForm(forms.ModelForm):
    """Formulario para crear/editar promociones.
    
    Campos: porcentaje de descuento, fecha de inicio, fecha de fin.
    """
    class Meta:
        model = Promotion
        fields = ['discount_percent', 'start_date', 'end_date']
        widgets = {
            'discount_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 1,
                'max': 100,
                'placeholder': 'Porcentaje de descuento (1-100)'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora de inicio'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora de fin'
            }),
        }
        labels = {
            'discount_percent': 'Porcentaje de Descuento (%)',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha de Fin',
        }
