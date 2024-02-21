from django.shortcuts import render
from .models import Product

def home(request):
    page_name = "Home"
    return render(request, 'home.html', {'page_name': page_name})

def products_index(request):
    page_name = "Shop All"
    products = Product.objects.all()
    return render(request, 'products/index.html', { 'products': products, 'page_name': page_name })

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'products/detail.html', { 'product': product })

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')
