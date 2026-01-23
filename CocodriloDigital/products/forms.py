"""Formularios para la aplicación 'products'.

Contiene formularios de creación y edición de productos y promociones
con validaciones y estilos personalizados.
"""
from django import forms
from django.utils import timezone
from .models import Product, Promotion


class ProductForm(forms.ModelForm):
    """Formulario para crear/editar productos con validaciones.
    
    Campos: nombre, descripción, precio, stock, categoría, imagen.
    Validaciones: precio positivo, stock no negativo.
    """
    price = forms.DecimalField(
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'placeholder': 'Ingresa el precio'
        })
    )
    
    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'placeholder': 'Cantidad disponible'
        })
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'name': 'Nombre del Producto',
            'description': 'Descripción',
            'price': 'Precio',
            'stock': 'Stock',
            'category': 'Categoría',
            'image': 'Imagen',
        }
    
    def clean_price(self):
        """Valida que el precio sea positivo."""
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return price
    
    def clean_stock(self):
        """Valida que el stock no sea negativo."""
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock


class PromotionForm(forms.ModelForm):
    """Formulario para crear/editar promociones con validaciones de fechas.
    
    Campos: porcentaje de descuento, fecha de inicio, fecha de fin.
    Validaciones: descuento válido, fecha fin > fecha inicio, fechas futuras.
    """
    discount_percent = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': 1,
            'max': 100,
            'placeholder': 'Porcentaje de descuento (1-100)'
        })
    )
    
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'placeholder': 'Fecha y hora de inicio'
        })
    )
    
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'placeholder': 'Fecha y hora de fin'
        })
    )
    
    class Meta:
        model = Promotion
        fields = ['discount_percent', 'start_date', 'end_date']
        labels = {
            'discount_percent': 'Porcentaje de Descuento (%)',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha de Fin',
        }
    
    def clean(self):
        """Validaciones cruzadas del formulario."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError(
                    'La fecha de fin debe ser posterior a la fecha de inicio.'
                )
    
    def clean_discount_percent(self):
        """Valida que el descuento esté entre 1 y 100."""
        discount = self.cleaned_data.get('discount_percent')
        if discount and (discount < 1 or discount > 100):
            raise forms.ValidationError('El descuento debe estar entre 1 y 100%.')
        return discount
