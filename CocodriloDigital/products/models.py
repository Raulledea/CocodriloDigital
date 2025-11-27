from django.db import models
from category.models import Category

class Product(models.Model):
    # Nombre del producto
    name = models.CharField(max_length=200)

    # Descripción detallada
    description = models.TextField(blank=True, null=True)

    # Precio
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Stock disponible
    stock = models.PositiveIntegerField(default=0)
    
    #Imagen
    image = models.ImageField(upload_to="products/", blank=True, null=True,default='products/default/default01.jpg')
    
    #Categoria del producto
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    
    def __str__(self):
        return self.name
