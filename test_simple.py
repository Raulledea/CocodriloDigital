#!/usr/bin/env python
"""Pruebas simples sin pytest-django para evitar problemas de configuración."""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CocodriloDigital.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from products.models import Product, Category, Promotion
from cart.models import Cart, CartItem, Receipt, ReceiptItem
from datetime import datetime, timedelta
from django.test import Client
from django.urls import reverse


def test_product_creation():
    """Prueba simple de creación de producto."""
    print("🧪 Probando creación de producto...")
    
    category = Category.objects.create(
        name="Electrónica",
        description="Productos electrónicos"
    )
    
    product = Product.objects.create(
        name="Laptop",
        description="Laptop de alta gama",
        price=Decimal('1000.00'),
        stock=10,
        category=category
    )
    
    assert product.name == "Laptop"
    assert product.price == Decimal('1000.00')
    assert product.stock == 10
    assert product.category == category
    print("✅ Prueba de creación de producto exitosa")


def test_cart_creation():
    """Prueba simple de creación de carrito."""
    print("🧪 Probando creación de carrito...")
    
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    
    cart = Cart.objects.create(user=user)
    assert cart.user == user
    assert str(cart) == f"Carrito de {user.username}"
    print("✅ Prueba de creación de carrito exitosa")


def test_cart_item_creation():
    """Prueba simple de creación de item de carrito."""
    print("🧪 Probando creación de item de carrito...")
    
    user = User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123'
    )
    
    category = Category.objects.create(
        name="Ropa",
        description="Productos de ropa"
    )
    
    product = Product.objects.create(
        name="Camisa",
        description="Camisa de algodón",
        price=Decimal('50.00'),
        stock=20,
        category=category
    )
    
    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=2,
        price=Decimal('50.00')
    )
    
    assert cart_item.cart == cart
    assert cart_item.product == product
    assert cart_item.quantity == 2
    assert cart_item.subtotal == Decimal('100.00')
    print("✅ Prueba de creación de item de carrito exitosa")


def test_receipt_creation():
    """Prueba simple de creación de recibo."""
    print("🧪 Probando creación de recibo...")
    
    user = User.objects.create_user(
        username='testuser3',
        email='test3@example.com',
        password='testpass123'
    )
    
    receipt = Receipt.objects.create(
        user=user,
        receipt_id=Receipt.generate_receipt_id(),
        total_amount=Decimal('200.00')
    )
    
    assert receipt.user == user
    assert receipt.total_amount == Decimal('200.00')
    assert str(receipt) == f"Recibo {receipt.receipt_id} - {user.username}"
    print("✅ Prueba de creación de recibo exitosa")


def test_cart_total_calculation():
    """Prueba simple de cálculo de total de carrito."""
    print("🧪 Probando cálculo de total de carrito...")
    
    user = User.objects.create_user(
        username='testuser4',
        email='test4@example.com',
        password='testpass123'
    )
    
    category = Category.objects.create(
        name="Libros",
        description="Productos de libros"
    )
    
    product = Product.objects.create(
        name="Libro Django",
        description="Libro de Django",
        price=Decimal('30.00'),
        stock=15,
        category=category
    )
    
    cart = Cart.objects.create(user=user)
    CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=3,
        price=Decimal('30.00')
    )
    
    assert cart.get_total() == Decimal('90.00')
    assert cart.get_total_items() == 3
    print("✅ Prueba de cálculo de total de carrito exitosa")


def test_promotion_creation():
    """Prueba simple de creación de promoción."""
    print("🧪 Probando creación de promoción...")
    
    category = Category.objects.create(
        name="Tecnología",
        description="Productos tecnológicos"
    )
    
    product = Product.objects.create(
        name="Smartphone",
        description="Smartphone Android",
        price=Decimal('500.00'),
        stock=5,
        category=category
    )
    
    promotion = Promotion.objects.create(
        product=product,
        discount_percent=15,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7)
    )
    
    assert promotion.product == product
    assert promotion.discount_percent == 15
    assert promotion.is_active == True
    print("✅ Prueba de creación de promoción exitosa")


def test_views():
    """Prueba simple de vistas."""
    print("🧪 Probando vistas principales...")
    
    client = Client()
    
    # Probar vista principal
    response = client.get('/')
    assert response.status_code == 200
    print("✅ Vista principal funciona")
    
    # Probar vista de productos
    response = client.get('/productos/')
    assert response.status_code == 200
    print("✅ Vista de productos funciona")
    
    # Probar vista de carrito
    response = client.get('/carrito/carrito/')
    assert response.status_code == 200
    print("✅ Vista de carrito funciona")


def run_all_tests():
    """Ejecutar todas las pruebas."""
    print("🚀 Iniciando pruebas automáticas...")
    print("=" * 50)
    
    try:
        test_product_creation()
        test_cart_creation()
        test_cart_item_creation()
        test_receipt_creation()
        test_cart_total_calculation()
        test_promotion_creation()
        test_views()
        
        print("=" * 50)
        print("🎉 Todas las pruebas pasaron exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
