from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime
import uuid


class Cart(models.Model):
    """Modelo para guardar los carritos de compras con persistencia."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        if self.user:
            return f"Carrito de {self.user.username}"
        return f"Carrito anónimo {self.session_key[:8]}"
    
    @classmethod
    def get_or_create_cart(cls, request):
        """Obtiene o crea un carrito para el usuario o sesión actual."""
        # Si el usuario está autenticado, buscar su carrito activo
        if request.user.is_authenticated:
            cart = cls.objects.filter(user=request.user, is_active=True).first()
            if cart:
                return cart
            
            # Si no tiene carrito, migrar carrito de sesión si existe
            session_key = request.session.session_key
            if session_key:
                session_cart = cls.objects.filter(session_key=session_key, is_active=True).first()
                if session_cart:
                    session_cart.user = request.user
                    session_cart.session_key = None
                    session_cart.save()
                    return session_cart
            
            # Crear nuevo carrito para el usuario
            return cls.objects.create(user=request.user)
        
        # Para usuarios anónimos, usar sesión
        if not request.session.session_key:
            request.session.create()
        
        session_key = request.session.session_key
        cart = cls.objects.filter(session_key=session_key, is_active=True).first()
        if cart:
            return cart
        
        return cls.objects.create(session_key=session_key)
    
    def get_total(self):
        """Calcula el total del carrito."""
        return sum(item.subtotal for item in self.items.all())
    
    def get_total_items(self):
        """Obtiene el número total de items en el carrito."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Modelo para guardar los items de un carrito."""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio al momento de agregar
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Item de carrito'
        verbose_name_plural = 'Items de carritos'
        unique_together = ['cart', 'product']
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product']),
        ]
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    @property
    def subtotal(self):
        """Calcula el subtotal del item."""
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        """Actualiza el precio del producto al guardar."""
        if not self.price:
            self.price = self.product.final_price if hasattr(self.product, 'final_price') else self.product.price
        super().save(*args, **kwargs)


class Receipt(models.Model):
    """Modelo para guardar los recibos de compras."""
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='receipts')
    receipt_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'
    
    def __str__(self):
        user_info = f"{self.user.username}" if self.user else "Usuario eliminado"
        return f"Recibo {self.receipt_id} - {user_info}"
    
    @classmethod
    def generate_receipt_id(cls):
        """Genera un ID único para el recibo."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"RC-{timestamp}"


class ReceiptItem(models.Model):
    """Modelo para guardar los items de un recibo."""
    
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Opcional: guardar referencia al producto (no obligatoria para mantener integridad histórica)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Item de recibo'
        verbose_name_plural = 'Items de recibos'
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
