from django.shortcuts import render
from products.models import Product
from django.utils import timezone
from django.views.generic import ListView

# Create your views here.


def home(request):
    
    now = timezone.now()
    
    discounted_products = Product.objects.filter(
        promotions__discount_percent__isnull=False,
        promotions__start_date__lte=now,
        promotions__end_date__gte=now
        ).distinct()
    
    dit= {'discounted_products':discounted_products}
    
    return render(request, 'home/home.html',dit)


class Home(ListView):
    model = Product
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        
        now = timezone.now()
        
        discounted_products = Product.objects.filter(
        promotions__discount_percent__isnull=False,
        promotions__start_date__lte=now,
        promotions__end_date__gte=now
        ).distinct()
        
        context = super().get_context_data(**kwargs)
        context['discounted_products'] = discounted_products
        return context
    