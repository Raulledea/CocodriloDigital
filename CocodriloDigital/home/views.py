from django.shortcuts import render
from products.models import Product

# Create your views here.


def home(request):
    
    products = Product.objects.all()
    
    dit= {'products':products}
    
    return render(request, 'home/home.html',dit)