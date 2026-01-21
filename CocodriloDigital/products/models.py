"""Modelos de la aplicación 'products'.

Contiene los modelos para productos y promociones.
"""
from decimal import Decimal
from django.db import models
from category.models import Category
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator 


class Product(models.Model):
    """Modelo de producto con información básica.
    
    Atributos:
        name (str): Nombre del producto.
        description (str): Descripción detallada.
        price (Decimal): Precio original del producto.
        stock (int): Cantidad disponible en inventario.
        image (ImageField): Imagen del producto.
        category (Category): Categoría a la que pertenece.
    """
    # Nombre del producto
    name = models.CharField(max_length=200, help_text="Nombre del producto")

    # Descripción detallada
    description = models.TextField(blank=True, null=True, help_text="Descripción del producto")

    # Precio del producto en moneda decimal
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio original")

    # Stock disponible en el inventario
    stock = models.PositiveIntegerField(default=0, help_text="Cantidad en stock")
    
    # Imagen representativa del producto
    image = models.ImageField(upload_to="products/", blank=True, null=True, help_text="Foto del producto")
    
    # Categoría a la cual pertenece el producto
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', help_text="Categoría")
    
    @property
    def final_price(self):
        """Calcula el precio final aplicando descuentos activos.
        
        Si existe una promoción activa (en rango de fechas), retorna el precio
        con descuento. Si no, retorna el precio original.
        
        Returns:
            Decimal: Precio final (con o sin descuento).
        """
        now = timezone.now()
        # Busca la primera promoción activa del producto
        promo = self.promotions.filter(start_date__lte=now, end_date__gte=now).first()
        if promo:
            # Aplica el descuento: precio * (1 - descuento%/100)
            return self.price * (Decimal(1) - Decimal(promo.discount_percent) / Decimal(100))
        return self.price

    def __str__(self):
        """Retorna el nombre del producto."""
        return self.name
    

class Promotion(models.Model):
    """Modelo de promoción/descuento para productos.
    
    Define el período y porcentaje de descuento aplicable a un producto.
    
    Atributos:
        product (Product): Producto al que se aplica la promoción.
        discount_percent (int): Porcentaje de descuento (1-100%).
        start_date (DateTime): Fecha y hora de inicio de la promoción.
        end_date (DateTime): Fecha y hora de fin de la promoción.
    """
    # Producto al que aplica la promoción
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="promotions", help_text="Producto con descuento")
    # Porcentaje de descuento (validado entre 1 y 100)
    discount_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Descuento en porcentaje (1-100)"
    )
    # Fecha de inicio de la promoción
    start_date = models.DateTimeField(help_text="Cuándo comienza el descuento")
    # Fecha de fin de la promoción
    end_date = models.DateTimeField(help_text="Cuándo termina el descuento")

    def is_active(self):
        """Verifica si la promoción está activa en el momento actual.
        
        Returns:
            bool: True si la fecha/hora actual está entre start_date y end_date.
        """
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def get_discounted_price(self):
        """Calcula el precio del producto aplicando el descuento.
        
        Solo calcula el precio con descuento si la promoción está activa.
        
        Returns:
            Decimal: Precio con descuento si está activo, precio original si no.
        """
        if self.is_active():
            # Aplica: precio * (1 - descuento% / 100)
            return self.product.price * (Decimal(1) - Decimal(self.discount_percent) / Decimal(100))
        return self.product.price
    
    def __str__(self):
        """Retorna identificador de la promoción (nombre del producto)."""
        return self.product.name