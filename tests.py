import pytest
import os
import sys

# Configurar Django para pruebas
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CocodriloDigital.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from products.models import Product, Category, Promotion
from cart.models import Cart, CartItem, Receipt, ReceiptItem
from datetime import datetime, timedelta


@pytest.mark.django_db
class TestProductModels(TestCase):
    """Pruebas para los modelos de productos."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Electrónica",
            description="Productos electrónicos"
        )
        self.product = Product.objects.create(
            name="Laptop",
            description="Laptop de alta gama",
            price=Decimal('1000.00'),
            stock=10,
            category=self.category
        )
    
    def test_product_creation(self):
        """Prueba la creación de productos."""
        assert self.product.name == "Laptop"
        assert self.product.price == Decimal('1000.00')
        assert self.product.stock == 10
        assert self.product.category == self.category
    
    def test_product_str(self):
        """Prueba el método __str__ del producto."""
        assert str(self.product) == "Laptop"
    
    def test_category_creation(self):
        """Prueba la creación de categorías."""
        assert self.category.name == "Electrónica"
        assert str(self.category) == "Electrónica"


@pytest.mark.django_db
class TestCartModels(TestCase):
    """Pruebas para los modelos del carrito."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Electrónica",
            description="Productos electrónicos"
        )
        self.product = Product.objects.create(
            name="Laptop",
            description="Laptop de alta gama",
            price=Decimal('1000.00'),
            stock=10,
            category=self.category
        )
    
    def test_cart_creation_for_user(self):
        """Prueba la creación de carrito para usuario."""
        cart = Cart.objects.create(user=self.user)
        assert cart.user == self.user
        assert str(cart) == f"Carrito de {self.user.username}"
    
    def test_cart_creation_for_anonymous(self):
        """Prueba la creación de carrito para usuario anónimo."""
        cart = Cart.objects.create(session_key='test_session')
        assert cart.session_key == 'test_session'
        assert 'Carrito anónimo' in str(cart)
    
    def test_cart_item_creation(self):
        """Prueba la creación de items del carrito."""
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2,
            price=Decimal('1000.00')
        )
        assert cart_item.cart == cart
        assert cart_item.product == self.product
        assert cart_item.quantity == 2
        assert cart_item.subtotal == Decimal('2000.00')
    
    def test_cart_get_total(self):
        """Prueba el cálculo del total del carrito."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2,
            price=Decimal('1000.00')
        )
        assert cart.get_total() == Decimal('2000.00')
    
    def test_cart_get_total_items(self):
        """Prueba el cálculo de items totales del carrito."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=3,
            price=Decimal('1000.00')
        )
        assert cart.get_total_items() == 3


@pytest.mark.django_db
class TestReceiptModels(TestCase):
    """Pruebas para los modelos de recibos."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Electrónica",
            description="Productos electrónicos"
        )
        self.product = Product.objects.create(
            name="Laptop",
            description="Laptop de alta gama",
            price=Decimal('1000.00'),
            stock=10,
            category=self.category
        )
    
    def test_receipt_creation(self):
        """Prueba la creación de recibos."""
        receipt = Receipt.objects.create(
            user=self.user,
            receipt_id=Receipt.generate_receipt_id(),
            total_amount=Decimal('1000.00')
        )
        assert receipt.user == self.user
        assert receipt.total_amount == Decimal('1000.00')
        assert str(receipt) == f"Recibo {receipt.receipt_id} - {self.user.username}"
    
    def test_receipt_item_creation(self):
        """Prueba la creación de items de recibo."""
        receipt = Receipt.objects.create(
            user=self.user,
            receipt_id=Receipt.generate_receipt_id(),
            total_amount=Decimal('1000.00')
        )
        receipt_item = ReceiptItem.objects.create(
            receipt=receipt,
            product=self.product,
            product_name="Laptop",
            product_price=Decimal('1000.00'),
            quantity=1,
            subtotal=Decimal('1000.00')
        )
        assert receipt_item.receipt == receipt
        assert receipt_item.product == self.product
        assert receipt_item.subtotal == Decimal('1000.00')
    
    def test_receipt_with_deleted_user(self):
        """Prueba recibos con usuario eliminado."""
        receipt = Receipt.objects.create(
            user=self.user,
            receipt_id=Receipt.generate_receipt_id(),
            total_amount=Decimal('1000.00')
        )
        # Eliminar usuario
        self.user.delete()
        receipt.refresh_from_db()
        assert receipt.user is None
        assert "Usuario eliminado" in str(receipt)
    
    def test_receipt_item_with_deleted_product(self):
        """Prueba items de recibo con producto eliminado."""
        receipt = Receipt.objects.create(
            user=self.user,
            receipt_id=Receipt.generate_receipt_id(),
            total_amount=Decimal('1000.00')
        )
        receipt_item = ReceiptItem.objects.create(
            receipt=receipt,
            product=self.product,
            product_name="Laptop",
            product_price=Decimal('1000.00'),
            quantity=1,
            subtotal=Decimal('1000.00')
        )
        # Eliminar producto
        self.product.delete()
        receipt_item.refresh_from_db()
        assert receipt_item.product is None
        assert receipt_item.product_name == "Laptop"  # Datos históricos preservados


@pytest.mark.django_db
class TestPromotionModels(TestCase):
    """Pruebas para los modelos de promociones."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Electrónica",
            description="Productos electrónicos"
        )
        self.product = Product.objects.create(
            name="Laptop",
            description="Laptop de alta gama",
            price=Decimal('1000.00'),
            stock=10,
            category=self.category
        )
    
    def test_promotion_creation(self):
        """Prueba la creación de promociones."""
        promotion = Promotion.objects.create(
            product=self.product,
            discount_percent=20,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7)
        )
        assert promotion.product == self.product
        assert promotion.discount_percent == 20
        assert promotion.is_active == True
    
    def test_promotion_is_active(self):
        """Prueba el estado activo de la promoción."""
        promotion = Promotion.objects.create(
            product=self.product,
            discount_percent=20,
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now() + timedelta(days=7)
        )
        assert promotion.is_active == True
        
        # Promoción expirada
        promotion.end_date = datetime.now() - timedelta(days=1)
        promotion.save()
        assert promotion.is_active == False


@pytest.mark.django_db
class TestViews(TestCase):
    """Pruebas para las vistas."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Electrónica",
            description="Productos electrónicos"
        )
        self.product = Product.objects.create(
            name="Laptop",
            description="Laptop de alta gama",
            price=Decimal('1000.00'),
            stock=10,
            category=self.category
        )
    
    def test_home_view(self):
        """Prueba la vista principal."""
        response = self.client.get(reverse('home'))
        assert response.status_code == 200
        assert 'discounted_products' in response.context
    
    def test_list_products_view(self):
        """Prueba la vista de lista de productos."""
        response = self.client.get(reverse('products:list_products'))
        assert response.status_code == 200
        assert 'categories' in response.context
    
    def test_product_detail_view(self):
        """Prueba la vista de detalle de producto."""
        response = self.client.get(
            reverse('products:product_detail', kwargs={'product_id': self.product.id})
        )
        assert response.status_code == 200
        assert 'product' in response.context
    
    def test_cart_view(self):
        """Prueba la vista del carrito."""
        response = self.client.get(reverse('cart:carrito'))
        assert response.status_code == 200
        assert 'cart_items' in response.context
        assert 'total' in response.context
    
    def test_add_to_cart_view(self):
        """Prueba agregar producto al carrito."""
        response = self.client.post(
            reverse('cart:add_to_carrito', kwargs={'product_id': self.product.id})
        )
        assert response.status_code == 302  # Redirect
        
        # Verificar que el producto se agregó al carrito
        cart = Cart.get_or_create_cart(self.client)
        assert CartItem.objects.filter(cart=cart, product=self.product).exists()
    
    def test_search_products_view(self):
        """Prueba la vista de búsqueda de productos."""
        response = self.client.get(
            reverse('products:search_products'), 
            {'q': 'Laptop'}
        )
        assert response.status_code == 200
        assert 'categories' in response.context
        assert 'search_query' in response.context
    
    def test_search_products_empty_query(self):
        """Prueba búsqueda con query vacío."""
        response = self.client.get(reverse('products:search_products'))
        assert response.status_code == 302  # Redirect to list_products


@pytest.mark.django_db
class TestCartFunctionality(TestCase):
    """Pruebas funcionales del carrito."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Electrónica",
            description="Productos electrónicos"
        )
        self.product = Product.objects.create(
            name="Laptop",
            description="Laptop de alta gama",
            price=Decimal('1000.00'),
            stock=10,
            category=self.category
        )
    
    def test_cart_persistence_for_user(self):
        """Prueba la persistencia del carrito para usuario."""
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Agregar producto al carrito
        self.client.post(
            reverse('cart:add_to_carrito', kwargs={'product_id': self.product.id})
        )
        
        # Verificar carrito
        cart = Cart.get_or_create_cart(self.client)
        assert cart.user == self.user
        assert CartItem.objects.filter(cart=cart, product=self.product).exists()
    
    def test_cart_persistence_for_anonymous(self):
        """Prueba la persistencia del carrito para usuario anónimo."""
        # Agregar producto al carrito sin login
        self.client.post(
            reverse('cart:add_to_carrito', kwargs={'product_id': self.product.id})
        )
        
        # Verificar carrito anónimo
        cart = Cart.get_or_create_cart(self.client)
        assert cart.user is None
        assert cart.session_key is not None
        assert CartItem.objects.filter(cart=cart, product=self.product).exists()
    
    def test_cart_migration_anonymous_to_user(self):
        """Prueba migración de carrito anónimo a usuario."""
        # Agregar producto al carrito sin login
        self.client.post(
            reverse('cart:add_to_carrito', kwargs={'product_id': self.product.id})
        )
        
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Obtener carrito después del login
        cart = Cart.get_or_create_cart(self.client)
        assert cart.user == self.user
        assert CartItem.objects.filter(cart=cart, product=self.product).exists()


@pytest.mark.django_db
class TestCheckoutFunctionality(TestCase):
    """Pruebas funcionales del checkout."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Electrónica",
            description="Productos electrónicos"
        )
        self.product = Product.objects.create(
            name="Laptop",
            description="Laptop de alta gama",
            price=Decimal('1000.00'),
            stock=10,
            category=self.category
        )
    
    def test_checkout_process(self):
        """Prueba el proceso completo de checkout."""
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Agregar producto al carrito
        self.client.post(
            reverse('cart:add_to_carrito', kwargs={'product_id': self.product.id})
        )
        
        # Realizar checkout
        response = self.client.post(reverse('cart:checkout'))
        assert response.status_code == 302  # Redirect
        
        # Verificar recibo creado
        assert Receipt.objects.filter(user=self.user).exists()
        receipt = Receipt.objects.get(user=self.user)
        assert receipt.total_amount == Decimal('1000.00')
        
        # Verificar items del recibo
        assert ReceiptItem.objects.filter(receipt=receipt).exists()
        receipt_item = ReceiptItem.objects.get(receipt=receipt)
        assert receipt_item.product_name == "Laptop"
        assert receipt_item.product_price == Decimal('1000.00')
        
        # Verificar carrito vacío
        cart = Cart.get_or_create_cart(self.client)
        assert not CartItem.objects.filter(cart=cart).exists()


if __name__ == '__main__':
    pytest.main([__file__])
