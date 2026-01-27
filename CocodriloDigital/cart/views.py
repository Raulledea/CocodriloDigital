from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from products.models import Product
from .models import Receipt, ReceiptItem


@require_http_methods(["GET"])
def carrito_view(request):
    """
    Vista para mostrar el carrito de compras.
    """
    carrito = request.session.get('carrito', {})
    
    # Convertir el carrito a formato más amigable para el template
    cart_items = []
    total = 0
    
    for product_id, item in carrito.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item.get('image', ''),
            'subtotal': subtotal
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'cart/carrito.html', context)


@require_http_methods(["POST"])
def add_to_carrito(request, product_id):
    """
    POST: Agrega un producto al carrito usando sesión.
    """
    product = get_object_or_404(Product, pk=product_id)

    carrito = request.session.get('carrito', {})

    product_id_str = str(product.id)

    if product_id_str in carrito:
        carrito[product_id_str]['quantity'] += 1
    else:
        carrito[product_id_str] = {
            'name': product.name,
            'price': float(product.final_price if hasattr(product, 'final_price') else product.price),
            'quantity': 1,
            'image': product.image.url if product.image else '',
        }

    request.session['carrito'] = carrito
    request.session.modified = True

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
    
    carrito = request.session.get('carrito', {})
    product_id_str = str(product_id)

    if product_id_str in carrito:
        carrito[product_id_str]['quantity'] = quantity
        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, 'Cantidad actualizada.')

    return redirect('cart:carrito')


@require_http_methods(["POST"])
def remove_from_carrito(request, product_id):
    """
    POST: Elimina un producto del carrito.
    """
    carrito = request.session.get('carrito', {})
    product_id_str = str(product_id)

    if product_id_str in carrito:
        del carrito[product_id_str]
        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, 'Producto eliminado del carrito.')

    return redirect('cart:carrito')


@login_required
@require_http_methods(["POST"])
def checkout(request):
    """
    POST: Procesa el checkout y guarda el recibo en la base de datos.
    """
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('cart:carrito')
    
    # Crear el recibo
    total = sum(item['price'] * item['quantity'] for item in carrito.values())
    receipt = Receipt.objects.create(
        user=request.user,
        receipt_id=Receipt.generate_receipt_id(),
        total_amount=total
    )
    
    # Crear los items del recibo
    for item in carrito.values():
        ReceiptItem.objects.create(
            receipt=receipt,
            product_name=item['name'],
            product_price=item['price'],
            quantity=item['quantity'],
            subtotal=item['price'] * item['quantity']
        )
    
    # Limpiar el carrito
    request.session['carrito'] = {}
    request.session.modified = True
    
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
