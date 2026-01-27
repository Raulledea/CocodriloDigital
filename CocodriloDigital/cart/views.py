from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from products.models import Product
from .models import Cart, CartItem, Receipt, ReceiptItem


def get_cart_context(request):
    """Obtiene el contexto del carrito para las plantillas."""
    cart = Cart.get_or_create_cart(request)
    cart_items = []
    total = 0
    
    for item in cart.items.all():
        cart_items.append({
            'product_id': item.product.id,
            'name': item.product.name,
            'price': item.price,
            'quantity': item.quantity,
            'image': item.product.image.url if item.product.image else '',
            'subtotal': item.subtotal
        })
    
    total = cart.get_total()
    
    return {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart.get_total_items()
    }


@require_http_methods(["GET"])
def carrito_view(request):
    """
    Vista para mostrar el carrito de compras.
    """
    context = get_cart_context(request)
    return render(request, 'cart/carrito.html', context)


@require_http_methods(["POST"])
def add_to_carrito(request, product_id):
    """
    POST: Agrega un producto al carrito usando persistencia.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.get_or_create_cart(request)
    
    # Obtener o crear el item del carrito
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            'quantity': 1,
            'price': product.final_price if hasattr(product, 'final_price') else product.price
        }
    )
    
    if not created:
        # Si el item ya existe, incrementar cantidad
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, 'Producto añadido al carrito.')
    return redirect('cart:carrito')


@require_http_methods(["POST"])
def update_carrito(request, product_id):
    """
    POST: Actualiza la cantidad de un producto en el carrito.
    """
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        messages.error(request, 'La cantidad debe ser al menos 1.')
        return redirect('cart:carrito')
    
    cart = Cart.get_or_create_cart(request)
    
    try:
        cart_item = cart.items.get(product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cantidad actualizada.')
    except CartItem.DoesNotExist:
        messages.error(request, 'El producto no está en tu carrito.')
    
    return redirect('cart:carrito')


@require_http_methods(["POST"])
def remove_from_carrito(request, product_id):
    """
    POST: Elimina un producto del carrito.
    """
    cart = Cart.get_or_create_cart(request)
    
    try:
        cart_item = cart.items.get(product_id=product_id)
        cart_item.delete()
        messages.success(request, 'Producto eliminado del carrito.')
    except CartItem.DoesNotExist:
        messages.error(request, 'El producto no está en tu carrito.')
    
    return redirect('cart:carrito')


@login_required
@require_http_methods(["POST"])
def checkout(request):
    """
    POST: Procesa el checkout y guarda el recibo en la base de datos.
    """
    cart = Cart.get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('cart:carrito')
    
    # Crear el recibo
    total = cart.get_total()
    receipt = Receipt.objects.create(
        user=request.user,
        receipt_id=Receipt.generate_receipt_id(),
        total_amount=total
    )
    
    # Crear los items del recibo
    for item in cart.items.all():
        ReceiptItem.objects.create(
            receipt=receipt,
            product=item.product,  # Guardar referencia al producto
            product_name=item.product.name,
            product_price=item.price,
            quantity=item.quantity,
            subtotal=item.subtotal
        )
    
    # Limpiar el carrito
    cart.items.all().delete()
    
    messages.success(request, f'Compra realizada exitosamente. Recibo: {receipt.receipt_id}')
    return redirect('cart:receipt_detail', receipt_id=receipt.id)


@login_required
@require_http_methods(["GET"])
def receipt_list(request):
    """
    GET: Muestra la lista de recibos del usuario.
    """
    receipts = Receipt.objects.filter(user=request.user)
    return render(request, 'cart/receipt_list.html', {'receipts': receipts})


@login_required
@require_http_methods(["GET"])
def receipt_detail(request, receipt_id):
    """
    GET: Muestra los detalles de un recibo específico.
    """
    receipt = get_object_or_404(Receipt, id=receipt_id, user=request.user)
    return render(request, 'cart/receipt_detail.html', {'receipt': receipt})
