from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime


class Receipt(models.Model):
    """Modelo para guardar los recibos de compras."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipts')
    receipt_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'
    
    def __str__(self):
        return f"Recibo {self.receipt_id} - {self.user.username}"
    
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
    
    class Meta:
        verbose_name = 'Item de recibo'
        verbose_name_plural = 'Items de recibos'
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
