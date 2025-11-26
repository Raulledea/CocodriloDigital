from django.shortcuts import render, redirect
from .forms import ProductForm

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # redirige a tu página principal
    else:
        form = ProductForm()
    return render(request, 'products/add_products.html', {'form': form})