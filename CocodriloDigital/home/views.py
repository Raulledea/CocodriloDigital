from django.shortcuts import render
from products.models import Product
from django.utils import timezone

# Create your views here.


def home(request):
    
    now = timezone.now()
    
    discounted_products = Product.objects.filter(
        promotions__discount_percent__isnull=False,
        promotions__start_date__lte=now,
        promotions__end_date__gte=now
        )
    
    
    products = Product.objects.all()
    
    dit= {'discounted_products':discounted_products}
    
    return render(request, 'home/home.html',dit)