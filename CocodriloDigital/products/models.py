from django.db import models

class Product(models.Model):
    # Nombre del producto
    name = models.CharField(max_length=200)

    # Descripción detallada
    description = models.TextField(blank=True, null=True)

    # Precio
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Stock disponible
    stock = models.PositiveIntegerField(default=0)

    # Categoría opcional (ejemplo: electrónica, ropa, etc.)
    category = models.CharField(max_length=100, blank=True, null=True)
    
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    
    def __str__(self):
        return self.name
