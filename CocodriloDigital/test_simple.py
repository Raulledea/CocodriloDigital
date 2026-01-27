#!/usr/bin/env python
"""Pruebas simples sin pytest-django para evitar problemas de configuración."""

import os
import sys
import django
import random
import logging
from datetime import datetime
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CocodriloDigital.settings')

django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from products.models import Product, Category, Promotion
from cart.models import Cart, CartItem, Receipt, ReceiptItem
from datetime import datetime, timedelta
from django.test import Client
from django.urls import reverse


def setup_logging():
    """Configura el logging para las pruebas."""
    # Crear directorio de logs si no existe
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Nombre del archivo de log con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'test_results_{timestamp}.log')
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)  # También mostrar en consola
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("🚀 INICIANDO SESIÓN DE PRUEBAS AUTOMÁTICAS")
    logger.info(f"📁 Archivo de log: {log_file}")
    logger.info(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    return logger


def log_test_start(logger, test_name):
    """Registra el inicio de una prueba."""
    logger.info(f"🧪 INICIANDO: {test_name}")
    logger.info("-" * 40)


def log_test_result(logger, test_name, success, error_msg=None):
    """Registra el resultado de una prueba."""
    if success:
        logger.info(f"✅ EXITO: {test_name}")
    else:
        logger.error(f"❌ FALLO: {test_name}")
        if error_msg:
            logger.error(f"   Error: {error_msg}")
    logger.info("-" * 40)


def log_summary(logger, passed, failed, total_time):
    """Registra el resumen final de pruebas."""
    logger.info("=" * 60)
    logger.info("📊 RESUMEN FINAL DE PRUEBAS")
    logger.info(f"   ✅ Pruebas pasadas: {passed}")
    logger.info(f"   ❌ Pruebas fallidas: {failed}")
    logger.info(f"   📈 Total pruebas: {passed + failed}")
    logger.info(f"   ⏱️  Tiempo total: {total_time:.2f} segundos")
    
    if failed == 0:
        logger.info("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        logger.warning(f"⚠️  {failed} pruebas fallaron - Revisar logs")
    
    logger.info("=" * 60)
    logger.info("📋 FIN DE SESIÓN DE PRUEBAS")
    logger.info("=" * 60)


def test_product_creation():
    """Prueba simple de creación de producto."""
    print("🧪 Probando creación de producto...")
    
    category = Category.objects.create(
        name=f"Electrónica_{random.randint(1000, 9999)}",
        description="Productos electrónicos"
    )
    
    product = Product.objects.create(
        name=f"Laptop_{random.randint(1000, 9999)}",
        description="Laptop de alta gama",
        price=Decimal('1000.00'),
        stock=10,
        category=category
    )
    
    assert product.price == Decimal('1000.00')
    print("✅ Prueba de creación de producto exitosa")


def test_cart_creation():
    """Prueba simple de creación de carrito."""
    print("🧪 Probando creación de carrito...")
    
    user = User.objects.create_user(
        username=f'testuser_{random.randint(1000, 9999)}',
        email=f'test{random.randint(1000, 9999)}@example.com',
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
        username=f'testuser_{random.randint(1000, 9999)}',
        email=f'test{random.randint(1000, 9999)}@example.com',
        password='testpass123'
    )
    
    category = Category.objects.create(
        name=f"Ropa_{random.randint(1000, 9999)}",
        description="Productos de ropa"
    )
    
    product = Product.objects.create(
        name=f"Camisa_{random.randint(1000, 9999)}",
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
        username=f'testuser_{random.randint(1000, 9999)}',
        email=f'test{random.randint(1000, 9999)}@example.com',
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
        username=f'testuser_{random.randint(1000, 9999)}',
        email=f'test{random.randint(1000, 9999)}@example.com',
        password='testpass123'
    )
    
    category = Category.objects.create(
        name=f"Libros_{random.randint(1000, 9999)}",
        description="Productos de libros"
    )
    
    product = Product.objects.create(
        name=f"Libro Django_{random.randint(1000, 9999)}",
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
        name=f"Tecnología_{random.randint(1000, 9999)}",
        description="Productos tecnológicos"
    )
    
    product = Product.objects.create(
        name=f"Smartphone_{random.randint(1000, 9999)}",
        description="Smartphone Android",
        price=Decimal('500.00'),
        stock=5,
        category=category
    )
    
    promotion = Promotion.objects.create(
        product=product,
        discount_percent=15,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=7)
    )
    
    assert promotion.product == product
    assert promotion.discount_percent == 15
    assert promotion.is_active() == True
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
    import time
    
    # Configurar logging
    logger = setup_logging()
    start_time = time.time()
    
    passed = 0
    failed = 0
    
    tests = [
        test_product_creation,
        test_cart_creation,
        test_cart_item_creation,
        test_receipt_creation,
        test_cart_total_calculation,
        test_promotion_creation,
        test_views
    ]
    
    logger.info(f"📋 Se ejecutarán {len(tests)} pruebas")
    logger.info("=" * 60)
    
    for test in tests:
        test_start_time = time.time()
        log_test_start(logger, test.__name__)
        
        try:
            test()
            test_duration = time.time() - test_start_time
            logger.info(f"⏱️  Duración: {test_duration:.3f} segundos")
            log_test_result(logger, test.__name__, True)
            passed += 1
        except Exception as e:
            test_duration = time.time() - test_start_time
            logger.info(f"⏱️  Duración: {test_duration:.3f} segundos")
            log_test_result(logger, test.__name__, False, str(e))
            failed += 1
    
    total_time = time.time() - start_time
    log_summary(logger, passed, failed, total_time)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
