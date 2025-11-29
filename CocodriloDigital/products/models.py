from decimal import Decimal
from django.db import models
from category.models import Category
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator 

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
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    
    #Categoria del producto
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    @property
    def final_price(self):
        now = timezone.now()
        promo = self.promotions.filter(start_date__lte=now, end_date__gte=now).first()
        if promo:
            return self.price * (Decimal(1) - Decimal(promo.discount_percent) / Decimal(100))
        return self.price
    
    

    def __str__(self):
        return self.name
    
    
class Promotion(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="promotions")
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def get_discounted_price(self):
        if self.is_active():
            return self.product.price * (Decimal(1) - Decimal(self.discount_percent) / Decimal(100))
        return self.product.price
    
    def __str__(self):
        return self.product